from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form
from GANEX.dlexmongo import addInfoToExp, getInfoExp, addImage, getImagePaths
from GANEX.fastGAN.ganInit.ganInit import createDataLoader, initDevice, generateInputImageGrid

# Blue print
bp = Blueprint('data', __name__, url_prefix='/run')

dataloader = None

# datasetup page
@bp.route('/<pid>/<expid>/data/', methods=('GET',))
def data(pid, expid):
    db = get_db()

    print()

    infoDict = getInfoExp(db, expid)
    return render_template('run/data.html', pid=pid, expid=expid, infoDict = infoDict)

# get data folder
@bp.route('/<pid>/<expid>/setDataFolder', methods=('GET', 'POST'))
def setDataFolder(pid, expid):
    print("test")
    print(request.args.get('path'))

    db = get_db()


    addInfoToExp(db, expid, "expDataPath", request.args.get('path'))
    infoDict = getInfoExp(db, expid)
    return jsonify(current_path = infoDict["expDataPath"])


@bp.route('/<pid>/<expid>/testDataLoad', methods=('GET', 'POST'))
def testDataLoad(pid, expid):
    db =get_db()
    img_path_list  = getImagePaths(db, expid, "INPUTDATA")
    
    print("test data load")
    print(img_path_list)
    
    return jsonify(x=img_path_list)


@bp.route('/<pid>/<expid>/testData', methods=('GET', 'POST'))
def testData(pid, expid):
    db =get_db()

    try:
        dataloader = createDataLoader(db, pid, expid)
        device = initDevice(db, pid, expid)
        print(device)
        print(dataloader)
        imgpath = addImage(db, expid, "INPUTDATA")
        print(imgpath)

        generateInputImageGrid(dataloader, imgpath, device)

        print("test data")
        


    except Exception as e:
        flash(e)

    img_path_list  = getImagePaths(db, expid, "INPUTDATA")

    
    return jsonify(imgpaths=img_path_list)

