from bs4 import BeautifulSoup
import urllib2
import unicodedata

def main():
	response = urllib2.urlopen('http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp')
	html = response.read()
	soup = BeautifulSoup(html)
	breakfast_entrees = get_entrees(soup, 'B')
	lunch_entrees = get_entrees(soup, 'L')
	dinner_entrees = get_entrees(soup, 'D')

def get_entrees(soup, meal):
	""" 
	Return a list containg all entrees for a certain meal in the format:
	[[Crossroads_entrees], [Cafe3_entrees], [Foothill_entrees], [CKC_entrees]]
	"""
	if meal == 'B':
		tags = soup.find_all('b', text='Breakfast')
	elif meal == 'L':
		tags = soup.find_all('b', text='Lunch')
	elif meal == 'D':
		tags = 	soup.find_all('b', text='Dinner')
	entrees_by_hall = []
	for tag in tags:
		entrees = tag.next_sibling.find_all('a') #all entrees are <a> tags who are siblings of the <b> meal tag.
		entrees_by_hall.append([unicodedata.normalize('NFKD', x.text).encode('ascii','ignore') for x in entrees])
	return entrees_by_hall
main()