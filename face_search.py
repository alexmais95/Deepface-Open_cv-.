from deepface import DeepFace
import json
from read_photo import ListPath
from post_db import DataPost
from log_conf import loggin_conf
import logging
from logging.config import dictConfig
from log_conf import loggin_conf

dictConfig(loggin_conf)
logger = logging.getLogger('my_logger')

class DetectFace:
    def __init__(self) -> None:
        self.models = [
            "VGG-Face", 
            "Facenet", 
            "Facenet512", 
            "OpenFace", 
            "DeepFace", 
            "DeepID", 
            "ArcFace", 
            "Dlib", 
            "SFace",
            "GhostFaceNet",
        ]
        self.db = DataPost()

    
    def photo_path_list(self):
        '''
            Функція поверне список із повним шляхом до фото.
            Якщо якась папка чи файл написані українською чи рос.
            ця функція замінить букви на англійські.
            (DeepFace - не сприймає кирилицю)

        '''
        make_ls = ListPath()
        return [path for path in make_ls.walk_file()]
    
    def make_json(self, result, name):
        with open(f'{name}.json', 'w') as file:
                json.dump(result, file, indent=4, ensure_ascii=False)
    
    def face_verify(self, img_1, img_2):
        try:
            result = DeepFace.verify(img1_path=img_1, img2_path=img_2)
            self.make_json(result=result, name='face_verify')
           
        except Exception as _ex:
            return _ex

    def face_search(self, search_path):
        '''
            Функція робить пошук співпадінь обличь, і якщо співпадає заносить шлях до фото в базу данних.
            img1_path - фото зі списку(photo_path_list)
            img2_path - зразок до якого застосовується порівняння
            result - повертає словник (ключ 'verified' => True || False)
            enforce_detection = False - ігнорує помилки повязані з відсутністю обличь

        '''

        try:
            for key, value in search_path.items():
                for img_path in self.photo_path_list():
                    #result = DeepFace.find(img_path=img_path, db_path=value, enforce_detection=False)
                    result = DeepFace.verify(img1_path=img_path, img2_path=value, enforce_detection=False)
                    if result['verified'] == True:
                        logger.debug(f'[FIND]: face identifi : {img_path}')
                        self.db.insert_into_db(key, img_path)
                        
                    else:
                        logger.debug('[NOT FOUND]: face dont identifi')

        except Exception as _ex:
            return logger.debug(f'[EXCEPTION]:{_ex}')
            
        
        finally:
            '''
            Після закінчення циклу || при помилці,
            закривається зєднання з базою данних.
            
            '''
            self.db.close_con()
            logger.debug('[CONNECTION CLOSE]: conn to db close')


def main(): 
    # данний словник містить ключ який записується в базу данних (name).
    # адреса веде до фото зразка для пошуку.
    search_path = {'Alex': 'F:\\open_cv\\alex_face\\alex_3.jpg'}
    detect_face = DetectFace()
    detect_face.face_search(search_path)
   
    


if __name__=="__main__":
    main()



