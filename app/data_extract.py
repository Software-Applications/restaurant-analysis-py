################################################################################################
# purpose: the purpose of this code is to read data from yelp api and upload it to google sheets
# review_analysis.py
# note: the commented code is preserved for future proposals
# author: dheeraj rekula (rekula.d@gmail.com)
################################################################################################

import requests
from dotenv import load_dotenv
import datetime
import os
import csv
import re
import json
from pprint import pprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import sys
import sendgrid
from sendgrid.helpers.mail import *
#from send_email_notification import send_email

###############################
# loading environment variables
###############################

#> loads contents of the .env file into the script's environment
load_dotenv() 

#> assign the API_Key to a variable and create a headers variable that can be used for authentication.
#  headers variable will be used to pass requests to YELP Fusion APIs
API_KEY = os.environ.get("API_KEY", "Authentication Error!!")
headers = {'Authorization': 'Bearer %s' % API_KEY}

###########################
# program functions
###########################

def cur_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d:%I:%M:%S %p")

def google_sheets_data(gsheet, data_set = [], ind = 2):
    load_dotenv()
    GOOGLE_API_CREDENTIALS = os.environ.get("GOOGLE_API_CREDENTIALS")
    DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS! The desination does not exist")
    SHEET_NAME = gsheet
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    #file_name = os.path.join(os.getcwd(), "google_credentials", "gcreds.json")
    #creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
    #creds = ServiceAccountCredentials.from_json_keyfile_name(json.loads(GOOGLE_API_CREDENTIALS), scope)
    creds = ServiceAccountCredentials._from_parsed_json_keyfile(json.loads(GOOGLE_API_CREDENTIALS), scope)
    client = gspread.authorize(creds)
    doc = client.open_by_key(DOCUMENT_ID)
    sheet = doc.worksheet(SHEET_NAME)
    sheet.insert_row(data_set, ind)
 
def google_sheets_cleanup(gsheet, rows, columns, header = []):
    load_dotenv()
    GOOGLE_API_CREDENTIALS = os.environ.get("GOOGLE_API_CREDENTIALS")
    DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS! The desination does not exist")
    SHEET_NAME = gsheet
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    #file_name = os.path.join(os.getcwd(), "google_credentials", "gcreds.json")
    #creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
    #creds = ServiceAccountCredentials.from_json_keyfile_name(json.loads(GOOGLE_API_CREDENTIALS), scope)
    creds = ServiceAccountCredentials._from_parsed_json_keyfile(json.loads(GOOGLE_API_CREDENTIALS), scope)
    client = gspread.authorize(creds)
    doc = client.open_by_key(DOCUMENT_ID)
    SHEET1 = doc.worksheet(SHEET_NAME)
    doc.del_worksheet(SHEET1)
    doc.add_worksheet(SHEET_NAME, rows, columns)
    SHEET2 = doc.worksheet(SHEET_NAME)
    SHEET2.insert_row(header, 1)

def send_email(text):    
    load_dotenv()
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
    MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    ### load email variables
    from_email = Email(MY_EMAIL_ADDRESS)
    to_email = Email(MY_EMAIL_ADDRESS)
    subject = "Example Notification"
    sub_text = text
    message_text = f"Dear User, \nThis is an automated email response. \n {sub_text}"
    content = Content("text/plain", message_text)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response

#####################################################################################
#> STEP 1 : PULL REQUIRED DATA USING BUSINESS SEARCH, REVIEW APIS
#####################################################################################

#> define your cuisines
#cuisines = ['indian']
cuisines = ['indian', 'chinese', 'italian', 'japanese', 'mediterranean', 'thai', 'american', 'greek', 'fusion', 'korean', 'french', 'spanish', 'middle_eastern', 'moroccan', 'turkish', 'lebanese', 'peruvian', 'german', 'african', 'caribbean']


#######################
#> BUSINESS SEARCH API
#######################
# deletes the old dataset of business_search, and creates a new one with same name

try:
    google_sheets_cleanup('business_search', 10, 7, header = ['alias', 'category', 'restaurant_id', 'id_closed', 'name','rating', 'review_count', 'update_date'])
except:
    err_text = " Business Reviews dataset has been sucessfully truncated"
    send_email(err_text)
    err_cd = 15
    sys.exit(err_cd)

