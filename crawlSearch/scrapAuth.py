from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from parsel import Selector
import math
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import pymongo
from datetime import datetime
from time import sleep
import re

from selenium.webdriver.firefox.options import Options as FirefoxOptions

# aaa='robert a. weinberg'
# bbb='mit'
########################################################################
myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient["Fyp"]
authorCol = mydb["Authors"]
pubCol = mydb["Publications"]
###################################################################################

startSear = ''
startSearch = ''
authProfile = {'Name': '', 'urlLink': '', 'affiliation': '', 'researchInterest': [], 'totalPaper': '',
               'totalCitation': ''}
authList = []
url = ''
publications = []
publicatio = {
    'title': '',
    'year': '',
    'overview': '',
    'catogories': '',
    'author': '',
    'coAuthors': [{'name': 'profileUrl'}],
    'papaerLink': '',
    'abstract':'',
    'pdf':{}
}
urlss = ''
UrlsAuth = []
nameTo = ''
pubData=[]
dupCheck=False
check2=True
options = FirefoxOptions()
options.add_argument("--headless")

driver = webdriver.Firefox(executable_path=r'E:\\project\\Python\\FYP\\Test\\scrape\\geckodriver.exe')

newCoauthDriver = webdriver.Firefox(executable_path=r'E:\\project\\Python\\FYP\\Test\\scrape\\geckodriver.exe')


def closeBrowserInstances():
    driver.stop_client()
    driver.close()
    driver.quit()
    newCoauthDriver.stop_client()
    newCoauthDriver.close()
    newCoauthDriver.quit()


# 2

def singleAuthorCrawl(name):
    global dupCheck
    if authorCol.find({'Name': name}).count() < 1:
        dupCheck = False
        getAuthInfoLink(name)
    else:
        # TODO write this in the scrapProfile, see if the totalPapers are less than records in our db then delete the old ones and scrap new or scrap from the next those are left
        dupCheck = True
        for oldAuthor in authorCol.find({'urlLink': url}):
            oldAuthorId = oldAuthor['_id']
            if pubCol.find({'author': oldAuthorId}).count() < 1:
                getAuthInfoLink(name)


def authProfileGet(startSearch,name4):
    nameBol=False
    nameBoll=False
    name33=[]
    name=[]
    a = name4.lower()
    print(a)
    # print(startSearch)
    soup = BeautifulSoup(str(startSearch), 'html.parser')
    try:
        name = soup.find_all('a', {'class': 'au-target', 'aria-label': 'Name',
                                   'data-appinsights-title.bind': 'model.displayName',
                                   'data-appinsights-action': 'OpenAuthorDetails'})
        nameBol=True
    except AttributeError as e:
        name = []
        nameBol=False
        return None

    
    try:
        name2=soup.find_all('ma-entity-suggestion')
        nameBoll=True
        if(nameBoll):
            for kk in name2:
                name33.append(kk.find('a', {'class': 'name au-target', 'aria-label': 'Name','data-appinsights-action': 'SimilarAuthor'}))
    except AttributeError:
        nameBoll=False
        name33=[]
    print(name33)
    name.extend(name33)

    if((nameBol or nameBoll) and len(name)>=1):
        for names in name:
            print(names)
            if(names!=None):
                tx=re.search(".*"+str(a)+".*",names.get_text().strip().lower())
                ttt=True
                if (ttt):
                    href = names.attrs['href']
                    url = 'https://academic.microsoft.com/' + href
                    # authProfile['Name'] = names.get_text().strip()
                    # authList.append(authProfile)
                    # print(url)
                    global dupCheck
                    if authorCol.find({'urlLink': url}).count() < 1:
                        dupCheck = False
                        scrapProfile(url)
                        UrlsAuth.append(url)
                    else:
                        # TODO write this in the scrapProfile, see if the totalPapers are less than records in our db then delete the old ones and scrap new or scrap from the next those are left              
                        dupCheck = True
                        for oldAuthor in authorCol.find({'urlLink': url}):
                            oldAuthorId = oldAuthor['_id']
                            if pubCol.find({'author': oldAuthorId}).count() < 1:
                                scrapProfile(url)
                                UrlsAuth.append(url)
    nameBol=False
    nameBoll=False
        
    print(UrlsAuth)
    print(len(UrlsAuth))


