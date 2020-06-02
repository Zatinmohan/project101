from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
import requests
from time import sleep
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
            print("Website busy... wait ")
            sleep(5)
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
    #body = html_page.find('body')
    #div = body.find('article').find('ul',class_='search-result-list')
    li = html_page.find('ul', class_='search-result-list').find_all('li',class_='search-result-list__item')

    for i in li:
        course_name = i.find('h4').find('a').text
        link = i.find('h4').find('a').attrs['href']
        nlist.append(course_name)
        llist.append(link)

def category(html_page):
    body = html_page.find('body')
    div = body.find('main').find('div',class_='container').find('div',class_='col-md-9 col-lg-6').find_all('table')
    count=0
    for i in div:
        tr = i.find('tbody').find_all('tr')
        for j in tr:
            count+=1
            course_name = j.find('a').text
            link = j.find('a').attrs['href']
            print(count.__str__() + " " + course_name + " " + link)
            inside_course(count,course_name,link)

def inside_course(count,course_name,link):
    page = javascript_link(link)
    body = page.find('body')
    try:
        div = body.find('main').find('div', class_='content-toggle').find('div', class_='col-md-10 offset-md-1').find_all('div',class_='accordion')
    except:
        div = body.find('main').find('div',class_='content-toggle').find('div',class_='col-md-8').find_all('div',class_='accordion')

    for i in div:
        try:
            tr = i.find('table',class_='table').find('tbody').find_all('tr')
            year = i.find_previous('h3').text
            print(year)
            for j in tr:
                subject = j.find('td').find('a').text
                clist.append(course(count, course_name, link, year, subject))
                print(' ' + subject)
        except:
            try:
                d_tag = body.find('main').find('div', class_='content-toggle').find('div', class_='col-md-10 offset-md-1')
                h3 = d_tag.find_all('h3')
            except:
                d_tag = body.find('main').find('div', class_='content-toggle').find('div',class_='col-md-8')
                h3 = d_tag.find_all('h3')

            for j in h3:
                year = j.text
                print(year)
                subject = j.find_next('p').find_next('p').text
                clist.append(course(count, course_name, link, year, subject))
                print(subject)
            break
        print('\n')

if __name__ == '__main__':
    clist = []
    url = 'https://www.cardiff.ac.uk/study/undergraduate/courses/a-to-z'
    html_page = simple_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\cardiff.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)