from celery import Celery
import time
from flask_socket 

celery=Celery('demo',broker='amqp://')
print("Test ok")