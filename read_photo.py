import os
import re
from transliterate import translit
import logging
from logging.config import dictConfig
from log_conf import loggin_conf

dictConfig(loggin_conf)
logger = logging.getLogger('my_logger')


class ListPath:
    def __init__(self) -> None:
        self.ls = []

    
    def path_has_cyrillic(self, path_name):
        '''
            Функція повертає True || False, в залежності 
            чи містить шлях кирилицю.

        '''
        return bool(re.search('[а-яА-Я]', path_name))
    
    
    def chenge_path_name(self, path_name):
        '''
            Якщо шлях до файлу містить кирилицю змінює назву,
            замінюючи англійськими буквами.
        
        '''
        if self.path_has_cyrillic(path_name):
            path_n = translit(path_name, reversed=True)
            logger.debug(f'[CHANGE PATH NAME]: {path_name} => {path_n} ')
            return path_n
        return path_name
    
    
    def walk_file(self, path = 'D:\photo famely'):    
        '''
            Рекурсивна функція яка обходить заданний каталог.
        
        '''

        for i in os.listdir(path):
            new_path = self.chenge_path_name(i)
            os.rename(f'{path}\{i}', f'{path}\{new_path}')
            
            if os.path.isdir(f'{path}\{new_path}'):
                self.walk_file(f'{path}\{new_path}')
            else:
                self.ls.append(f'{path}\{new_path}')

        return self.ls

