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
    body = html_page.find('body')
    div= body.find('div',class_='site-container-md').find('main').find('div').find('div',class_='wrapper-pd-md wrapper-lg').find('div').find_all('div')
    count=0
    for i in div:
        table = i.find('table').find('tbody').find_all('tr')
        for j in table:
            count+=1
            link = "https:" + j.find('a').attrs['href']
            course_name = j.find('a').text
            print(count.__str__() + " " + course_name + " " + link)
            inside_course(count,course_name,link)
            print('\n')


def inside_course(count,course_name,link):
    year = "Year "
    c=0
    page = simple_link(link)
    body = page.find('body')
    div = body.find('div',class_='site-container-md').find('main').find('div').find('div',class_='skin-bg-module-light').find('div',class_='tk-row anchor-link-scroll')
    div = div.find('div', id='section2').find('div', class_='accordion-body').find_all('div',class_='accordion-body')

    for i in div:
        c+=1
        year = year + c.__str__()
        #print(year)
        li = i.find('ul').find_all('li')
        if(len(li)!=0):
            for j in li:
                subject = j.find('span',class_='module-title').text
                clist.append(course(count, course_name, link, year, subject))
                #print(subject)
        else:
            p = i.find('h3').find_next('p').text
            clist.append(course(count, course_name, link, year, subject))
            #print(p)
        year = year[0:4]
        print('\n')

if __name__ == '__main__':
    clist = []
    url = 'https://courses.leeds.ac.uk/a-z'
    html_page = simple_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\leeds.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)