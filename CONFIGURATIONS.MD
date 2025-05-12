# HOW TO RUN THE DOCKER FILE LOCALLY

The dockerfile should contain the below in order to run the flask development server instead of the gunicorn approach which is relevant for prodution

```
FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY . .
CMD [ "flask", "run",  "--host", "0.0.0.0"]
```

Then ensure that all three programs run as follows

- Postman, for sending requests
- VScode for code changes etc
- Docker 

To run the docker app then use the following command from within the VSCode terminal 

```
docker run -dp 5000:5000 -w //app -v "C:\Users\petro\OneDrive\Documents\APIcourse\pythonrefresher\StoreAPIproject://app" rest-apis-flask-python
```

if any changes are made then we may need to rebuild the image first with

```
docker build -t rest-apis-flask-python .
```

if any packages are missing then install them using pip

```
pip install -r requirements.txt
```


if no changes were  made then docker compose up should work too

```
docker compose up
```
