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

if __name__ == '__main__':
    nlist = []
    llist = []
    p=1
    url = 'https://www.city.ac.uk/study/courses'
    backUrl = '?p='

    while(p<641):
        purl = url + backUrl +p.__str__()
        html_page = javascript_link(purl)

        body = html_page.find('body')
        div = body.find('div', class_='course-finder__results')

        short = div.find_all('div', class_='course-finder__results__item course-finder__results__item--short-courses')
        cpd = div.find_all('div', class_='course-finder__results__item course-finder__results__item--cpd')
        pg = div.find_all('div', class_='course-finder__results__item course-finder__results__item--postgraduate')
        ug = div.find_all('div', class_='course-finder__results__item course-finder__results__item--undergraduate')
        fo = div.find_all('div', class_='course-finder__results__item course-finder__results__item--foundation')
        red = div.find_all('div', class_='course-finder__results__item course-finder__results__item--research-degrees')
        exe = div.find_all('div', class_='course-finder__results__item course-finder__results__item--executive-education')

        for i in short:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        for i in cpd:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        for i in pg:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        for i in ug:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        for i in fo:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        for i in exe:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            llist.append(course_name)

        for i in red:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        p+=10

    count=1
    for i in llist:
        print(count.__str__() + " " + i)
        count+=1
