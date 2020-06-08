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

count=0
def category(html_page):
    baseUrl = 'https://www.hull.ac.uk'
    body = html_page.find('body')
    div = body.find('article').find_all('section')
    global count
    for i in range(2,len(div)):
        d_tag = div[i].find('div',class_='grid').find('ul').find_all('li')
        for j in d_tag:
            count+=1
            link = baseUrl + j.find('a').attrs['href']
            course_name = j.find('a').text
            print(count.__str__() + " " + course_name + " " + link)
            if (count != 55):
                inside_course(count,course_name,link)
            else:
                foundation_year(count,link)


def foundation_year(count,link):
    page = simple_link(link)
    body = page.find('body')
    div = body.find('div', class_='courses-container').find('div', class_='course-list').find_all('p')
    for i in div:
        try:
            course_name = i.find('a').text
            link = i.find('a').attrs['href']
            print(count.__str__() + " " + course_name + " " + link)
            inside_course(count,course_name,link)
        except:
            break

        count+=1

def inside_course(count,course_name,link):
    page = simple_link(link)
    body = page.find('body')
    try:
        div = body.find('div',class_='tab-container').find('div',class_='tabs flex-tabs').find_all('div',class_='panel')
        c=0
        for i in div:
            year = i.find('h3').text
            print(year)
            li = i.find('ul').find_all('li')
            if(len(li)!=0):
                for j in li:
                    d = j.find_all('div')
                    for k in d:
                        subject = k.find('h3').text
                        print(' ' + subject)
                        clist.append(course(count, course_name, link, year, subject))
            else:
                subject = "NULL"
                print(' ' + subject)
                clist.append(course(count, course_name, link, year, subject))
            print('\n')
    except:
        try:
            div = body.find('article').find_all('section', class_='course-section')[1].find('div',
                                                                                            class_='unit golden-large')
            year = div.find('div', class_='accordion-header teal').text
            li = div.find('ul').find_all('li')

            for i in li:
                p = i.find('p').find('strong')
                subject = p.text
                print(' ' + subject)
                clist.append(course(count, course_name, link, year, subject))
        except:
            try:
                div = body.find('article').find('section', class_='course-section').find('div',
                                                                                         class_='unit golden-large')
                li = div.find('ul').find_all('p',class_='module')

                if(len(li)!=0):
                    print("About")

                    for i in li:
                        subject = i.text
                        print(' ' + subject)
                        clist.append(course(count, course_name, link, "About", subject))
                else:
                    print("Research")
                    div = body.find('article').find('section', class_='course-section study').find('div',
                                                                                                   class_='unit golden-large')
                    li = div.find('ul').find_all('li')
                    for i in li:
                        subject = i.text
                        print(' ' + subject)
                        clist.append(course(count, course_name, link, "Research", subject))
            except:
                year = "Null"
                subject = "Null"
                print(year)
                print(subject)
                clist.append(course(count, course_name, link, year, subject))

if __name__ == '__main__':
    clist = []
    url = 'https://www.hull.ac.uk/study'
    html_page = simple_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\hull.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)