// var socket = io('/experiments');
// var pid = window.pid;






function init_load(){
  //  alert("inti load")

    window.socket.on('get_default_hyperparams', function(data){
      //  alert("get default hyper param initializations")
        update_table(data)
      //  alert("data" + data)
    })  

    window.socket.on('get-exp-default-para', function(data){
      console.log(data)
    })

    window.socket.emit("get_initial_default_params", pid= window.pid)

    window.socket.emit("request_default_exp_para", window.pid)

    
}

function btn_del_click(value){
    //alert("btn clicked" + value)
    window.socket.emit("default_param_del", key=value, pid=window.pid)

    //socket.on('get_default_hyperparams', function(data){
     //   alert("get default hyper param btn del clicked")
      //  update_table(data)
    //})
}

function btnAddClick(){
    //alert("btn add clicked")
    window.socket.emit('default_param_add', {"para_name": $("#para_name").val(), 
                        "para_key": $("#para_key").val(),
                        "para_value": $("#para_value").val()}, pid=window.pid);

    document.getElementById("para_name").value ="";
    document.getElementById("para_key").value ="";
    document.getElementById("para_value").value ="";

    //socket.on('get_default_hyperparams', function(data){
     //   alert("get default hyper param btn add click")
      //  update_table(data)
    //})
}

function update_table(para_list){
    
    var tbl = document.getElementById("tbl_params")
    tbl.innerHTML = ""

    var header = tbl.createTHead();

    var row = header.insertRow(0)

    var cell0 = row.insertCell(0)
    var cell1 = row.insertCell(1)
    var cell2 = row.insertCell(2)

    cell0.innerHTML = "Parameter Name"
    cell1.innerHTML = "Parameter Key"
    cell2.innerHTML = "Parameter Default Value"

    var i ;
    for (i= 0; i < para_list.length; i++){

        var row = tbl.insertRow(i+1);

        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);

        var btn_del = document.createElement("BUTTON");
        var btn_text = document.createTextNode("Delete")
        btn_del.setAttribute("value",para_list[i].para_key)
        btn_del.setAttribute("name", "btn_delete")
        btn_del.setAttribute("onclick", "btn_del_click(this.value)")
        btn_del.appendChild(btn_text)

        cell1.innerHTML = para_list[i].para_name;
        cell2.innerHTML = para_list[i].para_key;
        cell3.innerHTML = para_list[i].para_value;
        cell4.appendChild(btn_del)       
       // alert(i)

    }
    
    // alert("table updated")
}

/////////// Exp para add /////////////////////

function btn_exp_para_add(){

  window.socket.emit('default-exp-para-add', {"para_name": $("#para_name").val(), 
                        "para_key": $("#para_key").val(),
                        "para_value": $("#para_value").val()}, pid=window.pid);

    document.getElementById("para_name").value ="";
    document.getElementById("para_key").value ="";
    document.getElementById("para_value").value ="";

}