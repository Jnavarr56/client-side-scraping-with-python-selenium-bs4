# Scraping Client Rendered Pages With Python, Selenium, and BeautifulSoup4

I created this to practice and help teach Selenium.

## Description

Lets use https://www.wunderground.com/history/monthly/KMSY/date as an example.

This page is client rendered, meaning the HTML isn't built on the server and then sent to your browser. It's sent to the browser partially built, and then it finishes building inside of the browser. This means that normal programmatic webscraping won't work, because since the code doing the scraping isn't a browser, it the code will never get the fully completed HTML page.

Selenium is a browser automation tool that allows you to programmatically control a browser. With Selenium, you CAN parse client rendered rendered pages by programming the a browser window to go to a website, visit a page, and then have the built HTML page text be passed to your code.

### Requirements

pip, Python 3.8+, Chrome browser, Linux or Mac OS

## To Run

When this runs, it'll open up your Chrome browser. The whole thing might take a few minutes at most so make sure you let it finish. When it's done, it will open up the scraped data in a CSV file.

### Make Sure You Know

On line 13 of `main.py` there's a url to the download link for a file that corresponds to Chrome 87 (as of 01/13/2021). If you have a different version of Chrome, just replace that url with the one that matches your version of Chrome. You can find the urls here https://chromedriver.chromium.org/downloads.

To specify the months you want included in the scraped dataset, see the variable at line 74 of `main.py`. Just have the list there include the months you want in YYYY-M format.

### Steps

1. Clone this repo.
2. `cd` into the project root directory
3. Run: `python -m venv ./.venv`
4. If virtualenv not already activated run: `source ./.venv/bin/activate`
5. Run: `pip install -r requirements.txt`
6. Run: `python ./main.py`