# *********
def getAuthInfoLink(name):
    global startSearc
    global nameTo
    invalid1=True
    nameTo = name
    query = name
    newUrl = urllib.parse.quote(query)
    url = 'https://academic.microsoft.com/search?q=' + newUrl + '&f=&orderBy=0&skip=0&take=10'
    count = 0
    while True:
        count += 1
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Staring time of getting author Info =", current_time)

            driver.get(url)
            wait = True
            ccc = 0
            while wait:
                ccc +=1
                try:
                    if driver.page_source != '':
                        sleep(4)
                        startSear = driver.page_source
                        wait = False
                except InvalidArgumentException:
                    if ccc >= 10:
                        print('invalid')
                        break
                    else:
                        continue
                else:
                    break

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Ending time of getting author Info =", current_time)

            
            invalid1=True
        except TimeoutException as ex:
            print('internet is slow, error occured in searching author, trying again')
            print(ex)
            continue
        except InvalidArgumentException:
            if count >= 10:
                invalid1=False
                print('invalid')
                break
            else:
                continue
        else:
            invalid1=True
            print("successfull in searching author")
            break
    # 3 execute method
    if(invalid1):
        authProfileGet(startSear,name)


# 1
# startSearch = startSearc


# # # method to open urlProfile page + or any profile page , etc publications , user profile
def completeProfileSouceUrl(linkk):
    while True:
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Staring time of getting profile source =", current_time)

            driver.get(linkk)
            wait = True
            ccc = 0
            while wait:
                ccc +=1
                try:
                    if driver.page_source != '':
                        wait = False
                except InvalidArgumentException:
                    if ccc >= 10:
                        print('invalid')
                        break
                    else:
                        continue
                else:
                    break

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Ending time of getting profile source =", current_time)

            sleep(4)
            return driver.page_source
        except TimeoutException as ex:
            print('internet is slow, error occured in getting profile url, trying again')
            print(ex)
            continue
        else:
            print("successfull in crawling to author's profile")
            break


# getting coauthers method called below
def getCoauthInfo(tileLi, namee):
    global check2
    soursou = ''
    count2 = 0
    invalid2 = True
    while True:
        count2 += 1
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Staring time of getting coauthor Info =", current_time)

            newCoauthDriver.get(tileLi)
            wait = True
            ccc = 0
            while wait:
                ccc +=1
                try:
                    if newCoauthDriver.page_source != '':
                        wait = False
                except InvalidArgumentException:
                    if ccc >= 10:
                        print('invalid')
                        break
                    else:
                        continue
                else:
                    break

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Ending time of getting coauthor Info =", current_time)
            invalid2 = True
            sleep(4)
            # soursou = newCoauthDriver.page_source
        except TimeoutException as ex:
            print('internet is slow, error occured in searching publication, trying again')
            print(ex)
            continue
        except InvalidArgumentException:
            if count >= 10:
                invalid2=False
                print('invalid')
                break
            else:
                continue
        else:
            print("successfull in searching publication")
            invalid2 = True
            break
    coauthors = []
    catList=[]
    abstract=''

    if(invalid2):
        ddd = {'name': '', 'linkUrl': ''}
        try:
            staleCounter = 0
            while True:
                staleCounter += 1
                try:
                    # newCoauthDriver.find_element_by_xpath('//*[@au-target-id="215"]')
                    moreButton = newCoauthDriver.find_element_by_xpath('//*[@class="au-target show-more"]')

                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print("Staring time of getting more button data of coauthor =", current_time)

                    moreButton.click()
                    wait = True
                    ccc2 = 0
                    while wait:
                        ccc2 +=1
                        try:
                            if newCoauthDriver.page_source != '':
                                wait = False
                        except InvalidArgumentException:
                            if ccc2 >= 10:
                                print('invalid')
                                break
                            else:
                                continue
                        else:
                            break
                        

                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print("Ending time of getting more button data of coauthor =", current_time)

                    sleep(3)
                except NoSuchElementException:
                    print('retrying to click "see more button"')
                    if staleCounter >= 5:
                        break
                    else:
                        continue
                except StaleElementReferenceException :
                    print('StaleElementReferenceException on click "see more" button')
                    if staleCounter >= 5:
                        check2=False
                        break
                    else:
                        continue
                else:
                    break
            if(check2):
                while True:
                    try:
                        # soursou = newCoauthDriver.page_source

                        while True:
                            try:
                                spanss = newCoauthDriver.find_element_by_xpath(
                                    '/html/body/div[2]/div/div/router-view/compose[1]/div/div/ma-entity-detail-info/compose/div/div/div[1]/ma-author-string-collection')
                            except NoSuchElementException:
                                try:
                                    spanss = newCoauthDriver.find_element_by_xpath(
                                        '/html/body/div/div/div/router-view/compose[1]/div/div/ma-entity-detail-info/compose/div/div/div[1]/ma-author-string-collection')
                                except NoSuchElementException:
                                    continue
                                else:
                                    break
                            else:
                                break

                        span = spanss.find_elements_by_tag_name('span')
                        # soup = BeautifulSoup(str(soursou), 'html.parser')
                        # span = soup.find_all('span', {'class': 'author-item au-target', 'show.bind': 'author.displayName'})
                        # target = span.find_next()
                        for coauth in span:
                            llll = coauth.find_element_by_tag_name('a')

                            if llll.text.strip() != namee:
                                ddd['name'] = llll.text.strip()
                                ddd['linkUrl'] = llll.get_attribute('href')
                                coauthors.append(ddd.copy())
                    except StaleElementReferenceException :
                        print('StaleElementReferenceException on click "see more" button')
                        continue
                    else:
                        break

        except NoSuchElementException:
            print('can not find "show more" button.')
        except ElementClickInterceptedException:
            print('"show more" button is not clickable or can not find it.')
