"""
Configuration loader that combines YAML config with environment variables
"""
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

#Load environment variables from .env file#
load_dotenv()

def load_config():
    """Load configuration from config.yaml and environment variables"""
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Add database credentials from environment variables
    if 'database' in config and 'postgres' in config['database']:
        config['database']['postgres']['username'] = os.getenv('DB_USERNAME')
        config['database']['postgres']['password'] = os.getenv('DB_PASSWORD')
    
    return config

def get_db_connection_string():
    """Generate PostgreSQL connection string from config"""
    config = load_config()
    db_config = config['database']['postgres']
    
    conn_string = (
        f"postgresql://{db_config['username']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )
    
    if db_config.get('require_ssl'):
        conn_string += "?sslmode=require"
    
    return conn_string

if __name__ == "__main__":
    # Test the config loader
    config = load_config()
    print("✅ Config loaded successfully!")
    print(f"Default org: {config['salesforce']['default_org']}")
    print(f"Database: {config['database']['postgres']['database']}")
    print(f"Default record count: {config['data_generation']['default_record_count']}")
