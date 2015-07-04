import urllib
import json
import BeautifulSoup
import re

url= 'http://data.gov.au/dataset/3fd356c6-0ad4-453e-82e9-03af582024c3/resource/3182591a-085a-465b-b8e5-6bfd934137f1/download/Localphotostories2009-2014-JSON.json'
abcJson = urllib.urlopen(url).read()
abcData = json.loads(abcJson.decode('utf-8-sig', 'ignore'))

def removeEverythingButAlphaNumeric(stringToClean):
    textFinal = re.sub(r'\W+', ' ', stringToClean)
    return textFinal
    
def removeSpaces(stringToClean):
    pattern = re.compile(r'\s+')
    cleanString = re.sub(pattern, '', stringToClean)
    return cleanString

def getText(url):
    textString = ""
    Soup = BeautifulSoup.BeautifulSoup
    source = urllib.urlopen(url).read()
    soup = Soup(source)
    for i in soup.findAll("p"):
        textString += i.text
    return textString
    
def createSearchString(year, town, url, title):
    #create dom object
    doc = xml.dom.minidom.Document()
    #create anchor element
    anchor = doc.createElement('a')
    #add attributes to element
    anchor.attributes['href']= url
    anchor.attributes['target']= "_blank"
    #create text for inside the element
    txt = doc.createTextNode("%s - %s a news story from %s" % (title, year, town))
    anchor.appendChild(txt)
    return anchor.toxml()
    
currentDir = os.getcwd()
print "Current working directory is %s" % (currentDir)
print "Creating output environment"
pTrt = os.path.join(currentDir, "files", "texts", "raw")
#TODO symlink the text files to the raw directory
if (not os.path.exists(pTrt)):
    os.makedirs(pTrt)
os.makedirs(os.path.join(currentDir, "files", "metadata"))
#TODO put a copy of the field_descriptions.json file here (duplicate copy)
print "Copying our field_descriptions.json file from %s to the files/metadata dir " % (currentDir)
subprocess.call(['cp', 'field_descriptions.json', 'files/metadata/'])
print "Creating the jsoncatalog.txt file"
jsonCatalogFile = codecs.open(os.path.join(currentDir, "files", "metadata" , "jsoncatalog.txt"), 'wb', "utf-8")

for item in abcData:
    url = item['URL']
    print url
    date = item['Date']
    print date
    title = item['Title']
    print title
    subjects = item['Subjects']
    print subjects 
    station = item['Station']
    print station
    place = item['Place']
    print place
    keywords = item['Keywords']
    print keywords
    textP = getText(url)
    print textP
    print "creating full text"
    fullText = " ".join([title, textP, subjects, station, place, keywords])
    searchString = createSearchString(paper_year, uni, manuscript_url, paper_title)
