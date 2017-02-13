#Project Python
#To retrive titles,links and description from news.aspx file and obtain the rss.xml to public_html.
#Validate the generated XML file using Feed Validator.
 
import re
import sys
import os
import urllib2
import PyRSS2Gen
from os.path import expanduser

#open MU news web page and load html using Python package urllib2.

url = 'http://www.monmouth.edu/academics/CSSE/news.asp'
response = urllib2.urlopen(url)
input = response.read()

#Obtain headlines,titles,descriptions from the above file.

headlines = re.findall("<strong>(.+)\</strong>", input)
urls = re.findall("<a name=\"(.+)\\\" class=\"anchorMargin\">", input)
descs = re.findall(r'</strong>(.+?)<hr />', input,re.DOTALL)	#to obtain text from <p> for description.	

#direct the output under public_html 
home = expanduser("~")  
rssfile = home + "/public_html/cssenews.rss.xml"

#Use PyRSS2Gen to append the headlines,titles and descriptions to generate the feed.  
rss = PyRSS2Gen.RSS2(
  title = "Monmouth News Feed",
  link = "http://www.monmouth.edu/school-of-science/news-and-events.aspx",
  description = "Monmouth University News",
  items = [])

for i in range(len(headlines)):
  item = PyRSS2Gen.RSSItem(
							title = headlines[i],
							link = "http://www.monmouth.edu/academics/CSSE/news.asp#"+ urls[i],
							description = (re.sub('<[^>]*>','',descs[i])[:140]))
  rss.items.append(item)  

#Write the XML file to disk.
rss.write_xml(open(rssfile, "w"))
