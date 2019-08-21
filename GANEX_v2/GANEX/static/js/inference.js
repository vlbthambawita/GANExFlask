function init_socket_ons(){
    window.socket.on('inference-get-available-models', function(model_list){
        console.log(model_list)
        generate_tbl_for_models(model_list)
    })

    window.socket.on('inference-get-inferenced-imgs', function(img_list){
        generate_tbl_for_inferenced_images(img_list)
    })

    window.socket.on("inf-get-img-plt", function(plot){
        const graph = JSON.parse(plot)
        Plotly.newPlot('plot_inferenced', graph,{})
    })

}


function request_available_model_list(){
    window.socket.emit("inference-request-available-models", window.pid, window.expid) 
}

function request_available_inferenced_imgs(){
    window.socket.emit("inference-request-available-inferenced-imgs", window.pid, window.expid)
}


function del_model(){
    console.log("Delete models")
}

function del_img(){
    console.log("Delete img")
    window.socket.emit("inference-rqst-del-img", window.expid, this.value)
}

function show_img(){
    console.log("show img")
    window.socket.emit("inf-rqst-show-img", this.value)
}

function onclick_btn_inference(){
    var radios = document.getElementsByName("inference_model")

    for (var i = 0, length = radios.length; i < length; i++)
    {
        if (radios[i].checked)
        {
        // do whatever you want with the checked radio
            alert(radios[i].value);
            window.socket.emit("inference-request-inference-generate", window.pid, window.expid, radios[i].value);
            
            break;
        }

        if (i == length -1){
            alert("Please select a model to inference...!")
        }


    }

    
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


// Inference image list
function generate_tbl_for_inferenced_images(img_list){

    var tbl = document.getElementById("tbl_gen_images")
    tbl.innerHTML = ""

    var header = tbl.createTHead();

    var row = header.insertRow(0)

    var cell0 = row.insertCell(0)



    cell0.innerHTML = "Image Iter"



    var i ;
    for (i= 0; i < img_list.length; i++){

        var row = tbl.insertRow(i+1);

        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        

        var btn_del = document.createElement("BUTTON");
        var btn_text = document.createTextNode("Delete")
        btn_del.setAttribute("value",img_list[i].imgpath)
        btn_del.onclick =  del_img;       
        btn_del.appendChild(btn_text)

        var btn_show = document.createElement("BUTTON");
        var btn_text = document.createTextNode("Show")
        btn_show.setAttribute("value",img_list[i].imgpath)
        btn_show.onclick =  show_img;       
        btn_show.appendChild(btn_text)


        cell1.innerHTML = img_list[i].iter;
        cell2.appendChild(btn_del)  
        cell3.appendChild(btn_show)        
        // alert(i)

    }

// alert("table updated")
}