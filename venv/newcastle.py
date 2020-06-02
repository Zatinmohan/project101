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
    baseUrl = 'https://www.ncl.ac.uk/undergraduate/degrees/'
    body = html_page.find('body')
    div = body.find('section',id='courseDisplayResults').find('div',class_='row')
    ul = div.find_all('ul')[1]
    li = ul.find_all('li')
    i=1
    while i<len(li):
        try:
            if(li[i].find('a').text!="Back to top"):
                course_name = li[i].find('a').text
                if (len(li[i].find_all('span')[1].text) != 0):
                    link = baseUrl + li[i].find_all('span')[1].text.lower().strip()
                    print(i.__str__() + "  "  + course_name + " " + link)
                    inside_category(i,course_name,link)

            i+=1
        except:
            i+=1
            if(li[i].find('a').text!="Back to top"):
                course_name = li[i].find('a').text
                if(len(li[i].find_all('span')[1].text)!=0):
                    link = baseUrl + li[i].find_all('span')[1].text.lower().strip()
                    print(i.__str__() + " " + course_name + " " + link)
                    inside_category(i,course_name,link)

            i+=1
        print('\n')

def inside_category(count,course_name,link):
    year = "Year "
    yc=0
    page = simple_link(link)
    body = page.find('body')
    try:
        div = body.find('section',class_='tabs yearTabs').find_all('div',class_='tabContent')

        for i in div:
            yc+=1
            year = year + yc.__str__()
            section = i.find('section',class_='brief').find('ul')
            print(year)
            try:
                if(section==None):
                    tr = i.find('section', class_='modules').find('table').find('tbody').find_all('tr')

                    for j in range(1, len(tr)):
                        subject = tr[j].find('td').find('a').text
                        clist.append(course(count, course_name, link, year, subject))
                        print(' ' + subject)

                else:
                    li = section.find_all('li')
                    for j in li:
                        subject = j.text
                        clist.append(course(count, course_name, link, year, subject))
                        print(' ' + subject)
            except:
                subject = i.find('section', class_='brief').find('p').text
                clist.append(course(count, course_name, link, year, subject))
                print(subject)

            year = year[0:4]
            print('\n')
    except:
        div = body.find('div', class_='column-block')
        h4 = div.find_all('h4')
        for k in h4:
            year = k.text
            if (year.find("Year") == 0):
                print(year)
                subject = k.find_next('p').text
                clist.append(course(count, course_name, link, year, subject))
                print(subject)
            else:
                break





if __name__ == '__main__':
    clist = []
    url = 'https://www.ncl.ac.uk/undergraduate/degrees/'
    html_page = javascript_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\newcastle.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)