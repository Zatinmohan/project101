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
    div = body.find('div',class_='id7-fixed-width-container').find('main').find('div',class_='id7-main-content').find('div').find('div',class_='column-1-content').find('h2')
    div = div.find_all('dl')

    count=0
    for i in div:
        dd = i.find('dd').find_all('h3')
        for j in dd:
            count+=1
            link = j.find('a').attrs['href']
            course_name = j.text
            print(count.__str__() + " " + course_name + " " + link)
            inside_course(count,course_name,link)



def inside_course(count,course_name,link):
    year = "Year "
    c=0
    page = simple_link(link)
    body = page.find('body')
    div = body.find('div',class_='id7-fixed-width-container').find('main').find('div',class_='id7-main-content').find('div',class_='column-1-content').find('div',class_='container-text')
    try:
        div = div.find('div',class_='hp-layout').find('div',id='course-tab-3')
        ul = div.find_all('ul')

        if(len(ul)!=0):
            for i in ul:
                c+=1
                year = year + c.__str__()
                print(year)
                li = i.find_all('li')
                for j in li:
                    subject = j.text
                    #print(subject)
                    clist.append(course(count, course_name, link, year, subject))
                year = year[0:4]
                print('\n')

        else:
            h6 = div.find_all('h6')
            for i in h6:
                h5 = i.find_previous('h5')
                year = h5.text
                subject = i.text
                #print(year+'\n'+subject)
                clist.append(course(count, course_name, link, year, subject))

    except:
        print("Problem with Course " + course_name + " " + link)




if __name__ == '__main__':
    clist = []
    url = 'https://warwick.ac.uk/study/undergraduate/courses-2020/'
    html_page = simple_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\warwick.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)