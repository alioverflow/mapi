from flask import Flask
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
import requests
import pandas
import mysql.connector
import datascrape
import mailsender
app = Flask(__name__)
logger = get_task_logger(__name__)

def make_celery(app):
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['CELERYBEAT_SCHEDULE'] = {
        'periodic_task-every-day':{
            'task': 'email',
            'schedule': crontab("*")
            },
        'periodic_task2-every-day':{
            'task': 'periodic_task',
            'schedule': crontab("*") 
            }
    }
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task(name="email")
def sendEmaili():
    mailsender.sendEmail()

@celery.task(name ="periodic_task")
def periodic_task():
    datascrape.mysqloperations()
    r = requests.get('https://api.themoviedb.org/3/list/2?api_key=9ecd99d429e5c18c54f166a2192ca7bb&language=en-US')
    my_dict = r.json()
    return my_dict

if __name__ == "__main__":
    app.run(debug = True)
