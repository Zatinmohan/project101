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


def course_list(html_page):
    body = html_page.find('body')
    div = body.find('article').find('ul',class_='degree-list list-unstyled').find_all('li',class_='degree-list__group')
    count=0
    for i in div:
        div_tag = i.find('div',class_='degree-list__inner').find('table').find('tbody').find_all('tr')
        for j in div_tag:
            count += 1
            td = j.find_all('td')[0]
            link = "https:" + td.find('a').attrs['href']
            course_name = td.find('a').text
            course_code = j.find_all('td')[1].text

            print(count.__str__() + " " + course_code + " " + course_name + " " + link)
            inside_course(count,course_code,course_name,link)


def inside_course(count,course_code,course_name,link):
    page = simple_link(link)
    body = page.find('body')
    div = body.find('div',class_='site-content wrapper').find('div',class_='site-content__inner clearfix').find('div',class_='site-content__body').find('div',class_='site-content__main')
    div = div.find('div',class_='prospectus--programme').find('section',id='degree-structure').find('div',class_='collapse__content').find('div',class_='tabs')
    ul = div.find('ul').find_all('li')

    for i in range(0,len(ul)):
        year = ul[i].find('a').text
        tabs = div.find('div',class_='tabs__content island').find_all('div')

        try:
            tag = tabs[i].find_all('p')[1]
            if(len(tag)==0):
                #print(year)
                ul_tag = tabs[i].find('ul').find_all('li')
                for x in ul_tag:
                    subject = x.text
                    clist.append(course(count, course_name, link, year, subject))
                    #print(subject)
            else:
                subject = str(tag).split('<br/>')

                subject[0] = subject[0].replace('<p>', '')
                subject[len(subject) - 1] = subject[len(subject) - 1].replace('</p>', '')
                for xx in subject:
                    clist.append(course(count, course_name, link, year, xx))
                #print(year)
                #print(subject)


        except:
            try:
                print(year)
                ul_tag = tabs[i].find('ul').find_all('li')
                for x in ul_tag:
                    subject = x.text
                    clist.append(course(count, course_name, link, year, subject))
                    #print(subject)
            except:
                subject = "Year Abroad"
                clist.append(course(count, course_name, link, year, subject))
                #print(year)
                #print(subject)

if __name__ == '__main__':
    clist = []
    url = 'https://www.ucl.ac.uk/digital-presence-services/ugdegrees/www/degreesearch.php?collection=current'
    html_page = simple_link(url)

    course_list(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\ucl.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)