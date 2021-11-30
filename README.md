## A backend book store project

### Requirements

Run the following in the terminal.

```shell
pip install -r requirements.txt
cd frontend
npm install
```

### How to run in local

Run the following in the terminal.

```shell
# build the frontend  first
cd frontend
npm run build
# run the server
cd ..
python3 app.py
```

### Project Structure

- data: scripts for crawling data and uploading data into database through our own server

- entities: scripts of different type of entities of model

- store:
  - exceptions: define different exception for server to return
  - models: sqlalchemy models
  - sqlalchemy_store: support every operation to db
  - validation: validate the input data from requests

- frontend:
  - src: modules for React components and containers

### Deploy address

[app link](https://bookstore-jeff-901.herokuapp.com)
> Caution: you might need to wait for the server and database to warm up
