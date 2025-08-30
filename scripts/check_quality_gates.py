import json
import os
import sys

def check_quality_gates():
    print("Verificando umbrales de calidad...")
    
    performance_file = "reports/performance_metrics.json"
    dashboard_file = "reports/dashboard_data.json"
    
    if not os.path.exists(performance_file):
        print("ERROR: No se encontró el archivo de métricas de performance")
        return False
    
    with open(performance_file, 'r') as f:
        performance_data = json.load(f)
    
    quality_gates = performance_data.get("quality_gates", {})
    overall_status = performance_data.get("overall_status", "FAIL")
    
    print(f"Estado general: {overall_status}")
    print("\nVerificación de umbrales:")
    
    gate_results = []
    for gate, passed in quality_gates.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {gate}: {status}")
        gate_results.append(passed)
    
    if dashboard_file and os.path.exists(dashboard_file):
        with open(dashboard_file, 'r') as f:
            dashboard_data = json.load(f)
        
        alerts = dashboard_data.get("alerts", [])
        if alerts:
            print(f"\nAlertas activas ({len(alerts)}):")
            for alert in alerts:
                print(f"  [{alert['level'].upper()}] {alert['message']}")
    
    success_rate = (sum(gate_results) / len(gate_results)) * 100 if gate_results else 0
    print(f"\nTasa de éxito de umbrales: {success_rate:.1f}%")
    
    if overall_status == "PASS" and success_rate >= 80:
        print("✓ Todos los umbrales de calidad cumplidos")
        return True
    else:
        print("✗ Algunos umbrales de calidad no se cumplieron")
        return False

def generate_quality_report():
    report_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte de Calidad</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { background-color: #34495e; color: white; padding: 20px; border-radius: 5px; }
            .metric { background: white; margin: 10px 0; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .pass { color: #27ae60; }
            .fail { color: #e74c3c; }
            .alert { background: #ffe4e4; padding: 10px; margin: 5px 0; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Reporte de Calidad del Pipeline</h1>
            <p>Generado: {timestamp}</p>
        </div>
        <div id="metrics"></div>
    </body>
    </html>
    """
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/quality-report.html", "w", encoding="utf-8") as f:
        f.write(report_html.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

if __name__ == "__main__":
    success = check_quality_gates()
    generate_quality_report()
    
    if not success:
        sys.exit(1)