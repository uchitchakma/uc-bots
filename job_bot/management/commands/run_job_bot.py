#run_job_bot.py
from django.core.management.base import BaseCommand
from job_bot.bot import JobApplicationBot

class Command(BaseCommand):
    help = "Runs the job application bot to apply for jobs on selected platforms."

    def add_arguments(self, parser):
        # Add an optional argument for specifying platforms
        parser.add_argument(
            '--platforms',
            nargs='+',  # Accept multiple platform names
            type=str,
            help="List of platforms to run (e.g., --platforms linkedin naukri)"
        )

    def handle(self, *args, **options):
        # Get the platforms from command arguments or use all by default
        selected_platforms = options['platforms'] or ["linkedin", "glassdoor", "indeed", "naukri", "cutshort"]
        job_query = "Software Engineer"

        for platform in selected_platforms:
            self.stdout.write(f"Starting applications on {platform.capitalize()}...")
            try:
                bot = JobApplicationBot(platform)
                bot.run(job_query)
                self.stdout.write(f"Completed applications on {platform.capitalize()}.\n")
            except Exception as e:
                self.stderr.write(f"Error while applying on {platform.capitalize()}: {e}")

        self.stdout.write(self.style.SUCCESS("Selected applications completed successfully!"))