time.sleep(105)

# need to accumulate all businesses ids for reviews api
ids = []
#> BUSINESS SEARCH API. USED TO EXTRACT BUSINESS SEARCH DATA
url_search='https://api.yelp.com/v3/businesses/search'
google_search_index = 2
for cuisine in cuisines:
    ###  searches based on cuisine type in New York City
    params_search = {'term':cuisine,'location':'New York City'}

    ###  Making a get request to the API
    req_search=requests.get(url_search, params=params_search, headers=headers)

    ### checks whether the get request is successful or not
    try:
        req_search.status_code == 200
    except:
        err_text = "Connection to yelp api failed. the is no input available for data processing. contact dheeraj rekula"
        send_email(err_text)
        err_cd = 5
        sys.exit(5)

    ### converting into json format 
    business_search = json.loads(req_search.text)

    ### reading only relevant data
    restaurants = business_search["businesses"]
    rows_business = []
    for restaurant in restaurants:
        row = {
            'alias': restaurant['alias'],
            'categories': cuisine.lower(),
            'id': restaurant['id'],
            'id_closed': restaurant['is_closed'],
            'name': restaurant['name'],
            'rating': restaurant['rating'],
            'review_count': restaurant['review_count'],
            'update_date' : cur_date()
        }
        rows_business.append(row)
        # useful for reviews api below
        ids.append(row['id'])
    try:
        for row in rows_business:                
            row_value = [v for v in row.values()]
            google_sheets_data('business_search', row_value, google_search_index)
            google_search_index = google_search_index + 1
            time.sleep(1)
            if google_search_index % 49 == 0:
                time.sleep(105)
            else:
                pass
        pass_text = f"Data upload of business search for {cuisine} cuisine succeeded. If you find any issues contact dheeraj rekula"
        send_email(pass_text)
    except:
        fail_text = f"Data upload of business search for {cuisine} cuisine failed. contact the dheeraj rekula"
        send_email(fail_text)
        err_cd = 101
        sys.exit(err_cd)

#r = google_sheets_data_del('business_search')
#breakpoint()

#######################
#> BUSINESS REVIEWS API
#######################
### reviews api is https://api.yelp.com/v3/businesses/{id}/reviews. 
### it requires a business id to work. business ids are available in 'ids' list

time.sleep(105)

# removes old dataset of business_reviews
try:
    google_sheets_cleanup('business_reviews', 10, 4, header = ['restaurant_id', 'review_id', 'user_rating', 'text', 'update_date'])
except:
    err_text = " Business Reviews dataset has been sucessfully truncated"
    send_email(err_text)
    err_cd = 15
    sys.exit(err_cd)

time.sleep(105)
  
rows_reviews=[]
for id in ids:
    url_reviews = f"https://api.yelp.com/v3/businesses/{id}/reviews"
    req_reviews=requests.get(url_reviews, headers=headers)
    # email api error
    try:
        req_reviews.status_code == 200
    except:
        err_text = "Connection to yelp reviews api failed. the is no input available for data processing. contact dheeraj rekula"
        send_email(err_text)
        err_cd = 6
        sys.exit(5)
    business_review = json.loads(req_reviews.text)
    review_details = business_review['reviews']
    
    # reading only relevant data
    for detail in review_details:
        row = {
            'restaurant_id' : id,
            'review_id' : detail['id'],
            'user_rating' : detail['rating'],
            'text' : detail['text'],
            'update_date' : cur_date()
        }
        rows_reviews.append(row)

# writes review data to gsheets
google_review_index = 2

try:
    for row in rows_reviews:
        # doing this because i created a list of dictionaries above, as i am comfortable working with dictionaries
        row_value = [v for v in row.values()]
        google_sheets_data('business_reviews', row_value, google_review_index)
        google_review_index = google_review_index + 1
        # the following lines are important to ensure i maintain time restrictions on google drive api
        time.sleep(1)
        if google_review_index % 49 == 0:
            time.sleep(105)
        else:
            pass

    pass_text = "Data upload of business reviews succeeded. if you find any issues contact dheeraj rekula"
    send_email(pass_text)
except:
    fail_text = "Data upload of business search failed. contact the dheeraj rekula"
    send_email(fail_text)
    err_cd = 102
    sys.exit(102)







    