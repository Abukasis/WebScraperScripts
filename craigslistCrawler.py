import requests
from bs4 import BeautifulSoup

#reads craigslist postings 

userIn = input("Enter Job Search Criteria:" )
url2 = "https://losangeles.craigslist.org/search/jjj?query="
url2 += userIn

file = open("jobLinks.txt","w+")

result = requests.get(url2)
resultContent = result.content
soupResult = BeautifulSoup(resultContent,features="html.parser")

totalFound = soupResult.findAll("span",class_= "totalcount")
totalPages = int(totalFound[0].get_text()) / 120

if (totalPages % 120) != 0:
	totalPages += 1
	
foundLinks = soupResult.findAll("a", class_ = "result-title hdrlnk")
for link in foundLinks:
	t = str(link.get_text())
	tFull = link
	userIn = str(userIn)
	t = t.lower()
	userIn = userIn.lower()
	if userIn in t:
		file.write("Title: " + t)
		file.write("\n")
		file.write(tFull['href'])
		file.write("\n")
		file.write("\n")
index = 120
while index < totalPages:	
	url2 = "https://losangeles.craigslist.org/search/jjj?query=" + userIn + "&s=" + str(index)
	result = requests.get(url2)
	resultContent = result.content
	soupResult = BeautifulSoup(resultContent,features="html.parser")
	foundLinks = soupResult.findAll("a", class_ = "result-title hdrlnk")
	for link in foundLinks:
		t = str(link.get_text())
		tFull = link
		userIn = str(userIn)
		t = t.lower()
		userIn = userIn.lower()
		if userIn in t:
			file.write("Title: " + t)
			file.write("\n")
			file.write(tFull['href'])
			file.write("\n")
			file.write("\n")
	index =+ 120	
print("Jobs can be found in jobLinks.txt in the same dir as this file")
