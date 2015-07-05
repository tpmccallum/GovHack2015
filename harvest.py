import urllib
import json
import BeautifulSoup
import re
import os
import subprocess
import codecs
import xml.dom.minidom

url= 'http://data.gov.au/dataset/3fd356c6-0ad4-453e-82e9-03af582024c3/resource/3182591a-085a-465b-b8e5-6bfd934137f1/download/Localphotostories2009-2014-JSON.json'
abcJson = urllib.urlopen(url).read()
abcData = json.loads(abcJson.decode('utf-8-sig', 'ignore'))

def removeEverythingButAlphaNumeric(stringToClean):
    textFinal = re.sub(r'\W+', ' ', stringToClean)
    return textFinal

def createJsonCatalogTxt(year, town, filename, searchString):
    jsonObject1 = {u"date": int(year), u"town": town, u"filename": filename, u"searchstring": searchString}
    return json.dumps(jsonObject1)
    
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
    
def createTextFileName(pdfUrl):
    textFileName1 = removeEverythingButAlphaNumeric(pdfUrl)
    textFileName2 = removeSpaces(textFileName1)
    return [textFileName2 + ".txt", textFileName2] 
    
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
print "Creating text file dir"
textFileDir = os.path.join(currentDir, "textFiles")
if not os.path.exists(textFileDir):
    os.makedirs(textFileDir)
    
for item in abcData:
    url = item['URL']
    print url
    date = item['Date']
    print date
    year = date[-4:]
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
    fullTextPre = " ".join([title, textP, subjects, station, place, keywords])
    fullText = removeEverythingButAlphaNumeric(fullTextPre)

    print "Creating text file"
    textFileName = createTextFileName(url)
    textFileObject = codecs.open(os.path.join(textFileDir, textFileName[0]), 'wb', "utf-8")
    textFileObject.write(fullText)
    textFileObject.close()

    searchString = createSearchString(year, place, url, title)
    print "Writing to the jsoncatalogfile"
    jsonCatalogFile.write(createJsonCatalogTxt(year, place, textFileName, searchString))
    jsonCatalogFile.write("\n")
    
    print "* finished processing this single item"
print "Finished processing all items"

#move these files over to the bookworm instance and create the json file which has to go into files/metadata before running the make file
#[
#{"field":"date","datatype":"time","type":"numeric","unique":true,"derived":[{"resolution":"year"}]},
#{"field":"searchstring","datatype":"searchstring","type":"text","unique":true},
#{"field":"town","datatype":"categorical","type":"text","unique":true}
#]
