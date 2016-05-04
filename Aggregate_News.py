#!/usr/bin/env python
#Imports
import time
from datetime import datetime
import urllib
import mechanize
import getpass
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
    
#Functions
#done in two lines for readability 
def convertTime(time):
    try:
        time = time.replace(",","").replace("@","").replace("."," ").replace(":"," ") 
        t2 = datetime.strptime(time[3:], "%A %B %d %Y %I %M%p")
        return (t2-datetime(1970,1,1)).total_seconds()
    except Exception:
        print "Error while converting time to seconds"
        return 1
    
#Variables
outputList = []
articleheadlineList = []
posterList = []
timePostedList = []
response = []

totalRecords=0
totalRecordsOut=0
page=-1
timestamp=0
br = mechanize.Browser()

On_This_Page = False
logged_in = False

url = 'https://slashdot.org/'

#loop until logged in
br.open(url)
while not logged_in:
    nick = raw_input("Enter your nickname for slashdot.org: ") #Chazzio1
    passw = getpass.getpass("Enter your password: ")        #vBm5HbkA
    while(timestamp<1):
        try:
            timestamp = int(raw_input("Enter timestamp in seconds since 1970: ")) # 1461069600
        except Exception:
            "Not a valid number"
            
#find the login form required
#for form in br.forms():
#    print form 
    #br.set_debug_http(True)
    #br.set_debug_responses(True)
    br.select_form(nr=1)#login form - uses
    br.form['unickname'] = nick
    br.form['upasswd'] = passw
    result = br.submit()
    response = br.response()
    sou = BeautifulSoup(response)
    user = str(sou.find_all(class_="user-access"))
    if user.find(nick)>0:
        logged_in=True
        print "Logged in"
    else:
        print "Try Again\n"
    time.sleep(5)

#loop until date found
while not(On_This_Page):
    page+=1
    try:
        br.open(url)
    except Exception:
        print "Error cannot open next page "
        print "Page " + url + " may not exist"
        br.close()
        break
        #release resources
    
#html to BeautifulSoup
    response = ""
    response=br.response()
    soup = ""
    soup = BeautifulSoup(response.read())
#Find all Headlines
    articleHeadline = soup.find_all('span',class_="story-title")
    poster = soup.find_all('span', class_="story-byline")
    timePosted = soup.find_all('time')    
#Store all required info
    for headline in articleHeadline:
        articleheadlineList.append(headline.a.get_text()) #Get Text headline
        totalRecords+=1
    for t in timePosted:
        timePostedList.append(convertTime(t.get("datetime"))) 
    for val in poster:
        try:
            posterList.append(val.a.get_text())
        except:
            posterList.append("Author not logged in")
#Make output List as per format required    
    for j in xrange(totalRecords):
        if (int(timePostedList[j]) < timestamp):
            On_This_Page = True
            break
        else:
            outputList.append(str("{" "\n" "\"headline\": ") + str(articleheadlineList[j]) +"\n\"author\": \"" + str(posterList[j]) + "\"\n\"date\": " + str(int(timePostedList[j])) + "\n},\n")
            totalRecordsOut+=1;
    #All records on page within timeframe, open next page
    if totalRecordsOut%totalRecords == 0:
        totalRecordsOut=0
        url = str('https://slashdot.org/?page=')  + str(page+1)
        #debug message
        print "Opening next page " + url 

for headline in outputList:
    print headline

print "total headlines returned: " + str(totalRecordsOut)
br.close()


