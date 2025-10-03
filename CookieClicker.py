# Import required Selenium modules and time library 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#  Initialize Chrome WebDriver service 
# 'chromedriver.exe' must match the installed Chrome version
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

#  Open the Cookie Clicker game 
driver.get("https://orteil.dashnet.org/cookieclicker/")

#  Define element IDs and prefixes for game elements 
cookie_id = "bigCookie"                # ID of the main cookie to click
cookies_id = "cookies"                 # ID of the cookies counter text
product_price_prefix = "productPrice"  # Prefix for upgrade price elements
product_prefix = "product"             # Prefix for upgrade buttons

#  Step 1: Accept Consent Banner (if present) 
try:
    # Wait for the "Accept Consent" button to appear and become clickable
    consent_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-cta-consent"))
    )
    # Use JavaScript to click (avoids issues with overlays intercepting clicks)
    driver.execute_script("arguments[0].click();", consent_button)
    print("✅ Consent clicked!")

    # Wait until the consent overlay fully disappears before continuing
    WebDriverWait(driver, 15).until_not(
        EC.presence_of_element_located((By.CLASS_NAME, "fc-dialog-container"))
    )
    print("✅ Consent overlay dismissed!")
except Exception as e:
    # If no consent popup appears, continue the script without interruption
    print("⚠️ No consent popup found:", e)

#  Step 2: Select English as the game language 
try:
    # Wait for the English language button to be clickable
    language = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "langSelect-EN"))
    )
    # Again, use JavaScript click to bypass potential overlay issues
    driver.execute_script("arguments[0].click();", language)
    print("✅ English selected!")
except Exception as e:
    print("⚠️ Could not click English:", e)

#  Step 3: Wait until the Big Cookie is visible 
cookie = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, cookie_id))
)

#  Step 4: Main automation loop 
# Continuously clicks the cookie and attempts to buy upgrades
while True:
    try:
        # Click the big cookie
        cookie.click()

        # Get current cookie count from the game UI
        cookies_count_text = driver.find_element(By.ID, cookies_id).text.split(" ")[0]
        cookies_count = int(cookies_count_text.replace(",", ""))  # Remove commas and convert to int

        # Check the first 4 products (Cursor, Grandma, Farm, Mine)
        for i in range(4):
            price_text = driver.find_element(By.ID, product_price_prefix + str(i)).text.replace(",", "")

            # Skip locked products or those without a numeric price
            if not price_text.isdigit():
                continue

            price = int(price_text)

            # If enough cookies are available, purchase the upgrade
            if cookies_count >= price:
                product = driver.find_element(By.ID, product_prefix + str(i))
                product.click()
                print(f"✅ Bought product{i}")
                break  # Only buy one upgrade per loop iteration
    except Exception as e:
        # If an error occurs (e.g., stale element), log and continue
        print("⚠️ Error in loop:", e)

    # Small delay to control click speed (~100 clicks per second)
    time.sleep(0.01)







