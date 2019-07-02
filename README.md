# "Restaurant Analysis" Project

This is a data exploration project using data taken from YELP API, which helps potential investors understand customer dinining preferences so that they can make wise investment decisions when setting up new restaurants

This application provides stock recommendations by issuing requests to the [AlphaVantage Stock Market API](https://www.alphavantage.co/) in order to provide automated stock or cryptocurrency trading recommendations.

## Scope

For simplicity fo demonstration, and due to time restrictions set by GoogleDrive API, I have restricted the scope of data to below:

### Cuisines - 
'indian', 'chinese', 'italian', 'japanese', 'mediterranean', 'thai', 'american', 'greek', 'fusion', 'korean', 'french', 'spanish', 'middle_eastern', 'moroccan', 'turkish', 'lebanese', 'peruvian', 'german', 'african', 'caribbean'

### Location
'new york City'

These values have been embedded within the script. No further action is needed at your end. 

## Prerequisites

  + Anaconda 4.6.14 # (Earlier versions of Anaconda could work too. I built this application using v 4.6.14)
  + Python 3.7.3
  + Pip
  + Yelp Fusion API
  + SendGrid API Key
  + Google Drive API
  + Google Drive service account and its associated JSON file

https://www.yelp.com/developers/documentation/v3/authentication
 
## Installation

Fork this repository under your own control, then clone or download the resulting repository onto your computer. Then navigate there from the command line:

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

Talk about download_nltk ()  app

## Setup

### Yelp
Go to [Yelp Developers](https://www.yelp.com/developers) and sign up for an account. After signing in, use Yelp Fusion to generate a Yelp API key. Detailed instruction for creating the key are available [here.](https://www.yelp.com/developers/documentation/v3/authentication). After obtaiing the API key, create a new file in this repository called ".env", and update the contents of the ".env" file to specify your API key from Yelp using the syntax below

    API_KEY = "<Your Yelp API Key>"

### SendGrid
For email capabilities, [sign up for a SendGrid account](https://signup.sendgrid.com/), click the link in a confirmation email to verify your account, then [create a new API key](https://app.sendgrid.com/settings/api_keys) with "full access" permissions. Note the email address you used, and the value of the API Key, and store them in environment variables called `MY_EMAIL_ADDRESS` and `SENDGRID_API_KEY`, respectively in your ".env" file, using below syntax

    SENDGRID_API_KEY = "<Your SendGrid API Key>"
    MY_EMAIL_ADDRESS = "<Your email address>"  # (SendGrid will use this email to send notification to detination email addresses)

### Google Drive API Credentials
Write something here. Mention about Google Drive API key, Service account, Sheets ID, Table creation, gcreds.json file



Don't worry, the ".env" has already been [ignored](/.gitignore) from version control for you!

## Usage

To extract data from Yelp and load it to Google Sheets, run the data extract script :
```py
python app/data_extract.py
```
The scripts takes about an hour to complete. This is due to API restrictions by Google

After data extract is completed, run the data vix script to generate visuals:
```py
python app/data_extract.py
```
When prompted for an input to generate wordclouds, enter a cusine type that is within the scope of this project, mentioned above

## Testing

Install pytest (first time only):

```sh
pip install pytest
```

Run tests:

```sh
pytest


## [License](/LICENSE.md)
