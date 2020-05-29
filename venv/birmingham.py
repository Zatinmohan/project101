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
            print('Page not Responding...')
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
    baseUrl = 'https://www.birmingham.ac.uk'
    body = html_page.find('body')
    div = body.find('div',class_='tabs').find('section',id='CourseComplete_CollegesTab').find('div',class_='accordion accordion--no-collapse js-accordion accordion--bold')
    section = div.find_all('section')
    count=0
    for i in section:
        div_tag = i.find('div').find_all('ul')
        for j in div_tag:
            li = j.find_all('li')
            for k in li:
                count+=1
                course_name = k.find('a').text
                link = baseUrl + k.find('a').attrs['href']
                print(count.__str__() + " " + course_name + " " + link)
                inside_module(count,course_name,link)
                print('\n')

def inside_module(count,course_name,link):
    page = simple_link(link)
    body = page.find('body')
    yc=0
    try:
        div = body.find('div',class_='accordion accordion--bold accordion--modern accordion--no-collapse js-accordion push--top').find('section',id='Modules').find('div')
        ul = div.find_all('ul')
        h2 = div.find_all('h3')
        h3 = div.find_all('h2')

        if(len(ul)!=0):
            for i in ul:
                if(len(h2)==0):
                    if(len(h3)==0):
                        year = "Year 1"
                    else:
                        year = h3[yc].text
                        yc+=1
                else:
                    year = h2[yc].text
                    yc+=1
                if(year=="Law"):
                    year = "Optional Module"

                print(year)
                li = i.find_all('li')
                for j in li:
                    subject = j.text
                    print(' ' + subject)
                    clist.append(course(count, course_name, link, year, subject))
        else:
            year = h3[i].text
            print(year)
            p = div.find('p')
            subject = p.text
            print(' ' + subject)
            clist.append(course(count, course_name, link, year, subject))
    except:
        try:
            print("Year 1")
            table = div.find('table').find('tbody').find_all('tr')

            for t in range(1,table):
                subject = t.find('td').text
                clist.append(course(count, course_name, link, year, subject))
                print(subject)
        except:
            year = "Year 1"
            subject = "MOOCs/Distance Education/Field Trips"
            print(year)
            print(' ' + subject)
            clist.append(course(count, course_name, link, year, subject))


if __name__ == '__main__':
    clist = []
    url = 'https://www.birmingham.ac.uk/students/courses/index.aspx?CurrentTab=AtoZ&CourseComplete_AtoZ_AtoZLetter=A&AtoZFilter=All#CourseComplete_CollegesTab'
    html_page = simple_link(url)
    category(html_page)
    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\birmingham.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)