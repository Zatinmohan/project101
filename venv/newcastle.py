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
    div = body.find('section',id='courseDisplayResults').find('div',class_='row')
    ul = div.find_all('ul')[1]
    li = ul.find_all('li')
    i=1
    while i<len(li):
        try:
            if(li[i].find('a').text!="Back to top"):
                course_name = li[i].find('a').text
                link = li[i].find('a').attrs['href']
                print(i.__str__() + "  "  + course_name + " " + link)
                #inside_category(i,course_name,link)
                #break
            i+=1
        except:
            i+=1
            if(li[i].find('a').text!="Back to top"):
                course_name = li[i].find('a').text
                link = li[i].find('a').attrs['href']
                print(i.__str__() + " " + course_name + " " + link)
                #inside_category(i,course_name,link)
                #break
            i+=1

def inside_category(count,course_name,link):
    page = simple_link(link)
    body = page.find('body')
    print(body)

if __name__ == '__main__':
    url = 'https://www.ncl.ac.uk/undergraduate/degrees/'
    html_page = javascript_link(url)
    category(html_page)