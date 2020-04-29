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

        if(count!=82 and count!=83 and count!=84):
            div = page.find('div',id='content-box').find('div',id='page').find('div',class_='container content-template course-template').find('div',class_='row top flow-opposite').find('div',class_='col lg-9 wysiwyg')
            div_module = div.find_all('div',class_='module')

            inside_module=div_module[1].find_all('div')

            if(count==1 or count==2 or count==6 or count==7 or count==8 or count==26 or count==27 or count==28 or count==35 or count==36 or count==26 or count==55 or count==58 or count==60 or count==61 or count==62 or count==78or count==80 or count==81):
                inside_module = inside_module[7]
                #print(count.__str__() + " " + "found")
                #print(inside_module)
                #year = item.find('h3').text

            else:
                if(count==5 or count==12 or count==24 or count==38):
                    inside_module = inside_module[8]
                    #print(inside_module)

                elif(count==25):
                    inside_module = inside_module[6]
                    #print(inside_module)

                elif(count==10 or count==11 or count==15 or count==16 or count==30 or count==31 or count==34 or count==41 or count==44 or count==46 or count==48 or count==51):
                    inside_module = inside_module[10]
                    #print(inside_module)

                elif((count>=17 and count<=19) or count==23 or count==45):
                    inside_module = inside_module[12]
                    #print(inside_module)


                elif((count>=20 and count<=22) or count==47 or count==49 or count==53 or count==54):
                    inside_module = inside_module[11]
                    #print(inside_module)

                elif(count==56):
                    inside_module = inside_module[6]

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
                        course = j.text
                        print(" " + year + " " + course)

                except:
                    p = i.find('p')
                    course = p.text
                    print(" " + year + " " + course)
            print('\n')

        else:
            print("Proble with page " + count.__str__())