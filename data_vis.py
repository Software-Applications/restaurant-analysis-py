# gsheets_data.py

from dotenv import load_dotenv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import io
#import altair as alt

#import plotly
#import plotly.plotly as py
#import plotly.graph_objs as go


def google_sheets_data(gsheet):    
    load_dotenv()
    DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
    SHEET_NAME = gsheet
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    file_name = os.path.join(os.getcwd(), "google_credentials", "gcreds.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
    client = gspread.authorize(creds)
    doc = client.open_by_key(DOCUMENT_ID)
    sheet = doc.worksheet(SHEET_NAME)
    data = sheet.get_all_records()
    return data

def quality(x):
    if x == 5:
        return 'Exceptional'
    elif x==4.5 or x==4:
        return 'Very Good'
    elif x==3.5 or x==3:
        return 'Average'
    else:
        return 'Poor'




business_search = google_sheets_data('business_search')
business_reviews = google_sheets_data('business_reviews')
bs_data = pd.DataFrame(business_search)
br_data = pd.DataFrame(business_reviews)

################ Working Code###################################################
'''
##### How good are restaurants in general?
# groups count of restaurnts by rating in desc order. returns data series
rating_count = bs_data.groupby(['rating']).size().reset_index(name='counts').sort_values(by = 'rating', ascending = False)
#breakpoint()
# adding auality column to the data series
rating_count['quality'] = rating_count['rating'].apply(quality)
y_pos = rating_count['quality']
x_pos = rating_count['counts']
plt.bar(y_pos, x_pos, align='center')
plt.xlabel('Quality Rating')
plt.ylabel('# of Restaurants')
plt.title('How good are NYC restaurants??')
bytes_image = io.BytesIO()
plt.savefig(bytes_image, format='png')
plt.show()
'''
#################################################################################3
#user_input = input('Select a cuisine type - ')
########################working code. Better than above. You can delete above#######################
'''
if user_input.lower() == 'all':
    category_count = bs_data.groupby(['rating']).size().reset_index(name='counts')
else:
    bs_data_f = bs_data[bs_data['category'] == user_input]
    category_count = bs_data_f.groupby(['rating']).size().reset_index(name='counts')
category_count['quality'] = category_count['rating'].apply(quality)
#category_count.sort_values(by = 'rating', ascending = False, inplace = True)
del(category_count['rating'])
category_agg = category_count.groupby(['quality']).sum().reset_index()
category_agg['quality'] = pd.Categorical(category_agg['quality'], ['Exceptional', 'Very Good', 'Average', 'Poor'])
category_agg.sort_values(by = 'quality', inplace = True)
y_pos = category_agg['quality']
x_pos = category_agg['counts']
plt.bar(y_pos, x_pos, align='center')
plt.xlabel('Quality Rating')
plt.ylabel('# of Restaurants')
plt.title(f"How did {user_input} restaurants perform??")
plt.show()
'''
#########################################################################################33
bs_review = bs_data[['category', 'review_count']]
bs_rating = bs_data[['category', 'rating']]

bs_review_agg = bs_review.groupby(['category']).sum().reset_index()
bs_rating_agg = bs_rating.groupby(['category']).mean().reset_index()

####################Working. Fix color coding################################3
'''



categories = list(bs_data['category'].unique())
#new_cmap = plt.rand_cmap(100, type='bright', first_color_black=True, last_color_black=False, verbose=True)
colors = ['blue', 'crimson', 'deeppink', 'violet', 'c', 'olive', 'grey', 'plum', 'palegreen', 'sienna', 'navy', 'darkcyan', 'hotpink', 'pink', 'indianred', 'magenta', 'purple', 'brown', 'dimgrey', 'g']

for cat, col in zip(categories, colors):
    bs_review_s = bs_review[bs_review['category'] == cat]
    bs_rating_s = bs_rating[bs_rating['category'] == cat]
    c_bs_rr = pd.concat([bs_review, bs_rating], axis = 1)
    y_pos = c_bs_rr['rating']
    x_pos = c_bs_rr['review_count']
    plt.scatter(x_pos, y_pos, c = col, marker = 'o', s=1, label = cat)
    plt.legend()
plt.show()
'''
###############################################################################


pop_category = bs_review_agg.sort_values(by = 'review_count', ascending = False)
y_pos = pop_category['category']
x_pos = pop_category['review_count']
plt.barh(y_pos, x_pos, align='center')
plt.xlabel('Quality Rating')
plt.ylabel('# of Restaurants')
#plt.title(f"How did {user_input} restaurants perform??")
plt.show()




