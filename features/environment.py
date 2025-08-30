from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def before_all(context):
    context.base_url = os.environ.get('BASE_URL', 'http://localhost:8080')
    context.headless = os.environ.get('HEADLESS', 'False').lower() == 'true'

def before_scenario(context, scenario):
    chrome_options = Options()
    if context.headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
    
    context.driver = webdriver.Chrome(options=chrome_options)
    context.driver.maximize_window()

def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        if scenario.status == 'failed':
            screenshot_dir = 'reports/screenshots'
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = f"{screenshot_dir}/{scenario.name}_{scenario.status}.png"
            context.driver.save_screenshot(screenshot_path)
            print(f"Captura guardada: {screenshot_path}")
        
        context.driver.quit()

def after_all(context):
    pass