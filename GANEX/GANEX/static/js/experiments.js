// var socket = io('/experiments');
// var pid = window.pid;






function init_load(){
  //  alert("inti load")

    window.socket.on('get_default_hyperparams', function(data){
      //  alert("get default hyper param initializations")
        update_table(data)
      //  alert("data" + data)
    })  

    window.socket.on('get-exp-default-para', function(para_list){
      console.log(para_list)
      update_default_exp_para_table(para_list)
    })

    // update experiments table
    window.socket.on("exp-get-exps", function(exp_list){
      var exp_list = JSON.parse(exp_list)
      console.log(exp_list)
      generate_tbl_experiments(exp_list);
    })

    // update gan types
    window.socket.on("exp-get-gans", function(exp_gan_list){
      
      console.log(exp_gan_list)
     // generate_tbl_experiments(exp_list);

      update_gan_options(exp_gan_list);
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
  alert("btn clicked")
  window.socket.emit('default-exp-para-add', window.pid, 
                      document.getElementById("exp_para_name").value,
                      document.getElementById("exp_para_key").value,
                      document.getElementById("exp_para_value").value                  
  );

    document.getElementById("para_name").value ="";
    document.getElementById("para_key").value ="";
    document.getElementById("para_value").value ="";

}

function del_default_exp_para(value){

  window.socket.emit("request-del-default-para",  pid=window.pid, key=value )  
}


function update_default_exp_para_table(para_list){
    
  var tbl = document.getElementById("tbl_default_exp_para")
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
      btn_del.setAttribute("name", "btn_delete_exp_para")
      btn_del.setAttribute("onclick", "del_default_exp_para(this.value)")
      btn_del.appendChild(btn_text)

      cell1.innerHTML = para_list[i].para_name;
      cell2.innerHTML = para_list[i].para_key;
      cell3.innerHTML = para_list[i].para_value;
      cell4.appendChild(btn_del)       
     // alert(i)

  }
  
  // alert("table updated")
}

// ***************************************
/// Experiment Home window handling
// ***************************************

function update_gan_types_list(){
  
  window.socket.emit("exp-rqst-gan-types")
}

function rqst_exps_of_pid(){
  window.socket.emit("exp-rqst-exps", window.pid)
}

// create exp btn function
function click_btn_create_exp(){
  exp_name = document.getElementById("input_exp_name").value
  exp_type = document.getElementById("select_exp_gan_type").value

  alert(exp_type)
  window.socket.emit("exp-rqst-create-exp", window.pid, exp_name, exp_type)

}


function del_exp(){
  alert("Delete exp")
  window.socket.emit("exp-rqst-create-exp", window.pid, this.value)
}


// Table for available experiments
function generate_tbl_experiments(exp_list){ // gan_list -> a list of dictionary ()
    
  var tbl = document.getElementById("tbl_experiments")
  tbl.innerHTML = ""

  var header = tbl.createTHead();

  var row = header.insertRow(0)

  var cell0 = row.insertCell(0)
  var cell1 = row.insertCell(1)
  var cell2 = row.insertCell(2)
  var cell3 = row.insertCell(3)
 
  cell0.innerHTML = "<b>Experiment ID</b>"
  cell1.innerHTML = "<b>Experiment Name</b>"
  cell2.innerHTML = "<b>Experiment Path</b>"
  cell3.innerHTML = "<b>Experiment Type</b>"

  var url = window.location;
  var main_url = url.protocol + "//" + url.host + "/run"
  
 // alert(main_url)
  
  var i ;
  for (i= 0; i < exp_list.length; i++){

      var row = tbl.insertRow(i+1);

      // entry pid and expid
      var pid = exp_list[i].pid
      var expid = exp_list[i]._id.$oid

      var cell0 = row.insertCell(0);
      var cell1 = row.insertCell(1);
      var cell2 = row.insertCell(2);
      var cell3 = row.insertCell(3);
      var cell4 = row.insertCell(4);
     

      var btn_del = document.createElement("BUTTON");
      var btn_text = document.createTextNode("Delete")
      btn_del.setAttribute("value",expid) //$oid - comes form dumps function
      btn_del.onclick =  del_exp;       
      btn_del.appendChild(btn_text)
      btn_del.className = "btn btn-danger"

      var a = document.createElement('a');
      var linkText = document.createTextNode(exp_list[i].name);
      a.appendChild(linkText);
      a.href = main_url + "/" + pid + "/" + expid + "/summary";
      a.setAttribute("target", "_blank")
     // a.href= Flask.url_for('experiments.create', {pid:pro_id})

      


      cell0.innerHTML = expid;
     // cell1.innerHTML = project_list[i].name;
      cell1.appendChild(a)
      cell2.innerHTML = exp_list[i].path;
      cell3.innerHTML = exp_list[i].type
      
      cell4.appendChild(btn_del)  
      //cell3.appendChild(btn_show)        
     // alert(i)

  }
  
  // alert("table updated")
}


function update_gan_options(gan_list){

    var sel = document.getElementById("select_exp_gan_type")

    sel.innerHTML = ""

    for (var i =0; i < gan_list.length ; i++){
      var option = document.createElement("option");
      option.text = gan_list[i].name;
      option.value = gan_list[i].name;
      sel.add(option);
    }
    

}