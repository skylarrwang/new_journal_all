from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to ChromeDriver (Update if needed)
CHROMEDRIVER_PATH = "./chromedriver"

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": "./downloads",  # Your download folder
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
options.add_argument("--start-maximized")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

# --- LOGIN ---
driver.get("https://issuu.com/login")
wait.until(EC.presence_of_element_located((By.NAME, "email")))

email = driver.find_element(By.NAME, "email")
password = driver.find_element(By.NAME, "password")
email.send_keys("thenewjournal@gmail.com")
password.send_keys("305crown")
password.send_keys(Keys.RETURN)

# --- NAVIGATE TO PUBLICATIONS PAGE ---
wait.until(EC.url_contains("home"))
driver.get("https://issuu.com/home/published")
time.sleep(5)

# --- LOAD ALL PUBLICATIONS ---

while True:
    try:
        load_more_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//span[contains(text(), "Load more")]')))
        print("Clicking 'Load more'...")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_button)
        time.sleep(1)  # Brief pause after scrolling
        
        # Use JavaScript click for consistency with your other code
        driver.execute_script("arguments[0].click();", load_more_button)
        time.sleep(5)  # Wait for new content to load
    except Exception as e:
        print(f"No more 'Load more' buttons or timed out: {e}")
        break

time.sleep(5)


menu_buttons = driver.find_elements(By.XPATH, 
    '//div[contains(@class, "PopupBox__popup-box-container")]//button[contains(@class, "ProductButton__product-button--icon-alone") and @aria-expanded="false"]')

print(f"Found {len(menu_buttons)} publication menus.")

for index, menu_button in enumerate(menu_buttons):
    try:
        print(f"Opening menu for publication #{index + 1}")
        
        # Get the button's ID before clicking it
        button_id = menu_button.get_attribute('id')
        print(f"Button ID: {button_id}")
        
        # Scroll to ensure visibility
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu_button)
        time.sleep(1)
        
        # Click the button
        driver.execute_script("arguments[0].click();", menu_button)
        time.sleep(1)
        
        # Target the download option using the button ID prefix
        # This ensures we're looking at the dropdown connected to the button we just clicked
        button_prefix = button_id.split('-more-options')[0]
        download_xpath = f"//span[@id='{button_prefix}-more-options-option-0']//span[contains(text(), 'Download Publication')]"
        
        download_option = wait.until(EC.element_to_be_clickable((By.XPATH, download_xpath)))
        driver.execute_script("arguments[0].click();", download_option)
        print(f"Clicked 'Download Publication' for issue #{index + 1}")
        
        time.sleep(8)  # Allow more time for download
        
        # Close any modals
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        time.sleep(2)
        
    except Exception as e:
        print(f"Failed to download issue #{index + 1}: {e}")
        # Take a screenshot for debugging
        driver.save_screenshot(f"error_{index+1}.png")
        continue

print("All downloads attempted.")
driver.quit()
