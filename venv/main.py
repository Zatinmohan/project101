from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
import re

def simple_link(url):                                                                           #non javascript
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url,headers=headers)
    html = BeautifulSoup(page.content, 'html.parser')
    return html

def javascript_link(url):                                                                       #if Page is having javascript
    headers = {'User-Agent': 'Mozilla/5.0'}
    session = HTMLSession(browser_args=["--no-sandbox",'--user-agent=Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'])
    resp = session.get(url)
    resp.html.render(timeout=260)                                                               #160 Seconds --> Need to be bigger in case of slow internet
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

    counter=0                                           #To check whether the page is odd or even

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

        counter+=1

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

        if (counter!=36 and counter!=40):
            div7 = div4.find('div',class_='field-item odd').find('div',class_='ui-tabs-panel ui-widget-content ui-corner-bottom').find('table')
            table3 = div7.find('tbody')
            tr =  table3.find_all('tr')
            #counter+=1

            for i in range(1,len(tr),2):
                td = tr[i].find('td')
                year = tr[i-1].text

                print(course_code + " " + course_name + " " + duration)

                if(counter==7):                                                             #Page clasics is differnet from rest of the other pages
                    break                                                                   #fine arts, classics and oriental studies [same problem]
                                                                                            #Geography page problem, connection prolem
                for j in td:
                    try:
                        l = td.find('ul').find('li')
                        #print(course_code + " " + l.text)
                        try:
                            ll = j.find('ul')

                            for k in l.find('ul'):
                                print(" "+ year + " -> "  + " " + k.text)

                        except:
                            px = td.find_all('li')
                            for k in px:
                                 print(" "+ year + " -> " + " " + k.text)

                    except:
                        print(" "+ year + " -> " + " " + td.find('p').text)

                    break
                print('\n')
            #print(courselink)


