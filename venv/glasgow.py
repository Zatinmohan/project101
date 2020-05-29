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

def category(html_page):
    baseUrl = 'https://www.gla.ac.uk'
    body = html_page.find('body')
    div = body.find('div',class_='row').find('div',id='main').find('div',class_='row').find('div',class_='maincontent').find_all('li')
    link=[]
    for i in div:
        link.append(baseUrl + i.find('a').attrs['href'])
        course = i.find('a').text
        #print(link)
    sub_category(link)

def sub_category(link):
    baseUrl = 'https://www.gla.ac.uk'
    count=0
    for i in link:
        count += 1
        if(count!=2):
            page = simple_link(i)
            body = page.find('body')
            if(count==3):
                div = body.find('div',class_='row').find('div',id='main').find('div',class_='row').find('div',id='main-content-wrapper').find('ul').find_all('li')[1]
            else:
                div = body.find('div', class_='row').find('div', id='main').find('div', class_='row').find('div',
                                                                                                           id='main-content-wrapper').find(
                    'ul').find_all('li')[0]

            l = baseUrl + div.find('a').attrs['href']
            print(l)
            #print(l)
            inside_category(l)

def inside_category(link):
    baseUrl = 'https://www.gla.ac.uk'
    page = simple_link(link)
    body = page.find('body')
    div = body.find('div',class_='row').find('div',id='main').find('div',class_='row').find('div',id='main-content-wrapper').find('div').find('ul')
    li  = div.find_all('li')
    for i in li:
        course = i.find('a').text
        link = baseUrl + i.find('a').attrs['href']
        print(course + " " + link)
        inside_course(course,link)
    print('\n')

def inside_course(course,link):
    page = simple_link(link)
    body = page.find('body')
    div = body.find('div',class_='row').find('div',id='main').find('div',class_='row').find('div',class_='maincontent columns content tab-content eight large-12 medium-12')
    h3 = div.find_all('h3')
    for i in range(len(h3)):
        year = h3[i].text
        subject = h3[i].find_next('p').text

        print(year + '\n' + subject)
    print('\n')

if __name__ == '__main__':
    url = 'https://www.gla.ac.uk/subjects/?display=all'
    html_page = simple_link(url)
    category(html_page)

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