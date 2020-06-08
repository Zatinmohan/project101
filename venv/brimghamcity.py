from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
import requests
from time import sleep
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

count=0

def category(html_page):
    baseUrl = 'https://www.bcu.ac.uk'
    body = html_page.find('body')
    try:
        div = body.find_all('div',class_='page article pvl')[1].find('ul').find_all('li')
        global  count

        for i in div:
            count+=1
            course_name = i.find('h4').text
            link = baseUrl + i.find('h4').find('a').attrs['href']
            print(count.__str__() + " " + course_name + " " + link)
            inside_course(count,course_name,link)
            print('\n')

    except:
        print("NO Course available")

def inside_course(count,course_name,link):
    page = simple_link(link)
    body = page.find('body')
    try:
        div = body.find('div',class_='bcu-tabs-panel man pam secondary-bg-grey-light-3').find_all('div',class_='crs-dtl-content-tabs-panel')
        for i in div:
            year = i.find('h4',class_='hide-on-desktop mtl mbm').text
            print(year)
            table = i.find('table', class_='mvn plain-table').find_all('tr')

            for j in table:
                try:
                    td = j.find('td').find('div',class_='left-col inline-block size14of16')
                    subject = td.text.strip()
                    print(' ' + subject)
                    clist.append(course(count, course_name, link, year, subject))
                except:
                    continue
            print('\n')
    except:
        clist.append(course(count, course_name, link, "Null", "Null"))
        print("Year : Null" + '\n' + "Subject : Null"+ '\n')
if __name__ == '__main__':
    clist=[]
    url = 'https://www.bcu.ac.uk/courses/a-to-z-listing?atoz=1&isclearingsearch=False&perpage=999&'
    char = 64
    backUrl = 'letter='
    backUrl2 = '#results'

    while(char<90):
        char+=1
        c = chr(char)
        u = url + backUrl + c + backUrl2
        print(u)
        html_page = simple_link(u)
        category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\brimghamcity.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)