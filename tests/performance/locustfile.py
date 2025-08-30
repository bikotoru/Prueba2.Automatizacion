from locust import HttpUser, task, between
import json
import random
import time

class LoginPerformanceTest(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        self.client.verify = False
        self.users = [
            {"email": f"usuario{i}@ejemplo.com", "password": f"Password{i}!23"} 
            for i in range(1, 11)
        ]
        self.login_attempts = 0
        self.successful_logins = 0
        self.failed_logins = 0
    
    @task(3)
    def login_valid_user(self):
        user = random.choice(self.users)
        start_time = time.time()
        
        with self.client.post(
            "/api/login",
            json=user,
            catch_response=True,
            name="Login - Credenciales Válidas"
        ) as response:
            self.login_attempts += 1
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                self.successful_logins += 1
                response.success()
                
                if response_time > 2000:
                    response.failure(f"Tiempo de respuesta alto: {response_time:.0f}ms")
            else:
                self.failed_logins += 1
                response.failure(f"Login falló: {response.status_code}")
    
    @task(1)
    def login_invalid_password(self):
        with self.client.post(
            "/api/login",
            json={
                "email": "usuario@ejemplo.com",
                "password": "ContraseñaIncorrecta"
            },
            catch_response=True,
            name="Login - Contraseña Inválida"
        ) as response:
            if response.status_code == 401:
                response.success()
            else:
                response.failure(f"Código esperado 401, recibido: {response.status_code}")
    
    @task(1)
    def login_invalid_email(self):
        with self.client.post(
            "/api/login",
            json={
                "email": "emailinvalido",
                "password": "Password123!"
            },
            catch_response=True,
            name="Login - Email Inválido"
        ) as response:
            if response.status_code == 400:
                response.success()
            else:
                response.failure(f"Código esperado 400, recibido: {response.status_code}")
    
    @task(2)
    def check_session(self):
        with self.client.get(
            "/api/session",
            catch_response=True,
            name="Verificar Sesión"
        ) as response:
            if response.status_code in [200, 401]:
                response.success()
            else:
                response.failure(f"Error inesperado: {response.status_code}")
    
    def on_stop(self):
        print(f"Estadísticas del usuario:")
        print(f"  - Intentos de login: {self.login_attempts}")
        print(f"  - Logins exitosos: {self.successful_logins}")
        print(f"  - Logins fallidos: {self.failed_logins}")
        if self.login_attempts > 0:
            success_rate = (self.successful_logins / self.login_attempts) * 100
            print(f"  - Tasa de éxito: {success_rate:.2f}%")

class ApiStressTest(HttpUser):
    wait_time = between(0.5, 1.5)
    
    @task
    def stress_login_endpoint(self):
        payload = {
            "email": f"stress_user_{random.randint(1, 1000)}@test.com",
            "password": "StressTest123!"
        }
        
        with self.client.post(
            "/api/login",
            json=payload,
            catch_response=True,
            name="Stress Test - Login"
        ) as response:
            if response.elapsed.total_seconds() > 3:
                response.failure("Timeout: respuesta mayor a 3 segundos")
            elif response.status_code in [200, 401, 400]:
                response.success()
            else:
                response.failure(f"Error del servidor: {response.status_code}")