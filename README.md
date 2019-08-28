# GANExFlask

**This is the beta version GANExFLASK -  still under development**

## Requirements

1. dash
2. Flask-SocketIO
3. Flask-PyMongo
4. Flask-WTF

## How to RUN?

### 1. Install MongoDB
- [Install local MongoDB](https://docs.mongodb.com/manual/installation/).
        

- or [getting started with MongoDB Atlas Free account](https://docs.atlas.mongodb.com/getting-started/#deploy-a-free-tier-cluster)

###   2. Install Requirements (Using pip or conda)
Note: If you faced any problem to install one of the above requirements from conda command then try to install same package using pip. [Read this for more information](https://www.anaconda.com/using-pip-in-a-conda-environment/)

###    3. Download or clone this git repository

###    5. Add database linnk to GANExFlask/GANEX/GANEX/db.py file
Ex: current_app.config["MONGO_URI"] = "mongodb+srv://test:test_pswd@cluster0-uv3hx.mongodb.net/test?retryWrites=true&w=majority" #"mongodb://localhost:27017/GANEXdb"

###    4. Run the file called ganex.py
python GANExFlask/GANEX/ganex.py

:+1:
        