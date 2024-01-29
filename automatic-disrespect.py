import requests
import json
from time import sleep
import datetime
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import discord, aiohttp, asyncio, sys, time, yaml
from discord.ext import commands, tasks

def rand_sleep(int, delay_range):
    int += random.choice(range(0, delay_range))
    return int

with open('personalconfig.yml', 'r') as file:
  config = yaml.safe_load(file)

intents = discord.Intents.all()
client = discord.Client(intents = intents)

utc = datetime.timezone.utc
time = datetime.time(hour=20, minute=rand_sleep(0, 5), tzinfo=utc) # *should* be noon +/- 5 minutes

used = open('usedlinks.json', encoding='utf-8')
used_data = json.load(used)

subreddit = 'programming'
limit = 10
timeframe = 'day' #hour, day, week, month, year, all
listing = 'top' # controversial, best, hot, new, random, rising, top

def get_reddit(subreddit,listing,limit,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured trying to get the reddit data; abort mission')
    return request.json()

r = get_reddit(subreddit,listing,limit,timeframe)

def get_posts(r):
    '''
    Get a List of post titles
    '''
    posts = []
    for post in r['data']['children']:
        x = post['data']['url']
        posts.append(x)
    return posts

posts = get_posts(r)

def send_it(url_array, file):
    file_list = file
    for i in url_array:
        if i in file_list:
            print(f"we used this link already: {i}")
        else:
            print(f"we can probably post this: {i}")
            file_list.append(i)
            json_string = json.dumps(file_list)
            with open('usedlinks.json', 'w') as outfile:
                outfile.write(str(json_string))
            return i



def linkedin_poster(link, file):
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=C:\Users\13602\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    options.add_argument(r'--profile-directory=Default') #e.g. Profile 3
    driver = webdriver.Chrome(options=options)
    driver.get("https://linkedin.com")
    sleep(rand_sleep(5, 7))
    revealed = driver.find_element(By.ID, "ember24")
    driver.find_element(By.ID, "ember24").click()
    wait = WebDriverWait(driver, timeout=5)
    wait.until(lambda d : revealed.is_displayed())
    sleep(rand_sleep(5, 7))
    ActionChains(driver)\
        .send_keys(link)\
        .perform()
    sleep(rand_sleep(7, 7))
    revealed2 = driver.find_element(By.CLASS_NAME, "share-box_actions")
    driver.find_element(By.CLASS_NAME, "share-box_actions").click()
    sleep(rand_sleep(10, 10))

    
@client.event
async def on_ready():
  print("we have logged in as {0.user}".format(client))
  linkedin_timer.start()

@tasks.loop(time = time)
async def linkedin_timer():
    linkedin_poster(send_it(posts, used_data), used_data)
    
    
with open("token", "r+") as keyfile:
    key = keyfile.read()
    client.run(key)


# todo:

# discord bot integration for amazon affiliate link feature, analytics readouts
    
# very well, let's work on the amazon affiliate link feature another time.
# it's been quite a shift. the code works, and ought to post around noon as long as it's working
# the incorporation of a random sleep duration was easier than i had thought
# but it can be improved by timing in miliseconds for a true sense of randomness
# to improve it even further, enabling it to click in a random range within the element
# and changing in-built selenium variables to avoid detection would be best practice
# if not a little overkill.

# dumbass ideas that will make the codebase worse
# pishock integration
# add amazon affiliate links; every time i feed my discord bot an amazon link,
# it makes it an affiliate link and posts a little blurb about it to my linkedin
# i'm going to milk this hellscape one way or another.
# it's just a matter of finding the right udder.
# openkore integration; one kill, one linkedin job application or connection request sent
# discord integration so i can get a message when my widdle bot esplods