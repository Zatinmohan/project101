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

def inside_course():
    count=0
    for i in llist:
        count+=1
        page = javascript_link(i)
        body = page.find('body')
        course_name = body.find('h1').text
        print(count.__str__() + " " + course_name + " " + i)

        if(count==118 or count==215):
            subject = "Null"
            year = "Null"
            print(year + " " + subject)
            clist.append(course(count, course_name, i, year, subject))
        elif(i.find('short-courses')>=0):
           try:
              div = body.find('div',
                              class_='ui-accordion-content ui-helper-reset ui-widget-content ui-corner-bottom ui-accordion-content-active c1')
              li = div.find('ul').find_all('li')
              for j in li:
                  subject = j.text
                  print(subject)
                  clist.append(course(count, course_name, i, "Learning", subject))
           except:
               try:
                  div = body.find('div',class_='row section-fw-white').find('div',class_='panel-content').find('ul').find_all('li')
                  for j in div:
                     subject = j.text
                     print(subject)
                     clist.append(course(count, course_name, i, "Learning", subject))
               except:
                   div = body.find('div', class_='responsive-tabs').find('div', id='outcomes').find_all('p')
                   for j in div:
                       try:
                           subject = j.find('strong').text
                           print(subject)
                           clist.append(course(count, course_name, i, "Learning", subject))
                       except:
                           subject = j.find('p').text
                           print(subject)
                           clist.append(course(count, course_name, i, "Learning", subject))

        elif(i.find('undergraduate')>=0):
            try:
                div = body.find('div', class_='white-box').find('div',
                                                                class_='popup-def-list-group popup-def-list-group--yellow')
                d_tag = div.find_all('div')
                for j in range(0, len(d_tag)):
                    year = d_tag[j].find_previous('h4').text
                    print(year)

                    li = d_tag[j].find('ul').find_all('li')
                    for k in li:
                        subject = k.text
                        print(subject)
                        clist.append(course(count, course_name, i, year, subject))
            except:
                div = body.find_all('div', class_='fw-section-wrapper')[5].find_all('div', class_='col-sm-12')[1].find_all(
                     'div', class_='ui-accordion-content ui-helper-reset ui-widget-content ui-corner-bottom')

                for j in div:
                    year = j.find_previous('h3').text
                    print(year)
                    try:
                        li = j.find('ul').find_all('li')
                        for k in li:
                            subject = k.text
                            print(' ' + subject)
                            clist.append(course(count, course_name, i, year, subject))
                    except:
                        subject = j.find('p').text
                        print(subject)
                        clist.append(course(count, course_name, i, year, subject))


        elif (i.find('cpd') >= 0):
            div = body.find('div', id='eligibilty')
            try:
                li = div.find('ul').find_all('li')
                for j in li:
                    subject = j.text
                    print(subject)
                    clist.append(course(count, course_name, i, "Eligibility", subject))
            except:
                try:
                   p = div.find('p')
                   subject = p.text
                   print(subject)
                   clist.append(course(count, course_name, i, "Eligibility", subject))
                except:
                 print("Do Nothing..")
                 clist.append(course(count, course_name, i, "Null", "Null"))

        elif (i.find('postgraduate') >= 0):
            div = body.find('div', class_='course course-pg').find_all('div', class_='fw-section-wrapper')[5]
            div = div.find_all('div', class_='ui-accordion-content ui-helper-reset ui-widget-content ui-corner-bottom')

            if(len(div)!=0):
                for j in div:
                    year = j.find_previous('h3',
                                           class_='ui-accordion-header ui-helper-reset ui-state-default ui-corner-all ui-accordion-icons').text
                    print(year)
                    p = j.find_all('p')
                    for k in p:
                        subject = k.text
                        print(' ' + subject)
                        clist.append(course(count, course_name, i, year, subject))
            else:
                div = body.find('div', class_='course course-pg').find_all('div', class_='fw-section-wrapper')[4]
                div = div.find_all('div',
                                   class_='ui-accordion-content ui-helper-reset ui-widget-content ui-corner-bottom')

                for j in div:
                    year = j.find_previous('h3',
                                           class_='ui-accordion-header ui-helper-reset ui-state-default ui-corner-all ui-accordion-icons').text
                    print(year)
                    p = j.find_all('p')
                    for k in p:
                        subject = k.text
                        print(' ' + subject)
                        clist.append(course(count, course_name, i, year, subject))

        elif (i.find('executive-education') >= 0):
            div = body.find('div', class_='left-hand-navigation-grid__body')
            year = div.find_all('h2')[1].text
            subject = div.find_next('p').text
            print(year)
            print(' ' + subject)
            clist.append(course(count, course_name, i, year, subject))

        elif (i.find('masters') >= 0):
            print("DO nothing..")
            clist.append(course(count, course_name, i, "Null", "Null"))

        elif (i.find('research-degrees') >= 0):
            div = body.find_all('div', class_='container container-multiple')[2]
            div = div.find('div', id='structure')
            year = "Structure"
            print(year)
            try:
                li = div.find('ul').find_all('li')
                for j in li:
                    subject = j.text
                    print(' ' + subject)
                    clist.append(course(count, course_name, i, year, subject))

            except:
                p = div.find('p')
                subject = p.text
                print(' ' + subject)
                clist.append(course(count, course_name, i, year, subject))

        print('\n')

