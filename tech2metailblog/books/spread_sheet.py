import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
import pandas as pd

def create_df():
    '''
    basedir = os.getcwd()
    l = basedir.split('/')
    del l[-4:]
    print(l)
    l_new = l[0]
    for i in range(len(l)):
        l_new = os.path.join(l_new,l[i])
    basedir = l_new
    dir = os.path.join('/',basedir,'secrets')
    '''
    secrets_dict = {'type':os.getenv('type'),
                    'project_id':os.getenv('project_id'),
                    'private_key_id':os.getenv('private_key_id'),
                    'client_x509_cert_url':os.getenv('client_x509_cert_url'),
                    'auth_provider_x509_cert_url':os.getenv('auth_provider_x509_cert_url'),
                    'token_uri':os.getenv('token_uri'),
                    'auth_uri':os.getenv('auth_uri'),
                    'client_id':os.getenv('client_id'),
                    'client_email':os.getenv('client_email')}
    
    # use creds to create a client to interact with the Google Drive API
    scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    json_file = json.dumps(secrets_dict)
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("本データベース").sheet1

    # Extract and print all of the values
    df = pd.DataFrame(sheet.get_all_values())
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    return df
    
if __name__ == '__main__':
    create_df()
