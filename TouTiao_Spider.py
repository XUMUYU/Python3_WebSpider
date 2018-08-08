# 2018.08.08
# TouTiao JiePai
# Joe Xu

import requests
import os
from urllib.parse import urlencode
from hashlib import md5
from multiprocessing.pool import Pool


GROUP_START = 1
GROUP_END = 4


def get_pages(offset):
    params = {
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'1'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)    

    try:
        response = requests.get(url)
        if response.status_code == 200:            
            return response.json()
    except requests.ConnectionError:
        return None

def get_images(json):
    data = json.get('data')
    if data:
        for item in data:            
            title = item.get('title')
            images = item.get('image_list')            
            if images:
                for image in images:                                     
                    yield{
                        'title':title,
                        'image':image.get('url'),                        
                    }

def save_images(item):
    #print(item)
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        old_image_url = item.get('image')
        new_image_url = old_image_url.replace('list', 'origin')        
        response = requests.get('http:' + new_image_url)
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')                                
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Download', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

def main(offset):
    json = get_pages(offset)
    for item in get_images(json):
        save_images(item)




if __name__ == '__main__':
    print("main function start...")
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
