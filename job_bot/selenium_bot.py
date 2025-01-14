from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


class JobApplicationBot:
    def __init__(self, platform):
        self.platform = platform.lower()
        options = Options()
        options.add_argument("--start-maximized")
        # Uncomment the following lines for headless mode (no browser window)
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def login(self, email, password):
        try:
            if self.platform == "glassdoor":
                self.driver.get("https://www.glassdoor.com/profile/login_input.htm")
                self.driver.find_element(By.ID, "userEmail").send_keys(email)
                self.driver.find_element(By.ID, "userPassword").send_keys(password)
                self.driver.find_element(By.XPATH, '//button[text()="Sign In"]').click()

            elif self.platform == "linkedin":
                self.driver.get("https://www.linkedin.com/login")
                self.driver.find_element(By.ID, "username").send_keys(email)
                self.driver.find_element(By.ID, "password").send_keys(password)
                self.driver.find_element(By.XPATH, '//button[text()="Sign in"]').click()

            elif self.platform == "indeed":
                self.driver.get("https://secure.indeed.com/account/login")
                self.driver.find_element(By.ID, "login-email-input").send_keys(email)
                self.driver.find_element(By.ID, "login-password-input").send_keys(password)
                self.driver.find_element(By.XPATH, '//button[text()="Sign in"]').click()

            elif self.platform == "naukri":
                self.driver.get("https://www.naukri.com/nlogin/login")
                self.driver.find_element(By.ID, "usernameField").send_keys(email)
                self.driver.find_element(By.ID, "passwordField").send_keys(password)
                self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

            elif self.platform == "cutshort":
                self.driver.get("https://cutshort.io/login")
                self.driver.find_element(By.ID, "email").send_keys(email)
                self.driver.find_element(By.ID, "password").send_keys(password)
                self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

            print(f"Login successful on {self.platform}.")
        except Exception as e:
            print(f"Login failed on {self.platform}: {e}")
            self.driver.quit()

    def search_and_apply(self, job_query):
        applied_jobs = []
        try:
            if self.platform == "glassdoor":
                self.driver.get("https://www.glassdoor.com/Job/index.htm")
                self.driver.find_element(By.ID, "sc.keyword").send_keys(job_query)
                self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
                jobs = self.driver.find_elements(By.CLASS_NAME, "jobCard")
                for job in jobs[:5]:  # Apply to the first 5 jobs
                    job.click()
                    time.sleep(2)
                    try:
                        self.driver.find_element(By.XPATH, '//button[text()="Apply"]').click()
                        applied_jobs.append(job.text)
                    except Exception:
                        pass

            elif self.platform == "linkedin":
                self.driver.get("https://www.linkedin.com/jobs/")
                self.driver.find_element(By.XPATH, '//input[@placeholder="Search jobs"]').send_keys(job_query)
                self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
                jobs = self.driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
                for job in jobs[:5]:
                    job.click()
                    time.sleep(2)
                    try:
                        self.driver.find_element(By.XPATH, '//button[text()="Easy Apply"]').click()
                        applied_jobs.append(job.text)
                    except Exception:
                        pass

            elif self.platform == "indeed":
                self.driver.get("https://www.indeed.com/")
                self.driver.find_element(By.ID, "text-input-what").send_keys(job_query)
                self.driver.find_element(By.XPATH, '//button[text()="Find Jobs"]').click()
                jobs = self.driver.find_elements(By.CLASS_NAME, "tapItem")
                for job in jobs[:5]:
                    job.click()
                    time.sleep(2)
                    try:
                        self.driver.find_element(By.XPATH, '//button[text()="Apply Now"]').click()
                        applied_jobs.append(job.text)
                    except Exception:
                        pass

            elif self.platform == "naukri":
                self.driver.get("https://www.naukri.com/")
                self.driver.find_element(By.ID, "qsb-keyword-sugg").send_keys(job_query)
                self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
                jobs = self.driver.find_elements(By.CLASS_NAME, "jobTuple")
                for job in jobs[:5]:
                    job.click()
                    time.sleep(2)
                    try:
                        self.driver.find_element(By.XPATH, '//button[text()="Apply"]').click()
                        applied_jobs.append(job.text)
                    except Exception:
                        pass

            elif self.platform == "cutshort":
                self.driver.get("https://cutshort.io/jobs")
                self.driver.find_element(By.XPATH, '//input[@placeholder="Search by job title"]').send_keys(job_query)
                self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
                jobs = self.driver.find_elements(By.CLASS_NAME, "job-card")
                for job in jobs[:5]:
                    job.click()
                    time.sleep(2)
                    try:
                        self.driver.find_element(By.XPATH, '//button[text()="Apply"]').click()
                        applied_jobs.append(job.text)
                    except Exception:
                        pass

            print(f"Successfully applied to jobs on {self.platform}: {applied_jobs}")
        except Exception as e:
            print(f"Error searching or applying on {self.platform}: {e}")
        finally:
            self.driver.quit()
        return applied_jobs


# Test the bot for a specific platform
if __name__ == "__main__":
    email = "your_email@example.com"  # Replace with your email
    password = "your_password"        # Replace with your password
    job_query = "Software Engineer"   # Replace with the job title you're searching for

    # Test for Glassdoor
    bot = JobApplicationBot(platform="glassdoor")
    bot.login(email, password)
    bot.search_and_apply(job_query)
