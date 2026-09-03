"""
Automated Browser Screenshot Capture Script
Uses Selenium with Chrome Headless to:
1. Verify Desktop Web UI (1280x800):
   - Home page (screenshots/web/web_home.png)
   - Diabetes prediction result (screenshots/web/diabetes_web_result.png)
   - House price prediction result (screenshots/web/house_web_result.png)
   - E-commerce prediction result (screenshots/web/ecommerce_web_result.png)
2. Verify Mobile Viewport (390x844):
   - Mobile home (screenshots/mobile/mobile_home.png)
   - Mobile diabetes result (screenshots/mobile/diabetes_mobile.png)
   - Mobile house price result (screenshots/mobile/house_mobile.png)
   - Mobile e-commerce result (screenshots/mobile/ecommerce_mobile.png)
3. Verify Swagger UI:
   - Swagger documentation (screenshots/api/swagger_docs.png)
   - API diabetes endpoint (screenshots/api/api_diabetes_result.png)
   - API house endpoint (screenshots/api/api_house_result.png)
   - API e-commerce endpoint (screenshots/api/api_ecommerce_result.png)
"""

import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_WEB = PROJECT_ROOT / "screenshots" / "web"
SCREENSHOTS_MOBILE = PROJECT_ROOT / "screenshots" / "mobile"
SCREENSHOTS_API = PROJECT_ROOT / "screenshots" / "api"

SCREENSHOTS_WEB.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_MOBILE.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_API.mkdir(parents=True, exist_ok=True)


