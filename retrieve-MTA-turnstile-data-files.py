'''

This script retrieves the list of all available turnstile data files 
from the New York MTA web site, and saves the files to a local folder.

The page where the files are listed is http://web.mta.info/developers/turnstile.html

The file names from the page do not include the first two digits for 
the year, the missing digits are added to the file name when the file 
is saved. Didn't they live through Y2K?

In their defense, the available files go back to 2010 (as I write this),
so there is no risk of confusion.

Note: I use the requests library instead of urllib2 because I prefer writing
   r = requests.get(myurl)
instead of 
   r = urllib2.urlopen(myurl)
It saves me 3 characters. Otherwise functionality is the same for this simple case.

'''

import requests
from bs4 import BeautifulSoup as BS4
import re
from timeit import default_timer as timer
import humanfriendly

# initialize URL and folder, record start time
urlroot = r'http://web.mta.info/developers/'
path = r'e:\python\MTAturnstile\turnstile_20'
starttime = timer()

# read the page html and use BeautifulSoup to extract the list of data files
r = requests.get(urlroot + 'turnstile.html')
soup = BS4(r.content, features = 'html.parser')
files = soup.find('div', {'id': 'contentbox'}).find('div', {'class': 'container'}).find('div', {'class': 'span-84 last'}).findAll('a', attrs={'href': re.compile("^data/nyct/turnstile/")})

# iterate through the list of files, retrieve the data for each file, and save file to the local folder
for file in files:
	print('Saving file turnstile_20' + str(file)[39:49])
	datafile = requests.get(urlroot + str(file)[9:49])
	with open(path + str(file)[39:49], 'w') as outf:
		for line in datafile.text:
		      outf.writelines(line)

# record completion time and display duration
endtime = timer()
print('Completed in ' + humanfriendly.format_timespan(endtime-starttime))
