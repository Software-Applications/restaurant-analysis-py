# gsheets_data.py

from dotenv import load_dotenv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

def google_sheets_data():
    
    load_dotenv()

    DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
    SHEET_NAME = os.environ.get("SHEET_NAME", "products")

    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    file_name = os.path.join(os.getcwd(), "google_credentials1", "gcreds.json")

    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)

    client = gspread.authorize(creds)

    doc = client.open_by_key(DOCUMENT_ID)

    sheet = doc.worksheet(SHEET_NAME)

    data = sheet.get_all_records()

    return data


''' #working  code. Ignore this for now
 scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
 
 creds = ServiceAccountCredentials.from_json_keyfile_name("gcreds.json", scope)
 
 client = gspread.authorize(creds)
 
 sheet = client.open("shopping_cart").sheet1  # Open the spreadhseet
 
 data = sheet.get_all_records()  # Get a list of all records
 pprint(data)
'''