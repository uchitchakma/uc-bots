#indeed.py
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Indeed:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.email = os.getenv("INDEED_EMAIL")
        self.password = os.getenv("INDEED_PASSWORD")

        if not self.email or not self.password:
            raise ValueError("Indeed credentials are not set in the .env file")

    def login(self):
        """Login to Indeed."""
        try:
            self.driver.get("https://secure.indeed.com/account/login")
            self.driver.find_element(By.ID, "login-email-input").send_keys(self.email)
            self.driver.find_element(By.ID, "login-password-input").send_keys(self.password)
            self.driver.find_element(By.XPATH, '//button[text()="Sign in"]').click()
            print("Logged into Indeed.")
        except Exception as e:
            print(f"Indeed login failed: {e}")
            self.driver.quit()

    def fill_dynamic_fields(self):
        """Fill dynamic fields based on predefined answers."""
        predefined_answers = {
            "expected salary": "1000000",
            "years of experience": "5",
            "notice period": "Immediate",
        }

        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        for input_field in inputs:
            label = input_field.get_attribute("aria-label") or input_field.get_attribute("placeholder")
            if label:
                key = label.lower()
                if key in predefined_answers:
                    input_field.send_keys(predefined_answers[key])
                elif not input_field.get_attribute("value"):
                    print(f"Manual input required for: {label}")
                    input("Press Enter after completing manual input...")

    def search_and_apply(self, job_query):
        """Search for jobs and apply."""
        try:
            self.driver.get("https://www.indeed.com/")
            search_box = self.driver.find_element(By.ID, "text-input-what")
            search_box.send_keys(job_query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)

            jobs = self.driver.find_elements(By.CLASS_NAME, "job_seen_beacon")  # Adjust as needed
            for job in jobs[:5]:
                try:
                    job.click()
                    time.sleep(2)
                    apply_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[text()='Apply Now']"))
                    )
                    apply_button.click()
                    self.fill_dynamic_fields()
                except Exception as e:
                    print(f"Failed to apply: {e}")
        except Exception as e:
            print(f"Indeed job search failed: {e}")

    def close(self):
        self.driver.quit()
