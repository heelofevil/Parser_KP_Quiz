from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import random

"""
НАДСТРОЙКА: Ввести команду в терминале: pip install -r requirements.txt

Данная программа выбирает верные ответы в викторине КиноПоиска.
Принцип следующий:
1. Вход на сайт;
2. Авторизация (Через qr-code, предварительно нужно подготовить открытое приложение на смартфоне);
3. Выбор ответа:
- Если ответ известен, то просто его выбрать;
- Если ответ не известен, записать в файл anser.txt;


Так как программа работает в бесконечном цикле, остановка осуществляется нажатием сочетанием клавиш CTRL+C 
Данные в файле anser.txt хранятся в текстовом формате.


TODO: Исправить баг, когда при длительном пользовании, драйвер теряет кнопку.
"""

link1 = 'https://passport.yandex.ru/auth?origin=kinopoisk&retpath=https%3A%2F%2Fsso.passport.yandex.ru%2Fpush%3Fretpath%3Dhttps%253A%252F%252Fwww.kinopoisk.ru%252Fapi%252Fprofile-pending%252F%253Fretpath%253Dhttps%25253A%25252F%25252Fwww.kinopoisk.ru%25252Fspecial%25252Fbirthday19%25252F%26uuid%3Dc61cfc89-12a9-440e-91aa-0317bb41faff'


browser1 = webdriver.Chrome()
browser1.get(link1)


# Открытие страницы логина
browser1.find_element(By.CLASS_NAME, 'AuthSocialBlock-provider_code_qr').click()

time.sleep(20)

# Нажание на кнопку Играть
browser1.find_element(By.CLASS_NAME, 'episode-card__btn_current').click()
time.sleep(5)

# Нажатие на кнопку начать игру
browser1.find_element(By.CLASS_NAME, 'modal-start__button').click()
time.sleep(1)


while True:

    # сбор вариантов ответа + вопрос
    list = []
    text2 = ''
    for word in range(1, 5):
        list.append(browser1.find_element(By.CSS_SELECTOR, f'.game__test-answers-item:nth-child({word}) span').text)
    text2 = browser1.find_element(By.CSS_SELECTOR, '.game__test-question').text


    time.sleep(1)


    # Вытащить из списка правильный ответ и нажать на него
    try:
        # Flag = True если ответ уже есть в anser.txt, выбирается правильный ответ
        flag = False
        with open('anser.txt', 'r', encoding='utf-8') as outfile:
            for i in outfile:
                if browser1.find_element(By.CSS_SELECTOR, '.game__test-question').text in i:
                    print(" I have answer!")
                    b = i[:i.find(':')]
                    for word in range(1, 5):
                        if b in browser1.find_element(By.CSS_SELECTOR,
                                                          f'.game__test-answers-item:nth-child({word}) span').text:
                            browser1.find_element(By.CSS_SELECTOR,
                                                  f'.game__test-answers-item:nth-child({word})').click()
                            print("Click on true answer.")
                            flag = True
        # Flag = False ответа нет в anser.txt, выбирается рандомный ответ
        if flag != True:
            print("I dont know answer, random choice")
            browser1.find_element(By.CSS_SELECTOR, f'.game__test-answers-item:nth-child({random.randint(1,5)})').click()
    except NoSuchElementException:
        print('Attention, there is no element for the cycle.')


    time.sleep(1)


    # Добавление ответа в файл anser.txt
    try:
        text11 = browser1.find_element(By.CSS_SELECTOR, '.modal-wrong-answer__title').text
        print(text11)
        for i in list:
            if i in text11:
                text1 = i
                print(f"Got the correct answer {text1}")

        with open('anser.txt', 'a', encoding='utf-8') as file:
            file.write(f'{text1}:{text2}' + '\n')

        time.sleep(1)

        browser1.find_element(By.CSS_SELECTOR, '.button_size_small').click()
    except NoSuchElementException:
        print('Attention, will not find an answer.')


    time.sleep(1)

    # Нажатие на кнопку новая игра
    try:
        browser1.find_element(By.CSS_SELECTOR, '.modal-wrong-answer__buttons-wrapper :first-child').click()
        time.sleep(1)
    except NoSuchElementException:
        print('Cant find new game button')


    # Нажатие на кнопку новая игра
    try:
        browser1.find_element(By.CSS_SELECTOR, '.result__btn').click()
    except NoSuchElementException:
        print('Cant find new game button')

    time.sleep(1)
