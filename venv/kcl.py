from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
import requests
from courses_list import course
from openpyxl import load_workbook,Workbook

count = 0

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

def sub(html_page):
    baseUrl = 'https://www.kcl.ac.uk'
    body = html_page.find('body')
    table = body.find('table').find('tbody').find_all('tr')
    for i in table:
        td = i.find_all('td')
        for j in td:
            links = baseUrl + j.find('a').attrs['href']
            print(links)
            inside_module(links)


def inside_module(link):
    clist = []
    baseUrl = 'https://www.kcl.ac.uk'
    page = simple_link(link)
    body = page.find('body')
    table = body.find_all('table')

    for i in table:
        tr = i.find_all('tr')
        for j in tr:
            td = j.find_all('td')
            for k in td:
                global count
                count+=1
                try:
                    l = baseUrl + k.find('p').find('a').attrs['href']
                    course_name = k.find('p').find('a',class_='pdf').text
                    print(count.__str__() + " " + course_name + " " + l)

                    inside_subject(count,course_name,l)
                except:
                    break
            print('\n')

def inside_subject(count,course_name,link):
    year = "Year "
    c=1
    page = simple_link(link)
    body = page.find('body')
    div = body.find('div',class_='box box-blue').find('div').find_all('div')


    for i in div:
        year = year + c.__str__()
        print(year)
        c+=1
        ul = i.find_all('ul')
        for j in ul:
            li = j.find_all('li')
            for k in li:
                subject = k.text
                print(' ' +subject)
                clist.append(course(count, course_name, link, year, subject))
        year = year[0:4]
        print('\n')
    #yc = div.find('div',class_='tab-nav tab-nav-cs tabs-3')



if __name__ == '__main__':
    clist = []
    url ='https://www.kcl.ac.uk/study/subject-areas'
    html_page = simple_link(url)
    sub(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\kcl.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)