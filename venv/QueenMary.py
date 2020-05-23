from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
import requests

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
    '''headers = {'User-Agent': 'Mozilla/5.0'}
    session = HTMLSession()
    resp = session.get(url)
    resp.html.render(timeout=260)                                                               #160 Seconds --> Need to be bigger in case of slow internet
    session.close()
    html = BeautifulSoup(resp.html.html, 'lxml')'''


    return html

def category(html_page):
    body = html_page.find('body')

    div1 = body.find('div', class_='slat slat--notched slat--grey pb-4 md:pb-6').find('div',class_='slat__container').find('div', class_='results-set').find('ol')

    all_course_list = div1.find_all('li')

    for i in all_course_list:

        link = i.find('a').attrs['href']
        link = link.replace('%2F', '/')
        link = link.replace('%3A', ':')
        link = link.split('&auth', 1)[0]
        link = link.split('url=', 1)[1]

        print(link)
        inside_link(link)

def inside_link(link):
    page_code = javascript_link(link)
    body = page_code.find('body').find('div',class_='slat__container container--xl py-4 centre study-info')

    try:
        div = body.find('div',class_='study-options-navigation')
        total_course = div.find('ul').find_all('li')
        key_info = body.find_all('section')

        for i in range(len(total_course)):
            course_name = total_course[i].find('a').text

            div_tag = key_info[i].find('div', class_='option-info').find('div', class_='info').find('dl')
            duration = div_tag.find_all('dd')[1].text
            course_code = div_tag.find_all('dd')[3].text

            years_detail = page_code.find('body').find('section',id='structure').find('div',class_='centre slat__container container--xl py-4').find('div',class_='column-item container container--md pt-2 clearfix').find('div',class_='tabs')
            years_detailes = years_detail.find_all('div')

            for jj in years_detailes:
                year = jj.find('h3', class_='year').text
                try:
                    ul = jj.find('ul').find_all('li')
                    print(course_code + " " + course_name + " " + duration + " ")
                    for kk in ul:
                        subject = kk.text
                        print(" " + year + " " +subject)

                except:
                    year = years_detailes.find('h3').text
                    subject = years_detail.find('h4').text

                    print(" " + year + " " + subject)

    except:
        course_n = page_code.find('body').find('section',class_='course slat mt-4').find('div',class_='centre page-heading slat__container container--xl').find('div',class_='grid').find('div',class_='course-title grid__item grid__item--1/2')
        course_name = course_n.find('h1',class_='th-s2 th-o text-blue').text

        key_info = page_code.find('body').find('div',class_='slat__container container--xl py-4 centre study-info')

        div_tag = key_info.find('div', class_='info').find('dl')
        duration = div_tag.find_all('dd')[1].text
        course_code = div_tag.find_all('dd')[3].text

        years_detail = page_code.find('body').find('section', id='structure').find('div',
                                                                                   class_='centre slat__container container--xl py-4').find(
            'div', class_='column-item container container--md pt-2 clearfix').find('div', class_='tabs')
        years_detailes = years_detail.find_all('div')

        for jj in years_detailes:
            year = jj.find('h3', class_='year').text

            try:
                ul = jj.find('ul').find_all('li')
                print(course_code + " " + course_name + " " + duration + " ")
                for kk in ul:
                    subject = kk.text
                    print(" " + year + " " + subject)
            except:
                years_detailes = years_detail.find('div')
                try:
                    year = years_detailes.find('h3', class_='year').text
                    subject = years_detail.find('h4').text
                    print(" " + year + " " + subject)
                except:
                    para = years_detail.find_all('p')

                    for l in para:
                        subject = l.text
                        print(" " + year + " " + subject)

if __name__ == '__main__':

    url = "https://search.qmul.ac.uk/s/search.html?collection=queenmary-coursefinder-undergraduate-meta&query=&sort=title"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=11"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=21"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=31"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=41"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=51"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=61"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=71"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=81"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=91"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=101"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=111"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=121"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=131"
    html_page = simple_link(url)
    category(html_page)

    url = "https://search.qmul.ac.uk/s/search.html?meta_yearentry_sand=2020&collection=queenmary-coursefinder-undergraduate-meta&form=simple&start_rank=141"
    html_page = simple_link(url)
    category(html_page)