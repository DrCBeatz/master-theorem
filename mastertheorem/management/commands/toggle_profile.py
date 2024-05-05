# mastertheorem/management/commands/toggle_profile.py
from django.core.management.base import BaseCommand
import yaml
import os

class Command(BaseCommand):
    help = 'Toggle the profile field in the .elasticbeanstalk/config.yml file'

    def handle(self, *args, **options):
        # Path to your config.yml file
        config_path = os.path.join(os.getcwd(), '.elasticbeanstalk', 'config.yml')

        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)

            # Toggle the profile field between null and 'eb-cli'
            if config['global']['profile'] == 'eb-cli':
                config['global']['profile'] = None
            else:
                config['global']['profile'] = 'eb-cli'

            # Write the updated config back to the file
            with open(config_path, 'w') as file:
                yaml.safe_dump(config, file, default_flow_style=False)

            self.stdout.write(self.style.SUCCESS('Successfully toggled the profile field.'))
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {config_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
