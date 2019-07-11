from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re
app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/', methods=['POST'])
def getvalue():
    sts=[]
    cname=request.form['cname']
    uname=request.form['uname']
    #coname=request.form['coname']
    quote_page = "https://www.timeshighereducation.com/world-university-rankings/"+uname.replace(" ","-")
    page = requests.get(quote_page)
    soup = BeautifulSoup(page.text, 'html.parser')
    name= soup.find('a',class_="link--country-flag")
    rank=soup.find('div',class_="rank__number")
    n=re.sub('<[^>]+>', '',str(name)).strip()
    last_n=n.rfind(',')
    n=str(n[int(last_n+1):])
    r=re.sub('<[^>]+>', '',str(rank))
    about=soup.findAll('div',class_="pane-content")
    about1=str(about[2:3])
    ab=str(re.findall('>.*[</div>]',about1))
    ab=ab[2:len(ab)-7]
    q=0
    i=0
    for i in range(0,len(ab)):
        if(ab[i]=='.'):
            q=q+1
        if(q==3):
            break
        else:continue
    ab=ab[:i+1]
    ab=ab.replace(",","")
    ab=ab.replace("<p>","")
    ab=ab.replace("</p>","")
    ab=ab.replace("\'","")
    ab=ab.replace(">","")
    ab=ab.replace("\"","")
    kst=str(about[6:7])
    kst=kst.replace("\n","")
    w=re.findall('\$[0-9].[^<]*<',kst)
    v=re.findall('[0-9]+%',kst)
    for q in range(0,len(w)):
        w[q]=w[q].replace("<","")
    for l in range(0,len(w)):
        sts.append(w[l])
    for l in range(0,len(v)):
        sts.append(v[l])
    if "world-university-rankings" in ab:
        ab="___________Information not available.___________"
    cr="1"
    if cname in n:
        rank=r
        if(len(sts)<4):
            sts=[]
            sts.append("NA")
            sts.append("NA")
            sts.append("NA")
            sts.append("NA")
            cr="NA"
        return render_template("result.html",cr=cr,rank=rank,uname=uname,about=ab,sal=str(sts[0]),cf=str(sts[2]),per=str(sts[3]))
    else:
        return render_template("cverify.html",cname=n,uname=uname,about=ab)
@app.route('/<value>')
def getvaluere(value):
    sts=[]
    uname=value
    #coname=request.form['coname']
    quote_page = "https://www.timeshighereducation.com/world-university-rankings/"+uname.replace(" ","-")
    page = requests.get(quote_page)
    soup = BeautifulSoup(page.text, 'html.parser')
    name= soup.find('a',class_="link--country-flag")
    rank=soup.find('div',class_="rank__number")
    n=re.sub('<[^>]+>', '',str(name)).strip()
    last_n=n.rfind(',')
    n=str(n[int(last_n+1):])
    r=re.sub('<[^>]+>', '',str(rank))
    about=soup.findAll('div',class_="pane-content")
    about1=str(about[2:3])
    ab=str(re.findall('>.*[</div>]',about1))
    ab=ab[2:len(ab)-7]
    q=0
    i=0
    for i in range(0,len(ab)):
        if(ab[i]=='.'):
            q=q+1
        if(q==3):
            break
        else:continue
    ab=ab[:i+1]
    ab=ab.replace(",","")
    ab=ab.replace("<p>","")
    ab=ab.replace("</p>","")
    ab=ab.replace("\'","")
    ab=ab.replace(">","")
    ab=ab.replace("\"","")
    kst=str(about[6:7])
    kst=kst.replace("\n","")
    sts=[]
    w=re.findall('\$[0-9].[^<]*<',kst)
    v=re.findall('[0-9]+%',kst)
    for q in range(0,len(w)):
        w[q]=w[q].replace("<","")
    for l in range(0,len(w)):
        sts.append(w[l])
    for l in range(0,len(v)):
        sts.append(v[l])
    cr="1"
    if "world-university-rankings" in ab:
        ab="___________Information not available.___________"
    if(len(sts)<4):
        sts=[]
        sts.append("NA")
        sts.append("NA")
        sts.append("NA")
        sts.append("NA")
        cr="NA"
    return render_template("result.html",cr=cr,rank=r,uname=uname,about=ab,sal=str(sts[0]),cf=str(sts[2]),per=str(sts[3]))
    
if __name__=='__main__':
    app.run()