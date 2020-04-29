from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests

def simple_link(url):                                                                           #non javascript
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url,headers=headers)
    html = BeautifulSoup(page.content, 'html.parser')
    return html

if __name__ == '__main__':
    url = "https://www.imperial.ac.uk/study/ug/courses"
    html_page = simple_link(url)

    body = html_page.find('body')
    div1 = body.find('div',id='content-box').find('div',id='page').find('div',class_='container content-template').find('div',id='main').find('div',class_='col lg-9 wysiwyg')
    div2 = div1.find('div',class_='module').find('div',class_='row top page-a-z').find('div',class_='col lg-12')
    main_div = div2.find_all('div',class_='module')[1]

    ol_tag = main_div.find('ol',class_='index-groups courses primary')

    count=0
    for li in ol_tag.find_all('li'):
        e_pages = "1 2 6 7 8 26 27 28 35 36 55 58 60 61 62 78 80 81"

        link = "https://www.imperial.ac.uk" + li.find('a').attrs['href']
        page = simple_link(link)

        count+=1

        course_title = li.find('h4').text
        dept = li.find('div',class_='type dept').text
        coures_code = li.find_all('div')[2].text
        duration = li.find_all('div')[3].text

        div = page.find('div',id='content-box').find('div',id='page').find('div',class_='container content-template course-template').find('div',class_='row top flow-opposite').find('div',class_='col lg-9 wysiwyg')
        div_module = div.find_all('div',class_='module')

        inside_module=div_module[1].find_all('div')

        if(count==51):
            inside_module = inside_module[11]
            print(inside_module)