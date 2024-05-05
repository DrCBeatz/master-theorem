# set_profile_to_null.py
import yaml
import os

def set_profile_to_null():
    config_path = os.path.join(os.getcwd(), '.elasticbeanstalk', 'config.yml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    config['global']['profile'] = None

    with open(config_path, 'w') as file:
        yaml.safe_dump(config, file, default_flow_style=False)

if __name__ == '__main__':
    set_profile_to_null()