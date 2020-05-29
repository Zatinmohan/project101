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
    baseUrl = 'https://www.sheffield.ac.uk/prospectus/'
    body = html_page.find('body')
    div = body.find('div',class_='col-xs-36').find_all('ul',class_='alpha')
    count=0
    for i in div:
        tr = i.find('table').find('tbody').find_all('tr')

        for j in range(1,len(tr)):
            count+=1
            course_name = tr[j].find('td').find('a').text
            link = baseUrl + tr[j].find('td').find('a').attrs['href']
            print(count.__str__() + " " + course_name + " " + link)
            inside_category(count,course_name,link)


def inside_category(count,course_name,link):
    page = javascript_link(link)
    body = page.find('body')

    if(count==97):
        div = body.find('div',class_='dialog-off-canvas-main-canvas').find('div',class_='off-canvas-content').find('main').find('section').find('div',class_='row page-body')
        div = div.find('div',class_='single-course-modules').find_all('div',class_='tabs-panel')
        year = "Year "
        c=1
        for i in div:
           year = year + c.__str__()
           #print(year)
           subject = i.find('p').text
           #print(subject)
           clist.append(course(count, course_name, link, year, subject))
           year = year[0:4]

    else:
        div = body.find('div',id='courseDetailsPage').find('div',id='modules')
        h4 = div.find_all('h4')
        table = div.find_all('table')
        yc=0
        for i in range(0,len(table)):
            if(table[i].find_previous('p').text=="Optional modules:"):
                year = table[i].find_previous('h4').text
            else:
                year = h4[yc].text
                yc+=1

            #print(year)
            tr = table[i].find('tbody').find_all('tr')
            for j in range(0,len(tr),2):
                subject = tr[j].find('a').text
                clist.append(course(count, course_name, link, year, subject))
                #print(subject)
            print('\n')


if __name__ == '__main__':
    clist = []
    url = 'https://www.sheffield.ac.uk/prospectus/courses-az.do?prospectusYear=2021'
    html_page = javascript_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\sheffield.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)