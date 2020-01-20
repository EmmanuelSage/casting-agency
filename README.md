# Casting Agency

[Hosted on Heroku at : https://casting-agency-nano.herokuapp.com](https://casting-agency-nano.herokuapp.com)

The motivation for this project is to create my capstone project for Udacity's Fullstack Nanodegree program.
It models a company that is responsible for creating movies and managing and assigning actors to those movies.
The assumption is that I am an Executive Producer within the company and wants to create a system to simplify and streamline my process process.

## Project dependencies

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended.

#### PIP Dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

- you may need to change the database url in setup.sh after which you can run
```bash
source setup.sh
```

- Start server by running
```bash
flask run
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Pycodestyle](https://pypi.org/project/pycodestyle/) - pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.


#### Authentication

Authentication is implemented using Auth0, it uses RBAC to assign permissions using roles, these are tokens you could use to access the endpoints.
Note: The tokens expires in 24 hours you can create your own tokens at [Auth0](https://auth0.com/). you would need to refelct this in auth.py
```py
AUTH0_DOMAIN = '<your auth domain>'
ALGORITHMS = ['RS256']
API_AUDIENCE = '<your api audience>'
```

> Casting Assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qQkNSa1EzTmtSRlJVUXdNME00TXpjNVJrTXlOelZCTTBORFJEUXlNVGsyUXpKQ1JrTXlRdyJ9.eyJpc3MiOiJodHRwczovL2VzYWdlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTIyMjI4NWY4MjhmYzBlOTM5ZWEyMTEiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU3OTUxMzk3OSwiZXhwIjoxNTc5NjAwMzc5LCJhenAiOiJ0S0lIT0NpVkVzTUQwYVZ1eUZ6WW1VU3BVUzFCV2hyeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.dWp9RxbudYBH4dOVGEBZhGJOQFF4XwS7DsBBFNmrF6dpCK4B-CEnJpV1JLVG8UMTbNJP_VtsraMhshwWVwb8godKroue4pgCrBsI8V5Q3cSHQ-8FhnpOTf0_te6ydoBy78uO9dQCYtA7i2A32QW9OU7MTV9m9iCj70-ktlhpYweP5SGMxyK8hfoNSXD9a1rKDAEvP4uY57eI-TQaHg-4odEZhACy78LBdeRADbu0O6bfkxa27sJTBq3cVLbyscVJRr-TrJpcqh42vv9SJRoDo1RRtnNeggmybg_UB_C2weK7HezvbsJA-v6Dz49pMY7v29Oj_QRLo5-2bD2M5cM-jw'

> Casting Director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qQkNSa1EzTmtSRlJVUXdNME00TXpjNVJrTXlOelZCTTBORFJEUXlNVGsyUXpKQ1JrTXlRdyJ9.eyJpc3MiOiJodHRwczovL2VzYWdlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTIxZGExNWVmMzkzNDBkY2QxYzczOWQiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU3OTUxNDAxNCwiZXhwIjoxNTc5NjAwNDE0LCJhenAiOiJ0S0lIT0NpVkVzTUQwYVZ1eUZ6WW1VU3BVUzFCV2hyeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.N93SmGsmSyZlJe_XjKxtYixj9O3HDBfXQcnUisNCme8e6OK2v_mz1Ws2xaSL_GXhuFIAfgciVXphOkIBxGDAN6Hr33CTzBFEjlGlMLodhbGehGM2WsNIb3-kKLQx4pqb-vtdpzIt7ECjdEIGoQM1osj_0bbu1aD6iXPHl3rqh9Tgzv3cHOi_uvWAcaX2uzYan5jtq7k5-0YoDJ2Ygd3M5N5XS-K9UUt1s66M647nWohL-b20RG9RLq-v60Y22MjZJ2l3HLKR05SL1EhzpyH5qPz0idFxZaU-BkpriUvSSKYAMRep3gjZsMXYp3BVONZ-DF22U-KqEF-0aIMSNswrfw'

>Executive Producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qQkNSa1EzTmtSRlJVUXdNME00TXpjNVJrTXlOelZCTTBORFJEUXlNVGsyUXpKQ1JrTXlRdyJ9.eyJpc3MiOiJodHRwczovL2VzYWdlLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMjc4NzYxODkzNDU0NDQ3NTgxNyIsImF1ZCI6WyJjYXN0aW5nLWFnZW5jeSIsImh0dHBzOi8vZXNhZ2UuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU3OTUxMzkwOSwiZXhwIjoxNTc5NjAwMzA5LCJhenAiOiJ0S0lIT0NpVkVzTUQwYVZ1eUZ6WW1VU3BVUzFCV2hyeSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.Ki2Dxc9aTHmlrAIOG0XOsUIS0CypvD3CG7JoxF3i6w_3gt4LyDow0zbnrdyIqoozF5pjspVG6slfgsU1Urff-MOOjK5PdbczB-qAUIKRQvI5X6PrfAYizriiFHGIYfYqGVXbI_e_urrwcpVQZhybRQaCUOXnmIAI3Smx7i7YgOsp1dMQXnzLJD6NMEZCNdAspl7aP4vW66ULObI8JWhLrnoe7kHc6uRrogJ0gV1gUfEiU0eG6tvs_xTFFeXYKJyVtNczwIe5wCpLJOATV4Gu44eqZFHqcRjPez_B-KAgswXBrCAjQq4-mY1U-Q89w2OKH-rIAa7TXgI9tydaj9d0gQ'


## Database Setup
The project uses Postgresql as its database, you would need to create one locally and reflect it in setup.sh.
To update the database and seed run the following :
```bash
python manage.py db upgrade
python manage.py seed
```


## Testing
Ensure a test database is created and reflectd in setup.sh.
To start tests, run
```
source test.sh
```

### Error Handling

- 401 errors due to RBAC are returned as

```json
    {
      "code": "unauthorized",
      "description": "Permission not found."
    }
```


Other Errors are returned in the following json format:

```json
      {
        "success": "False",
        "error": 422,
        "message": "Unprocessable entity",
      }
```

The error codes currently returned are:

* 400 – bad request
* 401 – unauthorized
* 404 – resource not found
* 422 – unprocessable
* 500 – internal server error



### Endpoints

#### GET /movies

- General:
  - Returns all the movies.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample:  `curl http://127.0.0.1:5000/movies`

```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Mon, 06 May 2019 00:00:00 GMT",
            "title": "Terminator Dark Fate"
        },
        {
            "id": 2,
            "release_date": "Tue, 06 May 2003 00:00:00 GMT",
            "title": "Terminator Rise of the machines"
        }
    ],
    "success": true
}
```

#### GET /movies/\<int:id\>

- General:
  - Route for getting a specific movie.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample:  `curl http://127.0.0.1:5000/movies/1`

```json
{
    "movie": {
        "id": 1,
        "release_date": "Mon, 06 May 2019 00:00:00 GMT",
        "title": "Terminator Dark Fate"
    },
    "success": true
}
```

#### POST /movies

- General:
  - Creates a new movie based on a payload.
  - Roles authorized : Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{
	"title": "Natasha romanov",
	"release_date": "2020-05-06"
}'`

```json
{
    "movie": {
        "id": 3,
        "release_date": "Wed, 06 May 2020 00:00:00 GMT",
        "title": "Natasha romanov"
    },
    "success": true
}
```

#### PATCH /movies/\<int:id\>

- General:
  - Patches a movie based on a payload.
  - Roles authorized : Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X POST -H "Content-Type: application/json" -d '{
	"title": "Natasha romanov patched",
	"release_date": "2020-05-06"
}'`

