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
    baseUrl = 'https://www.dundee.ac.uk'
    endUrl = '/teaching-and-assessment'
    body = html_page.find('body')
    div = body.find('div',class_='page__content').find('div',class_='panel').find('div',class_='filterable-lists').find_all('div',class_='filterable-list')
    count=0
    for i in div:
        #try:
        li = i.find('nav').find('ul').find_all('li')
        for j in li:
            count+=1
            link = baseUrl + j.find('a').attrs['href']+endUrl
            course_name = j.find('a').text
            print(count.__str__() + " " + course_name + " " + link)
            inside_module(count,course_name,link)
        #except:
            #continue

def inside_module(count,course_name,link):
    page = simple_link(link)
    body = page.find('body')
    div = body.find('section',class_='tabs')
    try:
        yc = div.find('ul').find_all('li')
        modules = div.find_all('div',class_='tabs__content')
        for i in range(0,len(yc)):
            year = yc[i].text
            print(year)
            div_tag = modules[i].find_all('div',class_='accordion__section')

            for j in div_tag:
                d = j.find('div',class_='accordion__header').find('h2').find('span',class_='accordion__button-title')
                subject = d.text
                print(' ' + subject)
                clist.append(course(count, course_name, link, year, subject))
    except:
        try:
            divv = body.find('article', class_='page__course_subpage course').find('div', class_='page__content').find(
                'div', class_='wysiwyg').find('p')
            year = "Year - "
            print(year)
            subject = divv.text
            print(' ' + subject)
            clist.append(course(count, course_name, link, year, subject))

        except:
            year = "Null"
            print(year)
            subject = "Null"
            print(' ' + subject)
            clist.append(course(count, course_name, link, year, subject))



if __name__ == '__main__':
    clist = []
    url = 'https://www.dundee.ac.uk/undergraduate/courses'
    html_page = simple_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\dundee.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)