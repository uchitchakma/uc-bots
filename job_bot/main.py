#main.py
from bot import JobApplicationBot

def main():
    platforms = ["linkedin", "glassdoor", "indeed", "naukri", "cutshort"]
    job_query = "Software Engineer"

    for platform in platforms:
        print(f"\nStarting applications on {platform.capitalize()}:")
        bot = JobApplicationBot(platform)
        bot.run(job_query)
        print(f"Completed applications on {platform.capitalize()}.\n")

    print("All applications completed!")

if __name__ == "__main__":
    main()
