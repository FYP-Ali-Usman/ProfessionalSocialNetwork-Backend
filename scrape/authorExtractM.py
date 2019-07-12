from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from parsel import Selector
import math
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import pymongo

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
               'totalCoAuthor': '', 'totalCitation': ''}
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
    'papaerLink': ''
}
urlss = ''
UrlsAuth = []
nameTo = ''
options=FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options,executable_path=r'D:\\Projects\\Python\\FYP\\Test\\scrape\\geckodriver.exe')


newCoauthDriver = webdriver.Firefox(options=options, executable_path=r'D:\\Projects\\Python\\FYP\\Test\\scrape\\geckodriver.exe')

# 2
def authProfileGet(startSearch):
    a = nameTo.lower()
    print(a)
    soup = BeautifulSoup(str(startSearch), 'html.parser')
    try:
        name = soup.find_all('a', {'class': 'au-target', 'aria-label': 'Name',
                                   'data-appinsights-title.bind': 'model.displayName',
                                   'data-appinsights-action': 'OpenAuthorDetails'})

    except AttributeError as e:
        name = []
        return None
    for names in name:
        # print(names.get_text().strip().lower())
        if a == names.get_text().strip().lower():
            href = names.attrs['href']
            url = 'https://academic.microsoft.com/' + href
            # authProfile['Name'] = names.get_text().strip()
            # authList.append(authProfile)
            # print(url)
            scrapProfile(url)
            UrlsAuth.append(url)
    print(UrlsAuth)
    print(len(UrlsAuth))


def getAuthInfoLink(name, university):
    global startSearc
    global nameTo
    nameTo = name
    query = name + ' ' + university
    newUrl = urllib.parse.quote(query)
    url = 'https://academic.microsoft.com/search?q=' + newUrl + '&f=&orderBy=0&skip=0&take=10'
    while True:
        try:
            driver.get(url)
            sleep(5)
            # print(driver.page_source)
            startSear = driver.page_source
        except TimeoutException as ex:
            print('internet is slow, error occured in searching author, trying again')
            print(ex)
            continue
        else:
            print("successfull in searching author")
            break
    # 3 execute method
    authProfileGet(startSear)


# 1
# startSearch = startSearc


# # # method to open urlProfile page + or any profile page , etc publications , user profile
def completeProfileSouceUrl(linkk):
    while True:
        try:
            driver.get(linkk)
            sleep(10)
            # print(driver.page_source)
            return driver.page_source
        except TimeoutException as ex:
            print('internet is slow, error occured in getting profile url, trying again')
            print(ex)
            continue
        else:
            print("successfull in crawling to author's profile")
            break


# getting coauthers method called below
def getCoauthInfo(tileLi, name):
    soursou = ''

    while True:
        try:
            newCoauthDriver.get(tileLi)
            sleep(8)
            soursou = newCoauthDriver.page_source
        except TimeoutException as ex:
            print('internet is slow, error occured in searching publication, trying again')
            print(ex)
            continue
        else:
            print("successfull in searching publication")
            break

    coauthors = []
    ddd = {'name': '', 'linkUrl': ''}
    try:
        staleCounter = 0
        while True:
            staleCounter += 1
            if staleCounter <= 5:
                break
            try:
                # newCoauthDriver.find_element_by_xpath('//*[@au-target-id="215"]')
                moreButton = newCoauthDriver.find_element_by_xpath('//*[@class="au-target show-more"]')
                moreButton.click()
                sleep(10)
            except StaleElementReferenceException:
                print('retrying to click "see more button"')
            else:
                break

        soursou = newCoauthDriver.page_source
        spanss = newCoauthDriver.find_element_by_xpath(
            '/html/body/div/div/div/router-view/compose[1]/ma-edp/div/div/ma-entity-detail-info/compose/div/div/div[1]/ma-author-string-collection')
        span = spanss.find_elements_by_tag_name('span')
        # soup = BeautifulSoup(str(soursou), 'html.parser')
        # span = soup.find_all('span', {'class': 'author-item au-target', 'show.bind': 'author.displayName'})
        # target = span.find_next()
        for coauth in span:
            llll = coauth.find_element_by_tag_name('a')

            if llll.text.strip() != name:
                ddd['name'] = llll.text.strip()
                ddd['linkUrl'] = llll.get_attribute('href')
            coauthors.append(ddd.copy())

    except NoSuchElementException:
        print('can not find "show more" button.')
    except ElementClickInterceptedException:
        print('"show more" button is not clickable or can not find it.')


    # print(coauthors)
    return coauthors


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
    totalCoAuthor = total[1].get_text().strip()
    totalCitation = total[2].get_text().strip()

    authProfile['urlLink'] = urlLink
    authProfile['Name'] = name
    authProfile['affiliation'] = affiliation
    authProfile['researchInterest'] = researchInterest
    authProfile['totalPaper'] = totalPaper
    authProfile['totalCoAuthor'] = totalCoAuthor
    authProfile['totalCitation'] = totalCitation

    # ####################################################
    x = authorCol.insert_one(authProfile.copy())
    objId = x.inserted_id
    ######################################################

    authList.append(authProfile)
    print(authList)
    #     publication extract
    # passl = 0
    a = int(totalPaper) / 10
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
            catogry = pap.find_all('a', {'class': 'ma-tag au-target',
                                         'data-appinsights-action': 'OpenLink'})
            for hyj in catogry:
                cocottog.append(hyj.find('div', {'class': 'text'}).get_text().strip())
            ####coaauthors
            # print(cocottog)
            coauthList = getCoauthInfo(tileLi, name)
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
            # publicatio['author'] = 'ObjectId("5cd9f220126dc5ff3984fc44")'
            publicatio['papaerLink'] = tileLi

            ##saving coauthors
            publicatio['coAuthors'] = coauthList
            print(publicatio)
            ########saving publications

            ###########################################################
            pubCol.insert_one(publicatio.copy())
            ###############################################################
            publications.append(publicatio.copy())

        try:
            nextButton = driver.find_element_by_xpath('//*[@aria-label="Next page"]')
        except NoSuchElementException:
            return None
        nextButton.click()
        sleep(15)
        soursou = driver.page_source

        #######authgors


# print authors url
print(UrlsAuth)
# printing authors profile
print(authList)
# printing publications
print(publications)