from selenium import webdriver
from bs4 import BeautifulSoup

if __name__ == '__main__':
    op = webdriver.FirefoxOptions()
    op.add_argument("--headless")
    driver = webdriver.Firefox(options=op)
    driver.get('https://www.undergraduate.study.cam.ac.uk/courses/anglo-saxon-norse-and-celtic')
    html_page = BeautifulSoup(driver.page_source)
    print(html_page)