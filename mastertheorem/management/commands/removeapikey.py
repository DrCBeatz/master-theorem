# mastertheorem/management/commands/removeapikey.py

from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Removes the MDB Pro API key from package.json and package-lock.json'

    def handle(self, *args, **kwargs):
        api_key = os.getenv('MDB_PRO_KEY')
        for filename in ['package.json', 'package-lock.json']:
            file_path = f'frontend/{filename}'
            with open(file_path, 'r') as file:
                content = file.read()

            updated_content = content.replace(api_key, '[api-key-redacted]')

            if content != updated_content:
                with open(file_path, 'w') as file:
                    file.write(updated_content)
                self.stdout.write(self.style.SUCCESS(f'Successfully removed the API key from {filename}.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'No changes made to {filename}.'))
