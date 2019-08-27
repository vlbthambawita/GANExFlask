function init_socket_ons(){
    window.socket.on("projects-get-gans", function(gan_type_list){
        console.log(gan_type_list)
        generate_tbl_gan_types(gan_type_list)
    })
}


function rqst_gan_types(){
   // alert("Request")
    window.socket.emit("projects-rqst-gan-types")
}

function del_gan_type(){
    console.log(this.value)
    window.socket.emit("projects-rqst-del-gantype", this.value)
}




function generate_tbl_gan_types(gan_list){ // gan_list -> a list of dictionary ()
    
    var tbl = document.getElementById("tbl_gan_types")
    tbl.innerHTML = ""
  
    var header = tbl.createTHead();
  
    var row = header.insertRow(0)
  
    var cell0 = row.insertCell(0)
    var cell1 = row.insertCell(1)
    var cell2 = row.insertCell(2)
    var cell3 = row.insertCell(3)
    
    
  
    cell0.innerHTML = "<b>GAN Name</b>"
    cell1.innerHTML = "<b>GAN Directory</b>"
    cell2.innerHTML = "<b>GAN File</b>"
    cell3.innerHTML = "<b>GAN Class Name</b>"
    
    
  
    var i ;
    for (i= 0; i < gan_list.length; i++){
  
        var row = tbl.insertRow(i+1);
  
        var cell0 = row.insertCell(0);
        var cell1 = row.insertCell(1);
        var cell2 = row.insertCell(2);
        var cell3 = row.insertCell(3);
        var cell4 = row.insertCell(4);
        
  
        var btn_del = document.createElement("BUTTON");
        var btn_text = document.createTextNode("Delete")
        btn_del.setAttribute("value",gan_list[i].name) //settings_list[i][0]
        btn_del.onclick =  del_gan_type;       
        btn_del.appendChild(btn_text)
        btn_del.className = "btn btn-danger"

        
  

        cell0.innerHTML = gan_list[i].name;
        cell1.innerHTML = gan_list[i].dir;
        cell2.innerHTML = gan_list[i].file;
        cell3.innerHTML = gan_list[i].class;
        
        cell4.appendChild(btn_del)  
        //cell3.appendChild(btn_show)        
       // alert(i)
  
    }
    
    // alert("table updated")
  }