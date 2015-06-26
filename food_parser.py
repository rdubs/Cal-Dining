from bs4 import BeautifulSoup
import urllib2
import unicodedata
import re


#mapping from string entree to entree object containing all nutrition facts
entrees_with_nutrition_facts = []
entrees_seen = set()
entrees = [
	{'hall' : 'crossroads', 'breakfast': None, 'lunch' : None, 'dinner' : None},
	{'hall': 'cafe3', 'breakfast': None, 'lunch' : None, 'dinner' : None},
	{'hall': 'foothill', 'breakfast': None, 'lunch' : None, 'dinner' : None},
	{'hall': 'ckc', 'breakfast': None, 'lunch' : None, 'dinner' : None}
]

def get_dining_info():
	response = urllib2.urlopen('http://web.archive.org/web/20141121140003/http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp')
	# response = urllib2.urlopen('http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp')
	html = response.read()
	soup = BeautifulSoup(html)
	breakfast_entrees = get_entrees(soup, 'B')
	lunch_entrees = get_entrees(soup, 'L')
	dinner_entrees = get_entrees(soup, 'D')
	
	#add breakfasts
	for i in range(0,4):
		entrees[i]['breakfast'] = breakfast_entrees[i]

	#add lunches
	for i in range(0,4):
		entrees[i]['lunch'] = lunch_entrees[i]

	#add dinners
	for i in range(0,4):
		entrees[i]['dinner'] = dinner_entrees[i]
	
	return (entrees, entrees_with_nutrition_facts)

def get_entrees(soup, meal):
	""" 
	Return a list containing all entrees for a certain meal in the format:
	[[Crossroads_entrees], [Cafe3_entrees], [Foothill_entrees], [CKC_entrees]]
	"""
	if meal == 'B':
		tags = soup.find_all('b', text='Breakfast')
	elif meal == 'L':
		tags = soup.find_all('b', text=re.compile('Lunch(/Brunch)?'))
	elif meal == 'D':
		tags = 	soup.find_all('b', text='Dinner')
	entrees_by_hall = []
	for tag in tags:
		entrees = tag.next_sibling.find_all('a') #all entrees are <a> tags that are siblings of the <b> meal tag.
		hall_entrees = []
		for entree in entrees:
			entree_string = unicodedata.normalize('NFKD', entree.text).encode('ascii','ignore')
			hall_entrees.append(entree_string)
			# update_nutrition(soup, entree_string, entree)
		entrees_by_hall.append(hall_entrees)
		# entrees_by_hall.append([unicodedata.normalize('NFKD', x.text).encode('ascii','ignore') for x in entrees])
	return entrees_by_hall

def update_nutrition(soup, entree_string, entree):
	if entree_string not in entrees_seen:
		entree_dict = extract_nutrition(soup, entree)
		entree_dict['name'] = entree_string
		entrees_with_nutrition_facts.append(entree_dict)
		entrees_seen.add(entree_string)

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
			ingredients = text.strip('INGREDIENTS:  ')
			ingredients = ingredients.split(', ')
			entree_facts['ingredients'] = ingredients
	return entree_facts
entrees, bogus = get_dining_info()
print(entrees)

