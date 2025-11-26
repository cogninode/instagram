# import os

# class Config:
#     # Flask Configuration
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
    
#     # Database
#     DATABASE_PATH = 'data/scraper.db'
    
#     # Scraping Configuration
#     IMPLICIT_WAIT = 10  # seconds
#     PAGE_LOAD_TIMEOUT = 30  # seconds
#     SCROLL_PAUSE_TIME = 2  # seconds
#     REQUEST_DELAY_MIN = 3  # minimum delay between requests
#     REQUEST_DELAY_MAX = 7  # maximum delay between requests
    
#     # Account Rotation
#     MAX_TASKS_PER_ACCOUNT = 5  # Switch account after N tasks
#     ACCOUNT_COOLDOWN_TIME = 300  # seconds (5 minutes)
    
#     # Instagram URLs
#     INSTAGRAM_URL = 'https://www.instagram.com'
#     INSTAGRAM_LOGIN_URL = 'https://www.instagram.com/accounts/login/'
    
#     # Scraping Limits
#     MAX_POSTS_PER_PROFILE = 50
#     MAX_FOLLOWERS_TO_SCRAPE = 100
#     MAX_COMMENTS_PER_POST = 50

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/scraper.db')
    
    # Scraping Configuration
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', 10))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', 30))
    SCROLL_PAUSE_TIME = int(os.getenv('SCROLL_PAUSE_TIME', 2))
    REQUEST_DELAY_MIN = int(os.getenv('REQUEST_DELAY_MIN', 3))
    REQUEST_DELAY_MAX = int(os.getenv('REQUEST_DELAY_MAX', 7))
    
    # Account Rotation
    MAX_TASKS_PER_ACCOUNT = int(os.getenv('MAX_TASKS_PER_ACCOUNT', 5))
    ACCOUNT_COOLDOWN_TIME = int(os.getenv('ACCOUNT_COOLDOWN_TIME', 300))
    
    # Instagram URLs
    INSTAGRAM_URL = 'https://www.instagram.com'
    INSTAGRAM_LOGIN_URL = 'https://www.instagram.com/accounts/login/'
    
    # Scraping Limits
    MAX_POSTS_PER_PROFILE = int(os.getenv('MAX_POSTS_PER_PROFILE', 50))
    MAX_FOLLOWERS_TO_SCRAPE = int(os.getenv('MAX_FOLLOWERS_TO_SCRAPE', 100))
    MAX_COMMENTS_PER_POST = int(os.getenv('MAX_COMMENTS_PER_POST', 50))
    
    # Instagram Accounts
    @staticmethod
    def get_instagram_accounts():
        """Parse Instagram accounts from environment variables"""
        accounts = []
        
        # Method 1: Load from INSTAGRAM_ACCOUNTS (comma-separated)
        accounts_str = os.getenv('INSTAGRAM_ACCOUNTS', '')
        if accounts_str:
            for account in accounts_str.split(','):
                account = account.strip()
                if ':' in account:
                    username, password = account.split(':', 1)
                    accounts.append({
                        'username': username.strip(),
                        'password': password.strip()
                    })
        
        # Method 2: Load from numbered variables (INSTAGRAM_ACCOUNT_1, etc.)
        i = 1
        while True:
            account_str = os.getenv(f'INSTAGRAM_ACCOUNT_{i}')
            if not account_str:
                break
            if ':' in account_str:
                username, password = account_str.split(':', 1)
                accounts.append({
                    'username': username.strip(),
                    'password': password.strip()
                })
            i += 1
        
        return accounts
