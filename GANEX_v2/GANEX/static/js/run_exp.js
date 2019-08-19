function init_sockets_ons(){
    window.socket.on("runexp-get-current-state-info", function(info_data){
            console.log(info_data)
            var status = info_data.current_status

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