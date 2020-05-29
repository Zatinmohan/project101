from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
from selenium import webdriver
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
    div = body.find('section',class_='visible-body').find('section',class_='page-level page-content').find('div',class_='wrapper').find('section',id='page-content-main')
    div = div.find('section',id='main-content').find('table').find('tbody').find('tr').find_all('td')

    counter=0
    for i in div:
        a = i.find_all('a')
        for j in a:
            counter+=1
            link = "https:"+j.attrs['href']
            cc = j.text
            print(counter.__str__()+ " " + cc + " " + link)
            if(counter!=36 and counter!=40 and counter!=7):
                inside_course(counter,cc,link)
            else:
                print(counter.__str__() + " " + 'problem with page ' + cc + " " + link)
                clist.append(course(counter,cc,link,"null","null"))


def inside_course(count,cc,link):
    page = javascript_link(link)
    body = page.find('body')
    div = body.find('section',class_='visible-body').find('section',class_='page-level page-content').find('div',class_='wrapper').find('section',id='page-content-main')
    div = div.find('section',id='main-content').find('div',class_='field-items').find('div',class_='field-item odd').find('table').find('tbody').find_all('tr')

    #year = div[0].find('td').text

    for i in range(1,len(div),2):
         year = div[i-1].find('td').text
         #print(year)
         try:
            li = div[i].find('td').find('ul')
            try:
                ul = li.find('ul')
                for k in ul:
                    subject = k.text
                    clist.append(course(count,cc,link,year,subject))
            except:
                l = li.find_all('li')
                for k in l:
                    subject = k.text
                    clist.append(course(count,cc,link,year,subject))
         except:
             subject = div[i].find('p').text
             clist.append(course(count, cc, link, year, subject))
             #print(subject)
         print('\n')



if __name__ == '__main__':
    clist = []
    url = 'http://www.ox.ac.uk/admissions/undergraduate/courses/course-listing'
    html_page = simple_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\Oxford.xlsx'
    #wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)



