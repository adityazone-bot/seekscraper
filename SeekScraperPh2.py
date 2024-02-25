import requests
from bs4 import BeautifulSoup
import os
import sys
import dblibs
import time
import datetime
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

connection = dblibs.openDB()

headers = {'Accept': 'application/xhtml+xml'}
baseURL = "https://www.seek.com.au"

def scrapeJob(row):
    jobURL = baseURL + row[2]
    print (f"Fetching {jobURL}")

    resp = requests.get(jobURL, headers = headers, verify = False)
    page = BeautifulSoup(resp.text, "lxml")

    if 'This job is no longer advertised' in page.text:
        connection.execute("DELETE FROM JOB WHERE JOBID=?", (int(row[0]),))
        connection.commit()
        return

    jobType = page.find('span', {"data-automation": "job-detail-work-type"}).text

    pageText = page.find('div', {"data-automation": "jobDetailsPage"}).text
    timePosted = pageText[pageText.find('Posted')+6:pageText.find('ago')].strip()
    if 'h' in timePosted:
        daysAgo = 1
    else:
        daysAgo = int(timePosted.replace('d',''))
    datePosted = (datetime.datetime.utcnow() - datetime.timedelta(days=daysAgo)).strftime('%Y-%m-%d')

    description = page.find('div', {"data-automation": "jobAdDetails"}).text

    connection.execute("UPDATE JOB SET STATUS='PHASE2', DATEPOSTED=?, TYPE=?, DESCRIPTION=? WHERE JOBID=?",(datePosted, jobType, description, row[0]))
    connection.commit()

print ("Restarting Phase2 Scraper")

cursor = connection.execute("SELECT * from JOB WHERE STATUS = 'PHASE1'")
for row in cursor:
    try:
        scrapeJob(row)
    except Exception as err:
        print (f"Error fetching {row[0]}: {err}")

    time.sleep(5)


dblibs.closeDB(connection)
