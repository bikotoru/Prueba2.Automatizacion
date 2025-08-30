import csv
import json
import os
from datetime import datetime
import statistics

class PerformanceAnalyzer:
    def __init__(self):
        self.thresholds = {
            "response_time_p50": 500,
            "response_time_p95": 1500,
            "response_time_p99": 3000,
            "error_rate_max": 5.0,
            "min_throughput": 10.0
        }
    
    def analyze_csv_results(self, csv_file):
        metrics = {
            "total_requests": 0,
            "failed_requests": 0,
            "response_times": [],
            "throughput": 0,
            "error_rate": 0
        }
        
        if not os.path.exists(csv_file):
            print(f"Archivo no encontrado: {csv_file}")
            return metrics
        
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Type'] == 'GET' or row['Type'] == 'POST':
                    metrics["total_requests"] += int(row['Request Count'])
                    metrics["failed_requests"] += int(row['Failure Count'])
                    
                    if row['Average Response Time']:
                        avg_time = float(row['Average Response Time'])
                        metrics["response_times"].append(avg_time)
        
        if metrics["total_requests"] > 0:
            metrics["error_rate"] = (metrics["failed_requests"] / metrics["total_requests"]) * 100
            metrics["throughput"] = metrics["total_requests"] / 60
        
        return metrics
    
    def calculate_percentiles(self, response_times):
        if not response_times:
            return {"p50": 0, "p95": 0, "p99": 0}
        
        sorted_times = sorted(response_times)
        return {
            "p50": statistics.median(sorted_times),
            "p95": sorted_times[int(len(sorted_times) * 0.95)],
            "p99": sorted_times[int(len(sorted_times) * 0.99)]
        }
    
    def generate_metrics_json(self, metrics, percentiles):
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_requests": metrics["total_requests"],
                "failed_requests": metrics["failed_requests"],
                "error_rate": round(metrics["error_rate"], 2),
                "throughput_rps": round(metrics["throughput"], 2)
            },
            "response_times": {
                "p50": round(percentiles["p50"], 2),
                "p95": round(percentiles["p95"], 2),
                "p99": round(percentiles["p99"], 2)
            },
            "quality_gates": {
                "p50_passed": percentiles["p50"] <= self.thresholds["response_time_p50"],
                "p95_passed": percentiles["p95"] <= self.thresholds["response_time_p95"],
                "p99_passed": percentiles["p99"] <= self.thresholds["response_time_p99"],
                "error_rate_passed": metrics["error_rate"] <= self.thresholds["error_rate_max"],
                "throughput_passed": metrics["throughput"] >= self.thresholds["min_throughput"]
            },
            "indicators": {
                "TPS": round(metrics["throughput"], 2),
                "latencia_promedio": round(sum(metrics["response_times"]) / len(metrics["response_times"]), 2) if metrics["response_times"] else 0,
                "tasa_error": round(metrics["error_rate"], 2),
                "usuarios_concurrentes": 50
            }
        }
        
        all_passed = all(report["quality_gates"].values())
        report["overall_status"] = "PASS" if all_passed else "FAIL"
        
        return report
    
    def create_dashboard_data(self, report):
        dashboard_data = {
            "performance_metrics": {
                "TPS": {
                    "value": report["indicators"]["TPS"],
                    "threshold": self.thresholds["min_throughput"],
                    "status": "good" if report["quality_gates"]["throughput_passed"] else "critical"
                },
                "latencia": {
                    "p50": report["response_times"]["p50"],
                    "p95": report["response_times"]["p95"],
                    "p99": report["response_times"]["p99"],
                    "status": "good" if report["quality_gates"]["p95_passed"] else "warning"
                },
                "errores": {
                    "rate": report["summary"]["error_rate"],
                    "threshold": self.thresholds["error_rate_max"],
                    "status": "good" if report["quality_gates"]["error_rate_passed"] else "critical"
                }
            },
            "alerts": [],
            "timestamp": report["timestamp"]
        }
        
        if not report["quality_gates"]["throughput_passed"]:
            dashboard_data["alerts"].append({
                "level": "critical",
                "message": f"TPS bajo umbral: {report['indicators']['TPS']} < {self.thresholds['min_throughput']}"
            })
        
        if not report["quality_gates"]["p95_passed"]:
            dashboard_data["alerts"].append({
                "level": "warning",
                "message": f"Latencia P95 alta: {report['response_times']['p95']}ms > {self.thresholds['response_time_p95']}ms"
            })
        
        if not report["quality_gates"]["error_rate_passed"]:
            dashboard_data["alerts"].append({
                "level": "critical",
                "message": f"Tasa de error alta: {report['summary']['error_rate']}% > {self.thresholds['error_rate_max']}%"
            })
        
        return dashboard_data

def main():
    analyzer = PerformanceAnalyzer()
    
    csv_file = "reports/performance_stats.csv"
    metrics = analyzer.analyze_csv_results(csv_file)
    
    if metrics["response_times"]:
        percentiles = analyzer.calculate_percentiles(metrics["response_times"])
        report = analyzer.generate_metrics_json(metrics, percentiles)
        dashboard_data = analyzer.create_dashboard_data(report)
        
        os.makedirs("reports", exist_ok=True)
        
        with open("reports/performance_metrics.json", "w") as f:
            json.dump(report, f, indent=2)
        
        with open("reports/dashboard_data.json", "w") as f:
            json.dump(dashboard_data, f, indent=2)
        
        print(f"Estado general: {report['overall_status']}")
        print(f"TPS: {report['indicators']['TPS']}")
        print(f"Latencia P95: {report['response_times']['p95']}ms")
        print(f"Tasa de error: {report['summary']['error_rate']}%")
        
        if dashboard_data["alerts"]:
            print("Alertas generadas:")
            for alert in dashboard_data["alerts"]:
                print(f"  - {alert['level'].upper()}: {alert['message']}")
        
        if report["overall_status"] == "FAIL":
            exit(1)
    else:
        print("No se encontraron datos de performance para analizar")
        exit(1)

if __name__ == "__main__":
    main()