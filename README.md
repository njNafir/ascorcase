Lunch API

## Installation steps

1. Ensure you have python3 installed

2. Clone the repository
3. create a virtual environment using `virtualenv venv`
4. Activate the virtual environment by running `source venv/bin/activate`

- On Windows use `source venv\Scripts\activate`

5. Install the dependencies using `pip install -r requirements.txt`

6. Migrate existing db tables by running `python manage.py migrate`

7. Run the django development server using `python manage.py runserver`


## Docker Environment

1. Setup Docker environment
2. Run command to clone docker repo, `docker pull njnafir/ascorcase:v1.0.0`
3. Run command to run docker repo, `docker run -p 80:80 njnafir/ascorcase:v1.0.0`