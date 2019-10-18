import requests

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
			


ItemList = []

ItemList.append(Item("test",["a","b","c"],["a","b","c"],"white_bean_stew-wide.jpg" ))

ItemList.append(Item("test",["a","b","c"],["a","b","c"],"white_bean_stew-wide.jpg" ))

ItemList.append(Item("test",["a","b","c"],["a","b","c"],"white_bean_stew-wide.jpg" ))

print(ItemList)



MyItem = ItemList[0]

def SendItemToServer(MyItem):
	if(MyItem.imageName == "NOIMAGE":
		return "This is a bad item"
	
	headers = {
    	'X-Parse-Application-Id': 'myAppId',
    	'X-Parse-REST-API-Key': 'key',
    	'Content-Type': 'image/jpeg',
	}

	data = open(MyItem.imageName, 'rb').read()
	response = requests.post(('https://mighty-wave-74435.herokuapp.com/parse/files/' + MyItem.imageName), headers=headers, data=data)

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


	headers = {
    	'X-Parse-Application-Id': 'myAppId',
    	'X-Parse-REST-API-Key': 'key',
    	'Content-Type': 'application/json',
	}


	response = requests.post('https://mighty-wave-74435.herokuapp.com/parse/classes/GameScore', headers=headers, data=data)

	print(response.json())