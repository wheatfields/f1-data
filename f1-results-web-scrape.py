
import pandas as pd
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import datetime


# -----------------------------------------------------------------------------

url = "https://www.formula1.com/en/results.html/2016/races/939/bahrain/race-result.html"
html = urlopen(url)
soup = BeautifulSoup(html, 'html')

# years for the URL loop
years_url = soup.find('select',{"class": "resultsarchive-filter-form-select", "name":"year"})
years_url = years_url.findAll('option')
years_url = str(years_url)
years_url = re.findall('"([^"]*)"', years_url)
filter_object = filter(lambda x: x != "", years_url)
years_url = list(filter_object)
years_url = years_url[0:15]

# apiType for the URL loop
apiType_url = soup.find('select',{"class": "resultsarchive-filter-form-select", "name":"apiType"})
apiType_url = apiType_url.findAll('option')
apiType_url = str(apiType_url)
apiType_url = re.findall('"([^"]*)"', apiType_url)
filter_object = filter(lambda x: x != "", apiType_url)
apiType_url = list(filter_object)

# resultType for the URL loop
resultType_url = soup.find('select',{"class": "resultsarchive-filter-form-select", "name":"resultType"})
resultType_url = resultType_url.findAll('option')
resultType_url = str(resultType_url)
resultType_url = re.findall('"([^"]*)"', resultType_url)
filter_object = filter(lambda x: x != '', resultType_url)
resultType_url = list(filter_object)

m = []
for year in years_url:
    url = "https://www.formula1.com/en/results.html/%s/races.html" %(year)
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html')
    # meetingKey for the URL loop
    meetingKey_url = soup.find('select',{"class": "resultsarchive-filter-form-select", "name":"meetingKey"})
    meetingKey_url = meetingKey_url.findAll('option')
    meetingKey_url = str(meetingKey_url)
    meetingKey_url = re.findall('"([^"]*)"', meetingKey_url)
    m = m + meetingKey_url
m = list(set(m))
meetingKey_url = m 

for resultType in resultType_url:  
    proper_header = [col.text for col in 
                     BeautifulSoup(urlopen('https://www.formula1.com/en/results.html/2013/races/883/spain/%s.html' %(resultType)), 
                                   'html').find('table',
                                                {"class":"resultsarchive-table"}).findAll(['th'])]
                                                
    print("%s started: %s" % (resultType, datetime.datetime.now()))

# -----------------------------------------------------------------------------
                                       
    f = pd.DataFrame()
    for meetingKey in meetingKey_url:
        for year in years_url:
                b = 'https://www.formula1.com/en/results.html/%s/races/%s/%s.html' %(year, meetingKey, resultType)
                html = urlopen(b)
                soup = BeautifulSoup(html, 'html')
                table = soup.find('table',{"class":"resultsarchive-table"})
                try:
                    th = table.findAll(['th'])
                    headers = [col.text for col in th]
                    if (headers == proper_header):
                        tr = table.findAll(['tr'])
                        a = pd.DataFrame()
                        
                        for cell in tr:
                            th = cell.find_all('th')
                            th_data = [row.text.strip('\n') for row in th]
                            td = cell.find_all('td')
                            row = [i.text.replace('\n','') for i in td]
                            row = pd.DataFrame(row).transpose()
                            row['year'] = year
                            row['meetingKey'] = meetingKey
                            a = a.append(row)
                        f = f.append(a) 
                except Exception:
                    pass
                                
    # -----------------------------------------------------------------------------
                    
    # add some more column titles to the 'proper headers' - this has to be done
    # after creating the data as the 'proper headers' is used to determine whether
    # the url is used or not
    proper_header.insert(0, 'meetingKey')           
    proper_header.insert(0, 'year')
    
    # add column titles
    f.columns = proper_header    
          
    # getting rid of empty columns
    del f['']
    
    # adding in a race name column from the meetingKey
    f['race'] = f['meetingKey'].str.split('/').str[1]
    
    #swap the race and meetingKey columns around
    columnsName = list(f.columns)
    F, H = columnsName.index('race'), columnsName.index('meetingKey')
    columnsName[F], columnsName[H] = columnsName[H],columnsName[F]
    f = f[columnsName]
    
    # exporting to csv
    os.chdir(r"C:\Users\adamw\Documents\Python Scripts\f1_data\2006 to Present")
    f.to_csv('%s.csv' %(resultType), index = False)

    print("%s ended: %s" % (resultType, datetime.datetime.now()))

# -----------------------------------------------------------------------------













