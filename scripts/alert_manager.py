import json
import yaml
import requests
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertManager:
    def __init__(self, config_file="config/alertas.yml"):
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
    
    def evaluate_rules(self, metrics_data):
        active_alerts = []
        
        for rule in self.config["alertas"]["reglas"]:
            if self._evaluate_condition(rule["condicion"], metrics_data):
                alert = {
                    "nombre": rule["nombre"],
                    "nivel": rule["nivel"],
                    "mensaje": rule["mensaje"],
                    "timestamp": datetime.now().isoformat(),
                    "canales": rule["canales"],
                    "datos": metrics_data
                }
                active_alerts.append(alert)
        
        return active_alerts
    
    def _evaluate_condition(self, condition, data):
        try:
            response_time_p95 = data.get("response_times", {}).get("p95", 0)
            error_rate = data.get("summary", {}).get("error_rate", 0)
            throughput = data.get("summary", {}).get("throughput_rps", 0)
            bdd_success_rate = data.get("bdd_metrics", {}).get("success_rate", 100)
            
            return eval(condition)
        except Exception as e:
            print(f"Error evaluando condición '{condition}': {e}")
            return False
    
    def send_slack_alert(self, alert):
        webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
        if not webhook_url:
            print("SLACK_WEBHOOK_URL no configurado")
            return False
        
        color = "#e74c3c" if alert["nivel"] == "critical" else "#f39c12"
        
        payload = {
            "attachments": [{
                "color": color,
                "title": f"🚨 Alerta {alert['nivel'].upper()}: {alert['nombre']}",
                "text": alert["mensaje"],
                "fields": [
                    {
                        "title": "Timestamp",
                        "value": alert["timestamp"],
                        "short": True
                    },
                    {
                        "title": "TPS",
                        "value": f"{alert['datos'].get('summary', {}).get('throughput_rps', 'N/A')}",
                        "short": True
                    },
                    {
                        "title": "Error Rate",
                        "value": f"{alert['datos'].get('summary', {}).get('error_rate', 'N/A')}%",
                        "short": True
                    },
                    {
                        "title": "Latencia P95",
                        "value": f"{alert['datos'].get('response_times', {}).get('p95', 'N/A')}ms",
                        "short": True
                    }
                ]
            }]
        }
        
        try:
            response = requests.post(webhook_url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Error enviando alerta a Slack: {e}")
            return False
    
    def send_email_alert(self, alert):
        try:
            smtp_config = self.config["alertas"]["canales"]["email"]
            
            msg = MIMEMultipart()
            msg['From'] = smtp_config["usuario"]
            msg['Subject'] = f"[ALERTA {alert['nivel'].upper()}] {alert['nombre']}"
            
            body = f"""
            Alerta de Pipeline de Pruebas
            
            Nivel: {alert['nivel'].upper()}
            Mensaje: {alert['mensaje']}
            Timestamp: {alert['timestamp']}
            
            Métricas actuales:
            - TPS: {alert['datos'].get('summary', {}).get('throughput_rps', 'N/A')}
            - Tasa de Error: {alert['datos'].get('summary', {}).get('error_rate', 'N/A')}%
            - Latencia P95: {alert['datos'].get('response_times', {}).get('p95', 'N/A')}ms
            
            Por favor revisar el dashboard de métricas para más detalles.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_config["smtp_server"], smtp_config["puerto"])
            server.starttls()
            server.login(
                os.environ.get('EMAIL_USER', smtp_config["usuario"]),
                os.environ.get('EMAIL_PASSWORD')
            )
            
            for destinatario in smtp_config["destinatarios"]:
                msg['To'] = destinatario
                server.send_message(msg)
                del msg['To']
            
            server.quit()
            return True
            
        except Exception as e:
            print(f"Error enviando email: {e}")
            return False
    
    def process_alerts(self, alerts):
        for alert in alerts:
            print(f"Procesando alerta: {alert['nombre']} [{alert['nivel']}]")
            
            for canal in alert["canales"]:
                if canal == "slack":
                    self.send_slack_alert(alert)
                elif canal == "email":
                    self.send_email_alert(alert)
    
    def monitor_metrics(self):
        metrics_file = "reports/performance_metrics.json"
        
        if not os.path.exists(metrics_file):
            print("No hay métricas para monitorear")
            return
        
        with open(metrics_file, 'r') as f:
            metrics_data = json.load(f)
        
        alerts = self.evaluate_rules(metrics_data)
        
        if alerts:
            print(f"Se generaron {len(alerts)} alertas")
            self.process_alerts(alerts)
            
            alert_log = {
                "timestamp": datetime.now().isoformat(),
                "alerts_count": len(alerts),
                "alerts": alerts
            }
            
            os.makedirs("logs", exist_ok=True)
            with open("logs/alerts.json", "w") as f:
                json.dump(alert_log, f, indent=2)
        else:
            print("No se generaron alertas")

if __name__ == "__main__":
    manager = AlertManager()
    manager.monitor_metrics()