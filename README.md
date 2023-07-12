# flaskTasks

Simple Task Management API with Flask, 
Python, SQLAlchemy, and PostgreSQL

Follow the steps below to get the project up and running on your local machine.

1. Clone the repository: <br />
git clone https://github.com/yousef71/flaskTasks.git

2. Navigate to the project directory <br />
cd flaskTasks

3. Install required dependencies: <br />
pip install Flask <br />
pip install SQLAlchemy <br />
pip install psycopg2 <br />
   
4. In config.py, change the variables for PostgreSQL credentials ( username, password, databaseName ) <br />

5. Make sure to create the Tasks Table in postgres <br />
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title TEXT,
  description TEXT,
  completed BOOLEAN,
  priority INTEGER,
  due_date DATE,
  category TEXT
);

6. run application <br />
python main.py
