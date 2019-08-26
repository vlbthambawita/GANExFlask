import time

from flask import session, flash
from flask_socketio import emit, join_room, leave_room
#from . import socketio
from GANEX.fastGAN.task import randnumber
# socketio = get_socket()
from GANEX.updates import updateplot
from GANEX.db import get_db
from GANEX.utils import create_gan_object

from GANEX.dlexmongo import (set_train_settings, set_default_hyperparam, get_default_hyperparams, del_default_hyperpram,
                                getImagePaths, delImgPath, addImage, getGANInfo,
                                getPlotStats, addPlotStat, getExpState, getInfoExp,
                                get_train_settings, 
                                set_default_exp_para, get_default_exp_para,
                                del_default_exp_para, get_exp_default_para_info,
                                get_output_imgs
                            )
# second import list from sama location
from GANEX.dlexmongo import (get_models, del_model, del_plt_stat, get_gan_types,
                                del_gan_type, setExpState, delTrainStats, update_exp_info
                            )

from GANEX.plots import imageplot, training_plots

import threading
import importlib

# from . import socketio

def init_events(socketio):

    # global socketio
   # db = get_db() # this is not working, some context problem

##################################################################
## Test caseses
#####################################################################

    @socketio.on('joined', namespace='/chat')
    def joined(message):
        """Sent by clients when they enter a room.
        A status message is broadcast to all people in the room."""
        print("Joined is running")
        emit('status', {'msg': 'connected from server'})

        x = threading.Thread(target=randnumber, args=(socketio,))
        x.start()



    

            # x = threading.Thread(target=updateplot, args=(socketio,get_db()))
            
            #if (msg["status"] == "connected") and (x.is_alive() != True):
            #    print("plot tab connected")
            #    x.start()

##########################################################################
# Projects window handling
##########################################################################
    @socketio.on("projects-rqst-gan-types", namespace='/projects')
    def rqst_gan_types():
        db = get_db()
        ganlist = get_gan_types(db)
        emit("projects-get-gans", ganlist, namespace="/projects")


    @socketio.on("projects-rqst-del-gantype", namespace='/projects')
    def rqst_del_gantype(gan_name):
        db = get_db()
        del_gan_type(db, gan_name)
        ganlist = get_gan_types(db)
        emit("projects-get-gans", ganlist, namespace="/projects")




    


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

    # Delete method for generated test data
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

    # Delete method for analyse data
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
        (ganDir, ganFile, ganClass) = getGANInfo(db, expid)
        # import gan from gan file
        #* my_module = importlib.import_module("GANEX.fastGAN.{}".format(ganFile))
        #* gan = eval("my_module.{}(db, pid, expid)".format(ganClass))
        gan = create_gan_object(db, pid, expid, ganDir, ganFile, ganClass)
        #gan.setDevice()
        #gan.prepareData()

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
                    "current_epoch": current_epoch, "current_iter": exp_info["iters"],
                    "dataloader_size": exp_info["dataloader_size"] }

                    
        emit('runexp-get-current-state-info', info_dict, namespace='/runexp')
        print("emitted to runexp")


    # send available checkpoints to window
    @socketio.on("runexp-rqst-available-checkpoints", namespace='/runexp')
    def rqst_available_checkpoints(pid, expid):
        db = get_db()
        model_data_list  = get_models(db, pid, expid)
        print(model_data_list)
        emit("runexp-get-available-checkpoints", model_data_list, namespace='/runexp')




    # Train button functionalities
    @socketio.on("runexp-rqst-train-exp", namespace='/runexp')
    def rqst_train_exp(pid, expid):
        print("Training")
        try:
            db = get_db()
           #  status = getExpState(db, expid)
            (ganDir, ganFile, ganClass) = getGANInfo(db, expid)
            gan = create_gan_object(db, pid, expid, ganDir, ganFile, ganClass)
            # gan.run()
            x = threading.Thread(target=gan.run)
            x.start()
            setExpState(db, expid, "RETRAIN")

            

        except Exception as e:
            print(str(e))

    # Retrain btn functionalities
    @socketio.on("runexp-rqst-retrain-exp", namespace='/runexp')
    def rqst_retrain_exp(pid, expid, model_path):
        print("Re-Training")
        print("Model path ", model_path)
        try:
            db = get_db()
            # status = getExpState(db, expid)
            (ganDir, ganFile, ganClass) = getGANInfo(db, expid)
            gan = create_gan_object(db, pid, expid, ganDir, ganFile, ganClass)
            # gan.rerun()
            x = threading.Thread(target=gan.rerun, args=(model_path,))
            x.start()
            setExpState(db, expid, "RETRAIN")

        except Exception as e:
            print(str(e))

    # Reset btn functionalities
    @socketio.on("runexp-rqst-reset-exp", namespace='/runexp')
    def rqst_reset_exp(pid, expid):
        try:
            db = get_db()
            delTrainStats(db, expid)
            setExpState(db, expid, "TRAIN")

            # reset default exp para
            exp_para_list = get_default_exp_para(db, pid)
            for exp_para in exp_para_list:
                temp_dict = {exp_para["para_key"]: exp_para["para_value"]}
                update_exp_info(db, expid, temp_dict)
                print("exp para :", exp_para )

        except Exception as e:
            print(str(e))

    
    

    @socketio.on("runexp-rqst-del-model", namespace='/runexp')
    def rqst_del_model_runexp_window(pid, expid, model_path):
        db = get_db()
        del_model(db, pid, expid, model_path)
        model_data_list  = get_models(db, pid, expid)
        emit("runexp-get-available-checkpoints", model_data_list, namespace='/runexp')







