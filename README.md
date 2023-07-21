This application is a simple REST API which can access an existing database. It has endpoints to create, search by "client", "description", or "creator", view a particular event by it's ID, or remove an event by it's ID. The Event object is created along with setters, getters, and to/from JSON methods. It is modeled for the database and it's table is created automatically upon application startup. This is achieved by having the Event class inherit from sqlalchemy's declarative_base. This inheritance allows metadata to be passed along so long as the main app is aware of the object. Base is declared in the database.py file, and can be inherited by any future objects for new tables. So long as the same Base declared in database.py is used, all metadata will be processed before the app initializes the database connection and all tables will be created. 

On a successful run, the API will either return a response with a JSON body detailing the information found by the query, or a succinct response declaring whether the attempt was successful or a failure. This is accompanied by an HTTP status code 200 for GET requests as well as the DELETE request, 201 for POST, and 400 for errors. 

Running the program:

First, you will want to install requirements. I recommend starting with the creation of a virtual environment with:
python -m venv env

Then activate it with:
./env/Scripts/activate.bat

With this done, you may install all requirements for the program. Simply run:
python -m pip install -r requirements.txt

Next is creating a mysql database. From your MySQL workbench, please create a new schema and give it any name you like. With this blank schema, we can create our .env file for storing database info. Add a file named .env in the same folder as main.py, and inside of it place variables for:
user = ""
password = ""
location = ""
port = ""
dbName = ""

Fill these variables with your database username, password, host ip(or localhost if running locally), port, and the name of the schema you just created respectively. These will be accessed by the program on startup to find our new schema and create our main table. Finally, we are ready to start the application. Simply run:
python -m main

you will see the program begin to run, and will be hosted on http://localhost:5000.
The current endpoints are:
http://localhost:5000/pulse/            Check that the application is running(GET)
http://localhost:5000/                  Send data to the application to create a new Event(POST)
http://localhost:5000/view/             Accepts a JSON body containing an id field to display a single event by it's id(GET)
http://localhost:5000/search/<keyword>/ Accepts a JSON body containing either a client, description, or creator field, depending on which is used as the "keyword". 
                                        Will search partial matches of any, returning a batch of results(GET)
http://localhost:5000/delete/           Accepts a JSON body containing an id field to delete a particular event(DELETE)


Finally, testing the endpoints. I have prepared several example scripts to run, shown below:

curl -X POST http://localhost:5000/ -H 'Content-Type: application/json' -d '{"id":1,"client":"David Konopka","description":"Routine Check-in","createdBy":"Admin"}'
curl -X POST http://localhost:5000/ -H 'Content-Type: application/json' -d '{"id":2,"client":"Bob Johnson","description":"Blood Work","createdBy":"Admin"}'
curl -X POST http://localhost:5000/ -H 'Content-Type: application/json' -d '{"id":3,"client":"Alice Royce","description":"Routine Check-in","createdBy":"Admin"}'
curl -X GET http://localhost:5000/view/ -H 'Content-Type: application/json' -d '{"id":1}'
curl -X GET http://localhost:5000/view/ -H 'Content-Type: application/json' -d '{"id":2}'
curl -X GET http://localhost:5000/search/client/ -H 'Content-Type: application/json' -d '{"client":"Dav","description":"Blood","createdBy":"Admin"}'
curl -X GET http://localhost:5000/search/description/ -H 'Content-Type: application/json' -d '{"client":"Dav","description":"Blood","createdBy":"Admin"}'
curl -X GET http://localhost:5000/search/creator/ -H 'Content-Type: application/json' -d '{"client":"Dav","description":"Blood","createdBy":"Admin"}'
curl -X DELETE http://localhost:5000/delete/ -H 'Content-Type: application/json' -d '{"id":2}'
curl -X GET http://localhost:5000/search/creator/ -H 'Content-Type: application/json' -d '{"client":"Dav","description":"Blood","createdBy":"Admin"}'
curl -X DELETE http://localhost:5000/delete/ -H 'Content-Type: application/json' -d '{"id":1}'
curl -X DELETE http://localhost:5000/delete/ -H 'Content-Type: application/json' -d '{"id":3}'

These scripts will create several new events, search by ID, search by client, description, and creator, delete one event, and search by creator again to show it's deletion. Then delete the remaining events. Currently, the json body requires a createdBy field for new/searched events, however this was written on the assumption that an authenticated user would be passing along some identifying information that could take its place.