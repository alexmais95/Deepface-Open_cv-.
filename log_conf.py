import logging


loggin_conf = {
    'version': 1,
    'formatters': {
        'console_msg': {
            'format': '{levelname} {lineno} {msg}',
            'style': '{'
        },
        'file_msg': {
            'format': '{levelname} {asctime} {lineno} {msg}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'console_msg'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'file_msg',
            "filename": "app.log",
            
        }
    },
    'loggers': {
        'my_logger': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}