import requests
from bs4 import BeautifulSoup
import os
import sys
import dblibs
import time
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

connection = dblibs.openDB()

headers = {'Accept': 'application/xhtml+xml'}
baseURL = "https://www.seek.com.au"
jobSearchURL = baseURL + "/jobs-in-information-communication-technology/in-All-Melbourne-VIC?sortmode=ListedDate&page={}"



pageNo = 1
while(True):
    resp = requests.get(jobSearchURL.format(pageNo), headers = headers, verify = False)
    
    page = BeautifulSoup(resp.text, "lxml")
    articles = page.findAll('article')

    if not articles:
        print ('Finished scraping PHASE1')
        break
        #pageNo = 1
        #continue

    for article in articles:
        print ("\nJOB\n")

        articlePage = BeautifulSoup(str(article), "lxml")

        jobID = article['data-job-id']
        print (jobID)
        jobTitle = articlePage.find('a', {"data-automation": "jobTitle"}).text
        print (jobTitle)
        URL = articlePage.find('a', {"data-automation": "jobTitle"})['href']
        print (URL)
        
        try:
            company = articlePage.find('a', {"data-automation": "jobCompany"}).text
        except Exception as err:
            if "Private Advertiser" in articlePage.text:
                company = "Private Advertiser"
            else:
                raise

        print (company)

        location = ""
        locations = articlePage.findAll('a', {"data-automation": "jobLocation"})
        for loc in locations:
            location = location + loc.text + ","

        location = location[0:-1]
        print (location)

        try:
            connection.execute("INSERT INTO JOB (JOBID,TITLE,URL,COMPANY,LOCATION,STATUS) VALUES (?,?,?,?,?,'PHASE1')",(jobID, jobTitle, URL, company, location,))
        except Exception as err:
            if not 'UNIQUE constraint failed' in str(err):
                raise
        #query = f"INSERT INTO JOB (JOBID,TITLE,URL,COMPANY,LOCATION,STATUS) VALUES ('{jobID}','{jobTitle}','{URL}','{company}','{location}','PHASE1');"
        #dblibs.executeQuery(connection, query)

    pageNo += 1
    connection.commit()

    print (f"\nSleeping... {pageNo}")
    time.sleep(5)

