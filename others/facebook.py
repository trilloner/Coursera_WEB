import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chromedriver = 'C:/Users/mamko/Documents/ChromeWeb/chromedriver.exe'

option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})

driver = webdriver.Chrome(chrome_options=option, executable_path=chromedriver)

print("Перед началом авторизуйтесь!")

login_facebook = '******'
#input("Введите ваш пароль: ")
password_facebook = '*****'

POSTS = []
LINKS = []

def auth_facebook():
    try:
       print("Выполняется авторизация...")

       driver.get('https://www.facebook.com/')

       driver.find_element_by_id('email').send_keys(login_facebook)

       driver.find_element_by_id('pass').send_keys(password_facebook)

       driver.find_element_by_id('u_0_b').click()

       if driver.find_element_by_id('pass'):
           print("Авторизация не выполнена. Повторяем")
           auth_facebook()
    except:
        print("Авторизация выполнена")



def reg_name(name):

    name = name.replace(' ', '%20')
    return name


def scroll_down():
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    print("Собираем данные...")
    for i in range(50):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def find_posts():
    name = input("Введите что хотите найти: ")

    url = 'https://www.facebook.com/search/posts/?q={posts}&epa=SERP_TAB'.format(posts=reg_name(name))

    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    all_posts= ''
    for el in soup.find_all(class_='_6ojs _19_p'):
        link = el.find('a')
        all_posts = 'https://www.facebook.com{posts}'.format(posts = link.get('href'))

    driver.get(all_posts)
    scroll_down()


def find_people():
    name = input("Введите имя и фамилию кого хотите найти: ")

    url = 'https://www.facebook.com/search/people?q={person}'.format(person=reg_name(name))

    driver.get(url)

    print("Скроллим вниз")

    scroll_down()


def find_links():
    name = input("Введите что хотите найти: ")
    url = 'https://www.facebook.com/search/links/?q={link}&epa=SERP_TAB'.format(link= reg_name(name))
    driver.get(url)
    print("Скроллим вниз")
    scroll_down()



def parse_html_people():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for el in soup.find_all(class_='_4p2o _87m1'):
        link = el.find('a')
        print(link.get('href'))

def parse_html_posts():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for el in soup.find_all(class_='_6-cp'):
        link = el.find('a')
        POSTS.append('https://www.facebook.com{posts}'.format(posts = link.get('href')))


def parse_html_links():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for el in soup.find_all(class_='_19_p'):
        link = el.find('a')
        LINKS.append(link.get('href'))


def display_posts(start,end):
    length = len(POSTS)
    if end > length:
        while start<length:
            print(POSTS[start])
            start = start + 1
        return
    while start < end:
        print(POSTS[start])
        start = start + 1
    return

def display_links(start,end):
    length = len(LINKS)
    if end > length:
        while start<length:
            print(LINKS[start])
            start = start + 1
        return
    while start < end:
        print(LINKS[start])
        start = start + 1
    return


def menu():
    print(" 1.Публикации \n 2.Ссылки")
    find = input("Выберите по каким критериям хотите искать: ")
    start = 0
    end = 10
    if int(find) == 1:
        find_posts()
        parse_html_posts()

        display_posts(start, end)
        while True:
            next = input("Что бы отобразить следующие 10 ссылок,нажмите 1. \nВыйти из программы нажмите 0:")
            if int(next) == 1:
                start = start + 10
                end = end + 10
                display_posts(start, end)
            else:
                return

    elif int(find) == 2:
        find_links()
        parse_html_links()
        display_links(start,end)
        while True:
            next = input("Что бы отобразить следующие 10 ссылок,нажмите 1. \nВыйти из программы нажмите 0:")
            if int(next) == 1:
                start = start + 10
                end = end + 10
                display_links(start, end)
            else:
                return

    else:
        print("Введите корректное значение")
        menu()




if __name__ == '__main__':
   auth_facebook()
   menu()


