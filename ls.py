import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

    
SearchInput = input("Enter search input:")
url = "https://www.twitter.com/" + SearchInput  
file = open("Tweets.txt","w+")
driver = webdriver.Chrome("/Users/admin/Desktop/chromedriver")
driver.get(url)
tweets = []
time.sleep(3)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
totalFound = driver.find_elements_by_class_name("js-tweet-text-container")
for tweet in totalFound:
	tweets.append(tweet.text)

print(len(tweets))

for t in tweets:
	print(t)
