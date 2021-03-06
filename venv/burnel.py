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

def category():
    count=0
    for i in llink:
        page = javascript_link(i)
        body = page.find('body')
        print(body)
        break

if __name__ == '__main__':
    llink = []
    nlist = []
    baseUrl = 'https://www.brunel.ac.uk'
    backUrl = '?page='
    url = 'https://www.brunel.ac.uk/study/Course-listing'
    p=1
    count = 0
    while(p<=27):
        u = url + backUrl + p.__str__()
        html_page = simple_link(u)
        body = html_page.find('body')
        tr = body.find('table',id='responsive-example-table').find('tbody').find_all('tr')
        for i in tr:
            count+=1
            link = baseUrl + i.find('td').find('a').attrs['href']
            course_name = i.find('td').find('a').text
            llink.append(link)
            print(count.__str__() + " " + course_name + " " + link)
        p += 1

    category()
