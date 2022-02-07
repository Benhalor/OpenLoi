## Introduction
It is developed using Python and Flask.

## How to start

### Developement
To start in a developement environement, first place yourself in the api/ folder and create a Python venv with :
```
python -m venv venv
```

Activate the venv :
```
source venv/bin/activate
```

If needed, install requirements with :
```
venv/bin/python -m pip install -r requirements.txt
```

Finally, you can start the server :
```
venv/bin/flask run
```

The server should start on 127.0.0.1:5000 by default.
When running in the developement environement, Flask should auto-reload the server if the code changes.

### Production
See README.MD in root folder