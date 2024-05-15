import os
from pyairtable import Api

api = Api(os.environ['AIRTABLE_API_KEY'])

jogos = api.table('appt1Ti26Kq8T2LUq', 'tblmhR0EON7a45Sod')

def get_secret():
    return os.environ['AIRTABLE_API_KEY']