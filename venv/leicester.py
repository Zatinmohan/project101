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

def inside_module(llist):
    count=0
    for i in llist:
        page = simple_link(i)
        body = page.find('body')
        course_name = nlist[count]
        print((count+1).__str__() + " " + course_name + " " + i)

        try:
            div = body.find('main').find('div', class_='col-xs-12 col-sm-12 col-md-12 u-p-bottom--3 u-p-right--0').find(
                'div', class_='course-block')
            div = div.find('div', class_='responsive-tabs vertical-tabs')
        except:
            page = javascript_link(i)
            body = page.find('body')
            div = body.find('main').find('div', class_='col-xs-12 col-sm-12 col-md-12 u-p-bottom--3 u-p-right--0').find(
                'div', class_='course-block')
            div = div.find('div', class_='responsive-tabs vertical-tabs responsive-tabs--enabled')

        d_tag = div.find_all('div')

        for j in d_tag:
            year = j.find_previous('h3').text
            print(year)

            try:
                li = j.find('ul').find_all('li')

                for k in li:
                    subject = k.text
                    print(' ' + subject)
                    clist.append(course(count, course_name, i, year, subject))
            except:
                try:
                    p = j.find('p')
                    subject = p.text
                    print(' ' + subject)
                    clist.append(course(count, course_name, i, year, subject))
                except:
                    break

        print('\n')
        count += 1


if __name__ == '__main__':
    llist = []
    nlist = []
    clist = []
    url = 'https://le.ac.uk/courses'
    endUrl = '?Q=&Page='
    html_page = simple_link(url)

    body = html_page.find('body')
    #div = body.find('article')
    #category(div)

    d = int(body.find('article').find('ul',class_='pagination pagination--alt').find_all('li')[4].text)

    for i in range(1,d+1):
        print("Page Number : " + i.__str__())
        u = url + endUrl + i.__str__()
        html_page = simple_link(u)
        body = html_page.find('body')
        div = body.find('article')
        category(div)

    inside_module(llist)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\leicester.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)







