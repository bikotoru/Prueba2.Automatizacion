import json
import os
from datetime import datetime
import subprocess

def generate_html_report():
    report_data = {
        "titulo": "Reporte de Pruebas BDD",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resumen": {
            "total": 0,
            "pasadas": 0,
            "falladas": 0,
            "omitidas": 0
        },
        "escenarios": []
    }
    
    result_file = "reports/behave-results.json"
    if os.path.exists(result_file):
        with open(result_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
            
            for feature in results:
                for scenario in feature.get('elements', []):
                    report_data["resumen"]["total"] += 1
                    
                    scenario_data = {
                        "nombre": scenario.get('name', 'Sin nombre'),
                        "estado": "pasado",
                        "duracion": 0,
                        "pasos": []
                    }
                    
                    for step in scenario.get('steps', []):
                        step_duration = step.get('result', {}).get('duration', 0)
                        scenario_data["duracion"] += step_duration
                        
                        step_data = {
                            "nombre": step.get('name', ''),
                            "estado": step.get('result', {}).get('status', 'skipped')
                        }
                        
                        if step_data["estado"] == "failed":
                            scenario_data["estado"] = "fallado"
                            step_data["error"] = step.get('result', {}).get('error_message', '')
                        
                        scenario_data["pasos"].append(step_data)
                    
                    if scenario_data["estado"] == "pasado":
                        report_data["resumen"]["pasadas"] += 1
                    else:
                        report_data["resumen"]["falladas"] += 1
                    
                    report_data["escenarios"].append(scenario_data)
    
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{titulo}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .header {{
                background-color: #2c3e50;
                color: white;
                padding: 20px;
                border-radius: 5px;
            }}
            .summary {{
                display: flex;
                gap: 20px;
                margin: 20px 0;
            }}
            .summary-card {{
                background: white;
                padding: 15px;
                border-radius: 5px;
                flex: 1;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .passed {{ color: #27ae60; }}
            .failed {{ color: #e74c3c; }}
            .skipped {{ color: #95a5a6; }}
            .scenario {{
                background: white;
                margin: 10px 0;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .scenario-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }}
            .steps {{
                margin-left: 20px;
            }}
            .step {{
                padding: 5px 0;
                border-left: 3px solid #ecf0f1;
                padding-left: 10px;
                margin: 5px 0;
            }}
            .step.passed {{
                border-left-color: #27ae60;
            }}
            .step.failed {{
                border-left-color: #e74c3c;
            }}
            .error {{
                background: #ffe4e4;
                padding: 10px;
                margin: 5px 0;
                border-radius: 3px;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{titulo}</h1>
            <p>Generado: {fecha}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total</h3>
                <h2>{total}</h2>
            </div>
            <div class="summary-card">
                <h3 class="passed">Pasadas</h3>
                <h2 class="passed">{pasadas}</h2>
            </div>
            <div class="summary-card">
                <h3 class="failed">Falladas</h3>
                <h2 class="failed">{falladas}</h2>
            </div>
        </div>
        
        <div class="scenarios">
            {scenarios_html}
        </div>
    </body>
    </html>
    """
    
    scenarios_html = ""
    for scenario in report_data["escenarios"]:
        status_class = "passed" if scenario["estado"] == "pasado" else "failed"
        steps_html = ""
        
        for step in scenario["pasos"]:
            step_class = "passed" if step["estado"] == "passed" else "failed"
            error_html = f'<div class="error">{step.get("error", "")}</div>' if step.get("error") else ""
            steps_html += f'''
                <div class="step {step_class}">
                    {step["nombre"]}
                    {error_html}
                </div>
            '''
        
        scenarios_html += f'''
            <div class="scenario">
                <div class="scenario-header">
                    <h3>{scenario["nombre"]}</h3>
                    <span class="{status_class}">{"✓" if scenario["estado"] == "pasado" else "✗"} {scenario["estado"].upper()}</span>
                </div>
                <div class="steps">
                    {steps_html}
                </div>
            </div>
        '''
    
    html_content = html_template.format(
        titulo=report_data["titulo"],
        fecha=report_data["fecha"],
        total=report_data["resumen"]["total"],
        pasadas=report_data["resumen"]["pasadas"],
        falladas=report_data["resumen"]["falladas"],
        scenarios_html=scenarios_html
    )
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/bdd-report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("Reporte HTML generado: reports/bdd-report.html")

def generate_allure_report():
    try:
        subprocess.run([
            "allure", "generate", 
            "reports/allure-results", 
            "-o", "reports/allure-report", 
            "--clean"
        ], check=True)
        print("Reporte Allure generado: reports/allure-report/index.html")
    except subprocess.CalledProcessError as e:
        print(f"Error generando reporte Allure: {e}")
    except FileNotFoundError:
        print("Allure no está instalado. Instálelo con: npm install -g allure-commandline")

if __name__ == "__main__":
    generate_html_report()
    generate_allure_report()