dblibs.closeDB(connection)
#<article class="yvsb870 yvsb871 h3f08h1 _14uh9946i _14uh9947i _14uh9949m _14uh9948m _14uh9945a h3f08h4 _14uh9949i" aria-label="IT Presales Engineer" data-automation="premiumJob" data-job-id="62256513"><div class="yvsb870 _14uh9945e _14uh9940 k7nppw0">This is a featured job</div><div class="yvsb870 _14uh9944u _14uh9944s"><a href="/job/62256513?type=promoted#sol=1b052b4c8ef7c74887ef815a95d62d955d1f3f40" class="yvsb870 yvsb87f _14uh9945e _14uh994j _14uh994k _14uh994l _14uh994m _14uh9947" target="_self"></a></div><div class="yvsb870 v8nw070 v8nw075"><div class="yvsb870 _14uh9946i"><div class="yvsb870 v8nw070 v8nw072"><div class="yvsb870 _14uh99466"><div class="yvsb870 _14uh99456 _14uh994ey v8nw0725"><div class="yvsb870 _14uh994r _14uh994p x5kz590"><div class="yvsb870 _14uh9949i _14uh994n _14uh9944u _14uh994ei x5kz591"><div class="yvsb870 v8nw070 v8nw075"><div class="yvsb870 _14uh9946i"><div class="yvsb870 _14uh994ai"><h3 class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhyl _1d0g9qk4 _1cshjhys _1cshjhy21"><a href="/job/62256513?type=promoted#sol=1b052b4c8ef7c74887ef815a95d62d955d1f3f40" data-automation="jobTitle" class="_1tmgvw5 _1tmgvw7 _1tmgvwa _1tmgvwb _1tmgvwe yvsb870 yvsb87f _14uh994h" target="_self">IT Presales Engineer</a></h3></div></div><div class="yvsb870 _14uh9946i"><span class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy2 _1cshjhy21 _1d0g9qk4 _1cshjhyd"><span class="yvsb870 _14uh9945e _14uh9940 k7nppw0">at </span><a href="/jobs?advertiserid=24298574" rel="nofollow" class="_842p0a0" title="Jobs at Perfekt Pty Ltd" aria-label="Jobs at Perfekt Pty Ltd" data-automation="jobCompany" target="_self">Perfekt Pty Ltd</a></span></div></div></div></div><div class="yvsb870 _14uh994r _14uh994fm x5kz590"><div class="yvsb870 _14uh9949i _14uh994n _14uh9944u _14uh994ei x5kz591"><div class="yvsb870 _14uh994ai" aria-hidden="true"><span class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy21 _1d0g9qk4 _1cshjhy7"><span class="yvsb870 h3f08h9" data-automation="jobPremium">Featured</span></span></div></div></div></div></div><div class="yvsb870 _14uh99466"><div class="yvsb870"><div class="yvsb870 _14uh9945e _14uh9940 k7nppw0"><p class="yvsb870">This is a Full Time job</p></div><div class="yvsb870 v8nw070 v8nw075"><div class="yvsb870 _14uh9946i"><span class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy21 _1d0g9qk4 _1cshjhy7"><a tabindex="-1" href="/jobs-in-information-communication-technology/in-Caulfield-VIC-3162?sortmode=ListedDate" rel="nofollow" class="_842p0a0" title="Limit results to Caulfield" aria-label="Limit results to Caulfield" data-automation="jobLocation" target="_self" style="pointer-events: none;">Caulfield</a>, <a tabindex="-1" href="/jobs-in-information-communication-technology/in-All-Melbourne-VIC?sortmode=ListedDate" rel="nofollow" class="_842p0a0" title="Limit results to Melbourne VIC" aria-label="Limit results to Melbourne VIC" data-automation="jobLocation" target="_self" style="pointer-events: none;">Melbourne VIC</a></span></div><div class="yvsb870 _14uh9946i _14uh9944q _14uh9944v"><span class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy21 _1d0g9qk4 _1cshjhy7"><div class="yvsb870 v8nw070 v8nw07a"><div class="yvsb870 _14uh994fe _14uh99456 _14uh994ey v8nw072a"><div class="yvsb870 _14uh994r _14uh994e2 _14uh994b2 _14uh9944u _14uh994ei"><span class="yvsb870 _14uh9945e _14uh9940 k7nppw0">classification: Information &amp; Communication Technology</span></div><div class="yvsb870 _14uh994r _14uh994e2 _14uh994b2 _14uh9944u _14uh994ei"><a tabindex="-1" href="/jobs-in-information-communication-technology?sortmode=ListedDate" rel="nofollow" class="_842p0a0" title="Limit results to Information &amp; Communication Technology" aria-label="Limit results to Information &amp; Communication Technology" data-automation="jobClassification" target="_self" style="pointer-events: none;">Information &amp; Communication Technology</a></div><div class="yvsb870 _14uh994r _14uh994e2 _14uh994b2 _14uh9944u _14uh994ei"><div class="yvsb870 _14uh994da _14uh994ca"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" xml:space="preserve" focusable="false" fill="currentColor" width="16" height="16" class="yvsb870 _1ko75050 _14uh99452 _14uh9945a vnye0o0 vnye0o2 vnye0o3 vnye0o4 _1ko75053" aria-hidden="true"><path d="M20.7 7.3c-.4-.4-1-.4-1.4 0L12 14.6 4.7 7.3c-.4-.4-1-.4-1.4 0s-.4 1 0 1.4l8 8c.2.2.5.3.7.3s.5-.1.7-.3l8-8c.4-.4.4-1 0-1.4z"></path></svg></div></div><div class="yvsb870 _14uh994r _14uh994e2 _14uh994b2 _14uh9944u _14uh994ei"><span class="yvsb870 _14uh9945e _14uh9940 k7nppw0">subClassification: Networks &amp; Systems Administration</span></div><div class="yvsb870 _14uh994r _14uh994e2 _14uh994b2 _14uh9944u _14uh994ei"><a tabindex="-1" href="/jobs-in-information-communication-technology/networks-systems-administration?sortmode=ListedDate" rel="nofollow" class="_842p0a0" title="Limit results to Networks &amp; Systems Administration in Information &amp; Communication Technology" aria-label="Limit results to Networks &amp; Systems Administration in Information &amp; Communication Technology" data-automation="jobSubClassification" target="_self" style="pointer-events: none;">Networks &amp; Systems Administration</a></div></div></div></span></div></div></div></div><div class="yvsb870 _14uh99466"><ul class="yvsb870 yvsb873 v8nw070 v8nw074"><li class="yvsb870 _14uh9946e"><div class="yvsb870 _14uh99456"><div class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy21 _1d0g9qk4 _1cshjhy7"><div class="yvsb870 _14uh99456 _14uh994ea _14uh9944 _1ev1esa1" aria-hidden="true"><div class="yvsb870 _14uh9945q _6gd0oa0 _6gd0oa2"></div></div></div><div class="yvsb870 _14uh994r _14uh994p _14uh9949i"><span class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy21 _1d0g9qk4 _1cshjhy7">Work in a team of highly skilled sales, presales and implementation engineers</span></div></div></li><li class="yvsb870 _14uh9946e"><div class="yvsb870 _14uh99456"><div class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy21 _1d0g9qk4 _1cshjhy7"><div class="yvsb870 _14uh99456 _14uh994ea _14uh9944 _1ev1esa1" aria-hidden="true"><div class="yvsb870 _14uh9945q _6gd0oa0 _6gd0oa2"></div></div></div><div class="yvsb870 _14uh994r _14uh994p _14uh9949i"><span class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy21 _1d0g9qk4 _1cshjhy7">Work with some of Australias top companies who are our clients</span></div></div></li><li class="yvsb870 _14uh9946e"><div class="yvsb870 _14uh99456"><div class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy21 _1d0g9qk4 _1cshjhy7"><div class="yvsb870 _14uh99456 _14uh994ea _14uh9944 _1ev1esa1" aria-hidden="true"><div class="yvsb870 _14uh9945q _6gd0oa0 _6gd0oa2"></div></div></div><div class="yvsb870 _14uh994r _14uh994p _14uh9949i"><span class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy21 _1d0g9qk4 _1cshjhy7">Work in a flexible and friendly environment with the ability to work from home</span></div></div></li></ul></div><div class="yvsb870 _14uh99466"><div class="yvsb870 _14uh9948z"><span class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy22 _1d0g9qk4 _1cshjhy7" data-automation="jobShortDescription">Perfekt is on the hunt for a dynamic, talented and awesome IT Presales Engineer to join our growing team</span></div></div></div></div><div class="yvsb870 _14uh9946i"><div class="yvsb870 _14uh99456 _14uh994ey _14uh994ee v8nw072a"><div class="yvsb870 _14uh994r _14uh994p x5kz590"><div class="yvsb870 _14uh994a2 _14uh994n _14uh9944u _14uh994ei x5kz591"><div class="yvsb870 _14uh9946i _14uh9947i"><div class="yvsb870 _1ox42gn1 _14uh99452 _14uh9945a"><span class="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy22 _1d0g9qk4 _1cshjhya"><span class="yvsb870 _14uh9946m _14uh99473 _14uh9947m _14uh99483 _14uh994p"><a href="/oauth/login?returnUrl=%2Fjobs-in-information-communication-technology%2Fin-All-Melbourne-VIC%3Fpage%3D2%26savejob%3D62256513%26sortmode%3DListedDate" rel="nofollow" title="Sign in to save this job" data-automation="signed-out-save-job" class="_1tmgvw5 _1tmgvw7 _1tmgvwa yvsb870 yvsb87f _14uh994h" target="_self"><div class="yvsb870 v8nw070 v8nw074"><div class="yvsb870 _14uh994fe _14uh99456 _14uh994ey _14uh994ei _14uh994ea v8nw0724"><div class="yvsb870 _14uh994r _14uh994de _14uh994ae _14uh9944u _14uh994ei"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" xml:space="preserve" focusable="false" fill="currentColor" width="16" height="16" class="yvsb870 _1cshjhy21 _14uh99452 _14uh9945a vnye0o0 vnye0o2 vnye0o3 vnye0o4" aria-hidden="true"><path d="M23 9c-.1-.4-.4-.6-.8-.7l-6.4-.9-2.9-5.8c-.3-.7-1.5-.7-1.8 0L8.2 7.3l-6.3 1c-.4 0-.7.3-.9.7-.1.4 0 .8.3 1l4.6 4.5-1.1 6.4c-.1.4.1.8.4 1 .2 0 .4.1.6.1.2 0 .3 0 .5-.1l5.7-3 5.7 3c.3.2.7.1 1.1-.1.3-.2.5-.6.4-1l-1.1-6.4 4.6-4.5c.3-.2.4-.6.3-.9zm-6.7 4.4c-.2.2-.3.6-.3.9l.8 4.9-4.4-2.3c-.3-.2-.6-.2-.9 0l-4.4 2.3.9-4.9c0-.3-.1-.7-.3-.9L4.1 10 9 9.3c.3 0 .6-.3.8-.5L12 4.3l2.2 4.4c.1.3.4.5.8.5l4.9.7-3.6 3.5z"></path></svg></div><div class="yvsb870 _14uh994r _14uh994de _14uh994ae _14uh9944u _14uh994ei"><span class="yvsb870">Save</span></div></div></div></a></span></span></div></div></div></div><div class="yvsb870 _14uh994r _14uh994fm x5kz590"><div class="yvsb870 _14uh994a2 _14uh994n _14uh9944u _14uh994ei x5kz591"><div class="yvsb870 _14uh994n _14uh9945a sofrzj3" data-testid="bx-logo-container"><div class="yvsb870 _14uh99456 _14uh994ea _14uh994n"><div class="yvsb870 _14uh994p _14uh994n _1cshjhy18 _1cshjhy1b _14uh99432 _14uh99435"><div class="yvsb870 _14uh99456 _14uh994n" data-testid="bx-logo-image"><img src="https://bx-branding-gateway.cloud.seek.com.au/9993b95a-feac-449e-a966-274411f2de03/serpLogo" alt="" class="_1cbgtdg0"></div></div></div></div></div></div></div></div></div></article>