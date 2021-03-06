from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
import requests
from courses_list import course
from openpyxl import load_workbook,Workbook


def simple_link(url):                                                                           #non javascript
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url,headers=headers)
    html = BeautifulSoup(page.content, 'html.parser')
    return html

def javascript_link(url):                                                                       #if Page is having javascript
    op = webdriver.FirefoxOptions()
    op.add_argument("--headless")
    driver = webdriver.Firefox(options=op)
    driver.get(url)
    html = BeautifulSoup(driver.page_source,'html.parser')
    driver.quit()
    return html

def category(html_page):
    count=0
    baseUrl = 'https://www.manchester.ac.uk/study/undergraduate/courses/2021/'
    backUrl = 'course-details/#course-profile'
    body = html_page.find('body')
    div = body.find('div',class_='pageWrapper').find('article').find('div',class_='row tripleVertPadding').find('div',class_='oneColLayoutContainer').find('div',class_='mainContentContainer')

    div = div.find('div',id='course-list').find('ul').find_all('li')

    for i in div:
        count+=1
        cc = i.find('div',class_='title').find('a').text
        link = baseUrl + i.find('div',class_='title').find('a').attrs['href'] + backUrl
        print(count.__str__() + " " + cc + " " + link)
        inside_course(count,cc,link)

        #print(course)

def inside_course(count,cc,link):
    year = "Year "
    c=0
    page = simple_link(link)
    body = page.find('body')
    div = body.find('div',class_='pageWrapper').find('article').find('div',class_='row tripleVertPadding').find('div',class_='oneColLayoutContainer').find('div',class_='mainContentContainer')
    div = div.find('div',class_='corporate').find('div',class_='course-profile-content')

    table = div.find_all('table')

    for i in table:
        c+=1
        year = year + c.__str__()
        #print(year)
        tr = i.find('tbody').find_all('tr')
        for j in tr:
            subject = j.find('td').text
            clist.append(course(count, cc, link, year, subject))
            #print(subject)

        year = year[0:4]
        print('\n')

if __name__ == '__main__':
    clist = []
    url = 'https://www.manchester.ac.uk/study/undergraduate/courses/2021/'
    html_page = javascript_link(url)

    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\manchaster.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)
