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
                btn_retrain.disabled = true;
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

  //  window.socket.on("runexp-get-available-checkpoints")

}

function request_current_info(){
    window.socket.emit('runexp-request-info', window.onpagehide, window.expid)
}