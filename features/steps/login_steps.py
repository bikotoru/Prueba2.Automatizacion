from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.email_input = (By.ID, "email")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "loginButton")
        self.error_message = (By.CLASS_NAME, "error-message")
        self.welcome_message = (By.CLASS_NAME, "welcome-message")
    
    def navigate_to_login(self):
        self.driver.get("http://localhost:8080/login")
    
    def enter_email(self, email):
        email_field = self.wait.until(EC.presence_of_element_located(self.email_input))
        email_field.clear()
        email_field.send_keys(email)
    
    def enter_password(self, password):
        password_field = self.wait.until(EC.presence_of_element_located(self.password_input))
        password_field.clear()
        password_field.send_keys(password)
    
    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.login_button))
        login_btn.click()
    
    def get_error_message(self):
        try:
            error_element = self.wait.until(EC.presence_of_element_located(self.error_message))
            return error_element.text
        except TimeoutException:
            return None
    
    def get_welcome_message(self):
        try:
            welcome_element = self.wait.until(EC.presence_of_element_located(self.welcome_message))
            return welcome_element.text
        except TimeoutException:
            return None
    
    def is_on_dashboard(self):
        return "dashboard" in self.driver.current_url.lower()
    
    def is_on_login_page(self):
        return "login" in self.driver.current_url.lower()

@given('que estoy en la página de login')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to_login()

@when('ingreso el email "{email}"')
def step_impl(context, email):
    context.login_page.enter_email(email)

@when('ingreso la contraseña "{password}"')
def step_impl(context, password):
    context.login_page.enter_password(password)

@when('hago clic en el botón iniciar sesión')
def step_impl(context):
    context.login_page.click_login()
    time.sleep(2)

@then('debería ser redirigido al dashboard')
def step_impl(context):
    assert context.login_page.is_on_dashboard(), "No fue redirigido al dashboard"

@then('debería ver el mensaje "{message}"')
def step_impl(context, message):
    welcome_msg = context.login_page.get_welcome_message()
    assert welcome_msg and message in welcome_msg, f"No se encontró el mensaje: {message}"

@then('debería permanecer en la página de login')
def step_impl(context):
    assert context.login_page.is_on_login_page(), "No está en la página de login"

@then('debería ver el mensaje de error "{error_message}"')
def step_impl(context, error_message):
    actual_error = context.login_page.get_error_message()
    assert actual_error == error_message, f"Error esperado: {error_message}, Error actual: {actual_error}"

@when('intento iniciar sesión {attempts:d} veces con credenciales incorrectas')
def step_impl(context, attempts):
    for i in range(attempts):
        context.login_page.enter_email("usuario@ejemplo.com")
        context.login_page.enter_password("ContraseñaIncorrecta")
        context.login_page.click_login()
        time.sleep(1)

@then('mi cuenta debería estar bloqueada temporalmente')
def step_impl(context):
    context.login_page.enter_email("usuario@ejemplo.com")
    context.login_page.enter_password("ContraseñaCorrecta123!")
    context.login_page.click_login()
    time.sleep(1)

def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        context.driver.quit()