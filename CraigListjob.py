import requests
import cfscrape
import time
from bs4 import BeautifulSoup
SearchInput = input("Enter search input:")
listURL = []
headers = {
        'user-agent': 'Mozilla/5.0',
    }
    

url = "https://www.manta.com/search?search_source=business&search=" + SearchInput  
file = open("Emails.txt","w+")
scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
# Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
#h1  h3 pl-xs
content = scraper.get(url).content
print(content)
soup = BeautifulSoup(content,features="html.parser")
totalFound = soup.findAll("a",class_= "media-heading text-primary h4")
for link in totalFound:
	businessLink = link['href']
	print("i found link " + businessLink)
	print("adding link to index")
	listURL.append(("https://www.manta.com" + businessLink))
index = 1

while(index < 10):
	newUrl = url + "&pg=" + str(index)
	time.sleep(2)
	content = scraper.get(newUrl).content
	soup = BeautifulSoup(content,features="html.parser")
	totalFound = soup.findAll("a",class_= "media-heading text-primary h4")
	for link in totalFound:
		newAmount =+ 1
		businessLink = link['href']
		print("i found link " + businessLink)
		print("adding link to index")
		listURL.append(("https://www.manta.com" + businessLink))
	index += 1
print("scraped all page URLS")

dataWeWant = []

def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16)^k)

    return de

for businessURL in listURL:
	time.sleep(1)
	content = scraper.get(businessURL).content	
	soup = BeautifulSoup(content,features="html.parser")
	print(soup.content)
	print(soup.cookies)
	totalFound = soup.findAll("div", class_ = "break-word")
	for item in totalFound:
		print("checking for email")
		text = item.get_text()
		print(text)
		if "Email:" in text:
			print("found email in " + text)
			start = False
			cleanString = ""
			for char in text:
				if(start == True):
					cleanString += char
				if(char == ':'):
					start = True
					
			text = cleanString
			print(text)
			dataWeWant.append(text)
##h1  h3 pl-xs
for data in dataWeWant:
	file.write(data)
	file.write("\n")