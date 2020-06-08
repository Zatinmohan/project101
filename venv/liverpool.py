from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
import requests
from time import sleep
from courses_list import course
from openpyxl import load_workbook,Workbook

def simple_link(url):                                                                           #non javascript
    while(True):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            page = requests.get(url,headers=headers)
            html = BeautifulSoup(page.content, 'html.parser')
            return html
        except:
            print("Website busy...Please wait")
            sleep(5)
            continue


def javascript_link(url):                                                                       #if Page is having javascript

    op = webdriver.FirefoxOptions()
    op.add_argument("--headless")
    driver = webdriver.Firefox(options=op)
    driver.get(url)
    html = BeautifulSoup(driver.page_source,'html.parser')
    driver.quit()
    return html

count=0
def category(html_page):
    baseUrl = 'https://www.liverpool.ac.uk'
    backUrl = 'module-details'
    body = html_page.find('body')

    tables = body.find_all('table',class_='datatable')
    global count
    for i in tables:
        tr = i.find_all('tr')
        for j in range(1,len(tr)):
            try:
                count+=1
                link = tr[j].find('td',class_='course-name').find('a').attrs['href']
                course_name = tr[j].find('td', class_='course-name').find('a').text
                if(count==218):
                    print(count.__str__() + " " + course_name + " " + link)
                    link = baseUrl + link
                    inside_course(count, course_name, link)

                elif(link.find('https')>=0):
                    print(count.__str__() + " " + course_name + " " + link)

                    if(link.find('postgraduate')>=0):
                        link = link.replace("overview",backUrl)
                        master_course(course_name,link)

                    elif(course_name=='Applied English BA (Hons)' or course_name=='Basque (Honours Select)' or course_name=='Catalan (Honours Select)  'or
                            course_name=='Chinese (Honours Select)' or course_name=='Combined Honours' or course_name=='Criminology and Security BA (Hons)' or
                    course_name=='Game Design BA (Hons)' or course_name=='Honours Select' or course_name=='Italian (Honours Select)'
                    or course_name=='Joint Honours' or course_name=='Portuguese (Honours Select)' or course_name=='Social Policy (Honours Select)'
                    or course_name=='Spanish (Honours Select)' or course_name=='Veterinary Conservation Medicine BSc'
                    or course_name == 'Veterinary Conservation Medicine Intercalated Honours BSc'):

                        year = "Null"
                        subject = "Null"
                        print(year)
                        print(subject)
                        clist.append(course(count, course_name, link, year, subject))

                    elif (link.find('undergraduate') >= 0):
                        link = link.replace("overview", backUrl)
                        print(count.__str__() + " " + course_name + " " + link)
                        inside_course(count, course_name, link)

                    else:
                        inside_course_list(count, course_name, link)

                else:
                    link = link.replace("overview", backUrl)
                    link = baseUrl + tr[j].find('td',class_='course-name').find('a').attrs['href']
                    link = link.replace("overview", backUrl)
                    print(count.__str__() + " " + course_name + " " + link)
                    inside_course(count, course_name, link)

            except:
                continue

            print('\n')


def master_course(course_name,link):
    page = simple_link(link)
    body = page.find('body')
    div = body.find('section', class_='content').find('section', id='module-details').find('div').find_all('h5')
    year = body.find('section', class_='content').find('h2').text
    print(year)

    global count
    for i in div:
        count+=1
        subject = i.text
        print(subject)
        clist.append(course(count, course_name, link, year, subject))



def inside_course_list(count,course_name,link):
    backUrl = 'module-details'
    page = simple_link(link)
    body = page.find('body')
    div = body.find('header', class_='online-deg-content-head').find('div', id='main-content').find('ul').find_all('li')
    for i in div:
        count+=1
        course_name = i.find('a').text
        link = i.find('a').attrs['href']
        link = link.replace("overview", backUrl)
        print(count.__str__() + " " + course_name + " " + link)
        inside_course(count,course_name,link)
        print('\n')

def inside_course(count,course_name,link):
    page = simple_link(link)
    body = page.find('body')
    div = body.find('div',class_='course-detail').find_all('section',id='module-details')

    for i in range(1,len(div)):
        try:
            year = div[i].find('h4').text
        except:
            continue

        print(year)

        d_tag = div[i].find('div').find('ul').find_all('li')
        for j in d_tag:
            try:
                subject = j.find('h5').text
                print(' ' + subject)
                clist.append(course(count, course_name, link, year, subject))
            except:
                subject = j.text
                print(subject)
                clist.append(course(count, course_name, link, year, subject))


if __name__ == '__main__':
    clist = []
    url = 'https://www.liverpool.ac.uk/study/undergraduate/courses/'
    html_page = simple_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\liverpool.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)