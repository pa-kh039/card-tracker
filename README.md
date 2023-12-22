## Current Flow

    1) Server is started.
    2) Database and table is created, if not present.
    3) Connection is set-up with the database.
    4) Database is synced with all csv files, in a proper sequence.
    5) The API endpoint receives request from user and checks the user-input. If phone number/card id is given, corresponding card's status is fetched from database and returned, else appropriate error is thrown. 

## Frameworks

#### Web framework - FastAPI

    Reasons for choosing FastAPI:

    1) APIs respond faster 
    2) It supports asynchronous code
    3) Quick and easy development
    4) Easy testing with features like: TestClient, swaggerUI(inbuilt, interactive platform for API testing) , etc.
    5) The convenience of using Python - quick to write, readable code, with no worries for data types

#### Database - PostgreSQL

    Reasons:

    1) The data being circulated, right from csv files to database, to APIs has a definite structure. Hence, I chose a SQL database.
    2) Each entry in the csv files can be treated as a transaction in the database, and PostgreSQL features high data consistency and integrity, along with adherence to ACID properties to ensure transactions remain reliable and correct. 

## Scopes of improvement

    1) No user entities in database. Once,we start maintaining user entities, we can implement user authentication, phone number verification, and maintain a 1-to-1 relationship between cards and users.
    2) Before changing status of a card, we can verify if the card went through all the previous statuses in a proper order, with respect to timestamp.
    3) Come up with mechanisms to deal with failures/conflicts in syncing database with entries from csv files.
    4) Accessing csv files remotely.
    5) Setup periodic/relatime sync of database with remote csv files.
    6) Proper data validation, and adherence to schemas to ensure Data Abstraction.