from job_bot.job_platforms.linkedin import LinkedIn
from job_bot.job_platforms.glassdoor import Glassdoor
from job_bot.job_platforms.indeed import Indeed
from job_bot.job_platforms.naukri import Naukri
from job_bot.job_platforms.cutshort import Cutshort


class JobApplicationBot:
    def __init__(self, platform):
        self.platform = platform.lower()
        platform_mapping = {
            "linkedin": LinkedIn,
            "glassdoor": Glassdoor,
            "indeed": Indeed,
            "naukri": Naukri,
            "cutshort": Cutshort,
        }
        self.platform_bot = platform_mapping.get(self.platform)
        if not self.platform_bot:
            raise ValueError(f"Unsupported platform: {self.platform}")

    def run(self, job_query):
        bot = self.platform_bot()
        bot.login()
        bot.search_and_apply(job_query)
