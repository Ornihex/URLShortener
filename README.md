https://roadmap.sh/projects/url-shortening-service

Installation:
 1) Download (https://github.com/Ornihex/URLShortener/archive/refs/heads/master.zip)
 2) Download and install MongoDB
    In MongoDB, you need to create a database "data" in which you need to create a collection called "shortCodes"
 3) `pip install poetry`
 4) Go to the URLShortener folder
 5) `poetry install`
 6) Create a .env file

Example for .env file:
  ```
  db_host = '127.0.0.1'
  db_port = 27017
  ```

Running:
  1) Make sure that you have selected the poetry virtual environment.
     To activate the poetry virtual environment, enter `poetry shell` in the terminal.
     In the IDE, you can also choose a poetry environment for the entire IDE (this is done differently in different IDEs.
     For example, in VS Code, you need to point to the lower right corner, click and select the desired environment)
 3) Go to the urlshortener/app
 4) `uvicorn main:app`
 5) Type Y if you want to enable force redirection(
    When enabled, clicking on a short link will immediately redirect to the original url,
    otherwise the original url will be displayed first.

