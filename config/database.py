import os

def get_secret():
    return os.environ['AIRTABLE_API_KEY']
