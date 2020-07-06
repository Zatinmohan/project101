from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
import requests
import time
from courses_list import course
from openpyxl import load_workbook,Workbook

def simple_link(url):                                                                           #non javascript
    while(True):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            page = requests.get(url,headers=headers)
            html = BeautifulSoup(page.content, 'html.parser')
            return html
        except:
            print("Page is busy.. wait for few seconds")
            time.sleep(5)
            continue

def javascript_link(url):                                                                       #if Page is having javascript
    op = webdriver.FirefoxOptions()
    op.add_argument("--headless")
    driver = webdriver.Firefox(options=op)
    driver.get(url)
    html = BeautifulSoup(driver.page_source,'html.parser')
    driver.quit()
    return html

Cou = 0

def category(html_page):
    baseUrl = 'https://www.gla.ac.uk'
    body = html_page.find('body')
    div = body.find('div',class_='row').find('div',id='main').find('div',class_='row').find('div',class_='maincontent').find_all('li')
    for i in div:
        llist.append(baseUrl + i.find('a').attrs['href'])
        c_name = i.find('a').text
        print(c_name + " " + baseUrl + i.find('a').attrs['href'])
    sub_category(llist)

def postCategory(html_page):
    baseUrl = 'https://www.gla.ac.uk'
    body = html_page.find('body')
    div = body.find('div', class_='row').find('div', id='main').find('div', class_='row').find('div',
                                                                                               class_='maincontent').find_all(
        'li')
    for i in div:
        link = baseUrl + i.find('a').attrs['href']
        c_name = i.find('a').text
        print(c_name + " " + baseUrl + i.find('a').attrs['href'])
        inside_post(c_name,link)

def inside_post(course_name,link):
    page = simple_link(link)
    body = page.find('body')
    global Cou
    try:
        div = body.find('div',class_='program-courses tab').find_all('section',class_='row')
        for i in div:
            Cou+=1
            year = i.find('h5').text
            print(year)
            li = i.find('ul').find_all('li')

            for j in li:
                subject = j.find('header').find('span',class_='name').text
                clist.append(course(Cou, course_name, link, year, subject))
                print(' ' + subject)
    except:
        try:
            div = body.find('div',class_='maincontent columns content tab-content eight large-12 medium-12').find_all('ul')
        except:
            div = body.find('div',class_='content_opener').find_all('ul')

        year = " - "
        print(year)
        for i in div:
            li = i.find_all('li')
            for j in li:
                subject = j.text
                print(' ' + subject)
                clist.append(course(Cou, course_name, link, year, subject))

    print('\n')


def sub_category(llist):
    baseUrl = 'https://www.gla.ac.uk'
    count=0
    for i in llist:
        count += 1
        page = simple_link(i)
        body = page.find('body')
        print(count.__str__() + " " + i)
        div = body.find('div', class_='row').find('div', id='main').find('div', class_='row').find('div',
                                                                                                   id='main-content-wrapper').find(
            'ul').find_all('li')

        for x in div:
            t = x.find('a').attrs['href']
            if(t.find('undergraduate')>=0):
                l = t
                break

        if(l.find('https')>=0 or l.find('http')>=0):
            print(l)
        else:
            #l = baseUrl + div.find('a').attrs['href']
            l = baseUrl + l
            print(l)

        inside_category(l)

def inside_category(link):
    baseUrl = 'https://www.gla.ac.uk'
    page = simple_link(link)
    body = page.find('body')
    global Cou
    try:
        div = body.find('div',class_='row').find('div',id='main').find('div',class_='row').find('div',id='main-content-wrapper').find('div').find('ul')
        li  = div.find_all('li')
        for i in li:
            course_name = i.find('a').text
            link = i.find('a').attrs['href']

            if(link.find('http')>=0 or link.find('https')>=0):
                print(course_name + " " + link)

            else:
                link = baseUrl + i.find('a').attrs['href']
                print(course_name + " " + link)

            inside_course(course_name,link)
        print('\n')

    except:
        try:
            course_name = body.find('div', id='prog-title').find('h1').text
            print(course_name)
            Cou+=1
            h3 = body.find_all('h3')
            for i in range(len(h3)):
                year = h3[i].text
                subject = h3[i].find_next('p').text
                print(year)
                print(' ' + subject)
                clist.append(course(Cou, course_name, link, year, subject))
        except:
            Cou+=1
            print("Nothing...")
            clist.append(course(Cou, "Null", link, "Null", "Null"))

def inside_course(course_name,link):
    global Cou
    page = simple_link(link)
    body = page.find('body')
    div = body.find('div',class_='row').find('div',id='main').find('div',class_='row').find('div',class_='maincontent columns content tab-content eight large-12 medium-12')
    try:
        h3 = div.find_all('h3')
        Cou+=1
        for i in range(len(h3)):
            year = h3[i].text
            subject = h3[i].find_next('p').text
            clist.append(course(Cou, course_name, link, year, subject))
            print(year + '\n' + subject)
    except:
        Cou+=1
        print("Problem with this link...")
        clist.append(course(Cou, course_name, link, "Null", "Null"))
    print('\n')

if __name__ == '__main__':
    clist=[]
    llist = []
    url = 'https://www.gla.ac.uk/subjects/?display=all'
    html_page = simple_link(url)
    category(html_page)

    url = 'https://www.gla.ac.uk/postgraduate/taught/'
    html_page = simple_link(url)
    postCategory(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\glassgow.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)