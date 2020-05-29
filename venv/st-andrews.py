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
    baseUrl = 'https://www.st-andrews.ac.uk'
    body = html_page.find('body')
    section = body.find('section',role='main').find('div',class_='col-xs-12').find('nav',class_='navigation-grid collapse-top').find('ul')

    li = section.find_all('li')
    count=0

    for i in li:
        count+=1
        course = i.text
        link = baseUrl + i.find('a').attrs['href']
        #print(count.__str__() + " " + course + " " + link)
        inside_category(count,course,link)

def inside_category(count,course,link):
    page = javascript_link(link)
    body = page.find('body')
    div = body.find('section',role='main').find('div',class_='padding-top padding-bottom').find_all('section')

    for i in div:
        in_course = []
        if(count==5 or count==28 or count==29 or count==31 or count==42):
            try:
                sec = i.find('div',class_='col-md-8').find('ul').find('li',class_='accordion-item')
            except:
                break
        else:
            try:
                sec = i.find('div',class_='col-md-8').find('ul').find('div',class_='accordion-item')
            except:
                break

        try:
            div_tag = sec.find('div',class_='accordion-item__content').find('div',class_='list-group').find_all('a',class_='list-group-item')
        except:
            break

        #print(div_tag)
        for k in div_tag:
            links = k.attrs['href']
            in_course.append(links)
            #print(links)
        main_courses(count,in_course)

def main_courses(count,in_course):
    for i in in_course:
        subject = ""
        page = javascript_link(i)
        body = page.find('body')

        course_name = body.find('section',role='main').find('div',class_='page-intro__wrapper').find('div',class_='page-intro__text').find('h1').text

        try:
            sec = body.find('section',role='main').find('div',class_='container course').find_all('div',class_='row')[1].find('div',class_='col-lg-8')
            ul = sec.find('ul').find_all('li')

            print(count.__str__() + " " + course_name + " " + i)

            for j in range(0,len(ul)):
                try:
                    div = sec.find('div',class_='tab-content').find_all('div')[j].find('ul').find_all('li')
                    year = ul[j].text
                    print(year)
                    for k in range(0,len(div)):
                        try:
                            subject = div[k].find('strong').text
                            clist.append(course(count, course_name, i, year, subject))
                            #print(" " + subject)

                        except:
                            subject = div[k].text
                            clist.append(course(count, course_name, i, year, subject))
                            #print(" " + subject)
                except:
                    div = sec.find('div',class_='tab-content').find_all('div')[j].find('p')
                    subject = div.text
                    clist.append(course(count, course_name, i, year, subject))
                    #print(" " + subject)

                print('\n')
            print('\n')
        except:
            sec = body.find('section',role='main').find('section',
                                                        class_='').find('div',
                                                        class_='container padding-top--half padding-bottom--half').find_all('div',
                                                        class_='row')[1].find('div',class_='col-sm-8').find('ul').find_all('li')

            for x in sec:
                subject = x.find('strong').text
                year = "Year 1"
                #print(year)
                #print(" " + subject)
                clist.append(course(count, course_name, i, year, subject))
                print('\n')

if __name__ == '__main__':
    clist = []
    url = "https://www.st-andrews.ac.uk/subjects/"
    html_page = simple_link(url)
    category(html_page)

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\andrews.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)