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
    baseUrl = 'https://www.surrey.ac.uk'
    body = html_page.find('body')
    div = body.find('div',class_='dialog-off-canvas-main-canvas').find('div',class_='layout-container').find('main').find('div',class_='node node--type-study node--view-mode-full')
    div = div.find('section').find('div',class_='row').find_all('div',class_='row list mb-4')
    count=0
    for i in div:
        div_tag = i.find_all('div')
        for j in div_tag:
            count += 1
            link = baseUrl + j.find('a').attrs['href']
            course_name = j.find('a').find('span').text
            print(count.__str__() + " "  + course_name + " " +link)
            inside_course(count,course_name,link)


def inside_course(count,course_name,link):
    page = javascript_link(link)
    body = page.find('body')

    div = body.find('div',class_='dialog-off-canvas-main-canvas').find('div',class_='layout-container').find('main')
    

    div = div.find('div',class_='layout-content').find('article').find('section',class_='scrollspy-wrapper position-relative py-0').find('div',class_='bg-white section-padding section--triangle z-3')

    try:
        div = div.find('div',class_='body-content').find_all('div')[2].find('div',class_='module-list').find('div',class_='tab-content').find('div',class_='tab-pane active')

        div2 = div.find_all('div',class_='module-year accordion')


        for i in div2:

            tr = i.find('div',class_='card').find_all('div')[1].find('table').find('tbody').find_all('tr')

            year = i.find('div',class_='card').find(
                'div',class_='card-header border border-deep-cerulean border-right-0 border-bottom-0 border-left-0 p-0').find('h5').text

            print(year)
            for j in tr:
                subject = j.find('td').text
                clist.append(course(count, course_name, link, year, subject))
                #print(subject)
            print('\n')
    except:
        clist.append(course(count, course_name, link, "null", "null"))
        #print('Null')


if __name__ == '__main__':
    clist = []
    url = 'https://www.surrey.ac.uk/undergraduate'
    html_page = javascript_link(url)

    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\surrey.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)