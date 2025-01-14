from django.core.management.base import BaseCommand
from job_bot.selenium_bot import JobApplicationBot  # Adjust the import according to your project structure

class Command(BaseCommand):
    help = 'Runs the job application bot to apply for jobs automatically'

    def add_arguments(self, parser):
        # Optionally add arguments to control which platforms or job queries to run
        parser.add_argument('-p', '--platform', type=str, help='Specify the platform to apply on')

    def handle(self, *args, **options):
        platform = options.get('platform') if options.get('platform') else 'glassdoor'
        self.stdout.write(f"Starting the job application bot for {platform}...")
        
        # Initialize and run your bot
        bot = JobApplicationBot(platform)
        bot.login()
        # You might want to pass more parameters to search_and_apply based on command arguments
        bot.search_and_apply("Software Engineer")  # Example job query

        self.stdout.write(self.style.SUCCESS('Successfully ran the job application bot.'))
