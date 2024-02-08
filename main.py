import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract
from googlesearch import search
import time
import requests
from urllib.parse import urljoin
import time


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
      print("Failed getting DOM for url: " + url + " failed")


url = "https://www.nitc.ac.in/departments"
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
query_url = "https://www.nitc.ac.in/"
query_url_DOM = getDOM(query_url)         #this input is the URL that the user wants to visit. 

soup = getDOM("https://www.nitc.ac.in/departments")

css_files = []
for css in soup.find_all("link"):
    if css.attrs.get("href"):
        # if the link tag has the 'href' attribute
        css_url = urljoin(url, css.attrs.get("href"))
        css_files.append(css_url)
# print(css_files)

js_files = []
for js in soup.find_all("script"):
    if js.attrs.get("src"):
        # if the link tag has the 'href' attribute
        js_url = urljoin(url, js.attrs.get("src"))
        js_files.append(js_url)
# print(js_files)

img_files = []
for img in soup.find_all("img"):
    if img.attrs.get("src"):
        # if the link tag has the 'href' attribute
        img_url = urljoin(url, img.attrs.get("src"))
        img_files.append(img_url)
# print(img_files)

links_files = []
for links in soup.find_all("a"):
    if links.attrs.get("href"):
        # if the link tag has the 'href' attribute
        links_url = urljoin(url, links.attrs.get("href"))
        links_files.append(links_url)
# print(links_files)
        

suspicious_page_count = len(img_files) + len(links_files) + len(js_files) + len(css_files)
print("suspicoenriugvnerjogne count = ", suspicious_page_count)


def CalculateJaccardSimilarity(matched_domain_DOM, matched_url):
#    print("need to do this function")
   common_elements_count = 0
   img_tags = matched_domain_DOM.find_all(['img'])
   script_tags = matched_domain_DOM.find_all(['script'])
   style_tags = matched_domain_DOM.find_all(['style'])
   a_tags = matched_domain_DOM.find_all(['a'])
   matched_page_count = len(img_tags) + len(script_tags) + len(style_tags) + len(a_tags) 

   for img in img_tags:
       if img.attrs.get("src"):
           img_url = urljoin(matched_url,img.attrs.get("src"))
           if img_url in img_files:
                common_elements_count += 1
    
   for script in script_tags:
        if script.attrs.get("src"):
            script_url = urljoin(matched_url,script.attrs.get("src"))
            if script_url in js_files:
                common_elements_count += 1
    
   for style in style_tags:
       if style.attrs.get("href"):
           style_url = urljoin(matched_url,style.attrs.get("href"))
           if style_url in css_files:
               common_elements_count += 1

   for a in a_tags:
       if a.attrs.get("href"):
           a_url = urljoin(matched_url,a.attrs.get("href"))
           if a_url in links_files:
                common_elements_count += 1

#    print("common elements = ", common_elements_count)
   similarity_score = common_elements_count/(suspicious_page_count + matched_page_count - common_elements_count)
   return similarity_score
 

# print(CalculateJaccardSimilarity(query_url_DOM, query_url))  #change 2nd variable to each matched result URL

def step40():
    threshold = 0.75
    similarity_score = CalculateJaccardSimilarity(matched_domain_DOM,matched_domain_url)
    if similarity_score > threshold:
        legit_status = True
    else:
        legit_status = False
    if legit_status == True:
        print("From Jailphish similarity, LEGITIMATE")
        exit()
    else:
        print("From jailphish similarity, PHISHING")
        exit()

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
            exit()
         matched_domain_DOM = getDOM(r)#19
         matched_domain_url = r
   if domain_status == False:
      query = domain_name              #23
   else:
      step40()
else:
   query = domain_name                 #28

results = get_search_results(query)    #30
for r in results:
   domain_r = get_domain_name(r)       #32
   if domain_r == domain_name:         #34
      domain_status = True             #35
      matched_domain_DOM = getDOM(r)   #36
      matched_domain_url = r

if domain_status == True:              #39
    step40()
else:
    print("Domain status false - PHISHING!")