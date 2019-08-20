function init_socket_ons(){
    window.socket.on("summary-get-exp-info", function(exp_info_dict){
        console.log(exp_info_dict)
        
        //for (const [key, value] of Object.entries(exp_info_dict)) {
         //   console.log(key, value);
       // }
       if (exp_info_dict != null){
        update_table(exp_info_dict)
       }
       
    })
}

function request_editable_exp_info(){
    window.socket.emit("summary-request-editable", window.pid, window.expid)
}

function update_table(info_dict){
    
    var tbl = document.getElementById("tbl_exp_info_editable")
    tbl.innerHTML = ""

    var header = tbl.createTHead();

    var row = header.insertRow(0)

    var cell0 = row.insertCell(0)
    var cell1 = row.insertCell(1)
   

    cell0.innerHTML = "Parameter Key"
    cell1.innerHTML = "Parameter Value"
    

    var i=1 ;
    for (const [key, value] of Object.entries(info_dict)){

        var row = tbl.insertRow(i);

        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        
        var btn_del = document.createElement("BUTTON");
        var btn_text = document.createTextNode("Delete")
        btn_del.setAttribute("value",key)
        btn_del.setAttribute("name", "btn_delete")
        btn_del.setAttribute("onclick", "btn_del_click(this.value)")
        btn_del.appendChild(btn_text)

        cell1.innerHTML = key;
        cell2.innerHTML = value;
       // cell3.innerHTML = para_list[i].para_value;
        cell3.appendChild(btn_del)   
        i++;    
       // alert(i)

    }
    
    // alert("table updated")
}