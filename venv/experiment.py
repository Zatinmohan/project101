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


def oxfordcourses(html):
    section1 = html.find('section', class_='visible-body')
    section2 = section1.find('section', class_='page-level page-content')
    div1 = section2.find('div', class_='wrapper')
    return div1

if __name__ == '__main__':
    html_page = simple_link('http://www.ox.ac.uk/admissions/undergraduate/courses/course-listing')
    div = oxfordcourses(html_page)
    courselink = []

    section3 = div.find('section', class_='page-content-level column page-content-main')
    div2 = section3.find('div', class_='ds-1col node node-page view-mode-oxweb_full_content clearfix')

    table = div2.find('table')
    anchor = table.find_all('a')

    for links in anchor:
        #courselink.append("http:"+links['href'])
        course_name = links.text                        #Course Name
        s = "http:"+links['href']                       #Parsing each and every Course page
        html = javascript_link(s)
        div_tag = oxfordcourses(html)                   #Same Pattern

        div3 = div_tag.find('div',class_='row space-header')
        section4 = div3.find('section',class_='page-content-level column page-content-main').find('section',class_='page-content-container main-content')
        div4 = section4.find('div',class_='ds-1col node node-course view-mode-oxweb_full_content clearfix').find('div',class_='field field-name-field-body-multiple field-type-text-long field-label-hidden')
        div5 = div4.find('div',class_='field-items').find('div',class_='field-item even').find('div',class_='ui-tabs-panel ui-widget-content ui-corner-bottom')
        div6 = div5.find('div',class_='field field-name-field-intro field-type-text-long field-label-hidden').find('span',class_='field-item-single').find('div',class_='audience-copy')
        table2 = div6.find('tbody')

        tr = table2.find_all('tr')

        data = [tag.text for tag in tr[0]]
        course_code = data[2]
        duration = data[5]

        div7 = div4.find('div',class_='field-item odd').find('div',class_='ui-tabs-panel ui-widget-content ui-corner-bottom').find('table')
        table3 = div7.find('tbody')
        tr =  table3.find_all('tr')

        for i in range(1,len(tr),2):
            year = tr[i-1].text
            l = tr[i].find('ul').find('li')
            print(course_code + " " + course_name + " " + duration)

            for j in l.find('ul'):
                desp = j.text
                print(" "+year+": " + " " +desp)

            print('\n')
    #print(courselink)


