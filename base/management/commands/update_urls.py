from django.core.management.base import BaseCommand
from base.models import Credential

class Command(BaseCommand):
    help = 'Update URLs in the Credential model'

    def handle(self, *args, **options):
        credentials = Credential.objects.all()

        for credential in credentials:
            old_url = "https://my-portfolio.ridwaanhall.repl.co"  # Old URL to be replaced
            new_url = "https://aaff0b3f-edba-4302-84e4-4c21fe434e72-00-2jg27tl1pjs72.global.replit.dev"  # New URL

            if old_url in credential.company_logo:
                credential.company_logo = credential.company_logo.replace(old_url, new_url)
                credential.save()

        self.stdout.write(self.style.SUCCESS('URLs updated successfully'))
