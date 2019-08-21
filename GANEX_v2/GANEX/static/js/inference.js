function init_socket_ons(){
    window.socket.on('inference-get-available-models', function(model_list){
        console.log(model_list)
        generate_tbl_for_models(model_list)
    })

}


function request_available_model_list(){
    window.socket.emit("inference-request-available-models", window.pid, window.expid) 
}


function del_model(){
    console.log("Delete models")
}



// Generate a table for generated images
function generate_tbl_for_models(model_list){
    
    var tbl = document.getElementById("tbl_models")
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
        
  
        var btn_del = document.createElement("BUTTON");
        var btn_text = document.createTextNode("Delete")
        btn_del.setAttribute("value",model_list[i].imgpath)
        btn_del.onclick =  del_model;       
        btn_del.appendChild(btn_text)

        
  

        cell1.innerHTML = model_list[i].iter;
        cell2.appendChild(btn_del)  
       // cell3.appendChild(btn_show)        
       // alert(i)
  
    }
    
    // alert("table updated")
  }