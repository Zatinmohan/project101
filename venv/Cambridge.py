from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
from selenium import webdriver

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
    html = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return html

def category(html):
    body = html.find('body')
    div1 = body.find('div', class_='campl-row campl-content campl-recessed-content').find('div',
                                                                                          class_='campl-wrap clearfix').find(
        'div', class_='campl-column6 campl-main-content').find('div')
    div2 = div1.find('div', class_='region region-content').find('div', class_='block block-system').find('div',
                                                                                                          class_='attachment attachment-after')
    courses_list = div2.find_all('div', class_='view-content')
    count=0
    for i in courses_list:
        div_tags = i.find_all('div')
        for j in div_tags:
            count+=1
            course_name = j.find('a').text
            links = baseUrl + j.find('a').attrs['href']
            inside_course(count,course_name,links)

def inside_course(count,course_name,links):
    page = javascript_link(links)
    body = page.find('body')
    div_tag = body.find('div',class_='campl-row campl-content campl-recessed-content').find('div',class_='campl-wrap clearfix').find('div',class_='campl-column6 campl-main-content').find('div',class_='node node-course-profile clearfix')
    div_tag = div_tag.find('div',class_='content campl-content-container').find('div',class_='field-group-htabs-wrapper group-container-college field-group-htabs').find('div',class_='horizontal-tabs clearfix')
    div_tag = div_tag.find('div',class_='horizontal-tabs-panes horizontal-tabs-processed').find('fieldset',id='course-outline').find('div',class_='field-item even')

    total_year = div_tag.find_all('h2')
    print(count.__str__() + " " + course_name)
    for i in range(1,len(total_year)):
        year = total_year[i].text

        try:
            ul = div_tag.find('h2').find_all('ul')

            li = ul[i].find_all('li')

            for k in li:
                subject = k.text
                print(" " + year + " " + subject)

        except:

            p = div_tag.find_all('p')
            subject = p[i].text

            print(year + " " + subject)

    print('\n')

if __name__ == '__main__':
    baseUrl = "https://www.undergraduate.study.cam.ac.uk"
    url = "https://www.undergraduate.study.cam.ac.uk/courses"

    html = simple_link(url)
    category(html)
