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
            print("Website busy...Please wait")
            sleep(5)
            continue


def javascript_link(url):                                                                       #if Page is having javascript

    while(True):
        try:
            op = webdriver.FirefoxOptions()
            op.add_argument("--headless")
            driver = webdriver.Firefox(options=op)
            driver.get(url)
            html = BeautifulSoup(driver.page_source,'html.parser')
            driver.quit()
            return html
        except:
            print("Website busy.. Trying again")
            sleep(5)
            continue

def category(html_page):
    baseUrl = 'https://www.exeter.ac.uk'
    endUrl = '#course-content'
    body = html_page.find('body')
    div = body.find('div',id='all-courses-A-Z').find('ul',class_='course-list').find_all('li')
    count=0
    for i in div:
        count+=1
        course_name = i.find('a').text
        link = baseUrl + i.find('a').attrs['href'] + endUrl
        print(count.__str__() + " " + course_name + " " + link)
        if(course_name=='Foundation' or link=='https://www.exeter.ac.uk/undergraduate/courses/foundation/internationalyearone/#course-content'):
            clist.append(course(count, course_name, link, "Null", "Null"))
        else:
            inside_course(count, course_name, link)


def inside_course(count,course_name,link):
    page = javascript_link(link)
    body = page.find('body')
    div = body.find('div',id='course-content-accordion').find_all('div',class_='panel panel-default')

    for i in div:
        year = i.find('div',class_='panel-heading collapsed').find('h4').text
        print(year)
        d_tag = i.find('div',class_='panel-collapse collapse')
        try:
            iframe = "https:"+d_tag.find('iframe').attrs['src']
            try:
                p = simple_link(iframe).find('body').find('table').find_all('tr')

                for j in range(1,len(p)):
                    try:
                        subject = p[j].find_all('td')[1].text
                        clist.append(course(count, course_name, link, year, subject))
                    except:
                        break

                    print(subject)

            except:
                try:
                    p = simple_link(iframe).find('body').find('p')
                    subject = p.text
                    print(subject)
                    clist.append(course(count, course_name, link, year, subject))
                except:
                    li = simple_link(iframe).find('body').find('ul').find_all('li')
                    for j in li:
                        subject = j.text
                        print(subject)
                        clist.append(course(count, course_name, link, year, subject))

        except:
            p = d_tag.find('p')
            subject = p.text
            print(subject)
            clist.append(course(count, course_name, link, year, subject))
        print('\n')



if __name__ == '__main__':
    clist = []
    url = 'https://www.exeter.ac.uk/undergraduate/courses/all-courses/'
    html_page = javascript_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\exeter.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)