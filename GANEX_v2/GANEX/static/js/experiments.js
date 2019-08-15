var socket = io('/experiments');
var pid = window.pid;

function test(pid){
    alert(pid);
}

function set_pid_to_js_file(pid){
    pid = pid
}

function set_socket_to_js_file(socket){
    socket = socket;
}

function init_load(){
  //  alert("inti load")
    socket.emit("get_initial_default_params", pid= pid)

    socket.on('get_default_hyperparams', function(data){
        alert("get default hyper param initializations")
        update_table(data)
    })
}

function btn_del_click(value){
    alert("btn clicked" + value)
    socket.emit("default_param_del", key=value, pid=pid)

    socket.on('get_default_hyperparams', function(data){
        alert("get default hyper param")
        update_table(data)
    })
}

function btnAddClick(){
    //alert("btn add clicked")
    socket.emit('default_param_add', {"para_name": $("#para_name").val(), 
                        "para_key": $("#para_key").val(),
                        "para_value": $("#para_value").val()}, pid=pid);

    socket.on('get_default_hyperparams', function(data){
        alert("get default hyper param")
        update_table(data)
    })
}

function update_table(para_list){
    //alert(para_list.para_name)
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
    for (i= 1; i < para_list.length; i++){
        var row = tbl.insertRow(i);

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
    

}