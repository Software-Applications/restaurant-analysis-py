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
import sys
from itertools import chain
from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
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

def savefile(fileandext):
    file_name = os.path.join(os.getcwd(), "plot_images", fileandext)
    if os.path.exists(file_name):
        os.remove(file_name)
    return file_name

def float_format(data):
    x = "{0:.2f}".format(data)
    return x

if __name__ == "__main__":
    
    ### Defining the initial datasets

    business_search = google_sheets_data('business_search_bk')
    business_reviews = google_sheets_data('business_reviews_bk')
    bs_data = pd.DataFrame(business_search)
    br_data = pd.DataFrame(business_reviews)
    cumm_bs_br = bs_data.merge(br_data, on = 'restaurant_id', how = 'inner')

    bs_review = bs_data[['category','restaurant_id', 'review_count']]
    bs_rating = bs_data[['category', 'restaurant_id', 'rating']]
    bs_review_agg = bs_review.groupby(['category']).sum().reset_index()
    bs_rating_agg = bs_rating.groupby(['category']).mean().reset_index()

    colors = ['blue', 'crimson', 'deeppink', 'violet', 'c', 'olive', 'grey', 'plum', 'palegreen', 'sienna', 'navy', 'darkcyan', 'hotpink', 'pink', 'indianred', 'magenta', 'purple', 'brown', 'dimgrey', 'g']
    cuisine_types = bs_data.category.unique().tolist()
    ###################################################################################
    ### Bar Chart - How good are restaurants in general?
    # creates a bar chart based on user input

    category_count = bs_data.groupby(['rating']).size().reset_index(name='counts')
    category_count['quality'] = category_count['rating'].apply(quality)
    del(category_count['rating'])
    category_agg = category_count.groupby(['quality']).sum().reset_index()
    category_agg['quality'] = pd.Categorical(category_agg['quality'], ['Exceptional', 'Very Good', 'Average', 'Poor'])
    category_agg.sort_values(by = 'quality', inplace = True)
    x_pos = category_agg['quality']
    y_pos = category_agg['counts']
    bars = plt.bar(x_pos, y_pos, align='center')
    plt.xlabel('Quality Rating')
    plt.ylabel('# of Restaurants')
    plt.title(f"How did different cuisines perform??")
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + 0.3, yval + 5, yval, horizontalalignment='left')
    plt.grid(axis = 'y', which='minor')
    plt.savefig(savefile('1 restaurantcount.png'), bbox_inches='tight')
    plt.clf()

    #TODO: Background color, format axis labels, and text above each bar

    #########################################################################################
    ### HBar Chart - Popular Cusines
    # Assuming the one with highest reviews is more popular

    pop_category = bs_review_agg.sort_values(by = 'review_count', ascending = False)
    y_pos = pop_category['category']
    x_pos = pop_category['review_count']
    bars = plt.barh(y_pos, x_pos, align='center')
    plt.xlabel('# of Reviews')
    plt.ylabel('Cusine Type')
    plt.title("What are the most popular cuisines?")
    for bar in bars:
        xval = bar.get_width()
        plt.text(xval,bar.get_y(),xval)
    plt.grid(axis = 'x', which='minor')
    plt.savefig(savefile('2 mostreviews.png'), bbox_inches='tight')
    plt.clf()
    #TODO: Background color, format axis labels, and text next to each bar
    #############################################################################################
    ### Scatter Plot to show reviews and ratings in a single view to get deeper insight into what are the best performing cusines
    # Assuming higher number of reviews indicates more popularity
    cumm_bs_rr = bs_review_agg.merge(bs_rating_agg, on = 'category', how = 'inner')
    categories = list(cumm_bs_rr['category'])
    #breakpoint()
    metrics = []
    for i in range(0,20,1):
        rating = cumm_bs_rr.iloc[i]['rating']
        review = cumm_bs_rr.iloc[i]['review_count']
        lst = [rating, review]
        metrics.append(lst)

    for metric, color, category in zip(metrics, colors, categories):
        y, x = metric
        plt.scatter(x, y, alpha = 0.8, marker = '*', c = color, s = 30, label = category)
        plt.text(x-500, y-0.01, category, fontsize = 6)

    plt.xlabel('# of Reviews')
    plt.ylabel('Avg. Rating')
    plt.title("The best restaurants")

    min_rev = min(cumm_bs_rr['review_count'])
    max_rev = max(cumm_bs_rr['review_count'])
    mid_rev = (min_rev + max_rev)/2
    min_rat = min(cumm_bs_rr['rating'])
    max_rat = max(cumm_bs_rr['rating'])
    mid_rat = (min_rat + max_rat)/2

    plt.xlim((min_rev, max_rev))
    plt.ylim((min_rat, max_rat))
    plt.plot([mid_rev,mid_rev],[min_rat-1000,max_rat+1000], linewidth=1, color='gray' )
    plt.plot([min_rev-1000,max_rev+1000],[mid_rat,mid_rat], linewidth=1, color='gray' )

    plt.annotate('Leaders', xy=(mid_rev, mid_rat+0.02), fontsize = 6, c = 'red')
    plt.annotate('Popular', xy=(mid_rev, min_rat+0.02), fontsize = 6, c = 'red')
    plt.annotate('Highly Rated', xy=(min_rev, mid_rat+0.02), fontsize = 6, c = 'red')
    plt.annotate('Promising', xy=(min_rev, min_rat+0.02), fontsize = 6, c = 'red')
    plt.savefig(savefile('3 scatter.png'), bbox_inches='tight')
    plt.clf()
    #TODO: Clean up labels
    ##############################################################################
    ### Sentiment Anlayzer
    # show people mood when they were giving feedback
    sid = SentimentIntensityAnalyzer()
    cat_txts = cumm_bs_br[['category', 'text']]

    sentiment_list = []
    #sentiment_df = pd.DataFrame(columns=['cuisine_type', 'positive_score', 'negative_score'])
    columns = ['cuisine_type', 'positive_score', 'negative_score']
    i = 0
    index_lst = cat_txts.index.values.tolist()

    for i in index_lst:
        review = cat_txts['text'][i]
        sentiment = sid.polarity_scores(review)
        #breakpoint()
        row = [
            cat_txts['category'][i],
            sentiment['pos'],
            sentiment['neg']
        ]
        sentiment_list.append(row)

    sentiment_df = pd.DataFrame.from_dict(sentiment_list)
    sentiment_df.columns = columns
    sentiment_df_agg = sentiment_df.groupby(['cuisine_type']).mean().reset_index()

    y = sentiment_df_agg['cuisine_type']
    x_pos = sentiment_df_agg['positive_score']

    # ajoined '-' because these are negative scores
    x_neg = -sentiment_df_agg['negative_score']

    bars1 = plt.barh(y, x_pos, align='center', color = 'blue')
    bars2 = plt.barh(y, x_neg, align='center', color = 'red')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Cusine Type')
    plt.title("Sentiment Analysis of user feedback")


    for bar1, bar2 in zip(bars1, bars2):
        xval1 = bar1.get_width()
        plt.text(xval1,bar1.get_y()+0.01,float_format(xval1))
        xval2 = bar2.get_width()
        plt.text(xval2,bar2.get_y()+0.01,float_format(xval2))

    plt.savefig(savefile('4 sentiment.png'), bbox_inches='tight')
    plt.clf()

    ################################################################################################
    ### What do people like or dilike the mode, using word cloud
    # Word Cloud for adjectives and Nouns
    # User needs to run nltk.download()
    # TODO: mention that user need to run import nltk; nltk.download() for wordcloud in requirement and help document

    print("Please refer to README.MD file to identify the cusines within the scope of this project. To select all cusines, simply enter all")
    user_input = input('Select a cuisine type - ')


    if user_input.lower() == 'all':
        text_blocks = cumm_bs_br['text']
    elif user_input.lower() in cuisine_types:
        cumm_bs_br_ui = cumm_bs_br[cumm_bs_br['category'].str.lower() == user_input.lower()]
        text_blocks = cumm_bs_br_ui['text']
    else:
        print("Oops!! You entered an invalid value. Please refer to the README.MD file to identify cuisines within the scope.")
        print("Run the program again")
        sys.exit(5)

    big_text = ' '
    for block in text_blocks:
        big_text = big_text + block

    tokens = nltk.word_tokenize(big_text)
    pos = nltk.pos_tag(tokens)
    adj_words = [p[0] for p in pos if p[1] in ['JJ', 'JJR', 'JJS']]
    noun_words = [p[0] for p in pos if p[1] in ['NN', 'NNP', 'NNS']]
    adj_str = ' '
    noun_str = ' '
    for s in adj_words:
        adj_str = adj_str + ' ' + s

    for n in noun_words:
        noun_str = noun_str + ' ' + n

    stopwords = set(STOPWORDS)
    stopwords.update(['\n', '/n', 'everything', 'single', 'overall', 'many', 'relative', 'review', 'indian', 'Indian', 'city', 'ok', 'city', 'went', 'couple', 'time', 'village', 'yelp' ])
    wc_adj = WordCloud(max_font_size=50, background_color = "white", max_words = 200, stopwords=stopwords).generate(adj_str)
    plt.figure()
    plt.imshow(wc_adj, interpolation = 'bilinear')
    plt.axis('off')
    plt.savefig(savefile('5 adjective_wc.png'), bbox_inches = 'tight')

    wc_noun = WordCloud(max_font_size=50, background_color = "white", max_words = 200, stopwords=stopwords).generate(noun_str)
    plt.figure()
    plt.imshow(wc_noun, interpolation = 'bilinear')
    plt.axis('off')
    plt.savefig(savefile('6 noun_wc.png'), bbox_inches = 'tight')
    plt.clf()






