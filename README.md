# image-scraper
Python code for scraping an image form google with use of chrome driver

Now  scrape as many images as you want, from google images using Python, Chromdriver 

**Dependencies needed**
1) `Selenium`
Install as `pip install selenium`
2) [Python 3+](https://www.python.org/download/releases/3.0/?) - Pyhton 3.6+ verion
3) Download `chromedriver.exe`
4) Place your `chromedriver.exe` and `google_image_scraping_script.py` file in the same folder
5) Open your terminal (Command Prompt for Windows) from that location and execute the script by typing `python googe_image_scraping_script.py`


Line 105 change the queries you want to search: `queries = ["Manchester City", "Manchester United", 'Barcelona', 'Real Madrid']` in my case

Line 110 `links = fetch_image_urls(query,200,wd)`, 200 denotes no. of images you want to download 

**Note:** The script runs and scrapes images successfully if the range of no. of images is set somewhere between 200-250 and also if one query is passed at a time instead of a list of multiple queries

