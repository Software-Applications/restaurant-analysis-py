# "Restaurant Analysis" Project

This is a course project for nyu-info-2335-201905 at Stern School of Business

I have built this data exploration tool using sample data from Yelp. It helps potential investors analyze customer food preferences so that they can make wise investment decisions when setting up new restaurants in New York City. It also helps food lovers learn about non-native cusines before they can try and judge themselves.

## Functionality
This tool can do the following
  + Extract data from Yelp and write it to Google Sheets
  + Send an email to the end user updating them about data extract process
  + Read data from Google Sheets to create visuals
  + Send an email suggesting the visuals are ready to be viewed.

## Scope

For simplicity of demonstration, and due to time restrictions set by GoogleDrive API, I have restricted the scope of data to below:

### Cuisines -
'indian', 'chinese', 'italian', 'japanese', 'mediterranean', 'thai', 'american', 'greek', 'fusion', 'korean', 'french', 'spanish', 'middle_eastern', 'moroccan', 'turkish', 'lebanese', 'peruvian', 'german', 'african', 'caribbean'

### Location
'new york city'

These values have been harcoded in the script. No further action is needed at your end, unless you want to change the scope 

## Prerequisites

  + Anaconda 4.6.14 # (Earlier versions of Anaconda could work too. I built this application using v 4.6.14)
  + Python 3.7.3
  + Pip
  + Yelp Fusion API
  + SendGrid API Key
  + Google Drive API # (google service account and its associated json file)

## Installation

Fork this repository under your own control, then clone or download the resulting repository onto your computer. Then navigate there from the command line using the command line below:

```sh
cd <Your Path>/RESTAURANT-ANALYSIS-PY
```

> NOTE: subsequent usage and testing commands assume you are running them from the repository's root directory.

Use Anaconda to create and activate a new virtual environment, perhaps called "yelp":

```sh
conda create -n yelp python=3.7.3 # (first time only)
conda activate yelp
```

From inside the virtual environment, install package dependencies by running the below command.

```sh
pip install -r requirements.txt
```

The wordclouds and sentiment analyzer in this project are built using the nltk package. Before you can run the script to generate them, you need to run the below command from the command line.

```sh
python yelp_nltk.py
```
Doing so will activate custom trained models from nltk package. These models are used to tokenize sentences to create wordclouds. Moreover they are useful to calculate polarity scores to perform sentiment analysis.

## Setup

### Yelp
Go to [Yelp Developers](https://www.yelp.com/developers) and sign up for an account. After signing in, use Yelp Fusion to generate a Yelp API key. Detailed instruction for creating the key are available [here.](https://www.yelp.com/developers/documentation/v3/authentication)After obtaining the API key, create a new file in this repository called ".env", and update the contents of the ".env" file to specify your API key from Yelp using the syntax below

    API_KEY = "<Your Yelp API Key>"

### SendGrid
For email capabilities, [sign up for a SendGrid account](https://signup.sendgrid.com/), click the link in a confirmation email to verify your account, then [create a new API key](https://app.sendgrid.com/settings/api_keys) with "full access" permissions. Note the email address you used, and the value of the API Key, and store them in environment variables called `MY_EMAIL_ADDRESS` and `SENDGRID_API_KEY`, respectively in your ".env" file, using below syntax

    SENDGRID_API_KEY = "<Your SendGrid API Key>"
    MY_EMAIL_ADDRESS = "<Your email address>"  # (SendGrid will use this email to send notification to detination email addresses)

### Google Drive
To use google drive api to write data to google sheets, we need to set up a service account and generate its associated JSON credentials file. Follow the below steps in sequential order
  + Click on this [link](https://console.developers.google.com)
  + Create a new project, and give it your own name. Go inside the project.
  + From the menu, go to API & Services
  + Search and enable Gogle Drive API and Google Sheet API
  + From the project dashbord, click on 'Create Credentials' to create a service account Key
  + Select a name for your service account. Give it 'Owner' role. Make sure for the JSON is selected for key type
  + The above step will download a file to your computer. Rename this file as gcreds.json, and copy it to google_credentials folder in project respository

### Google Sheets Dataset
You need this dataset to collect data from Yelp API. Follow the steps below to set up Google Sheets
  + Go to Google sheets using your gmail account
  + Create a new sheet. Give it anyname.
  + Create 2 tabs - a) business_search b) business_reviews. The business search tab holds data about restaurant businesses and the business_reviews tab holds data about customer reviews.
  + Go to your gcreds.json file in google_credentials folder. Copy the 'Client Email' and give this email id 'edit' privileges to your google sheet document.
  + Copy the google sheet id from the url, and paste it in .env file using below syntax
  
  GOOGLE_SHEET_ID="<Your Google Sheet ID>"

A sample of .env called .envexample is available in project respository. You could use is as a template for .env file.

Don't worry, the ".env" has already been [ignored](/.gitignore) from version control for you!

## Usage

To extract data from Yelp and load it to Google Sheets, run the data extract script :
```py
python app/data_extract.py
```
The scripts takes about an hour to complete. This is due to API restrictions by Google

After data extract is completed, run the data vis script to generate visuals:
```py
python app/data_vis.py
```
When prompted for an input to generate wordclouds, enter a single cusine type that is within the scope of this project, mentioned above. To select all cusines, simply eneter 'all'.

## Testing

Install pytest (first time only):

```sh
pip install pytest
```

Run tests:

```sh
pytest


## [License](/LICENSE.md)