# ====================================282
    
    
        if(check2):
            while True:
                try:
                    try:
                        abstract=newCoauthDriver.find_element_by_xpath('/html/body/div[2]/div/div/router-view/compose[1]/div/div/ma-entity-detail-info/compose/div/div/div[1]/p').text.strip()
                    except NoSuchElementException:
                        try:
                            abstract=newCoauthDriver.find_element_by_xpath('/html/body/div/div/div/router-view/compose[1]/div/div/ma-entity-detail-info/compose/div/div/div[1]/p').text.strip()
                        except NoSuchElementException:
                            try:
                                abstract=newCoauthDriver.find_element_by_xpath('/html/body/div[1]/div/div/router-view/compose[1]/div/div/ma-entity-detail-info/compose/div/div/div[1]/p').text.strip()
                            except NoSuchElementException:
                                abstract=''
                        

                    
                    try:
                        catogory=newCoauthDriver.find_element_by_xpath('/html/body/div[2]/div/div/router-view/compose[1]/div/div/ma-entity-detail-info/compose/div/div/div[1]/ma-tag-cloud/div')
                    except NoSuchElementException:
                        try:
                            catogory=newCoauthDriver.find_element_by_xpath('/html/body/div/div/div/router-view/compose[1]/div/div/ma-entity-detail-info/compose/div/div/div[1]/ma-tag-cloud/div')
                        except NoSuchElementException:
                            try:
                                catogory=newCoauthDriver.find_element_by_xpath('/html/body/div[1]/div/div/router-view/compose[1]/div/div/ma-entity-detail-info/compose/div/div/div[1]/ma-tag-cloud/div')
                            except NoSuchElementException:
                                catogory='not found'
                    if(catogory!='not found'):
                        for cato in catogory.find_elements_by_tag_name('ma-link-tag'):
                            catList.append(cato.text.strip())
                    else:
                        catList=[]
                except StaleElementReferenceException :
                    print('StaleElementReferenceException on click "see more" button')
                    continue
                else:
                    break
                    
    a=0
    
    pubData1=[]
    
    
    pubData1.append(catList)
    pubData1.append(abstract)
    
    pubData1.append(coauthors)

    print(pubData1)
    check2=True
    return pubData1


