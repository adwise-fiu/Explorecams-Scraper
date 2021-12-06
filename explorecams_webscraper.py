from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from selenium import webdriver

import pandas as pd
import uuid
import time
import os


def retrieve_html_source(url, minutes):
    """
    scroll to bottom of the page, wait for page to load
    and then continue scrolling for a given amount of minutes

    return: source html code of web page
    """
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)

    script = ("window.scrollTo(0, document.body.scrollHeight);"
              "var lenOfPage=document.body.scrollHeight;return lenOfPage;")

    lenOfPage = browser.execute_script(script)

    stop_time = time.time() + 60 * minutes

    match = False
    while (match is False):
        lastCount = lenOfPage
        time.sleep(0.75)
        lenOfPage = browser.execute_script(script)
        time.sleep(0.75)
        if (lastCount == lenOfPage) or (time.time() >= stop_time):
            match = True

    source_data = browser.page_source
    bs_data = bs(source_data, 'html.parser')

    browser.close()

    return bs_data


def top_n_users(html_data, n=5):
    """
    feed in an html source code of web page

    return: the top 5 users (or as specified) by amount of photos posted
    """
    query = html_data.find_all('div', attrs={'class': 'sm-meta'})

    users = []
    for i in range(len(query)):
        users.append(query[i].text)

    # create DataFrame
    users = pd.DataFrame(users)

    # clean excess formatting from html
    users = users[0].str.split('© ', expand=True)
    users = users.drop([0], axis=1)
    users = pd.DataFrame(users[1].str.strip())

    # rename columns
    users.columns = ['name']

    # groupby user name; finds total number of images per user
    users_grouped = users.groupby(['name']).size().rename('imgs').reset_index()

    # sort users by imgs (largest -> smallest) and get top n users
    top_users = users_grouped.sort_values('imgs', ascending=False).head(n)

    # change and replace symbols to correct html encoding
    # so far only have seen '&' -> '&amp;' as an issue
    for idx, name in enumerate(top_users['name']):
        if '&' in name:
            top_users['name'].iloc[idx] = name.replace('&', '&amp;')

    return top_users


def find_user_elements(usernames, html_data):
    """
    feed in usernames to lookup within html content

    return: all of the user's div tags containing image resource urls
    """
    items = html_data.find_all('div', attrs={'class': 'item'})
    items_list = [str(items[index]) for index, tag in enumerate(items)]

    user_items = []
    for index, element in enumerate(items_list):
        if items_list[index].find(usernames) == -1:
            continue
        else:
            user_items.append(items_list[index])

    return user_items


def extract_user_urls(user_html_data):
    """
    feed in reduced html (div tags of users)

    return: all of the associated image urls
    """
    user_urls = []
    for div in user_html_data:
        i = 0
        while (div.find(' src', i) != -1):
            i = div.find(' src', i)
            j = i + 6
            s = ""
            flag = 0
            while (div[j] != '"'):
                s = s + div[j]
                j = j + 1
                flag = 1
            if flag == 1:
                user_urls.append(s)
            i = i + 1

    return list(set(user_urls))


def save_image_from_url(user_url_data, save_directory):
    """
    feed in url content to extract (referencing images) and will save
    in specified directory
    """
    os.chdir(save_directory)
    for url in user_url_data:
        if url.endswith('.jpg') is True:
            os.system('curl {} --output {}'.format(url,
                                                   url.split('/')[-1]))
        if url.endswith('.jpg') is False:
            os.system('curl "{}" --output {}.jpg'.format(url,
                                                         str(uuid.uuid4())))


# define url to web scrape
url = 'https://explorecams.com/photos/pair/x-t10=xf18-55mmf2-8-4-r-lm-ois'

# get top 'n' users
html_data = retrieve_html_source(url, 20)
top_users = top_n_users(html_data, n=6)

# separate div content from rest of html
users = top_users['name'].values

user_divs = {}
for idx, user in enumerate(users):
    user_divs["{}".format(user)] = find_user_elements(user, html_data)

# extract image urls from div tags
user_urls = []
for user, user_div_list in user_divs.items():
    user_urls.append(extract_user_urls(user_div_list))

# define local directories
dir1 = ''
dir2 = ''
dir3 = ''
dir4 = ''
dir5 = ''
dir6 = ''
directories = [dir1, dir2, dir3, dir4, dir5, dir6]

# make directories if they don't already exist
for directory in directories:
    if not os.path.isdir(directory):
        os.makedirs(directory)
        print("Folder Created: ", directory)

# save images to local directories
for idx, user_image_list in enumerate(user_urls):
    if idx == 0:
        save_image_from_url(user_image_list, directories[idx])
    if idx == 1:
        save_image_from_url(user_image_list, directories[idx])
    if idx == 2:
        save_image_from_url(user_image_list, directories[idx])
    if idx == 3:
        save_image_from_url(user_image_list, directories[idx])
    if idx == 4:
        save_image_from_url(user_image_list, directories[idx])
    if idx == 5:
        save_image_from_url(user_image_list, directories[idx])
