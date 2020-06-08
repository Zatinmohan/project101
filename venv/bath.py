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
    llist = []
    baseUrl = 'https://www.bath.ac.uk'
    div = html_page.find('main',class_='corporate-information').find('section',class_='main-content').find_all('h1')
    for i in div:
        link = baseUrl + i.find('a').attrs['href']
        #course_name = i.find('a').text
        print(link)
        llist.append(link)
    inside_category(llist)

def inside_category(llist):
    baseUrl = 'https://www.bath.ac.uk'
    count = 0
    for i in llist:
        page = simple_link(i)
        div = page.find('div',class_='flex-wrapper pinned-items text-only action-list black').find_all('div',class_='card standard-card single-item')

        for j in div:
            li = j.find('ul').find_all('li')

            for k in li:
                count+=1
                link = baseUrl + k.find('a').attrs['href']
                course_name = k.find('a').text
                print(count.__str__() + " " + course_name + " " + link)
                inside_course(count,course_name,link)


def inside_course(count,course_name,link):
    page = simple_link(link)
    div = page.find('div',class_='flex-wrapper pinned-items text-only action-list').find_all('div',class_='card standard-card single-item')

    for i in div:
        try:
            year = i.find('header').text
            print(year)
            li = i.find('ul').find_all('li')
            for j in li:
                subject = j.text
                print(' ' + subject)
                clist.append(course(count, course_name, link, year, subject))
        except:
            p = i.find('p')
            subject = p.text
            print(' ' + subject)
            clist.append(course(count, course_name, link, year, subject))

if __name__ == '__main__':
    clist = []
    url = 'https://www.bath.ac.uk/corporate-information/undergraduate-subjects-2021/'
    html_page = simple_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\bath.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)