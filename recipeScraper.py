import requests
from PIL import Image
from os.path  import basename
import urllib
from bs4 import BeautifulSoup
import time
def CleanString(string):
	s = string
	s = s.replace('\n', '')
	s = s.replace('’' , '')
	s = s.replace('—', '')
	
	return s
	
	
class Item:
	title = ""
	instructions = [""]
	ingredients = [""]
	imageName = ""
	def __init__(self, titl, instru, ingre, imgName):
		self.title = titl
		self.imageName = imgName
		self.instructions = []
		self.ingredients = []
		for steps in instru:
			self.instructions.append(steps)
		
		for things in ingre:
			self.ingredients.append(things)
			
def getItemFromURL(URL):
		
	url = URL

	result = requests.get(url)
	resultContent = result.content
	soupResult = BeautifulSoup(resultContent,features="html.parser")
	ingredients = soupResult.findAll("div",class_= "recipe__ingredients")

	ingredientList = ingredients[0].findAll("ul")
	ingredientItems = ingredientList[0].findAll("li")


	ingredientList = []
	for item in ingredientItems:
		ingredientText = item.get_text()
		ingredientList.append((CleanString(ingredientText)))

	steps = soupResult.findAll("div",class_= "recipe__preparation")

	stepList = steps[0].findAll("ul")
	stepItems = stepList[0].findAll("li")

	stepsList = []
	for step in stepItems:
		stepText = step.get_text()
		stepsList.append((CleanString(stepText)))


	imagePath = soupResult.findAll("figure",class_= "recipe__image--main")
	cleanName = ""
	if(len(imagePath) != 0):
		imageResult = imagePath[0].findAll("img")

		with open(basename(imageResult[0].get('src')), "wb") as f:
			f.write(requests.get("https:" + imageResult[0].get('src')).content)
	
		imageFileName = imageResult[0].get('src')
		
		for char in imageFileName:
			cleanName += char
			if char == '/':
				cleanName = ""
	else:
		cleanName = "NOPICTURE"
	titleLink = soupResult.findAll("h1", class_ = "recipe__title")

	title = (CleanString(titleLink[0].get_text()))
	
	print("adding new item: " + title )

	newItem = Item(title,stepsList,ingredientList,cleanName)
	return newItem
	
def getURLS():
	urlList = []
	url = "Website Hidden"
	result = requests.get(url)
	resultContent = result.content
	soupResult = BeautifulSoup(resultContent,features="html.parser")
	
	resultCount = soupResult.findAll("span",class_ = "pagination__count")
	
	resultCountText = resultCount[0].get_text()
	
	count = ""
	start = False
	for char in resultCountText:
		if(start == True):
			if char.isdigit():
				count += char
		if(char == 'f'):
			start = True
	print(count)
	
	urls = soupResult.findAll("a")
	
	for item in urls:
		if 'Website Hidden' in item.get('href'):
			urlList.append(item.get('href'))
	
	page = 2
	while(page <= int(count) ):
		print(("reading page # " + str(page)))
		time.sleep(1)
		url = "Website Hidden/" + str(page) + "Website Hidden"
		result = requests.get(url)
		resultContent = result.content
		soupResult = BeautifulSoup(resultContent,features="html.parser")
		urls = soupResult.findAll("a")
	
		for item in urls:
			if 'Website Hidden' in item.get('href'):
					urlList.append(item.get('href'))
		
		
		page += 1
		
	cleanList = []
	i = 0
	while(i < len(urlList)):
		cleanList.append(urlList[i])
		i += 2
	
	print(cleanList)
	return cleanList
	
def SendItemToServer(MyItem):
	if MyItem.imageName == "NOIMAGE":
		return "This is a bad item"
	headers = {
    	'X-Parse-Application-Id': 'myAppId',
    	'X-Parse-REST-API-Key': 'key',
    	'Content-Type': 'image/jpeg',
	}

	data = open(MyItem.imageName, 'rb').read()
	response = requests.post(('ENTER SERVER URL HERE' + MyItem.imageName), headers=headers, data=data)

	dict = response.json()

	imageURL = dict['url']
	imageNAME = dict['name']


	instructionsFormat = "["
	for item in MyItem.instructions:
		instructionsFormat += '"' + item + '"' + ", "
	
	instructionsFormat = instructionsFormat[:-1]
	instructionsFormat = instructionsFormat[:-1]
	instructionsFormat += "]"



	ingredientsFormat = "["
	for item in MyItem.ingredients:
		ingredientsFormat += '"' + item + '"' + ", "
	
	ingredientsFormat = ingredientsFormat[:-1]
	ingredientsFormat = ingredientsFormat[:-1]
	ingredientsFormat += "]"

	data = '{"title": "' + MyItem.title +  '" , "instructions" : ' + instructionsFormat +   ' , "ingredients" : ' + ingredientsFormat + '  ,"image": { "name": "' + imageNAME +'", "url": "' + imageURL + '", "__type": "File" } }'
	data.encode('utf-8')

	headers = {
    	'X-Parse-Application-Id': 'myAppId',
    	'X-Parse-REST-API-Key': 'key',
    	'Content-Type': 'application/json',
	}


	response = requests.post('SERVER URL HERE', headers=headers, data=data)

	print(response.json())
	
itemList = []
urlList = getURLS()

for url in urlList:
	print(url)
	try:
		itemList.append((getItemFromURL(url)))
	except:
		print("failed to read item")


for item in itemList:
	try:
		SendItemToServer(item)
	except:
		print("failed to send item to server")

