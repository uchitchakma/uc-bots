import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LinkedIn:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

        # Load email and password from .env
        self.email = os.getenv("LINKEDIN_EMAIL")
        self.password = os.getenv("LINKEDIN_PASSWORD")

        if not self.email or not self.password:
            raise ValueError("LinkedIn credentials are not set in the .env file")

        # Predefined answers for specific questions
        self.predefined_answers = {
            "expected salary": "1000000",
            "years of experience": "5",
            "notice period": "Immediate"
        }

    def login(self):
        """Login to LinkedIn."""
        try:
            self.driver.get("https://www.linkedin.com/login")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            self.driver.find_element(By.ID, "username").send_keys(self.email)
            self.driver.find_element(By.ID, "password").send_keys(self.password)

            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Sign in")]'))
            )
            login_button.click()
            print("Waiting for CAPTCHA to be resolved (if present).")
            self.handle_captcha()
            print("Logged into LinkedIn successfully.")
        except Exception as e:
            print(f"LinkedIn login failed: {e}")
            self.driver.quit()

    def handle_captcha(self):
        """Handle CAPTCHA if present."""
        try:
            WebDriverWait(self.driver, 60).until_not(
                EC.presence_of_element_located((By.CLASS_NAME, "captcha-internal"))
            )
            print("CAPTCHA resolved.")
        except Exception:
            print("CAPTCHA not resolved within the timeout period. Please resolve it manually.")
            input("Press Enter after completing the CAPTCHA manually...")

    def fill_dynamic_fields(self):
        """Handles filling in input fields dynamically in the modal."""
        try:
            # Fill text, email, and number input fields
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for input_field in inputs:
                field_label = (
                    input_field.get_attribute("aria-label")
                    or input_field.get_attribute("placeholder")
                    or input_field.get_attribute("name")
                )
                if field_label:
                    field_label_lower = field_label.lower()
                    print(f"Checking input field: {field_label}")

                    if field_label_lower in self.predefined_answers:
                        answer = self.predefined_answers[field_label_lower]
                        print(f"Filling field: {field_label} with {answer}")
                        input_field.clear()
                        input_field.send_keys(answer)
                    elif not input_field.get_attribute("value"):
                        print(f"Unrecognized field detected: {field_label}. Pausing for manual input.")
                        input("Press Enter after completing the input manually...")

            # Handle dropdowns
            dropdowns = self.driver.find_elements(By.TAG_NAME, "select")
            for dropdown in dropdowns:
                field_label = dropdown.get_attribute("aria-label") or dropdown.get_attribute("name")
                if field_label:
                    print(f"Selecting dropdown: {field_label}")
                    dropdown.click()
                    dropdown.send_keys(Keys.ARROW_DOWN)  # Select the first option
                    dropdown.send_keys(Keys.RETURN)

            # Handle checkboxes
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            for checkbox in checkboxes:
                field_label = checkbox.get_attribute("aria-label") or checkbox.get_attribute("name")
                if field_label and not checkbox.is_selected():
                    print(f"Selecting checkbox: {field_label}")
                    checkbox.click()

        except Exception as e:
            print(f"Error filling dynamic fields: {e}")

    def apply_job(self):
        """Handle applying for a job."""
        try:
            easy_apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button"))
            )
            easy_apply_button.click()
            print("Clicked 'Easy Apply'")

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "artdeco-modal"))
            )
            print("Modal detected. Handling steps.")

            # Fill out all steps of the modal
            step_number = 1
            while True:
                print(f"Handling step {step_number}.")
                self.fill_dynamic_fields()

                # Click the "Review" or "Next" button
                next_button = self.driver.find_elements(By.XPATH, '//button[contains(@aria-label, "Review") or contains(@aria-label, "Next")]')
                if next_button:
                    next_button[0].click()
                    step_number += 1
                    time.sleep(2)  # Add a small delay to allow the next modal step to load
                else:
                    break

            # Click the "Submit application" button
            submit_button = self.driver.find_elements(By.XPATH, '//button[contains(@aria-label, "Submit application")]')
            if submit_button:
                submit_button[0].click()
                print("Application submitted.")
            else:
                print("No Submit button found. Application might be incomplete.")
        except Exception as e:
            print(f"Error during application: {e}")

    def search_and_apply(self, job_query):
        """Search for jobs and apply."""
        try:
            self.driver.get("https://www.linkedin.com/jobs/")
            search_box = self.driver.find_element(By.CLASS_NAME, "jobs-search-box__text-input")
            search_box.send_keys(job_query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)

            jobs = self.driver.find_elements(By.CLASS_NAME, "job-card-container__link")
            for job in jobs[:5]:
                try:
                    job.click()
                    time.sleep(2)

                    external_link = self.driver.find_elements(By.CLASS_NAME, "jobs-apply-button--external")
                    if external_link:
                        print("Job has an external application link. Skipping.")
                        continue

                    self.apply_job()

                except Exception as e:
                    print(f"Failed to apply: {e}")
        except Exception as e:
            print(f"LinkedIn job search failed: {e}")

    def close(self):
        """Close the driver."""
        self.driver.quit()
        print("Driver closed.")


# Example of running the bot
if __name__ == "__main__":
    linkedin_bot = LinkedIn()
    linkedin_bot.login()
    linkedin_bot.search_and_apply("Software Engineer")
    linkedin_bot.close()
