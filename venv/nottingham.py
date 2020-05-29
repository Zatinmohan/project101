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
    baseUrl = 'https://www.nottingham.ac.uk'
    endUrl = '#yearsmodules'
    body = html_page.find('body')
    div = body.find('form').find('div',id='internalWrap').find('div',id='internal').find('div',id='main').find('div',id='content')
    div = div.find('div',class_='sys_twoColumns_7030').find('div').find('div',id='faculty-nav').find_all('div',class_='show-hide sys_bySubject')
    count=0

    for i in div:
        ul = i.find('div',class_='sys_GenericAnswerShowHide').find_all('ul')

        for j in ul:
            li = j.find_all('li')
            for k in li:
                count+=1
                link = baseUrl + k.find('a').attrs['href'] + endUrl
                course_n = k.find('a').text
                print(count.__str__() + " " + course_n + " " + link)
                if(count==6):
                    print("Error 404")
                else:
                    find_content(count,course_n,link)

def find_content(count,course_n,link):
    baseUrl = 'https://www.nottingham.ac.uk'
    endUrl = '#yearsmodules'

    if((count>=1 and count<=8) or count==16):
        inside_category(count,course_n,link)

    else:
        c=0
        body = simple_link(link).find('body')
        div = body.find('form').find('div', id='wrapper').find('div', id='internalWrap').find('div', id='holder').find(
            'div', id='main').find('div', class_='content-show-hides')
        div = div.find('div', id='Courses').find('div', class_='sys_GenericAnswerShowHide').find_all('h3')

        for i in div:
            count+=c
            c+=1
            course_name = i.find('a').text
            links = baseUrl + i.find('a').attrs['href'] + endUrl
            #print(course_name + " " + links)
            print(count.__str__() + "  " + course_name + " " + links)
            inside_category(count,course_name,links)
            break

def inside_category(count,course_name,link):
    c=0
    year = "Year "
    page = simple_link(link)
    body = page.find('body')
    div = body.find('form').find('div',class_='offcanvas-wrap').find('div',class_='offcanvas-content').find('div',id='content').find('div',id='modules').find('div',class_='row')
    divv = div.find('div',class_='column large-12').find('div',class_='modulesTabs').find_all('div',class_='content panel')
    li =  div.find('div',class_='column large-12').find('div',class_='modulesTabs').find('ul').find_all('li')

    for i in range(len(li)):
        #c+=1
        #year = year + c.__str__()
        year = li[i].text
        print(year)

        try:
            d_tag = divv[i].find('div',class_='moduleBlock').find_all('div',class_='js-expandmore')

            for j in d_tag:
                subject = j.text
                clist.append(course(count, course_name, link, year, subject))
                #print(subject)

        except:
            if(count==1):
                break
            else:
                try:
                    subject = divv[i].find('p').text
                    clist.append(course(count, cc, link, year, subject))
                    #print(subject)
                except:
                    break

        year = year[0:4]
if __name__ == '__main__':
    clist = []

    url = 'https://www.nottingham.ac.uk/ugstudy/courses/subjectareasearch.aspx'
    html_page = simple_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\nottingham.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)