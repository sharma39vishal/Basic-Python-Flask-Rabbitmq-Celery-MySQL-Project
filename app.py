# Import necessary modules from Flask, Celery, and other related modules
from flask import Flask, request, jsonify
from tasks import add  
from celery import Celery
from celery.result import AsyncResult

# Create a Flask app instance
app = Flask(__name__)

# Create a Celery instance named 'celery_app'
celery_app = Celery('tasks', broker='amqp://guest@localhost//')

# Configure Celery settings
celery_app.conf.update(
    # Configure the result backend using MySQL
    CELERY_RESULT_BACKEND='db+mysql://root:password@localhost:3306/QueueMgmt',
    
    # Set the task serializer to JSON
    CELERY_TASK_SERIALIZER='json',
    
    # Do not ignore results (set to False)
    CELERY_IGNORE_RESULT=False,
)

# Define a route for adding data using a POST request
@app.route('/add', methods=['POST'])
def adddata():
    try:
        # Extract data from JSON request
        data = request.get_json()
        x = data['x']
        y = data['y']
        
        # Call the 'add' task asynchronously and get the result object
        result = add.delay(x, y)
        
        # Return the task ID as a JSON response
        return jsonify({'Task ID': result.id})
    except Exception as e:
        return jsonify({'error': str(e)})

# Define a route for getting the status of a task
@app.route('/getstatus/<task_id>')
def gettaskstatus(task_id):
    try:
        # Get the status of the task using the task ID
        task_status = celery_app.AsyncResult(task_id).status      
        
        # Return the task status as a JSON response
        return jsonify({'Task Status': task_status})
    except Exception as e:
        return jsonify({'error': str(e)})

# Define a route for getting the result of a completed task
@app.route('/getdone/<task_id>')
def getdone(task_id):
    try:
        # Get the result of the task using the task ID
        task_result = celery_app.AsyncResult(task_id).result      
        
        # Return the task result as a JSON response
        return jsonify({'Task Result': task_result})
    except Exception as e:
        return jsonify({'error': str(e)})

# Run the Flask app in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)
