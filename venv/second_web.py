from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
from courses_list import course
from openpyxl import load_workbook,Workbook

def simple_link(url):                                                                           #non javascript
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url,headers=headers)
    html = BeautifulSoup(page.content, 'html.parser')
    return html

if __name__ == '__main__':
    clist = []
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


        if(count!=83 and count!=84 and count!=101 and count!=111 and count!=112 and count!=120):                                         #Course 101 -> BSc mathematics is widhdrawn.
            div = page.find('div',id='content-box').find('div',id='page').find('div',class_='container content-template course-template').find('div',class_='row top flow-opposite').find('div',class_='col lg-9 wysiwyg')
            div_module = div.find_all('div',class_='module')

            inside_module=div_module[1].find_all('div')

            if(count==1 or count==2 or count==6 or count==7 or count==8 or count==26 or count==27 or count==28 or count==35 or count==36 or count==26 or count==55 or count==58 or count==60 or count==61 or count==62 or count==78or count==80 or count==81 or count==117 or count==118):
                inside_module = inside_module[7]
                #print(count.__str__() + " " + "found")
                #print(inside_module)
                #year = item.find('h3').text

            else:
                if(count==5 or count==12 or count==24 or count==38 or count==57 or count==68 or count==76 or count==77 or count==88 or count==90 or count==108 or count==110 or count==113 or count==119):
                    inside_module = inside_module[8]
                    #print(inside_module)

                elif(count==25 or count==59 or count==63 or count==64 or count==56 or count==94 or count==95 or (count>=102 and count<=107)):
                    inside_module = inside_module[6]
                    #print(inside_module)

                elif(count==65 or count==66 or count==67 or count==91 or count==92 or count==93 or (count>=96 and count<=100) or (count>=114 and count<=116)):
                    inside_module = inside_module[5]

                elif(count==10 or count==11 or count==15 or count==16 or count==30 or count==31 or count==34 or count==41 or count==44 or count==46 or count==48 or count==51 or count==70 or count==71):
                    inside_module = inside_module[10]
                    #print(inside_module)

                elif((count>=17 and count<=19) or count==23 or count==45 or count==74):
                    inside_module = inside_module[12]
                    #print(inside_module)


                elif((count>=20 and count<=22) or count==47 or count==49 or count==53 or count==54 or count==72):
                    inside_module = inside_module[11]
                    #print(inside_module)

                elif(count==75):
                    inside_module = inside_module[13]

                else:
                    inside_module = inside_module[9]
            #print(count.__str__() + " " + "not found")
                #print(inside_module)

            #item = inside_module.find_all('div', class_='item')

            print(count.__str__() + ": " + coures_code + " " + course_title + " " + dept + " " + duration + " ")
            for i in inside_module.find_all('div',class_='item'):
                year = i.find('h3').text
                ul = i.find('ul')

                try:
                    xx = ul.find_all('li')
                    for j in ul.find_all('li'):
                        cc = j.text
                        clist.append(course(count, course_title, link, year, cc))
                        #print(" " + year + " " + course)

                except:
                    p = i.find('p')
                    cc = p.text
                    clist.append(course(count, course_title, link, year, cc))
                    #print(" " + year + " " + course)
            print('\n')

        else:
            clist.append(course(count, course_title, link, "Null", "Null"))
            print("Proble with page " + count.__str__() + "\n")

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\imperial.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)