import selenium
from selenium import webdriver
import time
import requests
import os
from PIL import Image
import io
import hashlib

# All in same directory
#DRIVER_PATH = 'chromedriver.exe'

'''
wikipage="https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_by_continent_(data_file)"
result =requests.get(wikipage)
result.content

import requests
import pandas as pd
from bs4 import BeautifulSoup

# download wikipage
wikipage = "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_by_continent_(data_file)"
result = requests.get(wikipage)

# if successful parse the download into a BeautifulSoup object, which allows easy manipulation 
if result.status_code == 200:
    soup = BeautifulSoup(result.content, "html.parser")
    
# find the object with HTML class wikitable sortable
table = soup.find('table',{'class':'wikitable sortable'})

# loop through all the rows and pull the text
new_table = []
for row in table.find_all('tr')[1:]:
    column_marker = 0
    columns = row.find_all('td')
    new_table.append([column.get_text() for column in columns])
    
df = pd.DataFrame(new_table, columns=['ContinentCode','Alpha2','Alpha3','PhoneCode','Name'])
df['Name'] = df['Name'].str.replace('\n','')
df


res=pd.read_html(wikipage)
res[2]
'''

def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)        
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    error_clicks = 0
    while (image_count < max_links_to_fetch) & (error_clicks < 30): # error clicks to stop when there are no more results to show by Google Images. You can tune the number
        scroll_to_end(wd)

        print('Starting search for Images')

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        for img in thumbnail_results[results_start:max_links_to_fetch]:
            # try to click every thumbnail such that we can get the real image behind it
            print("Total Errors till now:", error_clicks)
            try:
                print('Trying to Click the Image')
                img.click()
                time.sleep(sleep_between_interactions)
                print('Image Click Successful!')
            except Exception:
                error_clicks = error_clicks + 1
                print('ERROR: Unable to Click the Image')
                if(results_start < number_results):
                	continue
                else:
                	break
                	
            results_start = results_start + 1

            # extract image urls    
            print('Extracting of Image URLs')
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            print('Current Total Image Count:', image_count)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
            else:
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")
            	        
        results_start = len(thumbnail_results)

    return image_urls

def persist_image(folder_path:str,file_name:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path,file_name)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

if __name__ == '__main__':
   # wd = webdriver.Chrome("/Users/reenalboddul/Documents/Scraping-Google-Images-using-Python-master/chromedriver.exe")
    wd = webdriver.Chrome()
   # queries = ["Manchester City", "Manchester United", 'Barcelona', 'Real Madrid']  #change your set of queries here
    queries = ["Idli"]  #change your set of queries here

    for query in queries:
        wd.get('https://google.com')
        search_box = wd.find_element_by_css_selector('input.gLFyf')
        search_box.send_keys(query)
        links = fetch_image_urls(query,5,wd) # 200 denotes no. of images you want to download
        images_path = 'dataset/'
        for i in links:
            persist_image(images_path,query,i)
    wd.quit()
