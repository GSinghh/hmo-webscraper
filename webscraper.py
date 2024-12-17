import requests
import json
import os
import send_sms
from bs4 import BeautifulSoup

WEB_PAGE_URL = 'https://www.hmotorsonline.com/whats-new/'
DIV_CLASS_NAME = 'flex_column av-ztsyz9-63e7b4b0ee123d3cd7f58c84edf84092 av_one_full avia-builder-el-18 el_after_av_one_full el_before_av_one_full first flex_column_div av-zero-column-padding column-top-margin'
H3_CLASS_NAME = 'av-special-heading-tag'
TITLE_CLASS_NAME = 'av-catalogue-title av-cart-update-title'
FILE_NAME = 'dc_integra.json'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

def get_bs_obj():
    page_data = requests.get(WEB_PAGE_URL, headers=headers)
    doc = BeautifulSoup(page_data.text, 'html.parser')
    return doc

def find_div():
    document = get_bs_obj()
    results = document.find_all('div', class_=DIV_CLASS_NAME)
    for result in results:
        title = result.find('h3', class_=H3_CLASS_NAME).text
        if title == 'DC2 1994-2001 Integra’s':
            return result
    print("Result not found")
        
def get_parts_data():
    div = find_div()
    list_items = div.find_all('li')
    parts = []
    for list_item in list_items:
        try:
            item_title = list_item.find('div', class_=TITLE_CLASS_NAME).text
            item_price = list_item.find('bdi').get_text() if list_item.find('bdi') else 'No Price Found'
            item_anchor_tag = list_item.find('a')
            item_link = item_anchor_tag['href']
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            temp = {
                'Item Title': item_title,
                'Item Price': item_price, 
                'Item Link': item_link
            }
            parts.append(temp)
            # print('Item Title: ', item_title)
            # print('Item Price: ', item_price)
            # print('Item Link: ', item_link)
    return parts        
        
def store_data_in_file(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def load_data_from_file(filename):
    with open(filename) as file:
        return json.load(file)
    
def identify_change(old_parts, new_parts):
    changes = []
    for part in new_parts:
        if part not in old_parts:
            changes.append(part)
    return changes


if not os.path.isfile(FILE_NAME):
    parts = get_parts_data()
    store_data_in_file(parts, FILE_NAME)
else:
    new_parts = get_parts_data()
    old_parts = load_data_from_file(FILE_NAME)
    changes = identify_change(old_parts, new_parts)
    if changes:
        store_data_in_file(new_parts, FILE_NAME)
        send_sms.send_email(changes)
        # Do this if changes are found between the old and new file
    
# Use only when file is not formatted correctly
"""
with open('page_data_formatted.html', 'w') as file:
    file.write(doc.prettify()) 
"""
