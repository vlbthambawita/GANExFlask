from celery import Celery
import time


celery=Celery('demo',broker='amqp://')
# print("Test ok")

@celery.task
def long_task(socketio):
    for i in range(10):
        print(i)
        socketio.emit('my response 2', {'data': i})
        time.sleep(1)