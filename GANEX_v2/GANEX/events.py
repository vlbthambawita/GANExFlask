import time

from flask import session
from flask_socketio import emit, join_room, leave_room
#from . import socketio
from GANEX.fastGAN.task import randnumber
# socketio = get_socket()
from GANEX.updates import updateplot
from GANEX.db import get_db

from GANEX.dlexmongo import (set_train_settings, set_default_hyperparam, get_default_hyperparams, del_default_hyperpram,
                                getImagePaths, delImgPath, addImage, getGANInfo,
                                getPlotStats, addPlotStat, getExpState, getInfoExp,
                                get_train_settings, 
                                set_default_exp_para, get_default_exp_para,
                                del_default_exp_para, get_exp_default_para_info,
                                get_output_imgs
                            )

from GANEX.plots import imageplot, training_plots

import threading
import importlib

# from . import socketio

def init_events(socketio):

    # global socketio
   # db = get_db() # this is not working, some context problem

    @socketio.on('joined', namespace='/chat')
    def joined(message):
        """Sent by clients when they enter a room.
        A status message is broadcast to all people in the room."""
        print("Joined is running")
        emit('status', {'msg': 'connected from server'})

        x = threading.Thread(target=randnumber, args=(socketio,))
        x.start()

    # plot sta handle - near real time
    @socketio.on('plotting', namespace='/plot')
    def plotting(msg):
        updateplot(socketio, get_db())

            # x = threading.Thread(target=updateplot, args=(socketio,get_db()))
            
            #if (msg["status"] == "connected") and (x.is_alive() != True):
            #    print("plot tab connected")
            #    x.start()
            

##############################################################################
# Experiments window handlings 
###############################################################################
    
    # Experiments window handlings           
    @socketio.on('default_param_add', namespace='/experiments')
    def add_default_param(data, pid):
        db = get_db()
        print("arg1", data)
        print("pid:", pid)

        # update db
        set_default_hyperparam(db, pid, data["para_name"], data["para_key"], data["para_value"])
        all_hyperparams = list(get_default_hyperparams(db, pid))

        emit('get_default_hyperparams', all_hyperparams, namespace='/experiments')

    
    @socketio.on("default_param_del", namespace='/experiments')
    def del_default_param(key,pid):
        print("key", key)
        print("pid", pid)
        db =get_db()
        del_default_hyperpram(db, pid, key)

        all_hyperparams = list(get_default_hyperparams(db, pid))

        emit('get_default_hyperparams', all_hyperparams, namespace='/experiments')

    @socketio.on("get_initial_default_params", namespace='/experiments')
    def get_initial_params(pid):
        db = get_db()
        all_hyperparams = list(get_default_hyperparams(db, pid))
        print("initial all hyperparams", all_hyperparams)
        emit('get_default_hyperparams', all_hyperparams , namespace='/experiments')


    # Exp para add
    @socketio.on("default-exp-para-add", namespace='/experiments')
    def default_exp_para_add(pid, para_name, para_key, para_value):
        db = get_db()

        set_default_exp_para(db, pid, para_name, para_key, para_value)
        default_exp_para_list = get_default_exp_para(db, pid)
        emit("get-exp-default-para", default_exp_para_list, namespace='/experiments')

    @socketio.on("request_default_exp_para", namespace='/experiments')
    def request_default_exp_para(pid):
        db = get_db()
        default_exp_para_list = get_default_exp_para(db, pid)
        emit("get-exp-default-para", default_exp_para_list, namespace='/experiments')

    @socketio.on("request-del-default-para", namespace='/experiments')
    def request_del_default_para(pid, key):
        db = get_db()
        del_default_exp_para(db, pid, key)
        default_exp_para_list = get_default_exp_para(db, pid)
        emit("get-exp-default-para", default_exp_para_list, namespace='/experiments')





###############################################################
# Summary tab handling
###############################################################
    @socketio.on("summary-request-editable", namespace='/summary')
    def summary_request_editable(pid, expid):
        db = get_db()
        output_dict = get_exp_default_para_info(db, expid)
        print(output_dict)
        emit("summary-get-exp-info", output_dict, namespace='/summary')
        print("emited editable summary")






