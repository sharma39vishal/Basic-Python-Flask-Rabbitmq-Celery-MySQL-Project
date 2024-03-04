# Import the Celery library
from celery import Celery

# Import the time module for the sleep function
import time

# Create a Celery instance named 'app'
app = Celery('tasks',backend='db+mysql://root:password@localhost:3306/QueueMgmt', broker='amqp://guest@localhost//')

# Define a Celery task named 'add'
@app.task()
def add(x, y):
    # Simulate a delay of 25 seconds (for demonstration purposes)
    time.sleep(25)
    
    # Perform the addition operation
    result = x + y
    
    # Return the result of the addition
    return result
