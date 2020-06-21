from bs4 import BeautifulSoup
import unittest

def parse(path_to_file):
    file = open(path_to_file, encoding='utf8')
    text = file.read()
    soup = BeautifulSoup(text,'lxml')
    html = soup.find(id="bodyContent")
    #Подсчитываем кол-ство картинок с шириной больше 200
    imgs = len(html.find_all('img',width = lambda x: int(x or 0) > 199))
    #Подсчитываем кол-ство заголовков текст,которых начинается на Е,Т,С
    temp =0
    for tag in html.find_all(['h1','h2','h3','h4','h5','h6']):
            if tag.get_text()[0] == 'E' or tag.get_text()[0] =='T' or tag.get_text()[0] =='C':
                temp+=1
    headers = temp
    #Подсчитываем самую длинную цепочку из ссылок
    linkslen = 0
    for a in html.find_all('a'):
        current_streak = 1

        for tag in a.find_next_siblings():
            if tag.name == 'a':
                current_streak += 1
            else:
                break

        linkslen = current_streak if current_streak > linkslen else linkslen
    #Количество не вложенных списков
    lists = sum(1 for tag in html.find_all(['ol', 'ul']) if not tag.find_parent(['ol', 'ul']))


    return [imgs, headers, linkslen, lists]




# 
# class TestParse(unittest.TestCase):
#     def test_parse(self):
#         test_cases = (
#             ('C:/Users/bo_10/Documents/GitHub/Coursera_WEB/2_week/Stone_Age', [13, 10, 12, 40]),
#             ('C:/Users/bo_10/Documents/GitHub/Coursera_WEB/2_week/Brain', [19, 5, 25, 11]),
#             ('C:/Users/bo_10/Documents/GitHub/Coursera_WEB/2_week/Artificial_intelligence', [8, 19, 13, 198]),
#             ('C:/Users/bo_10/Documents/GitHub/Coursera_WEB/2_week/Python_(programming_language)', [2, 5, 17, 41]),
#             ('C:/Users/bo_10/Documents/GitHub/Coursera_WEB/2_week/Spectrogram', [1, 2, 4, 7]),)
#
#         for path, expected in test_cases:
#             with self.subTest(path=path, expected=expected):
#                 self.assertEqual(parse(path), expected)
#
#
# if __name__ == '__main__':
#     unittest.main()