##############################################################
# Data window handlings
##############################################################

    @socketio.on("data-delete-img", namespace='/data')
    def del_img_path(pid, expid, path):
        db = get_db()
        print("pid:", pid)
        print("EXPID:", expid)
        print("path:", path)
        delImgPath(db,expid, path) # old method
        # del_img_path(db, expid, path) # new method
        img_path_list  = getImagePaths(db, expid, "INPUTDATA")
        emit('data-get-img-paths', img_path_list, namespace='/data')
        
        print("Emitted")

    
    @socketio.on("data-delete-gen-img", namespace='/data')
    def del_gen_img_path(pid, expid, path):
        
        db = get_db()
        delImgPath(db, expid, path)
        img_gen_list  = get_output_imgs(db, expid, "GENDATA")
        emit('data-get-gen-images', img_gen_list, namespace='/data')
        
        print("Emitted to data-get-gen-images")


    @socketio.on("data-load-imgs", namespace='/data')
    def load_img_paths(pid, expid):
        print("data load imgs")
        db = get_db()
        img_path_list  = getImagePaths(db, expid, "INPUTDATA")
        emit('data-get-img-paths', img_path_list, namespace='/data')
        print("Emitted dataload imgs")

    @socketio.on("data-gen-img", namespace='/data')
    def generate_sample_img(pid, expid):
        db =get_db()
        # add image path to db
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

        imgpath = addImage(db, expid, "INPUTDATA")

        gan.generate_input_image_grid(imgpath)

        img_path_list  = getImagePaths(db, expid, "INPUTDATA")
        emit('data-get-img-paths', img_path_list, namespace='/data')



    @socketio.on("data-show-img", namespace='/data')
    def show_img(path):

        plot = imageplot.createImagePlot(path)
        emit('data-get-img-plot', plot, namespace='/data')


    @socketio.on("data-show-gen-img", namespace='/data')
    def show_gen_img(path):

        plot = imageplot.createImagePlot(path)
        emit('data-get-gen-img-plot', plot, namespace='/data')



    @socketio.on('data-request-gan-gen-images', namespace='/data')
    def data_request_gan_gen_images(pid, expid):
        db =get_db()
        img_list  = get_output_imgs(db, expid, "GENDATA")
        emit('data-get-gen-images', img_list , namespace='/data')




#######################################################################
# RUN Experiment window handling
#######################################################################

    @socketio.on("runexp-request-info", namespace='/runexp')
    def request_runexp_info(pid, expid):

        db = get_db()
        status = getExpState(db, expid)

        exp_info = getInfoExp(db, expid)
        current_epoch = exp_info["current_epoch"]
        print("current epoch", current_epoch)

        # get total epochs to run
        train_settings = get_train_settings(db, expid)
        total_epochs_to_run = train_settings["num_epochs"]
        print("total epoch to run", total_epochs_to_run)
        
        print("trainsettings:", train_settings)

        info_dict = {"current_status": status, "total_epochs_to_run": total_epochs_to_run, 
                    "current_epoch": current_epoch }

                    
        emit('runexp-get-current-state-info', info_dict, namespace='/runexp')
        print("emitted to runexp")









##########################################################################
# Plot window handling
###########################################################################


    @socketio.on("plot-update-plots", namespace="/plot")
    def update_plots(expid):
        print("expid -",expid)

        db = get_db()
        statlist = getPlotStats(db, expid)
        
        if len(statlist) > 0:
            plots = training_plots.trainLossPlot(db, expid, statlist)
            emit("plot-get-plots-data", plots ,namespace="/plot")
            print("plot emited")

    @socketio.on("plot-update-plot-settings", namespace="/plot")
    def update_plot_settings(expid, plot_stat_name, plot_id):
        db = get_db()

        addPlotStat(db, expid, plot_stat_name, plot_id)
        print("plot settings updated")







       