function init_sockets_ons(){
    window.socket.on("runexp-get-current-state-info", function(info_data){
            console.log(info_data)
            var status = info_data.current_status

            var total_epochs_to_run = info_data.total_epochs_to_run
            var current_epoch = info_data.current_epoch

            var curren_progress = (Number(current_epoch) / Number(total_epochs_to_run)) * 100
            console.log(curren_progress)

            var pg_bar = document.getElementById("pg_bar_epoch")
            // set current progerss
            pg_bar.setAttribute("style", "width: "+ curren_progress + "%")


            // interation progress bar
            var total_iters = info_data.dataloader_size
            var curretn_iter = info_data.current_iter
            var current_iter_progress = (Number(curretn_iter) / Number(total_iters)) * 100
            
            var pg_iter_bar = document.getElementById("pg_bar_iters")
            pg_iter_bar.setAttribute("style", "width: "+ current_iter_progress + "%")
            


            var btn_train = document.getElementById("btnTrain")
            var btn_retrain = document.getElementById("btnRetrain")
            var btn_reset = document.getElementById("btnReset")


            if (status == "TRAIN"){
                
                btn_train.disabled = false;
                btn_retrain.disabled = false;
                btn_reset.disabled = true;
                           
            }

            else if (status == "RUNNING"){

                btn_train.disabled = true;
                btn_retrain.disabled = true;
                btn_reset.disabled = true;

            }

            else if (status == "RETRAIN"){

                btn_train.disabled = true;
                btn_retrain.disabled = false;
                btn_reset.disabled = false;
             
            }   
    })

    window.socket.on("runexp-get-available-checkpoints", function(model_list){
        console.log(model_list)
        generate_tbl_for_models(model_list)

    })

    

}

function request_current_info(){
    window.socket.emit('runexp-request-info', window.pid , window.expid)
}

// request available checkpoints to rerun
function rqst_available_checkpoints(){
    window.socket.emit('runexp-rqst-available-checkpoints', window.pid , window.expid)

}


// Button functions

function click_btn_train(){
    console.log("Train btn clicked")
    window.socket.emit("runexp-rqst-train-exp", window.pid, window.expid)

}

function click_btn_retrain(){
    console.log("Retrain btn clicked")

    var radios = document.getElementsByName("inference_model")

    for (var i = 0, length = radios.length; i < length; i++)
    {
        if (radios[i].checked)
        {
        // do whatever you want with the checked radio
            alert(radios[i].value);
            //window.socket.emit("inference-request-inference-generate", window.pid, window.expid, radios[i].value);
            window.socket.emit("runexp-rqst-retrain-exp", window.pid, window.expid, radios[i].value)
            break;
        }

        if (i == length -1){
            alert("Please select a model to inference...!")
        }


    }
    
}

function click_btn_reset(){
    console.log("BTn reset clicked")
    window.socket.emit("runexp-rqst-reset-exp", window.pid, window.expid)
}


function del_model(){
    console.log("Delete models")
    window.socket.emit("runexp-rqst-del-model", window.pid, window.expid, this.value)
}




// Generate a table for saved models
function generate_tbl_for_models(model_list){
    
    var tbl = document.getElementById("tbl_models_runexp_window")
    tbl.innerHTML = ""
  
    var header = tbl.createTHead();
  
    var row = header.insertRow(0)
  
    var cell0 = row.insertCell(0)
    
    
  
    cell0.innerHTML = "Model Iter"
    
    
  
    var i ;
    for (i= 0; i < model_list.length; i++){
  
        var row = tbl.insertRow(i+1);
  
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        
        var input_rd_btn = document.createElement("INPUT")
        input_rd_btn.setAttribute("type", "radio")
        input_rd_btn.setAttribute("name", "inference_model")
        input_rd_btn.setAttribute("value", model_list[i].path)
  
        var btn_del = document.createElement("BUTTON");
        var btn_text = document.createTextNode("Delete")
        btn_del.setAttribute("value",model_list[i].path)
        btn_del.onclick =  del_model;       
        btn_del.appendChild(btn_text)

        
  

        cell1.innerHTML = model_list[i].iter;
        cell2.appendChild(input_rd_btn)
        cell3.appendChild(btn_del)  
       // cell3.appendChild(btn_show)        
       // alert(i)
  
    }
    
    // alert("table updated")
  }