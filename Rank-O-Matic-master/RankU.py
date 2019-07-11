from urllib.parse import urlencode, urlparse, parse_qs
from lxml.html import fromstring
from requests import get
from bs4 import BeautifulSoup
import nltk
import requests
import re
import heapq
fo=""
def RankUCal(input_msg):
    target_text=str(input_msg)
    fo=""
    for n in range(2):
        target_url="https://www.google.com/search?q="+str(target_text)+"&tbm=nws&start="+str(n)
        raw = get(target_url).text
        page = fromstring(raw)
        for result in page.cssselect(".r a"):
            url = result.get("href")
            if url.startswith("/url?"):
                url = parse_qs(urlparse(url).query)['q']
                fo=fo+str(url[0])
                response = requests.get(url[0])
                soup = BeautifulSoup(response.content, "html.parser")
                links = soup.findAll("p")
                fo=fo+"\n\n"+re.sub('<[^>]+>', '',(str(links)).lower())
    
    #NE Tagging Target Text, Important Words Shortlisted          
    namedEnt = nltk.pos_tag(nltk.word_tokenize(target_text))
    named_entities = []
    search_query = []
    for x in namedEnt:
        if x[1] == 'NNP':
            named_entities.append(x[0])
    i=0
    
    while(True):
        try:
            search_query.append(str(named_entities[i][0][0]))
        except Exception as e:
            break
        i+=1
    
    k=0
    count=[0]*len(search_query)
    while(k<len(search_query)):
        search_text=(str(search_query[k])).lower()
        for i in fo:
            if(i==search_text):
                count[k]+=1
        k+=1
    try:
        min2=heapq.nsmallest(2,count)[-1]
    except Exception as e:
        rel=59
    try:
        rel=(min(count)/min2)*100
    except Exception as e:
        rel=61
    return rel