##########################################################################
# Plot window handling
###########################################################################

    # plot sta handle - near real time
    @socketio.on('plotting', namespace='/plot')
    def plotting(msg):
        updateplot(socketio, get_db())


    @socketio.on("plot-update-plots", namespace="/plot")
    def update_plots(expid):
        print("expid -",expid)

        db = get_db()
        statlist = getPlotStats(db, expid)
        
        if len(statlist) > 0:
            # plots = training_plots.trainLossPlot(db, expid, statlist)
            plots = training_plots.trainLossPlot_v3(db, expid, statlist)
            emit("plot-get-plots-data", plots ,namespace="/plot")
            print("plot emited")

    @socketio.on("plot-update-plot-settings", namespace="/plot")
    def update_plot_settings(expid, plot_stat_name, plot_id):
        db = get_db()

        addPlotStat(db, expid, plot_stat_name, plot_id)
        plt_settings_list = getPlotStats(db, expid)
        emit("plt-get-plt-settings",plt_settings_list,  namespace="/plot")
        print("plot settings updated")



    @socketio.on("plt-rqst-plt-setttings", namespace="/plot")
    def plt_rqst_plt_settings(pid, expid):
        db = get_db()
        plt_settings_list = getPlotStats(db, expid)
        print("plt settings list ", plt_settings_list)
        emit("plt-get-plt-settings",plt_settings_list,  namespace="/plot")

    
    @socketio.on("plt-rqst-del-plt-setting", namespace="/plot")
    def rqst_del_plt_setting(pid, expid, plt_values):  # plt_values = [plt_stat_name, plt_id]
        db = get_db()
        del_plt_stat(db, expid, plt_values[0], plt_values[1] )
        plt_settings_list = getPlotStats(db, expid)
        emit("plt-get-plt-settings",plt_settings_list,  namespace="/plot")



#################################################################################
# Inference window handling
#################################################################################

    @socketio.on("inference-request-available-models", namespace="/inference")
    def request_available_models(pid, expid):
        db = get_db()
        model_data_list  = get_models(db, pid, expid)
        emit("inference-get-available-models", model_data_list, namespace='/inference')

    @socketio.on("inference-request-available-inferenced-imgs", namespace="/inference")
    def request_available_inferenced_imgs(pid, expid):
        db = get_db()
        img_list = get_output_imgs(db, expid, "INFERENCED")

        emit("inference-get-inferenced-imgs", img_list, namespace='/inference' )

    
    @socketio.on("inference-request-inference-generate", namespace="/inference")
    def request_inference_generate(pid, expid, model_path):
        
        print("Request received to make inference plot")
        db =get_db()

        (ganDir, ganFile, ganClass) = getGANInfo(db, expid)
       # my_module = importlib.import_module("GANEX.fastGAN.{}".format(ganFile))
       # gan = eval("my_module.{}(db, pid, expid)".format(ganClass))
        gan = create_gan_object(db, pid, expid, ganDir, ganFile, ganClass)
        gan.inference(model_path)

        img_list = get_output_imgs(db, expid, "INFERENCED")

        emit("inference-get-inferenced-imgs", img_list, namespace='/inference' )
        print(img_list)


    @socketio.on("inference-rqst-del-img", namespace='/inference')
    def rqst_del_img(expid, path):
        db = get_db()
        delImgPath(db,expid, path) 
        img_list = get_output_imgs(db, expid, "INFERENCED")

        emit("inference-get-inferenced-imgs", img_list, namespace='/inference' )

    
    @socketio.on("inf-rqst-show-img", namespace='/inference')
    def rqst_show_img(path):
        plot = imageplot.createImagePlot(path)
        emit('inf-get-img-plt', plot, namespace='/inference')

    
    @socketio.on("inf-rqst-del-model", namespace='/inference')
    def rqst_del_model(pid, expid, model_path):
        db = get_db()
        del_model(db, pid, expid, model_path)
        model_data_list  = get_models(db, pid, expid)
        emit("inference-get-available-models", model_data_list, namespace='/inference')







       