def get_driver(width=1280, height=900, is_mobile=False):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--window-size={width},{height}")

    if is_mobile:
        options.add_experimental_option("mobileEmulation", {
            "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        })

    driver = webdriver.Chrome(options=options)
    return driver


def capture_desktop(base_url="http://127.0.0.1:8000"):
    print("\n--- CAPTURING DESKTOP SCREENSHOTS (1280x900) ---")
    driver = get_driver(width=1280, height=900, is_mobile=False)
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Web Home
        driver.get(f"{base_url}/")
        time.sleep(1.5)
        driver.save_screenshot(str(SCREENSHOTS_WEB / "web_home.png"))
        print(f"✓ Saved {SCREENSHOTS_WEB / 'web_home.png'}")

        # 2. Diabetes Prediction Result
        btn_diabetes = wait.until(EC.element_to_be_clickable((By.ID, "btn-predict-diabetes")))
        btn_diabetes.click()
        time.sleep(1.2)
        driver.save_screenshot(str(SCREENSHOTS_WEB / "diabetes_web_result.png"))
        print(f"✓ Saved {SCREENSHOTS_WEB / 'diabetes_web_result.png'}")

        # 3. House Price Tab & Result
        nav_house = wait.until(EC.element_to_be_clickable((By.ID, "nav-btn-house")))
        nav_house.click()
        time.sleep(0.8)
        btn_house = wait.until(EC.element_to_be_clickable((By.ID, "btn-predict-house")))
        btn_house.click()
        time.sleep(1.2)
        driver.save_screenshot(str(SCREENSHOTS_WEB / "house_web_result.png"))
        print(f"✓ Saved {SCREENSHOTS_WEB / 'house_web_result.png'}")

        # 4. E-Commerce Tab & Result
        nav_ecom = wait.until(EC.element_to_be_clickable((By.ID, "nav-btn-ecommerce")))
        nav_ecom.click()
        time.sleep(0.8)
        btn_ecom = wait.until(EC.element_to_be_clickable((By.ID, "btn-predict-ecommerce")))
        btn_ecom.click()
        time.sleep(1.2)
        driver.save_screenshot(str(SCREENSHOTS_WEB / "ecommerce_web_result.png"))
        print(f"✓ Saved {SCREENSHOTS_WEB / 'ecommerce_web_result.png'}")

    finally:
        driver.quit()


def capture_mobile(base_url="http://127.0.0.1:8000"):
    print("\n--- CAPTURING MOBILE SCREENSHOTS (390x844 Viewport) ---")
    driver = get_driver(width=390, height=844, is_mobile=True)
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Mobile Home
        driver.get(f"{base_url}/")
        time.sleep(1.5)
        driver.save_screenshot(str(SCREENSHOTS_MOBILE / "mobile_home.png"))
        print(f"✓ Saved {SCREENSHOTS_MOBILE / 'mobile_home.png'}")

        # 2. Mobile Diabetes Result
        btn_diabetes = wait.until(EC.element_to_be_clickable((By.ID, "btn-predict-diabetes")))
        # Scroll to button and click
        driver.execute_script("arguments[0].scrollIntoView(true);", btn_diabetes)
        time.sleep(0.5)
        btn_diabetes.click()
        time.sleep(1.2)
        # Scroll down to view result
        result_elem = driver.find_element(By.ID, "diabetes-result")
        driver.execute_script("arguments[0].scrollIntoView(true);", result_elem)
        time.sleep(0.5)
        driver.save_screenshot(str(SCREENSHOTS_MOBILE / "diabetes_mobile.png"))
        print(f"✓ Saved {SCREENSHOTS_MOBILE / 'diabetes_mobile.png'}")

        # 3. Mobile House Result
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        nav_house = wait.until(EC.element_to_be_clickable((By.ID, "nav-btn-house")))
        nav_house.click()
        time.sleep(0.8)
        btn_house = wait.until(EC.element_to_be_clickable((By.ID, "btn-predict-house")))
        driver.execute_script("arguments[0].scrollIntoView(true);", btn_house)
        time.sleep(0.5)
        btn_house.click()
        time.sleep(1.2)
        result_elem = driver.find_element(By.ID, "house-result")
        driver.execute_script("arguments[0].scrollIntoView(true);", result_elem)
        time.sleep(0.5)
        driver.save_screenshot(str(SCREENSHOTS_MOBILE / "house_mobile.png"))
        print(f"✓ Saved {SCREENSHOTS_MOBILE / 'house_mobile.png'}")

        # 4. Mobile E-Commerce Result
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        nav_ecom = wait.until(EC.element_to_be_clickable((By.ID, "nav-btn-ecommerce")))
        nav_ecom.click()
        time.sleep(0.8)
        btn_ecom = wait.until(EC.element_to_be_clickable((By.ID, "btn-predict-ecommerce")))
        driver.execute_script("arguments[0].scrollIntoView(true);", btn_ecom)
        time.sleep(0.5)
        btn_ecom.click()
        time.sleep(1.2)
        result_elem = driver.find_element(By.ID, "ecom-result")
        driver.execute_script("arguments[0].scrollIntoView(true);", result_elem)
        time.sleep(0.5)
        driver.save_screenshot(str(SCREENSHOTS_MOBILE / "ecommerce_mobile.png"))
        print(f"✓ Saved {SCREENSHOTS_MOBILE / 'ecommerce_mobile.png'}")

    finally:
        driver.quit()


def capture_swagger(base_url="http://127.0.0.1:8000"):
    print("\n--- CAPTURING SWAGGER API SCREENSHOTS ---")
    driver = get_driver(width=1280, height=900, is_mobile=False)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(f"{base_url}/docs")
        time.sleep(2.0)
        driver.save_screenshot(str(SCREENSHOTS_API / "swagger_docs.png"))
        print(f"✓ Saved {SCREENSHOTS_API / 'swagger_docs.png'}")

        # Expand /predict/diabetes
        try:
            op_block = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.opblock-summary-post")))
            op_block.click()
            time.sleep(1.0)
            driver.save_screenshot(str(SCREENSHOTS_API / "api_diabetes_result.png"))
            print(f"✓ Saved {SCREENSHOTS_API / 'api_diabetes_result.png'}")
        except Exception as e:
            print(f"Notice expanding operation block: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    capture_desktop()
    capture_mobile()
    capture_swagger()
    print("\n[✓] ALL SCREENSHOTS CAPTURED SUCCESSFULLY!")
