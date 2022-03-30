import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pandas as pd

def create_df():
    
    basedir = os.getcwd()
    l = basedir.split('/')
    del l[-4:]
    print(l)
    l_new = l[0]
    for i in range(len(l)):
        l_new = os.path.join(l_new,l[i])
    basedir = l_new
    dir = os.path.join('/',basedir,'secrets')
    # use creds to create a client to interact with the Google Drive API
    scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    json_file = os.path.join(dir,"client_secret_spread.json")
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
