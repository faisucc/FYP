import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract
from googlesearch import search
import time
import requests


title = ""
try:
  fp = urllib.request.urlopen("http://www.python.org")
  mybytes = fp.read()
  mystr = mybytes.decode("utf8")
  fp.close()
  soup = BeautifulSoup(mystr, 'html.parser')
  title = soup.find('title').text
except:
     title = "Title doesnt exist"

print("Title: ", title)

time.sleep(2)

domain = urlparse('https://att-mail-info-104416.weeblysite.com/juvnberdkjlsgvndrljvndrs;/fvdf/bdg/bdfv/dfb/tdgb/db/').netloc
print("Base URL: ", "https://" + domain)

def get_base_url(url):
   domain = urlparse(url).netloc
   baseUrl = "https://" + domain
   return baseUrl

time.sleep(2)

def get_domain_name(url):
    extracted_info = tldextract.extract(url)
    domain_name = extracted_info.registered_domain
    return domain_name

def getDOM(url):
   try:
      fp = urllib.request.urlopen(url)
      mybytes = fp.read()
      mystr = mybytes.decode("utf8")
      fp.close()
      soup = BeautifulSoup(mystr, 'html.parser')
      return soup
   except:
      print("Getting DOM for url: " + url + " failed")

def CalculateJaccardSimilarity(matched_domain_DOM, query_url_DOM):
   print("need to do this function")

url = "http://www.python.org"
domain_name = get_domain_name(url)
baseURL = get_base_url(url)
print("Domain name: ", domain_name)
print("Base URL: ", baseURL)

time.sleep(2)

def get_search_results(query, num_results = 10):
  links = list(search(query,num_results=num_results))
  return links

legit_status = False
domain_status = False
query_url_DOM = getDOM(url)         #this input is the URL that the user wants to visit. 

if title != "Title doesnt exist":      #7
   query = title + ' ' + domain_name   
   results = get_search_results(query) #9
   for r in results:                   #10
      domain_r = get_domain_name(r)    #11
      baseURL_r = get_base_url(r)      #12
      if domain_r == domain_name :     #14
         domain_status = True          #15
         if baseURL_r ==  baseURL :    #16
            print("Legitimate")        #17
         matched_domain_DOM = getDOM(r)#19
   
   if domain_status == False:
      query = domain_name              #23
   else:
      print("compute jaccard similarity")
else:
   query = domain_name                 #28

results = get_search_results(query)    #30
for r in results:
   domain_r = get_domain_name(r)       #32
   if domain_r == domain_name:         #34
      domain_status = True             #35
      matched_domain_DOM = getDOM(r)   #36
   

if domain_status == True:              #39
   similarity_score = CalculateJaccardSimilarity(matched_domain_DOM,query_url_DOM)