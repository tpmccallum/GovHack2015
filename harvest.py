import urllib
import json
url= 'http://data.gov.au/dataset/3fd356c6-0ad4-453e-82e9-03af582024c3/resource/3182591a-085a-465b-b8e5-6bfd934137f1/download/Localphotostories2009-2014-JSON.json'
abcJson = urllib.urlopen(url).read()
abcData = json.loads(abcJson.decode('utf-8-sig', 'ignore'))

getText(url):
  

#print j
for item in abcData:
    url = item['URL']
    date = item['Date']
    title = item['Title']
    subjects = item['Subjects']
    station = item['Station']
    place = item['Place']
    keywords = item['Keywords']
    text = getText(url)
    textString = " ".join(title, subjects, station, place, keywords, text)
