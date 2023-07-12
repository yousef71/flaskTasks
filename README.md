# flaskTasks

Simple Task Management API with Flask, 
Python, SQLAlchemy, and PostgreSQL

Follow the steps below to get the project up and running on your local machine.

1. Clone the repository: <br /><br />
git clone https://github.com/yousef71/flaskTasks.git

2. Navigate to the project directory <br /><br />
cd flaskTasks

3. Install required dependencies: <br /><br />
pip install Flask <br />
pip install SQLAlchemy <br />
pip install psycopg2 <br />
   
4. In config.py, change the variables for PostgreSQL credentials ( username, password, databaseName ) <br />

5. Make sure to create the Tasks Table in postgres <br /><br />
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY, <br />
  title TEXT, <br />
  description TEXT, <br />
  completed BOOLEAN, <br />
  priority INTEGER, <br />
  due_date DATE, <br />
  category TEXT <br />
);

6. run application <br /><br />
python main.py

Note: To test the endpoints on Postman, download the "FlaskTasks.postman_collection" file in the project directory then import it on postman!
