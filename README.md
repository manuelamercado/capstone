# Casptone Agency Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [psql](https://www.postgresql.org/download/) The core of the PostgreSQL object-relational database management system is available in several source and binary formats. The project uses commands of the cli.

### Setting up the databases:
* Create a database named 'capstone' using `createdb capstone`. You can pass the user if you want. Modify the database URI that is in `setup.sh`.
* Go to `starter` folder: `cd starter`.
* Run `source setup.sh` to get the environment variables available.

#### Migrations:
* Create the initial migrations configuration: `flask db init`.
* Detects migrations to run `flask db migrate`
* Upgrade (apply) changes `flask db upgrade`
* Downgrade changes `flask db downgrade`

OR:

* Use the `manage.py` file:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:actors`
    - `post:actors`
    - `patch:actors`
    - `delete:actors`
    - `get:movies`
    - `post:movies`
    - `patch:movies`
    - `delete:movies`
6. Create new roles for:
    - Casting Assistant
        - Can view actors and movies
    - Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies
    - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users - assign the Casting Assistant role to one, another as Casting Director, and Executive Producer role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for each role, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!
8. Set up your configuration variables in `setup.sh`.

## Endpoints

### GET '/actors'
- Fetches a dictionary of actors in which the keys are the fields of the Actor model and the values are the corresponding string of the fields.
- Request Arguments: None
- Request Headers: Token with the corresponding permission.
- Returns: An object with keys, Actor model fields.
```
{
  "actors": [
    {
      "age": 25,
      "gender": "F",
      "id": 2,
      "movies": [
          "Manuela Mercado"
      ],
      "name": "Manuela Mercado"
   },
   ...
  ],
  "success": true
}
```

### GET '/movies'
- Fetches a dictionary of movies in which the keys are the fields of the Movie model and the values are the corresponding string of the fields.
- Request Arguments: None
- Request Headers: Token with the corresponding permission.
- Returns: An object with keys, Movie model fields.
```
{
  "movies": [
    {
      "actors": [
          "Manuela Mercado"
      ],
      "id": 3,
      "release_year": "Fri, 15 May 2020 00:00:00 GMT",
      "title": "Manuela Mercado"
    },
    ...
  ],
  "success": true
}
```

### DELETE '/actors/<int:actor_id>'
- Deletes a specific actor.
- Request Arguments: Actor ID.
- Request Headers: Token with the corresponding permission.
- Returns: The deleted actor ID.
```
{
  "delete": <actor_id>,
  "success": true,
}
```

### DELETE '/movies/<int:movie_id>'
- Deletes a specific movie.
- Request Arguments: Movie ID.
- Request Headers: Token with the corresponding permission.
- Returns: The deleted movie ID.
```
{
  "delete": <movie_id>,
  "success": true,
}
```

### POST '/actors' to create a new actor 
- Creates a new actor.
- Request Arguments: A JSON object with the key:values of the Actor model fields.
```
{
  "name": "Manuela Mercado",
  "age": "25",
  "gender": "F",
  "movies": [1]
}
```
- Request Headers: Token with the corresponding permission.
- Returns the created actor formatted.
```
{ 
  "actors": [
    { 
      "name": "Manuela Mercado",
      "age": "25",
      "gender": "F",
      "movies": [
        "Manuela Mercado"
      ],
    }
  ],
  "success": true  
}
```

### POST '/movies' to create a new movie 
- Creates a new movie.
- Request Arguments: A JSON object with the key:values of the Movie model fields.
```
{
  "title": "Manuela Mercado",
  "release_year": "Fri, 15 May 2020 00:00:00 GMT",
  "actors": [1]
}
```
- Request Headers: Token with the corresponding permission.
- Returns the created movie formatted.
```
{ 
  "movies": [
    {
      "actors": [
        "Manuela Mercado"
      ],
      "title": "Manuela Mercado",
      "release_year": "Fri, 15 May 2020 00:00:00 GMT"
    }
  ],
  "success": true  
}
```

### PATCH '/actors' to create a update an actor 
- Update a new actor.
- Request Arguments: A JSON object with the key:values of the Actor model fields to update.
```
{
  "name": "Manuela Jacqueline"
}
```
- Request Headers: Token with the corresponding permission.
- Returns the updated actor formatted.
```
{ 
  "actors": [
    { 
      "name": "Manuela Jacqueline",
      "age": "25",
      "gender": "F",
      "movies": [
        "Manuela Mercado"
      ],
    }
  ],
  "success": true  
}
```

### PATCH '/movies' to update a new movie 
- Updates a new movie.
- Request Arguments: A JSON object with the key:values of the Movie model fields to update.
```
{
  "title": "Manuela Jacqueline"
}
```
- Request Headers: Token with the corresponding permission.
- Returns the updated movie formatted.
```
{ 
  "movies": [
    {
      "actors": [
        "Manuela Mercado"
      ],
      "title": "Manuela Jacqueline",
      "release_year": "Fri, 15 May 2020 00:00:00 GMT"
    }
  ],
  "success": true  
}
```

## Tests:
* Create a database for testing with the following command ` createdb capstone_test postgres`.
* Insert at least 3 values for actors and movies.
* Run the tests with `python3 test_app.py` in the `src` folder.
