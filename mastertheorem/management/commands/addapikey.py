# mastertheorem/management/commands/addapikey.py

from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Adds the MDB Pro API key to package.json and package-lock.json'

    def handle(self, *args, **kwargs):
        api_key = os.getenv('MDB_PRO_KEY')
        for filename in ['package.json', 'package-lock.json']:
            file_path = f'frontend/{filename}'
            with open(file_path, 'r') as file:
                content = file.read()

            updated_content = content.replace('[api-key-redacted]', api_key)

            if content != updated_content:
                with open(file_path, 'w') as file:
                    file.write(updated_content)
                self.stdout.write(self.style.SUCCESS(f'Successfully added the API key to {filename}.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'No changes made to {filename}.'))
