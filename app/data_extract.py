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
from send_email_notification import send_email

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
    # the commented code was an attempt to auto delete data from google sheets.
    # preserving it for future use

    #rows = sheet.row_count
    # deletes existing data with the api limits set by google
    #for i in range(2, rows+1, 1):
    #test = sheet.cell(2, 1)
    #breakpoint()
    #i = 1
    #if sheet.cell(2, 1) == "":
    #    break
    #else:
    #    sheet.delete_row(2)
    #    i = i + 1
    #    time.sleep(1)
    #    if i % 49 == 0:
    #        time.sleep(105)
    #    else:
    #        pass

    
# Activate this code if you want to write business search data in text file.
# Preserving the functionality for future use

#def write_to_csv_header(csv_filepath, header = []):
#    csv_header = header
#        
#    with open(csv_filepath, "w", newline = '') as csv_file:
#        writer = csv.DictWriter(csv_file, fieldnames=csv_header)
#        writer.writeheader()
#
#
#def write_to_csv_details(rows, csv_filepath, header = []):
#    # rows should be a list of dictionaries
#    # csv_filepath should be a string filepath pointing to where the data should be written
#
#    csv_header = header
#
#    with open(csv_filepath, "a", newline = '') as csv_file:
#        writer = csv.DictWriter(csv_file, fieldnames=csv_header)
#        # writer.writeheader() # uses fieldnames set above
#        for row in rows:
#            writer.writerow(row)
#
#def del_csv(file_name):
#    if os.path.exists(file_name):
#        os.remove(file_name)
#
#def text_parser(text_data):
#    symbol_parser = re.findall(r'[^\\n]+', text_data)
#    return symbol_parser

#####################################################################################
#> STEP 1 : PULL REQUIRED DATA USING BUSINESS SEARCH, REVIEW APIS
#####################################################################################

#> define your cuisines
#cuisines = ['indian', 'Indian', 'american', 'American', 'chinese', 'Chinese', 'italian', 'Italian', 'thai', 'Thai', 'greek', 'Greek', 'middle_eastern', 'Middle_eastern']
#cuisines = ['indian', 'american', 'chinese', 'italian', 'thai', 'greek', 'middle_eastern']
cuisines = ['indian', 'chinese', 'italian', 'japanese', 'mediterranean', 'thai', 'american', 'greek', 'fusion', 'korean', 'french', 'spanish', 'middle_eastern', 'moroccan', 'turkish', 'lebanese', 'peruvian', 'german', 'african', 'caribbean']

# Activate this code if you want to write business search data in text file.
# Preserving the functionality for future use
#file_name_search = os.path.join(os.getcwd(), "data", "business_search.csv")
#file_name_review = os.path.join(os.getcwd(), "data", "business_review.csv")
#del_csv(file_name_search)
#del_csv(file_name_review)
#write_to_csv_header(file_name_search, header = ['alias', 'categories', 'id', 'id_closed', 'name', 'rating', 'review_count'])
#write_to_csv_header(file_name_review, header = ['restaurant_id', 'text', 'user_rating'])

#######################
#> BUSINESS SEARCH API
#######################

# need to accumulate all businesses ids for reviews api
ids = []
#> BUSINESS SEARCH API. USED TO EXTRACT B
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
            'review_count': restaurant['review_count']
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

    # Activate this code if you want to write business search data in text file.
    # Preserving the functionality for future use

    # write_to_csv_details(rows, file_name_search, header = ['alias', 'categories', 'id', 'id_closed', 'name', 'rating', 'review_count'])

    


#######################
#> BUSINESS REVIEWS API
#######################
### reviews api is https://api.yelp.com/v3/businesses/{id}/reviews. 
### it requires a business id to work. business ids are available in 'ids' list

time.sleep(150)
  
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
            'text' : detail['text']
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


#cur_date()
google_sheets_data('meta', cur_date, 2)





    