if __name__ == '__main__':
    nlist = []
    clist = []
    p=1
    url = 'https://www.city.ac.uk/study/courses'
    backUrl = '?p='

    '''while(p<641):
        print("Page : " + p.__str__())
        purl = url + backUrl +p.__str__()
        html_page = javascript_link(purl)

        body = html_page.find('body')
        div = body.find('div', class_='course-finder__results')

        short = div.find_all('div', class_='course-finder__results__item course-finder__results__item--short-courses')          #For short courses
        cpd = div.find_all('div', class_='course-finder__results__item course-finder__results__item--cpd')                      #For continious coures
        pg = div.find_all('div', class_='course-finder__results__item course-finder__results__item--postgraduate')              #PG courses
        ug = div.find_all('div', class_='course-finder__results__item course-finder__results__item--undergraduate')             #UG courses
        fo = div.find_all('div', class_='course-finder__results__item course-finder__results__item--foundation')                #Foundation courses
        red = div.find_all('div', class_='course-finder__results__item course-finder__results__item--research-degrees')         #Research Courses
        exe = div.find_all('div', class_='course-finder__results__item course-finder__results__item--executive-education')      #Distance education

        for i in short:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        for i in cpd:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        for i in pg:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        for i in ug:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        for i in fo:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        for i in exe:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            llist.append(course_name)

        for i in red:
            course_name = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').text
            link = i.find('div', 'col-sm-24 col-md-18 col-lg-20').find('h2').find('a').attrs['href']
            llist.append(link)
            nlist.append(course_name)

        p+=10

    print(llist)'''

    llist =  ['https://www.city.ac.uk/study/courses/short-courses/courses/.net-core-web-applications-for-the-cloud',
     'https://www.city.ac.uk/study/courses/short-courses/courses/.net-object-oriented-programming-using-c',
     'https://www.city.ac.uk/study/courses/short-courses/courses/accounting-for-the-small-business',
     'https://www.city.ac.uk/study/courses/cpd/abdominal-ultrasound',
     'https://www.city.ac.uk/study/courses/cpd/develop-your-communication-skills-and-make-a-difference',
     'https://www.city.ac.uk/study/courses/cpd/acquired-language-impairments',
     'https://www.city.ac.uk/study/courses/postgraduate/academic-practice',
     'https://www.cass.city.ac.uk/study/masters/courses/actuarial-management',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/accounting-and-finance',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/accounting-and-finance-foundation',
     'https://www.city.ac.uk/study/courses/short-courses/courses/adobe-illustrator',
     'https://www.city.ac.uk/study/courses/cpd/Acute-and-High-Dependency-Care-Core-Skills',
     'https://www.city.ac.uk/study/courses/cpd/acute-and-high-dependency-care-specialist-role-development',
     'https://www.city.ac.uk/study/courses/cpd/adolescent-sexual-health',
     'https://www.city.ac.uk/study/courses/cpd/adult-dysphagia-training',
     'https://www.cass.city.ac.uk/study/masters/courses/actuarial-science',
     'https://www.city.ac.uk/study/courses/postgraduate/adult-mental-health-nursing-pre-registration',
     'https://www.city.ac.uk/study/courses/postgraduate/adult-mental-health',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/actuarial-science',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/actuarial-science-foundation',
     'https://www.city.ac.uk/study/courses/short-courses/courses/advanced-autocad-3d',
     'https://www.city.ac.uk/study/courses/short-courses/courses/advanced-database-concepts-with-sql-server',
     'https://www.city.ac.uk/study/courses/cpd/Advanced-Physical-Assessment-across-the-lifespan-neonate',
     'https://www.city.ac.uk/study/courses/cpd/advanced-physical-assessment-critical-thinking-and-diagnostic-reasoning-across-the-lifespan',
     'https://www.city.ac.uk/study/courses/cpd/advanced-criminal-advocacy',
     'https://www.city.ac.uk/study/courses/cpd/advanced-data-analysis',
     'https://www.city.ac.uk/study/courses/postgraduate/adult-nursing-pre-registration',
     'https://www.city.ac.uk/study/courses/postgraduate/advanced-clinical-practice',
     'https://www.city.ac.uk/study/courses/postgraduate/mechanical-engineering',
     'https://www.city.ac.uk/study/courses/undergraduate/adult-nursing',
     'https://www.city.ac.uk/study/courses/short-courses/courses/advanced-web-interfaces-with-css3-and-html5',
     'https://www.city.ac.uk/study/courses/cpd/advanced-ophthalmic-examination',
     'https://www.city.ac.uk/study/courses/cpd/advanced-research-methods',
     'https://www.city.ac.uk/study/courses/cpd/group-ante-natal-care',
     'https://www.city.ac.uk/study/courses/cpd/advancing-skills-and-knowledge-in-advanced-neonatal-practice-refresher-course',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/advocacy',
     'https://www.city.ac.uk/study/courses/postgraduate/advanced-ophthalmic-nurse-practitioner',
     'https://www.city.ac.uk/study/courses/postgraduate/air-safety-management',
     'https://www.city.ac.uk/study/courses/undergraduate/aeronautical-engineering-meng',
     'https://www.city.ac.uk/study/courses/undergraduate/beng-aeronautical-engineering',
     'https://www.city.ac.uk/study/courses/short-courses/courses/an-approach-to-creative-writing',
     'https://www.city.ac.uk/study/courses/short-courses/courses/an-approach-to-creative-writing-summer-school',
     'https://www.city.ac.uk/study/courses/cpd/an-overview-to-contraception',
     'https://www.city.ac.uk/study/courses/cpd/an-introduction-to-abdominal-wall-and-groin-ultrasound',
     'https://www.city.ac.uk/study/courses/cpd/an-introduction-to-sexual-health',
     'https://www.city.ac.uk/study/courses/cpd/aml-and-counter-terrorism-financing-course',
     'https://www.city.ac.uk/study/courses/postgraduate/air-transport-management',
     'https://www.city.ac.uk/study/courses/postgraduate/aircraft-maintenance-management',
     'https://www.city.ac.uk/study/courses/postgraduate/airport-management',
     'https://www.cass.city.ac.uk/study/executive-education/custom-programmes/anti-money-laundering',
     'https://www.city.ac.uk/study/courses/short-courses/courses/applied-ms-excel-for-business',
     'https://www.city.ac.uk/study/courses/short-courses/courses/arabic-beginners-year-1',
     'https://www.city.ac.uk/study/courses/short-courses/courses/arabic-beginners-fast-track',
     'https://www.city.ac.uk/study/courses/short-courses/courses/arabic-lower-intermediate-year-2',
     'https://www.city.ac.uk/study/courses/short-courses/courses/arabic-year-3-upper-intermediate',
     'https://www.city.ac.uk/study/courses/cpd/assessing-and-understanding-mental-health-problems',
     'https://www.city.ac.uk/study/courses/cpd/level-7-assessment-of-minor-injuries-and-illness-for-advanced-practice',
     'https://www.city.ac.uk/study/courses/cpd/asthma-and-chronic-obstructive-pulmonary-disease-bsc',
     'https://www.city.ac.uk/study/courses/cpd/asthma-and-chronic-obstructive-pulmonary-disease-msc',
     'https://www.city.ac.uk/study/courses/postgraduate/artificial-intelligence',
     'https://www.city.ac.uk/study/courses/short-courses/courses/autocad-masterclass-professional-drawing-production-and-management',
     'https://www.city.ac.uk/study/courses/short-courses/courses/bank-financial-management-incorporating-banking-finance-development',
     'https://www.city.ac.uk/study/courses/cpd/autism-informed-practice',
     'https://www.city.ac.uk/study/courses/cpd/basic-travel-health-introductory-course-for-nurses-and-qualified-professionals',
     'https://www.city.ac.uk/study/courses/cpd/beautifully-basic-core-concepts-of-quantitative-research',
     'https://www.cass.city.ac.uk/study/masters/courses/banking-and-international-finance',
     'https://www.city.ac.uk/study/courses/postgraduate/bar-vocational-studies',
     'https://www.city.ac.uk/study/courses/postgraduate/bar-vocational-studies-part-time',
     'https://www.city.ac.uk/study/courses/postgraduate/bar-vocational-studies-two-part',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/banking-and-international-finance',
     'https://www.city.ac.uk/study/courses/short-courses/courses/build-a-website-in-a-week-using-html5-and-css3',
     'https://www.city.ac.uk/study/courses/short-courses/courses/building-communication-skills',
     'https://www.city.ac.uk/study/courses/cpd/Biological-Foundation-in-Clinical-Practice-and-Related-Pharmacology',
     'https://www.city.ac.uk/study/courses/cpd/blockchain-and-cryptocurrencies',
     'https://www.city.ac.uk/study/courses/cpd/bsl-production-test-training-course',
     'https://www.city.ac.uk/study/courses/postgraduate/behavioural-economics',
     'https://www.city.ac.uk/study/courses/postgraduate/broadcast-journalism',
     'https://www.city.ac.uk/study/courses/undergraduate/biomedical-engineering',
     'https://www.city.ac.uk/study/courses/undergraduate/beng-biomedical-engineering',
     'https://www.cass.city.ac.uk/study/executive-education/our-programmes/becoming-an-effective-leader-for-aspiring-leaders',
     'https://www.city.ac.uk/study/courses/short-courses/courses/building-websites-with-html5-and-css3',
     'https://www.city.ac.uk/study/courses/short-courses/courses/introduction-to-programming-with-c',
     'https://www.cass.city.ac.uk/study/masters/courses/business-analytics',
     'https://www.city.ac.uk/study/courses/postgraduate/business-economics-international-business-economics',
     'https://www.city.ac.uk/study/courses/postgraduate/business-systems-analysis-and-design',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/business-management',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/business-management-digital-innovation-entrepreneurship',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/business-with-finance',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/business-with-marketing',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/business-management-foundation',
     'https://www.city.ac.uk/study/courses/short-courses/courses/object-oriented-programming-using-c',
     'https://www.city.ac.uk/study/courses/cpd/Cardiac-Care-Specialist-Role-Development',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/case-management-and-interim-procedures',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/case-planning-and-preparation',
     'https://www.city.ac.uk/study/courses/cpd/case-based-clinical-application',
     'https://www.city.ac.uk/study/courses/cpd/cervical-cytology-bsc',
     'https://www.city.ac.uk/study/courses/cpd/cervical-cytology-msc',
     'https://www.cass.city.ac.uk/study/masters/courses/charity-accounting-and-financial-management',
     'https://www.cass.city.ac.uk/study/masters/courses/charity-marketing-and-fundraising',
     'https://www.city.ac.uk/study/courses/short-courses/courses/chinese-mandarin-beginners-year-1',
     'https://www.city.ac.uk/study/courses/short-courses/courses/chinese-mandarin-beginners-refreshers',
     'https://www.city.ac.uk/study/courses/cpd/child-and-adolescent-mental-health-early-identification-and-assessment-camh',
     'https://www.city.ac.uk/study/courses/cpd/child-and-adolescent-mental-health-therapeutic-approaches-and-the-evidence-base',
     'https://www.city.ac.uk/study/courses/cpd/child-development-and-communication',
     'https://www.city.ac.uk/study/courses/cpd/Child-Protection-Working-Together-Risk-and-Resilience-BSc',
     'https://www.city.ac.uk/study/courses/cpd/Child-Protection-Working-Together-Risk-and-Resilience-MSc',
     'https://www.city.ac.uk/study/courses/postgraduate/child-and-adolescent-mental-health',
     'https://www.city.ac.uk/study/courses/postgraduate/childrens-nursing-pre-registration',
     'https://www.city.ac.uk/study/courses/undergraduate/child-nursing',
     'https://www.city.ac.uk/study/courses/short-courses/courses/chinese-mandarin-beginners-summer-intensive-year-1',
     'https://www.city.ac.uk/study/courses/short-courses/courses/chinese-mandarin-fast-track',
     'https://www.city.ac.uk/study/courses/short-courses/courses/chinese-mandarin-lower-intermediate-year-3',
     'https://www.city.ac.uk/study/courses/short-courses/courses/chinese-mandarin-upper-intermediate-year-4',
     'https://www.city.ac.uk/study/courses/postgraduate/civil-engineering-structures',
     'https://www.city.ac.uk/study/courses/postgraduate/civil-engineering-structures-nuclear-power-plants',
     'https://www.city.ac.uk/study/courses/undergraduate/civil-engineering-meng',
     'https://www.city.ac.uk/study/courses/undergraduate/civil-engineering-beng',
     'https://www.city.ac.uk/study/courses/undergraduate/civil-engineering-foundation-programme',
     'https://www.city.ac.uk/study/courses/research-degrees/civil-engineering',
     'https://www.city.ac.uk/study/courses/short-courses/courses/coaching-for-business',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/clear-writing-and-drafting',
     'https://www.city.ac.uk/study/courses/cpd/clinical-applications-of-computed-tomography',
     'https://www.city.ac.uk/study/courses/cpd/clinical-applications-of-medical-magnetic-resonance',
     'https://www.city.ac.uk/study/courses/cpd/Clinical-Assessment-in-Primary-Care-BSc',
     'https://www.city.ac.uk/study/courses/cpd/Clinical-Assessment-in-Primary-Care-MSc',
     'https://www.city.ac.uk/study/courses/cpd/clinical-observations-and-recognizing-a-deteriorating-patient',
     'https://www.city.ac.uk/study/courses/postgraduate/civil-litigation-and-dispute-resolution',
     'https://www.city.ac.uk/study/courses/postgraduate/clinical-optometry',
     'https://www.city.ac.uk/study/courses/postgraduate/clinical-social-cognitive-neuroscience',
     'https://www.city.ac.uk/study/courses/cpd/cognitive-communication-impairments',
     'https://www.city.ac.uk/study/courses/cpd/the-conversation-partner',
     'https://www.city.ac.uk/study/courses/cpd/commissioning-for-health-and-social-care2',
     'https://www.city.ac.uk/study/courses/cpd/common-dermatological-conditions',
     'https://www.city.ac.uk/study/courses/cpd/comparative-imaging',
     'https://www.city.ac.uk/study/courses/postgraduate/computer-games-technology',
     'https://www.city.ac.uk/study/courses/undergraduate/computer-science',
     'https://www.city.ac.uk/study/courses/undergraduate/computer-science-msci',
     'https://www.city.ac.uk/study/courses/undergraduate/computer-science-cyber-security-msci',
     'https://www.city.ac.uk/study/courses/research-degrees/computer-science',
     'https://www.city.ac.uk/study/courses/cpd/contact-lenses',
     'https://www.city.ac.uk/study/courses/cpd/contemporary-issues-in-mental-health',
     'https://www.city.ac.uk/study/courses/cpd/contemporary-nursing-midwifery-knowledge',
     'https://www.city.ac.uk/study/courses/cpd/contraception-and-reproductive-sexual-health-care-current-issues-and-practice',
     'https://www.city.ac.uk/study/courses/cpd/contraception-and-sexual-health-theory',
     'https://www.city.ac.uk/study/courses/cpd/contraception-for-hcas',
     'https://www.city.ac.uk/study/courses/cpd/contraception-update',
     'https://www.city.ac.uk/study/courses/postgraduate/construction-management',
     'https://www.city.ac.uk/study/courses/undergraduate/computer-science-games-technology-msci',
     'https://www.city.ac.uk/study/courses/undergraduate/computer-science-with-games-technology',
     'https://www.city.ac.uk/study/courses/short-courses/courses/creating-mobile-apps-with-android',
     'https://www.city.ac.uk/study/courses/short-courses/courses/crime-and-thriller-writing',
     'https://www.city.ac.uk/study/courses/short-courses/courses/crime-writing-summer-school',
     'https://www.city.ac.uk/study/courses/cpd/counselling-skills-workshop',
     'https://www.cass.city.ac.uk/study/masters/courses/corporate-finance',
     'https://www.city.ac.uk/study/courses/postgraduate/creative-writing',
     'https://www.city.ac.uk/study/courses/postgraduate/creative-writing-and-publishing',
     'https://www.city.ac.uk/study/courses/postgraduate/creative-writing-mfa',
     'https://www.city.ac.uk/study/courses/postgraduate/criminal-litigation',
     'https://www.city.ac.uk/study/courses/undergraduate/criminology',
     'https://www.city.ac.uk/study/courses/short-courses/courses/curating-and-exhibition-management',
     'https://www.city.ac.uk/study/courses/cpd/critical-approaches-in-advanced-practice',
     'https://www.city.ac.uk/study/courses/cpd/critical-thinking-and-diagnostic-reasoning-neonatal',
     'https://www.city.ac.uk/study/courses/cpd/critical-thinking-for-ophthalmic-practice',
     'https://www.city.ac.uk/study/courses/postgraduate/criminology',
     'https://www.city.ac.uk/study/courses/postgraduate/culture-policy-and-management',
     'https://www.city.ac.uk/study/courses/postgraduate/cyber-security',
     'https://www.city.ac.uk/study/courses/undergraduate/criminology-psychology',
     'https://www.city.ac.uk/study/courses/undergraduate/criminology-sociology',
     'https://www.city.ac.uk/study/courses/research-degrees/culture-creative-industries-phd-mphil',
     'https://www.city.ac.uk/study/courses/short-courses/courses/cyber-security-fundamentals',
     'https://www.city.ac.uk/study/courses/short-courses/courses/database-design-with-sql-server',
     'https://www.city.ac.uk/study/courses/cpd/cytology-update',
     'https://www.city.ac.uk/study/courses/cpd/dementia-awareness-full-day',
     'https://www.city.ac.uk/study/courses/cpd/dementia-awareness-half-day',
     'https://www.city.ac.uk/study/courses/cpd/developing-advanced-practice',
     'https://www.city.ac.uk/study/courses/postgraduate/data-science-msc',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/data-analytics-and-actuarial-science',
     'https://www.city.ac.uk/study/courses/undergraduate/data-science',
     'https://www.cass.city.ac.uk/study/executive-education/our-programmes/core-consulting-skills',
     'https://www.city.ac.uk/study/courses/short-courses/courses/digital-filmmaking-practical-introduction',
     'https://www.city.ac.uk/study/courses/short-courses/courses/digital-marketing-fundamentals',
     'https://www.city.ac.uk/study/courses/cpd/developmental-language-impairment',
     'https://www.city.ac.uk/study/courses/cpd/diabetes-care',
     'https://www.city.ac.uk/study/courses/cpd/diabetes-care-msc',
     'https://www.city.ac.uk/study/courses/cpd/diabetes-mellitus',
     'https://www.city.ac.uk/study/courses/cpd/diabetes-mellitus-for-practice-nurses',
     'https://www.city.ac.uk/study/courses/cpd/disability-awareness-for-professionals-working-in-the-justice-system',
     'https://www.city.ac.uk/study/courses/postgraduate/development-economics',
     'https://www.city.ac.uk/study/courses/postgraduate/diplomacy-and-foreign-policy',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/discrimination-law',
     'https://www.city.ac.uk/study/courses/cpd/domestic-violence-and-abuse-awareness-training',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/drafting-statements-of-case',
     'https://www.city.ac.uk/study/courses/cpd/dysphagia-and-disorders-of-eating-and-drinking',
     'https://www.city.ac.uk/study/courses/cpd/e-disclosure', 'https://www.city.ac.uk/study/courses/cpd/ear-care',
     'https://www.city.ac.uk/study/courses/cpd/ear-nose-and-throat-head-and-neck-core-skills',
     'https://www.city.ac.uk/study/courses/cpd/early-pregnancy-ultrasound',
     'https://www.city.ac.uk/study/courses/postgraduate/economic-evaluation-in-health-care',
     'https://www.city.ac.uk/study/courses/postgraduate/economics',
     'https://www.city.ac.uk/study/courses/postgraduate/energy-and-environmental-technology-and-economics',
     'https://www.cass.city.ac.uk/study/masters/courses/energy-trade-and-finance',
     'https://www.city.ac.uk/study/courses/undergraduate/economics-bsc',
     'https://www.city.ac.uk/study/courses/undergraduate/economics-with-accounting',
     'https://www.city.ac.uk/study/courses/undergraduate/electrical-electronic-engineering-meng',
     'https://www.city.ac.uk/study/courses/undergraduate/electrical-electronic-engineering-beng',
     'https://www.city.ac.uk/study/courses/undergraduate/electrical-and-electronic-engineering-foundation-programmes',
     'https://www.cass.city.ac.uk/study/executive-education/our-programmes/effective-negotiation-skills-influencing-with-impact',
     'https://www.city.ac.uk/study/courses/research-degrees/economics',
     'https://www.city.ac.uk/study/courses/research-degrees/electrical-and-electronic-engineering',
     'https://www.city.ac.uk/study/courses/cpd/Engaging-Technology',
     'https://www.city.ac.uk/study/courses/cpd/epidemiology2',
     'https://www.city.ac.uk/study/courses/postgraduate/english',
     'https://www.city.ac.uk/study/courses/postgraduate/midwifery-advanced-practice',
     'https://www.cass.city.ac.uk/study/masters/courses/entrepreneurship',
     'https://www.city.ac.uk/study/courses/postgraduate/journalism-media-and-globalisation',
     'https://www.city.ac.uk/study/courses/undergraduate/engineering-meng',
     'https://www.city.ac.uk/study/courses/undergraduate/engineering-beng',
     'https://www.city.ac.uk/study/courses/undergraduate/english',
     'https://www.city.ac.uk/study/courses/research-degrees/english',
     'https://www.city.ac.uk/study/courses/cpd/essential-skills-for-health-care-support-workers-in-primary-care',
     'https://www.city.ac.uk/study/courses/cpd/evidence-based-dementia-care',
     'https://www.city.ac.uk/study/courses/cpd/evidence-based-practice2',
     'https://www.city.ac.uk/study/courses/cpd/Evidence-Based-Health-Care-e-learning',
     'https://www.city.ac.uk/study/courses/cpd/evidence-based-psychosocial-interventions-in-mental-health',
     'https://www.city.ac.uk/study/courses/postgraduate/european-law',
     'https://www.cass.city.ac.uk/study/mba/executive-mba',
     'https://www.cass.city.ac.uk/study/mba/executive-mba-in-dubai',
     'https://www.city.ac.uk/study/courses/short-courses/courses/fact-based-storytelling',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/expert-witness-training',
     'https://www.cass.city.ac.uk/study/masters/courses/finance',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/finance',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/finance-foundation',
     'https://www.cass.city.ac.uk/study/executive-phd',
     'https://www.city.ac.uk/study/courses/short-courses/courses/finance-for-the-non-financial-manager',
     'https://www.city.ac.uk/study/courses/short-courses/courses/financial-engineering-in-interest-rates-and-fx-c-applications',
     'https://www.city.ac.uk/study/courses/short-courses/courses/financial-modelling-in-excel',
     'https://www.city.ac.uk/study/courses/postgraduate/financial-economics',
     'https://www.city.ac.uk/study/courses/postgraduate/financial-journalism',
     'https://www.cass.city.ac.uk/study/masters/courses/financial-mathematics',
     'https://www.city.ac.uk/study/courses/postgraduate/food-policy',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/finance-with-actuarial-science',
     'https://www.city.ac.uk/study/courses/undergraduate/financial-economics',
     'https://www.cass.city.ac.uk/study/executive-education/our-programmes/finance-for-non-finance-leaders',
     'https://www.city.ac.uk/study/courses/short-courses/courses/freelance-writing',
     'https://www.city.ac.uk/study/courses/short-courses/courses/french-beginners-year-1',
     'https://www.city.ac.uk/study/courses/short-courses/courses/french-beginners-fast-track',
     'https://www.city.ac.uk/study/courses/short-courses/courses/french-beginners-refreshers',
     'https://www.city.ac.uk/study/courses/short-courses/courses/french-lower-intermediate',
     'https://www.city.ac.uk/study/courses/short-courses/courses/french-upper-intermediate',
     'https://www.city.ac.uk/study/courses/cpd/foundation-programme-for-practice-nurses-who-are-new-to-general-practice',
     'https://www.city.ac.uk/study/courses/cpd/foundations-in-research-methods-and-data-analysis',
     'https://www.city.ac.uk/study/courses/cpd/foundations-in-research-methods-and-data-analysis-online-module',
     'https://www.city.ac.uk/study/courses/research-degrees/food-policy',
     'https://www.city.ac.uk/study/courses/short-courses/courses/german-year1-beginners',
     'https://www.city.ac.uk/study/courses/short-courses/courses/german-beginners-fast-track',
     'https://www.city.ac.uk/study/courses/short-courses/courses/german-lower-intermediate-year-2',
     'https://www.city.ac.uk/study/courses/short-courses/courses/german-year-3-upper-intermediate',
     'https://www.city.ac.uk/study/courses/cpd/fundamental-clinical-skills-general-wound-care',
     'https://www.city.ac.uk/study/courses/cpd/global-health',
     'https://www.cass.city.ac.uk/study/mba/full-time',
     'https://www.city.ac.uk/study/courses/postgraduate/global-creative-industries',
     'https://www.city.ac.uk/study/courses/postgraduate/global-political-economy',
     'https://www.cass.city.ac.uk/study/masters/courses/global-supply-chain-management',
     'https://www.city.ac.uk/study/courses/cpd/gynaecology-ultrasound',
     'https://www.city.ac.uk/study/courses/cpd/habilitative-audiology',
     'https://www.city.ac.uk/study/courses/cpd/head-and-neck',
     'https://www.city.ac.uk/study/courses/cpd/health-policy-in-britain',
     'https://www.city.ac.uk/study/courses/postgraduate/graduate-diploma-law-gdl',
     'https://www.city.ac.uk/study/courses/postgraduate/graduate-entry-llb',
     'https://www.cass.city.ac.uk/study/masters/courses/grantmaking-philanthropy-and-social-investment',
     'https://www.city.ac.uk/study/courses/postgraduate/health-economics',
     'https://www.city.ac.uk/study/courses/postgraduate/health-management',
     'https://www.city.ac.uk/study/courses/postgraduate/health-policy',
     'https://www.city.ac.uk/study/courses/cpd/Healthcare-Improvement-Project-e-learning',
     'https://www.city.ac.uk/study/courses/cpd/heart-disease-heart-failure-and-prevention-of-heart-disease',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/higher-rights',
     'https://www.city.ac.uk/study/courses/cpd/higher-rights-of-audience',
     'https://www.city.ac.uk/study/courses/cpd/how-to-be-an-evidence-based-optometrist',
     'https://www.city.ac.uk/study/courses/undergraduate/history',
     'https://www.city.ac.uk/study/courses/undergraduate/history-and-politics',
     'https://www.city.ac.uk/study/courses/research-degrees/health-sciences',
     'https://www.city.ac.uk/study/courses/short-courses/courses/human-resource-management',
     'https://www.city.ac.uk/study/courses/short-courses/courses/human-rights-law',
     'https://www.city.ac.uk/study/courses/short-courses/courses/immigration-law-an-introduction',
     'https://www.city.ac.uk/study/courses/short-courses/courses/indesign-an-introduction',
     'https://www.city.ac.uk/study/courses/cpd/identity-inclusion-and-living-with-disability',
     'https://www.city.ac.uk/study/courses/cpd/immunisation',
     'https://www.city.ac.uk/study/courses/cpd/immunisation-update',
     'https://www.city.ac.uk/study/courses/cpd/independent-and-supplementary-non-medical-prescribing',
     'https://www.city.ac.uk/study/courses/cpd/independent-prescribing',
     'https://www.city.ac.uk/study/courses/postgraduate/human-computer-interaction-design',
     'https://www.city.ac.uk/study/courses/postgraduate/information-science',
     'https://www.city.ac.uk/study/courses/cpd/Innovation-in-Health-Care-Leadership-and-Management-Perspectives-MSc',
     'https://www.city.ac.uk/study/courses/cpd/innovation-in-health-care-leadership-and-management-perspectives',
     'https://www.city.ac.uk/study/courses/cpd/instrumental-techniques-in-speech-sciences',
     'https://www.city.ac.uk/study/courses/cpd/Intensive-Care-Core-Skills',
     'https://www.city.ac.uk/study/courses/cpd/core-skills-intensive-care',
     'https://www.city.ac.uk/study/courses/cpd/Intensive-Care-Role-Development',
     'https://www.city.ac.uk/study/courses/postgraduate/innovation-and-entrepreneurship-in-healthcare-technology',
     'https://www.cass.city.ac.uk/study/masters/courses/innovation-creativity-and-leadership',
     'https://www.cass.city.ac.uk/study/masters/courses/insurance-and-risk-management',
     'https://www.city.ac.uk/study/courses/postgraduate/interactive-journalism',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/intermediary-training',
     'https://www.cass.city.ac.uk/study/masters/courses/international-accounting-and-finance',
     'https://www.city.ac.uk/study/courses/postgraduate/international-banking-and-finance',
     'https://www.cass.city.ac.uk/study/masters/courses/international-business',
     'https://www.city.ac.uk/study/courses/postgraduate/international-business-law-distance-learning',
     'https://www.city.ac.uk/study/courses/postgraduate/international-commercial-law',
     'https://www.city.ac.uk/study/courses/postgraduate/international-communications-and-development',
     'https://www.city.ac.uk/study/courses/postgraduate/international-dispute-resolution',
     'https://www.city.ac.uk/study/courses/postgraduate/international-economic-law',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/international-business',
     'https://www.city.ac.uk/study/courses/short-courses/courses/international-finance',
     'https://www.city.ac.uk/study/courses/short-courses/courses/international-law-systems-and-organisations',
     'https://www.city.ac.uk/study/courses/cpd/international-health-systems',
     'https://www.city.ac.uk/study/courses/postgraduate/international-energy-law-and-regulation',
     'https://www.city.ac.uk/study/courses/postgraduate/international-human-rights',
     'https://www.city.ac.uk/study/courses/postgraduate/international-journalism',
     'https://www.city.ac.uk/study/courses/postgraduate/international-politics',
     'https://www.city.ac.uk/study/courses/undergraduate/international-political-economy',
     'https://www.city.ac.uk/study/courses/undergraduate/international-politics',
     'https://www.city.ac.uk/study/courses/undergraduate/international-foundation-programme',
     'https://www.city.ac.uk/study/courses/short-courses/courses/introduction-to-autocad-2d-drawing-production',
     'https://www.city.ac.uk/study/courses/short-courses/courses/introduction-to-journalism',
     'https://www.city.ac.uk/study/courses/short-courses/courses/introduction-to-copywriting',
     'https://www.city.ac.uk/study/courses/short-courses/courses/introduction-to-data-analysis-and-machine-learning-with-python',
     'https://www.city.ac.uk/study/courses/cpd/intravenous-cannulation',
     'https://www.city.ac.uk/study/courses/cpd/introduction-to-12-lead-ecg-interpretation',
     'https://www.city.ac.uk/study/courses/postgraduate/international-politics-and-human-rights',
     'https://www.city.ac.uk/study/courses/postgraduate/international-publishing-studies',
     'https://www.city.ac.uk/study/courses/postgraduate/internet-of-things-with-entrepreneurship',
     'https://www.city.ac.uk/study/courses/undergraduate/international-politics-and-sociology',
     'https://www.city.ac.uk/study/courses/short-courses/courses/introduction-to-english-law-and-legal-method',
     'https://www.city.ac.uk/study/courses/short-courses/courses/introduction-to-programming-with-python',
     'https://www.city.ac.uk/study/courses/cpd/the-practice-nurse-distance-learning-module',
     'https://www.city.ac.uk/study/courses/cpd/introduction-to-long-term-conditions',
     'https://www.city.ac.uk/study/courses/cpd/introduction-to-long-term-conditions-msc',
     'https://www.city.ac.uk/study/courses/cpd/mental-capacity-course',
     'https://www.city.ac.uk/study/courses/cpd/introduction-to-minor-injury-and-ailment-management-for-practice-nurses',
     'https://www.city.ac.uk/study/courses/cpd/minor-injuries-management-for-school-nurses',
     'https://www.city.ac.uk/study/courses/undergraduate/introduction-to-health-sciences',
     'https://www.city.ac.uk/study/courses/undergraduate/introduction-optometry',
     'https://www.city.ac.uk/study/courses/short-courses/courses/introduction-to-r-for-data-analysis',
     'https://www.city.ac.uk/study/courses/short-courses/courses/introduction-to-sql-and-relational-databases-with-oracle',
     'https://www.city.ac.uk/study/courses/cpd/introduction-to-research-methods-and-applied-data-analysis',
     'https://www.city.ac.uk/study/courses/cpd/introduction-to-research-methods-and-data-analysis-online-module',
     'https://www.city.ac.uk/study/courses/cpd/introduction-to-rhythm-recognition',
     'https://www.city.ac.uk/study/courses/cpd/introduction-to-ultrasound-report-writing',
     'https://www.city.ac.uk/study/courses/cpd/introductory-immunisation-course-for-healthcare-assistants-and-assistant-practitioners',
     'https://www.city.ac.uk/study/courses/postgraduate/investigative-journalism',
     'https://www.cass.city.ac.uk/study/masters/courses/investment-management',
     'https://www.cass.city.ac.uk/study/undergraduate/courses/investment-and-financial-risk-management',
     'https://www.city.ac.uk/study/courses/short-courses/courses/italian-beginners-year-1',
     'https://www.city.ac.uk/study/courses/short-courses/courses/italian-year-3-intermediate',
     'https://www.city.ac.uk/study/courses/short-courses/courses/italian-lower-intermediate-year-2',
     'https://www.city.ac.uk/study/courses/short-courses/courses/japanese-beginners-year-1',
     'https://www.city.ac.uk/study/courses/short-courses/courses/japanese-beginners-fast-track',
     'https://www.city.ac.uk/study/courses/short-courses/courses/japanese-beginners-refreshers',
     'https://www.city.ac.uk/study/courses/short-courses/courses/japanese-beginners-summer-intensive',
     'https://www.city.ac.uk/study/courses/short-courses/courses/japanese-for-holidays',
     'https://www.city.ac.uk/study/courses/cpd/Issues-in-Advanced-Practice-1',
     'https://www.city.ac.uk/study/courses/cpd/intravenous-therapy',
     'https://www.city.ac.uk/study/courses/short-courses/courses/japanese-lower-intermediate-year-3',
     'https://www.city.ac.uk/study/courses/short-courses/courses/java-object-oriented-programming-with-java-part-1',
     'https://www.city.ac.uk/study/courses/short-courses/courses/java-object-oriented-programming-with-java-part-2',
     'https://www.city.ac.uk/study/courses/short-courses/courses/professional-java-developer-tools-and-best-practices',
     'https://www.city.ac.uk/study/courses/short-courses/courses/javascript-introduction-to-javascript-and-dom-scripting',
     'https://www.city.ac.uk/study/courses/short-courses/courses/advanced-javascript-for-websites-and-web-apps',
     'https://www.city.ac.uk/study/courses/short-courses/courses/korean-beginners-year-1',
     'https://www.city.ac.uk/study/courses/cpd/key-concepts-general-practice-nursing',
     'https://www.city.ac.uk/study/courses/undergraduate/journalism',
     'https://www.city.ac.uk/study/courses/research-degrees/journalism',
     'https://www.city.ac.uk/study/courses/short-courses/courses/leadership-and-management',
     'https://www.city.ac.uk/study/courses/cpd/language-therapy-in-bsl-course',
     'https://www.city.ac.uk/study/courses/cpd/learning-development-and-disorder',
     'https://www.city.ac.uk/study/courses/cpd/law-and-policing-for-intermediaries',
     'https://www.city.ac.uk/study/courses/cpd/Leadership-e-learning',
     'https://www.city.ac.uk/study/courses/cpd/leadership-in-long-term-conditions',
     'https://www.city.ac.uk/study/courses/undergraduate/law',
     'https://www.cass.city.ac.uk/study/executive-education/custom-programmes/leadership-communication-present-yourself-with-lasting-impact',
     'https://www.cass.city.ac.uk/study/executive-education/custom-programmes/leadership-in-a-digital-world',
     'https://www.city.ac.uk/study/courses/research-degrees/law',
     'https://www.city.ac.uk/study/courses/short-courses/courses/learn-japanese-five-day-summer-school',
     'https://www.city.ac.uk/study/courses/cpd/leadership-in-healthcare',
     'https://www.city.ac.uk/study/courses/cpd/education-in-the-workplace3',
     'https://www.city.ac.uk/study/courses/cpd/leading-and-facilitating-learning-in-practice-ptq',
     'https://www.city.ac.uk/study/courses/cpd/leading-care-in-dementia-and-frailty',
     'https://www.city.ac.uk/study/courses/postgraduate/leading-integrated-care',
     'https://www.city.ac.uk/study/courses/postgraduate/legal-practice',
     'https://www.city.ac.uk/study/courses/postgraduate/legal-practice-course',
     'https://www.cass.city.ac.uk/study/executive-education/custom-programmes/leading-business-model-innovation',
     'https://www.cass.city.ac.uk/study/executive-education/our-programmes/digital-transformations',
     'https://www.city.ac.uk/study/courses/cpd/level-7-acute-and-high-dependancy-care-core-skills',
     'https://www.city.ac.uk/study/courses/cpd/neonatal-care-specialist-core-skills-module-2',
     'https://www.city.ac.uk/study/courses/cpd/neonatal-care-specialist-role-development-module-3',
     'https://www.city.ac.uk/study/courses/cpd/acute-and-high-dependency-care-specialist-role-development2',
     'https://www.city.ac.uk/study/courses/cpd/level-7-cardiac-care-specialist-role-development-module-2',
     'https://www.city.ac.uk/study/courses/cpd/level-7-major-trauma-critical-care-patient-management',
     'https://www.city.ac.uk/study/courses/cpd/liaison-mental-health-care',
     'https://www.city.ac.uk/study/courses/cpd/liaison-mental-health-care-msc',
     'https://www.city.ac.uk/study/courses/postgraduate/library-science',
     'https://www.city.ac.uk/study/courses/research-degrees/library-and-information-science',
     'https://www.city.ac.uk/study/courses/short-courses/courses/linux-network-and-system-administration',
     'https://www.city.ac.uk/study/courses/short-courses/courses/linux-server-administration-security',
     'https://www.city.ac.uk/study/courses/short-courses/courses/major-event-management',
     'https://www.city.ac.uk/study/courses/cpd/major-trauma-critical-care-patient-management',
     'https://www.city.ac.uk/study/courses/cpd/makaton-foundation-workshop',
     'https://www.city.ac.uk/study/courses/cpd/makaton-taster-session',
     'https://www.city.ac.uk/study/courses/cpd/making-a-difference-research-and-development-in-care-for-older-people',
     'https://www.city.ac.uk/study/courses/cpd/Making-Sense-of-Clinical-Governance-e-learning',
     'https://www.city.ac.uk/study/courses/cpd/male-urethral-catheterisation-and-catheter-management',
     'https://www.city.ac.uk/study/courses/postgraduate/magazine-journalism',
     'https://www.city.ac.uk/study/courses/cpd/level-7-management-of-minor-injuries-and-illness-for-advanced-practice',
     'https://www.city.ac.uk/study/courses/cpd/managing-challenging-conversations-assertively',
     'https://www.city.ac.uk/study/courses/cpd/Managing-Change-e-learning',
     'https://www.city.ac.uk/study/courses/cpd/managing-staff-through-change',
     'https://www.city.ac.uk/study/courses/cpd/management-course',
     'https://www.cass.city.ac.uk/study/masters/courses/management',
     'https://www.city.ac.uk/study/courses/postgraduate/maritime-law',
     'https://www.city.ac.uk/study/courses/postgraduate/maritime-law-dubai',
     'https://www.city.ac.uk/study/courses/postgraduate/maritime-law-greece',
     'https://www.city.ac.uk/study/courses/postgraduate/maritime-operations-and-management',
     'https://www.city.ac.uk/study/courses/short-courses/courses/marketing',
     'https://www.city.ac.uk/study/courses/postgraduate/maritime-operations-management-greece',
     'https://www.city.ac.uk/study/courses/postgraduate/maritime-safety-and-security-management',
     'https://www.cass.city.ac.uk/study/masters/courses/marketing-strategy-and-innovation',
     'https://www.city.ac.uk/study/courses/postgraduate/master-of-laws',
     'https://www.cass.city.ac.uk/study/masters/courses/mathematical-trading-and-finance',
     'https://www.city.ac.uk/study/courses/undergraduate/mathematics',
     'https://www.city.ac.uk/study/courses/undergraduate/mathematics-finance',
     'https://www.city.ac.uk/study/courses/undergraduate/mathematics-with-finance-and-economics',
     'https://www.city.ac.uk/study/courses/research-degrees/mathematics',
     'https://www.city.ac.uk/study/courses/cpd/medicines-management',
     'https://www.city.ac.uk/study/courses/cpd/mental-capacity-act-training',
     'https://www.city.ac.uk/study/courses/cpd/mental-health-awareness-full-day',
     'https://www.city.ac.uk/study/courses/postgraduate/media-and-communications',
     'https://www.city.ac.uk/study/courses/postgraduate/medical-ultrasound',
     'https://www.city.ac.uk/study/courses/undergraduate/mechanical-engineering-meng',
     'https://www.city.ac.uk/study/courses/undergraduate/beng-mechanical-engineering',
     'https://www.city.ac.uk/study/courses/undergraduate/media-communication-sociology',
     'https://www.city.ac.uk/study/courses/undergraduate/mechanical-and-aeronautical-engineering-foundation-programmes',
     'https://www.city.ac.uk/study/courses/research-degrees/mechanical-engineering-aeronautics',
     'https://www.city.ac.uk/study/courses/short-courses/courses/microsoft-access-database',
     'https://www.city.ac.uk/study/courses/short-courses/courses/microsoft-access-vba-programming',
     'https://www.city.ac.uk/study/courses/short-courses/courses/mobile-journalism',
     'https://www.city.ac.uk/study/courses/cpd/mental-health-awareness-half-day',
     'https://www.city.ac.uk/study/courses/cpd/midwifery-theory-and-professionalism',
     'https://www.city.ac.uk/study/courses/postgraduate/mental-health-nursing-pre-registration',
     'https://www.city.ac.uk/study/courses/postgraduate/midwifery-90-week-shortened-programme-for-nurses',
     'https://www.cass.city.ac.uk/study/mba/modular-executive-mba',
     'https://www.city.ac.uk/study/courses/undergraduate/mental-health-nursing',
     'https://www.city.ac.uk/study/courses/undergraduate/midwifery',
     'https://www.city.ac.uk/study/courses/short-courses/courses/music-business-records-publishing-and-finance',
     'https://www.city.ac.uk/study/courses/short-courses/courses/narrative-non-fiction',
     'https://www.city.ac.uk/study/courses/cpd/my-home-life', 'https://www.city.ac.uk/study/courses/cpd/mhl-leadership',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/negotiation',
     'https://www.city.ac.uk/study/courses/cpd/neonatal-paediatric-cannulation-and-IV-Therapy',
     'https://www.city.ac.uk/study/courses/postgraduate/music-by-research',
     'https://www.city.ac.uk/study/courses/undergraduate/music',
     'https://www.city.ac.uk/study/courses/undergraduate/music-sound-and-technology',
     'https://www.city.ac.uk/study/courses/research-degrees/music',
     'https://www.city.ac.uk/study/courses/cpd/neonatal-care-clinical-decision-making',
     'https://www.city.ac.uk/study/courses/cpd/neonatal-pathophysiological-principles-for-advanced-practice',
     'https://www.city.ac.uk/study/courses/cpd/neonatal-surgical-care',
     'https://www.city.ac.uk/study/courses/cpd/neonatal-ventilation-study-day-for-neonatal-nurses-and-junior-doctors',
     'https://www.city.ac.uk/study/courses/cpd/newborn-assessment-and-examination-for-nurses-and-midwives',
     'https://www.city.ac.uk/study/courses/cpd/12-lead-ecg-and-its-use-in-assessment-of-the-patient',
     'https://www.city.ac.uk/study/courses/cpd/core-skills-in-supportive-and-end-of-life-care',
     'https://www.city.ac.uk/study/courses/postgraduate/newspaper-journalism',
     'https://www.cass.city.ac.uk/study/masters/courses/ngo-management',
     'https://www.cass.city.ac.uk/study/executive-education/our-programmes/new-venture-creation',
     'https://www.city.ac.uk/study/courses/short-courses/courses/novel-writing-and-longer-works',
     'https://www.city.ac.uk/study/courses/short-courses/courses/novel-writing-summer-school',
     'https://www.city.ac.uk/study/courses/cpd/core-skills-in-supportive-and-end-of-life-care2',
     'https://www.city.ac.uk/study/courses/cpd/non-medical-prescribing-and-advanced-physical-assessment',
     'https://www.city.ac.uk/study/courses/cpd/obstetric-ultrasound',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/opinion-writing',
     'https://www.city.ac.uk/study/courses/cpd/palliative-care',
     'https://www.city.ac.uk/study/courses/postgraduate/organisational-psychology',
     'https://www.city.ac.uk/study/courses/undergraduate/optometry',
     'https://www.city.ac.uk/study/courses/cpd/pathophysiological-basis-for-advanced-practice',
     'https://www.city.ac.uk/study/courses/cpd/personal-and-people-development',
     'https://www.city.ac.uk/study/courses/cpd/personal-and-people-development2',
     'https://www.city.ac.uk/study/courses/cpd/philosophy-and-politics-of-primary-care',
     'https://www.city.ac.uk/study/courses/cpd/philosophy-and-politics-of-primary-healthcare',
     'https://www.city.ac.uk/study/courses/cpd/philosophy-knowledge-skills-evidence-optimum-birth',
     'https://www.cass.city.ac.uk/study/phd/accounting',
     'https://www.cass.city.ac.uk/study/phd/actuarial-science',
     'https://www.cass.city.ac.uk/study/phd/finance',
     'https://www.cass.city.ac.uk/study/phd/management',
     'https://www.city.ac.uk/study/courses/short-courses/courses/photoshop-an-introduction',
     'https://www.city.ac.uk/study/courses/short-courses/courses/portuguese-beginners-year-1',
     'https://www.city.ac.uk/study/courses/short-courses/courses/portuguese-lower-intermediate-year-2',
     'https://www.city.ac.uk/study/courses/short-courses/courses/positive-psychology-becoming-the-best-of-you',
     'https://www.city.ac.uk/study/courses/short-courses/courses/positive-psychology',
     'https://www.city.ac.uk/study/courses/short-courses/courses/powershell-basics',
     'https://www.city.ac.uk/study/courses/cpd/physics-and-instrumentation-of-medical-magnetic-resonance',
     'https://www.city.ac.uk/study/courses/postgraduate/counselling-psychology-graduate-certificate',
     'https://www.city.ac.uk/study/courses/undergraduate/politics',
     'https://www.city.ac.uk/study/courses/research-degrees/politics',
     'https://www.city.ac.uk/study/courses/short-courses/courses/practical-digital-marketing-tools-and-tactics',
     'https://www.city.ac.uk/study/courses/short-courses/courses/presentation-skills',
     'https://www.city.ac.uk/study/courses/cpd/practical-management-of-dysphagia',
     'https://www.city.ac.uk/study/courses/cpd/practical-osce-preparation-course-for-pre-registration-optometrists',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/preparing-and-drafting-witness-statements',
     'https://www.city.ac.uk/study/courses/cpd/principles-of-prescribing',
     'https://www.city.ac.uk/study/courses/cpd/principles-of-prescribing-on-line',
     'https://www.city.ac.uk/study/courses/cpd/principles-of-therapeutics',
     'https://www.city.ac.uk/study/courses/postgraduate/primary-care-practice-nursing',
     'https://www.cass.city.ac.uk/study/executive-education/custom-programmes/practical-accounting-and-finance-for-entrepreneurs',
     'https://www.city.ac.uk/study/courses/cpd/glaucoma',
     'https://www.city.ac.uk/study/courses/cpd/visual-impairment2',
     'https://www.city.ac.uk/study/courses/cpd/medical-retina',
     'https://www.city.ac.uk/study/courses/cpd/professional-certificate-paediatric-eye-care',
     'https://www.city.ac.uk/study/courses/cpd/contact-lens-practice',
     'https://www.city.ac.uk/study/courses/cpd/professional-leadership',
     'https://www.city.ac.uk/study/courses/postgraduate/professional-advocacy',
     'https://www.city.ac.uk/study/courses/postgraduate/counselling-psychology-dpsych',
     'https://www.city.ac.uk/study/courses/postgraduate/professional-legal-skills',
     'https://www.city.ac.uk/study/courses/research-degrees/professional-education',
     'https://www.city.ac.uk/study/courses/short-courses/courses/project-management-an-introduction',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/professional-skills-course',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/project-management',
     'https://www.city.ac.uk/study/courses/cpd/Promoting-Child-and-Adolescent-Psychological-Development',
     'https://www.city.ac.uk/study/courses/cpd/Promoting-Child-and-Adolescent-Psychological-Development-MSc',
     'https://www.city.ac.uk/study/courses/postgraduate/professional-practice',
     'https://www.city.ac.uk/study/courses/postgraduate/project-management-finance-and-risk',
     'https://www.city.ac.uk/study/courses/undergraduate/psychology',
     'https://www.city.ac.uk/study/courses/research-degrees/psychology',
     'https://www.city.ac.uk/study/courses/research-degrees/psychology-and-social-neuroscience',
     'https://www.city.ac.uk/study/courses/cpd/psychology-for-health-and-social-care',
     'https://www.city.ac.uk/study/courses/cpd/public-health',
     'https://www.city.ac.uk/study/courses/cpd/qualified-lawyers-transfer-scheme-qlts',
     'https://www.city.ac.uk/study/courses/postgraduate/masters-in-public-health-mph',
     'https://www.city.ac.uk/study/courses/postgraduate/postgraduate-diploma-public-health',
     'https://www.city.ac.uk/study/courses/postgraduate/llm-public-international-law',
     'https://www.city.ac.uk/study/courses/postgraduate/public-international-competition-law',
     'https://www.city.ac.uk/study/courses/postgraduate/publishing-studies',
     'https://www.cass.city.ac.uk/study/masters/courses/quantitative-finance',
     'https://www.city.ac.uk/study/courses/postgraduate/radiography-computed-tomography',
     'https://www.city.ac.uk/study/courses/cpd/recognising-deterioration-patient',
     'https://www.city.ac.uk/study/courses/cpd/recognition-and-assessment-of-mental-health-conditions',
     'https://www.city.ac.uk/study/courses/cpd/Research-Methodologies-for-Practice-e-learning',
     'https://www.city.ac.uk/study/courses/postgraduate/radiography-magnetic-resonance-imaging',
     'https://www.cass.city.ac.uk/study/masters/courses/real-estate',
     'https://www.cass.city.ac.uk/study/masters/courses/real-estate-investment',
     'https://www.city.ac.uk/study/courses/postgraduate/renewable-energy-and-power-systems-management',
     'https://www.city.ac.uk/study/courses/postgraduate/research-methods-msc',
     'https://www.city.ac.uk/study/courses/undergraduate/radiography-diagnostic-imaging',
     'https://www.city.ac.uk/study/courses/undergraduate/radiography-radiotherapy-and-oncology',
     'https://www.city.ac.uk/study/courses/short-courses/courses/russian-for-beginners',
     'https://www.city.ac.uk/study/courses/short-courses/courses/russian-lower-intermediate-year-2',
     'https://www.city.ac.uk/study/courses/short-courses/courses/screenwriting-an-introduction',
     'https://www.city.ac.uk/study/courses/cpd/return-to-practice-nursing',
     'https://www.city.ac.uk/study/courses/cpd/risk-and-midwifery-practice',
     'https://www.city.ac.uk/study/courses/cpd/risk-assessment-management-mental-health-across-lifespan',
     'https://www.city.ac.uk/study/courses/cpd/role-development-intensive-care',
     'https://www.city.ac.uk/study/courses/cpd/science-and-instrumentation-of-computer-tomography',
     'https://www.city.ac.uk/study/courses/cpd/selective-mutism',
     'https://www.city.ac.uk/study/courses/postgraduate/research-methods-with-psychology',
     'https://www.city.ac.uk/study/courses/short-courses/courses/short-story-writing',
     'https://www.city.ac.uk/study/courses/cpd/social-communication-after-brain-injury',
     'https://www.city.ac.uk/study/courses/cpd/social-determinants-of-health',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/solicitors-accounts-rules',
     'https://www.city.ac.uk/study/courses/cpd/solicitors-accounts-rules-2019-new-versus-old',
     'https://www.cass.city.ac.uk/study/masters/courses/shipping-trade-and-finance',
     'https://www.city.ac.uk/study/courses/postgraduate/software-engineering',
     'https://www.city.ac.uk/study/courses/undergraduate/sociology',
     'https://www.city.ac.uk/study/courses/undergraduate/sociology-with-psychology',
     'https://www.city.ac.uk/study/courses/research-degrees/sociology',
     'https://www.city.ac.uk/study/courses/short-courses/courses/spanish-beginners-year-1',
     'https://www.city.ac.uk/study/courses/short-courses/courses/spanish-lower-intermediate-year-2',
     'https://www.city.ac.uk/study/courses/short-courses/courses/spanish-intermediate-year-3',
     'https://www.city.ac.uk/study/courses/short-courses/courses/starting-up-in-business',
     'https://www.city.ac.uk/study/courses/cpd/Cardiac-Care-Core-Skills',
     'https://www.city.ac.uk/study/courses/cpd/specialist-core-skills-cardiac-care-level-7',
     'https://www.city.ac.uk/study/courses/postgraduate/speech-and-language-therapy',
     'https://www.city.ac.uk/study/courses/postgraduate/speech-language-and-communication',
     'https://www.city.ac.uk/study/courses/undergraduate/speech-language-science',
     'https://www.city.ac.uk/study/courses/undergraduate/speech-therapy',
     'https://www.city.ac.uk/study/courses/short-courses/courses/strategic-digital-marketing',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/structured-litigation-programme',
     'https://www.city.ac.uk/study/courses/cpd/student-negotiated-module-1-and-2',
     'https://www.city.ac.uk/study/courses/cpd/summer-school-philosophy-knowledge-skills-and-evidence-for-optimal-birth',
     'https://www.city.ac.uk/study/courses/cpd/supervising-and-assessing-in-healthcare-practice',
     'https://www.city.ac.uk/study/courses/cpd/supervising-and-assessing-in-healthcare-practiceonline',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/tax-practitioners',
     'https://www.city.ac.uk/study/courses/postgraduate/tv-journalism',
     'https://www.city.ac.uk/study/courses/postgraduate/temporary-works-and-construction-method-engineering',
     'https://www.cass.city.ac.uk/study/executive-education/our-programmes/strategic-decision-making-for-leaders',
     'https://www.city.ac.uk/study/courses/short-courses/courses/the-business-of-the-visual-arts',
     'https://www.city.ac.uk/study/courses/short-courses/courses/the-novel-studio',
     'https://www.city.ac.uk/study/courses/cpd/training-in-the-use-of-the-early-sociocognitive-battery-esb-an-assessment-for-preschool-children-with-language-and-communication-difficulties',
     'https://www.city.ac.uk/study/courses/short-courses/courses/travel-writing',
     'https://www.city.ac.uk/study/courses/cpd/the-application-of-research-in-clinical-settings',
     'https://www.city.ac.uk/study/courses/cpd/health-policy-process-politics-power',
     'https://www.city.ac.uk/study/courses/cpd/thinking-about-your-career',
     'https://www.city.ac.uk/study/courses/cpd/tissue-viability-and-wound-care-for-health-care-support-workers',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/trial-preparation',
     'https://www.city.ac.uk/study/courses/research-degrees/translation',
     'https://www.city.ac.uk/study/courses/short-courses/courses/visual-basic-for-applications-in-excel-vba-part-1',
     'https://www.city.ac.uk/study/courses/short-courses/courses/visual-basic-for-applications-vba-in-excel-part-2',
     'https://www.city.ac.uk/study/courses/short-courses/courses/visual-basic-for-applications-vba-in-excel-part-3-building-applications',
     'https://www.city.ac.uk/study/courses/short-courses/courses/web-programming-using-php-mysql-part-1',
     'https://www.city.ac.uk/study/courses/short-courses/courses/web-programming-using-php-mysql-part-2',
     'https://www.city.ac.uk/study/courses/cpd/fundamental-principles-of-ultrasound-practice',
     'https://www.city.ac.uk/study/courses/cpd/understanding-common-respiratory-diseases',
     'https://www.city.ac.uk/study/courses/cpd/using-research-knowledge',
     'https://www.city.ac.uk/about/schools/law/courses/continuing-professional-development/in-house-courses/witness-familiarisation',
     'https://www.cass.city.ac.uk/study/masters/courses/voluntary-sector-management',
     'https://www.city.ac.uk/study/courses/short-courses/courses/writers-workshop',
     'https://www.city.ac.uk/study/courses/short-courses/courses/write-for-business',
     'https://www.city.ac.uk/study/courses/short-courses/courses/writing-for-children',
     'https://www.city.ac.uk/study/courses/cpd/womens-health',
     'https://www.city.ac.uk/study/courses/cpd/worked-based-learning-msc',
     'https://www.city.ac.uk/study/courses/cpd/work-based-learning-expert-specialist-practice',
     'https://www.city.ac.uk/study/courses/cpd/work-based-learning-in-practice',
     'https://www.city.ac.uk/study/courses/cpd/work-based-learning-in-practice-2',
     'https://www.city.ac.uk/study/courses/cpd/Work-Based-Project-BSc',
     'https://www.city.ac.uk/study/courses/cpd/how-to-run-peer-led-groups']

    inside_course()

    wb = Workbook()
    file_path = 'C:\\Users\\jatin\\Desktop\\london.xlsx'
    # wb = load_workbook(file_path)
    sheet = wb.active
    for i in range(len(clist)):
        sheet.cell(i + 1, 1).value = clist[i].count
        sheet.cell(i + 1, 2).value = clist[i].course
        sheet.cell(i + 1, 3).value = clist[i].year
        sheet.cell(i + 1, 4).value = clist[i].subject
        sheet.cell(i + 1, 5).value = clist[i].link
    wb.save(file_path)


