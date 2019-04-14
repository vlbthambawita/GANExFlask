#from celery import Celery
import time


#celery=Celery('demo',broker='amqp://')
# print("Test ok")

#@celery.task
#l = []

def long_task(socketio):
    l = [] 
    for i in range(10):
        print(i)
        l = l + [i]
        socketio.emit('my response 2', {'data': l})
        time.sleep(1)