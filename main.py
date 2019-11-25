from selenium import webdriver
import pickle
from selenium.webdriver.common.keys import Keys
import time

f = open("queries.txt", "r")
queries = f.readlines()
f.close()

f = open("results.txt", "r")
res = f.readlines()
f.close()

idx = int(len(res)/11)

if int(len(res)%11) != 0 :
	f = open("results.txt", "w")
	f.write(''.join(res[:(idx*11)]))
	f.close()

browser = webdriver.Chrome('./chromedriver') 
browser.get("http://www.google.com")
pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))

for cookie in pickle.load(open("cookies.pkl", "rb")):
	 if 'expiry' in cookie:
		 del cookie['expiry']

	 browser.add_cookie(cookie)

f = open("results.txt", "a")

for i, search_string in enumerate(queries[idx:]): 
	f.write(str(i+idx)+")  "+search_string)
	search_string = search_string.strip('\n')
	browser.get("http://www.google.com")
	search = browser.find_element_by_name('q')
	search.send_keys(search_string)
	search.send_keys(Keys.RETURN)

	flag = False
	num = 0
	web_links = []
	links = browser.find_elements_by_xpath('.//a')
	for i in range(len(links[1:])):
		if flag == True:
			if "google" not in str(links[i].get_attribute('href')):
				web_links.append(links[i].get_attribute('href'))
			
		if links[i-1].get_attribute('href') == None and links[i].get_attribute('href') == None:
			flag = True
			num = i + 1
			
	web_links = list(filter(lambda a: a != None, web_links))
	
	if len(web_links) >= 10:
		links_len = 10
	else:
		links_len = len(web_links)

	for j in web_links[0:links_len]:
		f.write(j+"\n")
	for j in range(10-links_len):
		f.write("Nil"+"\n")
		
	time.sleep(2)
	
f.close()

print("Done!")