```json
{
    "movie": {
        "id": 3,
        "release_date": "Wed, 06 May 2020 00:00:00 GMT",
        "title": "Natasha romanov patched"
    },
    "success": true
}
```


#### DELETE /movies/<int:id\>


- General:
  - Deletes a movies by id form the url parameter.
  - Roles authorized : Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X DELETE`

```json
{
    "message": "movie id 3, titled Natasha romanov patched was deleted",
    "success": true
}
```

#### GET /actors

- General:
  - Returns all the actors.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample:  `curl http://127.0.0.1:5000/actors`

```json
{
    "actors": [
        {
            "age": 40,
            "gender": "male",
            "id": 1,
            "name": "Will Smith"
        },
        {
            "age": 50,
            "gender": "male",
            "id": 2,
            "name": "Bruce Wills"
        }
    ],
    "success": true
}
```

#### GET /actors/\<int:id\>

- General:
  - Route for getting a specific actor.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample:  `curl http://127.0.0.1:5000/actors/1`

```json
{
    "actor": {
        "age": 40,
        "gender": "male",
        "id": 1,
        "name": "Will Smith"
    },
    "success": true
}
```

#### POST /actors

- General:
  - Creates a new actor based on a payload.
  - Roles authorized : Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{
	"name": "Mary",
	"age": 22,
	"gender": "female"
}'`

```json
{
    "actor": {
        "age": 22,
        "gender": "female",
        "id": 3,
        "name": "Mary"
    },
    "success": true
}
```

#### PATCH /actors/\<int:id\>

- General:
  - Patches an actor based on a payload.
  - Roles authorized : Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X POST -H "Content-Type: application/json" -d '{
	"name": "John",
	"age": 22,
	"gender": "female"
}'`

```json
{
    "actor": {
        "age": 22,
        "gender": "female",
        "id": 3,
        "name": "John"
    },
    "success": true
}
```


#### DELETE /actors/<int:id\>


- General:
  - Deletes an actor by id form the url parameter.
  - Roles authorized : Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X DELETE`

```json
{
    "message": "actor id 3, named John was deleted",
    "success": true
}
```

## Authors
- Udacity provided the specifications
- Emmanuel Oluyale worked on the application
