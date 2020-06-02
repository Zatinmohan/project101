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
    baseUrl = 'https://www.southampton.ac.uk'
    endUrl = '#course-structure'
    body = html_page.find('body')
    div = body.find('div',class_='courses-results w-full pb-2').find('ul').find_all('li')

    for i in div:
        count+=1
        course_name = i.find('a').text
        link = baseUrl + i.find('a').attrs['href'] + endUrl
        print(count.__str__() + " " + course_name + " " + link)
        inside_course(count,course_name,link)

def inside_course(count,course_name,link):
    page = javascript_link(link)
    body = page.find('body')
    div = body.find('main').find('div',class_='container mx-auto px-4 pb-12 min-h-screen').find('div',class_='lg:flex').find('article').find('section',class_='block')
    div = div.find_all('section')

    for i in div:
        year = i.find('h3').text
        print(year)

        try:
            if(count!=3):
                ul = i.find('ul').find_all('li')
                for j in ul:
                    subject = j.text
                    clist.append(course(count, course_name, link, year, subject))
                    print(subject)
            else:
                subject = i.find('p').text
                clist.append(course(count, course_name, link, year, subject))
                print(subject)

        except:
            subject = i.find('p').text
            clist.append(course(count, course_name, link, year, subject))
            print(subject)

        print('\n')

if __name__ == '__main__':
    clist = []
    url = 'https://www.southampton.ac.uk/courses/undergraduate/'
    html_page = simple_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\southampton.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)