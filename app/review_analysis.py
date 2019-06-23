# review_analysis.py

import requests
from dotenv import load_dotenv
import datetime
import os
import csv
import re
import json
from pprint import pprint

#> loads contents of the .env file into the script's environment
load_dotenv() 

#> assign the API_Key to a variable and create a headers variable that can be used for authentication.
#  headers variable will be used to pass requests to YELP Fusion APIs
API_KEY = os.environ.get("API_KEY", "Authentication Error!!")
headers = {'Authorization': 'Bearer %s' % API_KEY}
#breakpoint()


#> program functions

def write_to_csv_header(csv_filepath, header = []):
    csv_header = header
        
    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_header)
        writer.writeheader()


def write_to_csv_details(rows, csv_filepath, header = []):
    # rows should be a list of dictionaries
    # csv_filepath should be a string filepath pointing to where the data should be written

    csv_header = header

    with open(csv_filepath, "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_header)
        # writer.writeheader() # uses fieldnames set above
        for row in rows:
            writer.writerow(row)

def del_csv(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

#####################################################################################
#> STEP 1 : PULL REQUIRED DATA USING BUSINESS SEARCH, REVIEW APIS
#####################################################################################

#> define your cuisines
cuisines = ['indian', 'Indian', 'american', 'American', 'chinese', 'Chinese', 'italian', 'Italian', 'thai', 'Thai', 'greek', 'Greek', 'middle_eastern', 'Middle_eastern']

file_name_search = os.path.join(os.getcwd(), "data", "business_search.csv")
file_name_review = os.path.join(os.getcwd(), "data", "business_review.csv")

del_csv(file_name_search)
del_csv(file_name_review)

#if os.path.exists(file_name_search):
#    os.remove(file_name_search)

write_to_csv_header(file_name_search, header = ['alias', 'categories', 'id', 'id_closed', 'name', 'rating', 'review_count'])
write_to_csv_header(file_name_review, header = ['restaurant_id', 'text', 'user_rating'])

#######################
#> BUSINESS SEARCH API
#######################

# need to accumulate all businesses ids for reviews api
ids = []

#> BUSINESS SEARCH API. USED TO EXTRACT B
url_search='https://api.yelp.com/v3/businesses/search'

for cuisine in cuisines:
     
    ###  searches based on cuisine type in New York City
    params_search = {'term':cuisine,'location':'New York City'}

    ###  Making a get request to the API
    req_search=requests.get(url_search, params=params_search, headers=headers)

    ### checks whether the get request is successful or not
    #print('The status code is {}'.format(req_search.status_code))

    ### converting into json format 
    business_search = json.loads(req_search.text)
    
    ### sample - delete it at the end
    '''
    pprint(indian_restaurants[0]["categories"])
    pprint(indian_restaurants[0]["id"])
    pprint(indian_restaurants[0]["is_closed"])
    pprint(indian_restaurants[0]["name"])
    pprint(indian_restaurants[0]["price"])
    pprint(indian_restaurants[0]["rating"])
    pprint(indian_restaurants[0]["review_count"])
    #breakpoint()
    '''
    ### writing relevant data in csv file. doing so because it is easy to import as pandas dataframe
    restaurants = business_search["businesses"]
    rows = []

    for restaurant in restaurants:
        row = {
            'alias': restaurant['alias'],
            'categories': cuisine.lower(),
            'id': restaurant['id'],
            'id_closed': restaurant['is_closed'],
            'name': restaurant['name'],
            #'price': restaurant['price'],
            'rating': restaurant['rating'],
            'review_count': restaurant['review_count']
        }
        rows.append(row)
        # useful for reviews api
        ids.append(row['id'])

    write_to_csv_details(rows, file_name_search, header = ['alias', 'categories', 'id', 'id_closed', 'name', 'rating', 'review_count'])


#######################
#> BUSINESS REVIEWS API
#######################
### reviews api is https://api.yelp.com/v3/businesses/{id}/reviews. 
### it requires a business id to work. business ids are available in ids list
#breakpoint()
rows=[]
for id in ids:
    #pprint(id)
    url_reviews = f"https://api.yelp.com/v3/businesses/{id}/reviews"
    req_reviews=requests.get(url_reviews, headers=headers)
    #pprint(req_reviews)
    business_review = json.loads(req_reviews.text)
    review_details = business_review['reviews']

    for detail in review_details:
        row = {
            'restaurant_id' : detail['id'],
            'user_rating' : detail['rating'],
            'text' : detail['text']
        }
        rows.append(row)

    write_to_csv_details(rows, file_name_review, header = ['restaurant_id', 'text', 'user_rating'])

        


#
#    ###  searches based on cuisine type in New York City
#    #params = {'term':cuisine,'location':'New York City'}
#
#    ###  Making a get request to the API
#    req_reviews=requests.get(url_reviews, headers=headers)
#
#    ### checks whether the get request is successful or not
#    #print('The status code is {}'.format(req_reviews.status_code))
#
#    ### converting into json format 
#    business_review = json.loads(req_reviews.text)
#    print(business_review)
#    #business_reviews.append(business_review)
#    #pprint(business_reviews)
#
#    breakpoint()