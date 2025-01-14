from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JobApplicationBot:
    def __init__(self, platform):
        self.platform = platform.lower()
        options = Options()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        # Load credentials based on platform
        self.email = os.getenv(f"{self.platform.upper()}_EMAIL")
        self.password = os.getenv(f"{self.platform.upper()}_PASSWORD")

    def login(self):
        try:
            url_mapping = {
                "glassdoor": "https://www.glassdoor.com/profile/login_input.htm",
                "linkedin": "https://www.linkedin.com/login",
                "indeed": "https://secure.indeed.com/account/login",
                "naukri": "https://www.naukri.com/nlogin/login",
                "cutshort": "https://cutshort.io/login"
            }
            input_id_mapping = {
                "glassdoor": ("userEmail", "userPassword"),
                "linkedin": ("username", "password"),
                "indeed": ("login-email-input", "login-password-input"),
                "naukri": ("usernameField", "passwordField"),
                "cutshort": ("email", "password")
            }
            button_xpath_mapping = {
                "glassdoor": '//button[text()="Sign In"]',
                "linkedin": '//button[text()="Sign in"]',
                "indeed": '//button[text()="Sign in"]',
                "naukri": '//button[@type="submit"]',
                "cutshort": '//button[text()="Login"]'
            }
            
            self.driver.get(url_mapping[self.platform])
            user_input, pass_input = input_id_mapping[self.platform]
            self.driver.find_element(By.ID, user_input).send_keys(self.email)
            self.driver.find_element(By.ID, pass_input).send_keys(self.password)
            self.driver.find_element(By.XPATH, button_xpath_mapping[self.platform]).click()

            print(f"Login successful on {self.platform}.")
        except Exception as e:
            print(f"Login failed on {self.platform}: {e}")
            self.driver.quit()

    def search_and_apply(self, job_query):
        # Placeholder for the method body; this needs to be tailored to each site's structure
        print(f"Applying for jobs using query: {job_query} on {self.platform}")
        # Example logic might go here
        return ["List of applied jobs or status messages"]

def main():
    platforms = ["glassdoor", "linkedin", "indeed", "naukri", "cutshort"]
    job_queries = ["Product Designer", "UI/UX Designer", "UX Engineer", "Front-End Developer"]

    while True:
        for platform in platforms:
            print(f"\n=== Starting job applications on {platform} ===")
            bot = JobApplicationBot(platform=platform)
            bot.login()

            for job_query in job_queries:
                print(f"Searching for jobs: {job_query} on {platform}")
                applied_jobs = bot.search_and_apply(job_query)
                print(f"Jobs applied for '{job_query}' on {platform}: {applied_jobs}")

        # Pause or wait for user input to continue/exit
        should_continue = input("Press Enter to run again or type 'exit' to stop: ")
        if should_continue.lower() == 'exit':
            print("Stopping the job application bot.")
            break

if __name__ == "__main__":
    main()
