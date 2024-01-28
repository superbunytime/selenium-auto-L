import requests
import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

used = open('usedlinks.json', encoding='utf-8')
used_data = json.load(used)

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\13602\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
options.add_argument(r'--profile-directory=Default') #e.g. Profile 3
driver = webdriver.Chrome(options=options)


subreddit = 'programming'
limit = 10
timeframe = 'day' #hour, day, week, month, year, all
listing = 'top' # controversial, best, hot, new, random, rising, top

abort = False
# if this is ever true, all hope is lost

def get_reddit(subreddit,listing,limit,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured trying to get the reddit data; abort mission')
        abort = True
        # if we can't get a reddit post to steal and slap onto linkedin (i do not respect either)
        # this is where the process stops; we should get notified that something broke at this step
        # which is why i may integrate this into a discord bot set to message me.
    return request.json()

r = get_reddit(subreddit,listing,limit,timeframe)

def get_posts(r):
    '''
    Get a List of post titles
    '''
    posts = []
    for post in r['data']['children']:
        x = post['data']['title']
        y = post['data']['url']
        # posts.append(x)
        posts.append(y)
        # refactor into dicts
        # looks like the data will have to be sanitized into double quotes instead of single
    return posts

posts = get_posts(r)
# print(posts)

# alright now just check if the value is already in your json file;
# if it isn't, go ahead and try to post it to linkedin using selenium.
# once you've confirmed it's been posted to your linkedin, append it to the json file.

# if it *is* already in your json file, try one of the other entries on the list
# and loop.

def send_it(url_array, file):
    # iterate through the json file
    for i in url_array:
        # print(i)
        if i in file:
            print(f"we used this link already: {i}")
            # so it's extremely unlikely, but
            # we want a handle for if all the links have been used
        else:
            print(f"we can probably post this: {i}")
            # call the method to post to linkedin
            # if the post is successful, add it to the usedlinks.json
            # actually we're going to call this method within linkedinposter
            return i

def linkedin_poster(link):
    driver.get("https://linkedin.com")
    sleep(5)
        
    revealed = driver.find_element(By.ID, "ember24")
    driver.find_element(By.ID, "ember24").click()

    wait = WebDriverWait(driver, timeout=5)
    wait.until(lambda d : revealed.is_displayed())

    sleep(5)
    ActionChains(driver)\
        .send_keys(link)\
        .perform()

    sleep(7)

    revealed2 = driver.find_element(By.CLASS_NAME, "share-box_actions")
    driver.find_element(By.CLASS_NAME, "share-box_actions").click()

    # okay now write the link to the file, and make sure it gets written properly.
    # this is a good place to stop for the night though.


linkedin_poster(send_it(posts, used_data))

# dumbass ideas that will make the codebase worse
# pishock integration
# add amazon affiliate links; every time i feed my discord bot an amazon link,
# it makes it an affiliate link and posts a little blurb about it to my linkedin
# i'm going to milk this hellscape one way or another.
# it's just a matter of finding the right udder.
# openkore integration; one kill, one linkedin job application sent
# discord integration so i can get a message when my widdle bot esplods