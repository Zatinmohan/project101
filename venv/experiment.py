from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
import re

def simple_link(url):                                                                           #non javascript
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    return html

def javascript_link(url):                                                                       #if Page is having javascript
    session = HTMLSession()
    resp = session.get(url)
    resp.html.render(timeout=160)                                                               #160 Seconds --> Need to be bigger in case of slow internet
    html = BeautifulSoup(resp.html.html, 'lxml')
    session.close()
    return html


def oxfordcourses(html_page):
    body = html_page.find('body')
    div = body.find('div', class_='dialog-off-canvas-main-canvas').find('div', class_='off-canvas-content').find(
        'main').find('section').find('div', class_='row page-body')
    div = div.find('div', class_='single-course-modules').find_all('div', class_='tabs-panel')
    year = "Year "
    c = 1
    for i in div:
        year = year + c.__str__()
        c+=1
        print(year)
        subject = i.find('p').text
        print(subject)
        year = year[0:4]


if __name__ == '__main__':
    url = 'https://search.ncl.ac.uk/s/redirect?collection=neu-web-courses&url=https%3A%2F%2Fwww.ncl.ac.uk%2Fundergraduate%2Fdegrees%2Fn404%2F&auth=aFj77ZkomEuK3Dv94qYY%2FQ&profile=_default&rank=24&query=%7CstencilsCourseType%3Aundergraduate'
    html_page = simple_link(url)
    body = html_page.find('body')
    print(body)


