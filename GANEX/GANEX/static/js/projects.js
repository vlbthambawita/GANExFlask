function init_socket_ons(){
    window.socket.on("projects-get-gans", function(gan_type_list){
        //console.log(gan_type_list)
        generate_tbl_gan_types(gan_type_list)
    })

    window.socket.on("projects-get-projects", function(project_list){
        var p_list = JSON.parse(project_list)
        //console.log(p_list)
        generate_tbl_projects(p_list)
    })
}


function rqst_gan_types(){
   // alert("Request")
    window.socket.emit("projects-rqst-gan-types")
}

function del_gan_type(){
    //console.log(this.value)
    window.socket.emit("projects-rqst-del-gantype", this.value)
}


// Request projects
function rqst_projects(){
    window.socket.emit("projects-rqst-projects")
}

// create project btn click
function click_create_project(){
    //alert("project create request")
    pro_name = document.getElementById("input_proName").value
    pro_path = document.getElementById("input_proPath").value
    window.socket.emit("projects-rqst-create-project", pro_name, pro_path)
}

// Project delete function
function del_project(){

    //console.log("Delete project"+ this.value)
    window.socket.emit("projects-rqst-delete-project", this.value)
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


  // Table for available projects
  function generate_tbl_projects(project_list){ // gan_list -> a list of dictionary ()
    
    var tbl = document.getElementById("tbl_crnt_projects")
    tbl.innerHTML = ""
  
    var header = tbl.createTHead();
  
    var row = header.insertRow(0)
  
    var cell0 = row.insertCell(0)
    var cell1 = row.insertCell(1)
    var cell2 = row.insertCell(2)
   
    cell0.innerHTML = "<b>Project ID</b>"
    cell1.innerHTML = "<b>Project Name</b>"
    cell2.innerHTML = "<b>Project Path</b>"

    var url = window.location;
    var main_url = url.protocol + "//" + url.host
    
   // alert(main_url)
    
    var i ;
    for (i= 0; i < project_list.length; i++){
  
        var row = tbl.insertRow(i+1);

        var pro_id = project_list[i]._id.$oid
  
        var cell0 = row.insertCell(0);
        var cell1 = row.insertCell(1);
        var cell2 = row.insertCell(2);
        var cell3 = row.insertCell(3);
       
  
        var btn_del = document.createElement("BUTTON");
        var btn_text = document.createTextNode("Delete")
        btn_del.setAttribute("value",pro_id) //$oid - comes form dumps function
        btn_del.onclick =  del_project;       
        btn_del.appendChild(btn_text)
        btn_del.className = "btn btn-danger"

        var a = document.createElement('a');
        var linkText = document.createTextNode(project_list[i].name);
        a.appendChild(linkText);
        a.href = main_url + "/" + pro_id + "/create";
       // a.href= Flask.url_for('experiments.create', {pid:pro_id})

        
  

        cell0.innerHTML = pro_id;
       // cell1.innerHTML = project_list[i].name;
        cell1.appendChild(a)
        cell2.innerHTML = project_list[i].path;
        
        
        cell3.appendChild(btn_del)  
        //cell3.appendChild(btn_show)        
       // alert(i)
  
    }
    
    // alert("table updated")
  }