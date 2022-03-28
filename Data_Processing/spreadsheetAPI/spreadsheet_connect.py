from __future__ import print_function

import os
import os.path
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


data_range_start= int(input("Please enter starting ID"))
data_range_end= int(input("Please enter ending ID "))


# Before using this piece of code, you should register on google cloud project
# platform and create a project. Download the authorization file and rename it
# credentials.json then put it under the same directory.

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Cuy2e5aFFZABqxNwxDYxcOO5q__McrgajVGhzXMueac'
SAMPLE_RANGE_NAME = 'Sheet1!A2:C'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


###connect to google sheet and get the entire set of data in data ID range as a dataframe
def main():
    creds = None

    if os.path.exists('../../../googlesheetapiii/token.json'):
        creds = Credentials.from_authorized_user_file('../../../googlesheetapiii/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../../../googlesheetapiii/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../../../googlesheetapiii/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
            return

        df=pd.DataFrame(columns=['ID','URL','RATING'])
        for i in range(data_range_start-1,data_range_end):
                df=df.append({'ID': values[i][0], 'URL': values[i][1], 'RATING': values[i][2]}, ignore_index=True)
        return df

    except HttpError as err:
        print(err)


df=main()


