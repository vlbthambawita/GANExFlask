from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session, send_from_directory
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId
import importlib



from GANEX.db import get_db
from GANEX.forms import CreateProject_form
from GANEX.dlexmongo import addInfoToExp, getInfoExp, addImage, getImagePaths, getGANInfo
from GANEX.fastGAN.ganInit.ganInit import createDataLoader, initDevice, generateInputImageGrid
from GANEX.plots import imageplot

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

# when load test data section
@bp.route('/<pid>/<expid>/testDataLoad', methods=('GET', 'POST'))
def testDataLoad(pid, expid):
    db =get_db()
    img_path_list  = getImagePaths(db, expid, "INPUTDATA")

    # plot = imageplot.createImagePlot()
    
    print("test data load")
    print(img_path_list)
    
    return jsonify(imgpathlist=img_path_list)


@bp.route('/<pid>/<expid>/generateTestData', methods=('GET', 'POST'))
def generateTestData(pid, expid):
    db =get_db()

    #try:
    dataloader = createDataLoader(db, pid, expid)
    device = initDevice(db, pid, expid)
    print(device)
    print(dataloader)
    imgpath = addImage(db, expid, "INPUTDATA")
    print(imgpath)


    # generateInputImageGrid(dataloader, imgpath, device)
    
    #===============================================
    # Use selected GAN image grid generate function
    #===============================================
    (ganFile, ganClass) = getGANInfo(db, expid)
     # import gan from gan file
    my_module = importlib.import_module("GANEX.fastGAN.{}".format(ganFile))
    gan = eval("my_module.{}(db, pid, expid)".format(ganClass))
    gan.setDevice()
    gan.prepareData()
    gan.generate_input_image_grid(imgpath)


    print("test data")
    #return jsonify(imgpath=imgpath)
        


    #except Exception as e:
     #   flash(e)

   # img_path_list  = getImagePaths(db, expid, "INPUTDATA")
   # print("image path list:", img_path_list)

    
    return jsonify(imgpath=imgpath)


@bp.route('/loadselectimage/', methods=('GET',))
def loadselectimage():
    print("image selected")
    selected_img_path = request.args.get("selectedpath")
    print(selected_img_path)
    plot = imageplot.createImagePlot(selected_img_path)
    return jsonify(x=7878, plot=plot )


@bp.route('/<pid>/<expid>/sendImage', methods=('GET', 'POST'))
def sendImage(pid, expid):
    return send_from_directory("/home/vajira/DL/ganexprojects/p3/DCGAN ex1/output", "5d5179b3cc4f4a7e4c4c9860.png")

