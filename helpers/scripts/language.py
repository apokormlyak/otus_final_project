import re


def detect(word):
    if re.match('[а-яА-Я]', word[0]):
        return 'ru'
    elif re.match('[a-zA-Z]', word[0]):
        return 'en'
