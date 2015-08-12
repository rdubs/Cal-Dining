from bs4 import BeautifulSoup
import urllib2
import unicodedata
import re
import httplib
import json


#mapping from string entree to entree object containing all nutrition facts
index_to_dining_hall_mapping = {
	0: 'crossroads',
	1: 'cafe3',
	2: 'foothill',
	3: 'ckc'
}
entrees_with_nutrition_facts = []
entrees_seen = set()
entrees = {
	'crossroads': { 'breakfast': None, 'lunch' : None, 'dinner' : None},
	'cafe3': {'breakfast': None, 'lunch' : None, 'dinner' : None},
	'foothill': {'breakfast': None, 'lunch' : None, 'dinner' : None},
	'ckc': {'breakfast': None, 'lunch' : None, 'dinner' : None}
}

dining_hall = ''
meal_type = ''

def get_dining_info():
	# url = "http://web.archive.org/web/20141121140003/http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp"
	# req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36"})
	response = urllib2.urlopen('http://web.archive.org/web/20141121140003/http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp')
	# response = urllib2.urlopen('http://web.archive.org/web/20141121140003/http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp')
	# response = urllib2.urlopen('http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp')
	html = response.read()
	soup = BeautifulSoup(html)
	breakfast_entrees = get_entrees(soup, 'B')
	lunch_entrees = get_entrees(soup, 'L')
	dinner_entrees = get_entrees(soup, 'D')
	
	#add breakfasts
	for i in range(0,4):
		entrees[index_to_dining_hall_mapping[i]]['breakfast'] = breakfast_entrees[i]

	#add lunches
	for i in range(0,4):
		entrees[index_to_dining_hall_mapping[i]]['lunch'] = lunch_entrees[i]

	#add dinners
	for i in range(0,4):
		entrees[index_to_dining_hall_mapping[i]]['dinner'] = dinner_entrees[i]
	
	return entrees

def get_entrees(soup, meal):
	""" 
	Return a list containing all entrees for a certain meal in the format:
	[[Crossroads_entrees], [Cafe3_entrees], [Foothill_entrees], [CKC_entrees]]
	"""
	global meal_type
	global dining_hall
	if meal == 'B':
		tags = soup.find_all('b', text='Breakfast')
		meal_type = 'Breakfast'
	elif meal == 'L':
		tags = soup.find_all('b', text=re.compile('Lunch(/Brunch)?'))
		meal_type = 'Lunch'
	elif meal == 'D':
		tags = 	soup.find_all('b', text='Dinner')
		meal_type = 'Dinner'
	entrees_by_hall = []
	for i in range(0,4):
		entrees = tags[i].next_sibling.find_all('a') #all entrees are <a> tags that are siblings of the <b> meal tag.
		hall_entrees = {}
		dining_hall = index_to_dining_hall_mapping[i]
		for entree in entrees:
			entree_string = unicodedata.normalize('NFKD', entree.text).encode('ascii','ignore')
			hall_entrees[entree_string] = update_nutrition(soup, entree_string, entree)
		entrees_by_hall.append(hall_entrees)
		# entrees_by_hall.append([unicodedata.normalize('NFKD', x.text).encode('ascii','ignore') for x in entrees])
	return entrees_by_hall

def update_nutrition(soup, entree_string, entree):
	entree_dict = extract_nutrition(soup, entree)
	entree_dict['name'] = entree_string
	
	#set where the dining hall and meal type keys
	entree_dict['dining_hall'] = dining_hall
	entree_dict['meal_type'] = meal_type

	#send to parse
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('POST', '/1/classes/Entree', json.dumps(entree_dict),
	{
		"X-Parse-Application-Id": "pBlshDn1gMVHTKTgmUxZOK4h62TyA05jrUVOE7Ri",
		"X-Parse-REST-API-Key": "8v09lw9nLQA782PGShSGi6Qzq1WSYS6ZPUam5zsa",
		"Content-Type": "application/json"
	})

	# results = json.loads(connection.getresponse().read())

	entrees_with_nutrition_facts.append(entree_dict)
	entrees_seen.add(entree_string)
	return entree_dict

def extract_nutrition(soup, entree):
	response = urllib2.urlopen('http://services.housing.berkeley.edu/FoodPro/dining/static/' + entree.get('href'))
	html = response.read()
	soup = BeautifulSoup(html)
	results = soup.find_all('font')
	entree_facts = {}
	for tag in results:
		text = unicodedata.normalize('NFKD', tag.text).encode('ascii','ignore').strip()
		if text == 'Serving Size': 
			entree_facts['serving_size'] = unicodedata.normalize('NFKD', tag.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Total Fat':
			entree_facts['total_fat'] = unicodedata.normalize('NFKD', tag.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Sat. Fat':
			entree_facts['saturated_fat'] = unicodedata.normalize('NFKD', tag.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Trans Fat':
			entree_facts['trans_fat'] = unicodedata.normalize('NFKD', tag.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Cholesterol':
			entree_facts['cholesterol'] = unicodedata.normalize('NFKD', tag.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Sodium':
			entree_facts['sodium'] = unicodedata.normalize('NFKD', tag.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Tot. Carb.':
			entree_facts['carbs'] = unicodedata.normalize('NFKD', tag.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Dietary Fiber':
			entree_facts['fiber'] = unicodedata.normalize('NFKD', tag.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Sugars':
			entree_facts['sugars'] = unicodedata.normalize('NFKD', tag.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Protein':
			entree_facts['protein'] = unicodedata.normalize('NFKD', tag.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Vitamin C':
			entree_facts['vitaminc'] = unicodedata.normalize('NFKD', tag.next_sibling.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Calcium':
			entree_facts['calcium'] = unicodedata.normalize('NFKD', tag.next_sibling.next_sibling.text).encode('ascii','ignore').strip()
		elif text == 'Iron':
			entree_facts['iron'] = unicodedata.normalize('NFKD', tag.next_sibling.next_sibling.text).encode('ascii','ignore').strip()
		elif 'Calories' in text and 'Fat' in text:
			fat_calories = text.strip('Calories from fat ')
			entree_facts['fat_calories'] = fat_calories
		elif 'Calories' in text:
			calories = text.strip('Calories ')
			entree_facts['calories'] = calories
		elif 'ALLERGENS:' in text:
			allergens = text.strip('ALLERGENS:  ')
			allergens = allergens.split(', ')
			entree_facts['allergens'] = allergens
		elif 'INGREDIENTS:' in text:
			ingredients = text.strip('INGREDIENTS:')
			ingredients = ingredients.strip()
			ingredients = ingredients.split(', ')
			entree_facts['ingredients'] = ingredients
	return entree_facts
entrees = get_dining_info()