#
#
# # scrap complete profile + publication result with coauthors detail
def scrapProfile(lliik):
    soursoup = completeProfileSouceUrl(lliik)
    soursou = soursoup
    soup = BeautifulSoup(str(soursou), 'html.parser')

    urlLink = lliik
    researchInterest = []
    try:
        name = soup.find('div', {'class': 'name-section'}).find('div', {'class': 'name'}).get_text().strip()
    except AttributeError as e:
        print('Crawling stoped due to network problem')
    try:
        affiliation = soup.find('a',
                                {'class': 'au-target', 'data-appinsights-action': 'Institution'}).get_text().strip()
    except AttributeError as e:
        affiliation = ''
    research = soup.find_all('span',
                             {'class': 'au-target ma-topic-filter-item-text', 'click.trigger': 'toggleSelect()'})

    for klkl in research:
        klkl.span.decompose()
        researchInterest.append(klkl.get_text().strip())
    # print(researchInterest)
    total = soup.find_all('div', {'class': 'count'})
    totalPaper = total[0].get_text().strip()
    totalCitation = total[1].get_text().strip()

    authProfile['urlLink'] = urlLink
    authProfile['Name'] = name
    authProfile['affiliation'] = affiliation
    authProfile['researchInterest'] = researchInterest
    authProfile['totalPaper'] = totalPaper
    # authProfile['totalCoAuthor'] = totalCoAuthor
    authProfile['totalCitation'] = totalCitation

    # ####################################################
    global dupCheck
    if dupCheck:
        x = authorCol.find_and_modify({'urlLink': authProfile['urlLink']}, authProfile.copy())
        print(x)
        objId = x['_id']
    else:
        x = authorCol.insert_one(authProfile.copy())
        objId = x.inserted_id
    ######################################################
    dupCheck=False
    authList.append(authProfile)
    print(authList)
    #     publication extract
    # passl = 0
    bb = ''.join(i for i in totalPaper if i.isdigit())
    a = int(bb) / 10
    loops = math.ceil(a)
    for i in range(loops):
        # passl += 1
        # if passl > 5:
        soups = BeautifulSoup(str(soursou), 'html.parser')
        paper = soups.find_all('div', {'class': 'paper'})
        for pap in paper:
            tit = pap.find('a', {'class': 'title au-target', 'aria-label': 'Publication name',
                                 'data-appinsights-action': 'OpenPaperDetails'})
            date = pap.find('span', {'class': 'year', 'aria-label': 'Published date'})
            print(tit)
            tileLi = "https://academic.microsoft.com/" + tit.attrs['href']

            overview = date.find_next()
            cocottog = []
            # catogry = pap.find_all('a', {'class': 'ma-tag au-target',
            #                              'data-appinsights-action': 'OpenLink'})
            # for hyj in catogry:
            #     cocottog.append(hyj.find('div', {'class': 'text'}).get_text().strip())
            # ####coaauthors
            # print(cocottog)
            coauthList = getCoauthInfo(tileLi, name)

            cocottog=coauthList[0]
            abstractw=coauthList[1]
            
            coatherr=coauthList[2]
            # print(coauthList)
            ####################################################

            #         for yft in coauthhh:
            #             coauth['name']=yft.get_text().strip()
            #             coauth['linkurl']=yft.attrs['href']
            #             coauthList.append(coauth)

            publicatio['title'] = tit.get_text().strip()
            publicatio['year'] = date.get_text().strip()
            publicatio['overview'] = overview.get_text().strip()
            publicatio['catogories'] = cocottog
            publicatio['author'] = objId
            publicatio['abstract'] = abstractw
            # publicatio['author'] = 'ObjectId("5cd9f220126dc5ff3984fc44")'
            publicatio['papaerLink'] = tileLi
            publicatio['abstract'] = abstractw
            ##saving coauthors pdf
            publicatio['coAuthors'] = coatherr
            
            print(publicatio)
            ########saving publications

            ###########################################################
            pubCol.insert_one(publicatio.copy())
            ###############################################################
            publications.append(publicatio.copy())

        but=False
        while True:
            try:
                nextButton = driver.find_element_by_xpath('//*[@aria-label="Next page"]')
                but=True
            except NoSuchElementException:
                but=False
                break
            except StaleElementReferenceException :
                but=False
                print('StaleElementReferenceException on click "see more" button')
                continue
            else:
                break

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Staring time of getting next button data =", current_time)
        if(but):
            nextButton.click()
            but=False

        wait = True
        ccc = 0
        while wait:
            ccc +=1
            try:
                if driver.page_source != '':
                    sleep(3)
                    soursou = driver.page_source
                    wait = False
            except InvalidArgumentException:
                if ccc >= 10:
                    print('invalid')
                    break
                else:
                    continue
            else:
                break

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Ending time of getting next button data =", current_time)

        

        #######authgors
    


# print authors url
print(UrlsAuth)
# printing authors profile
print(authList)
# printing publications
print(publications)