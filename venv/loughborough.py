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

count = 0

def category(html_page):
    baseUrl = 'https://www.lboro.ac.uk'
    body = html_page.find('body')
    li = body.find('ul',class_='list list--courses js-courses-list').find_all('li')
    global count
    for i in li:
        count+=1
        link = baseUrl + i.find('a').attrs['href']
        course_name = i.find('a').find('h3').text
        print(count.__str__() + " " + course_name + " " + link)
        inside_category(count,course_name,link)

def master_category(html_page):
    baseUrl = 'https://www.lboro.ac.uk'
    body = html_page.find('body')
    li = body.find('ul',class_='list list--degrees js-degrees-list').find_all('li')
    global count
    for i in li:
        count+=1
        link = baseUrl + i.find('a').attrs['href']
        course_name = i.find('h3').text
        print(count.__str__() + " " + course_name + " " + link)
        inside_master(count,course_name,link)


def inside_master(count,course_name,link):
    page = simple_link(link)
    body = page.find('body')
    try:
        div = body.find_all('div',class_='content-type content-type--main')[2].find_all('ul')
        if(len(div)!=0):
            for i in div:
                li = i.find_all('li')
                for j in li:
                    subject = j.text
                    print(subject)
                    clist.append(course(count, course_name, link, "---", subject))
        else:
            div = body.find_all('div',class_='js-tabcontent')

            for i in div:
                d_tag = i.find_all('div',class_='content-type content-type--toggle')

                for j in d_tag:
                    subject = j.find('span').text
                    print(subject)
                    clist.append(course(count, course_name, link, "--", subject))
    except:
        print("Null")
        print("NULL")
        clist.append(course(count, course_name, link, "Null", "Null"))

def inside_category(count,course_name,link):
    year = "Year "
    page = simple_link(link)
    body = page.find('body')
    div = body.find('div',class_='js-tabs tabs').find_all('div',class_='js-tabcontent')
    c=0
    for i in div:
        c+=1
        year = year + c.__str__()
        print(year)

        d_tag = i.find_all('div',class_='content-type content-type--toggle')

        for j in d_tag:
            subject = j.find('span').text
            print(' ' + subject)
            clist.append(course(count, course_name, link, year, subject))

        year = year[0:4]


if __name__ == '__main__':
    clist = []
    url = 'https://www.lboro.ac.uk/study/undergraduate/courses/a-z/'
    html_page = simple_link(url)
    category(html_page)

    url = 'https://www.lboro.ac.uk/study/postgraduate/masters-degrees/a-z/'
    html_page = simple_link(url)
    master_category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\loughborough.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)