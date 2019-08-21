function init_socket_ons(){
    //var socket = io('/data')
    window.socket.on("data-get-img-paths", function(pathlist){
       // alert("data-get-img-path" + pathlist)
        createImageList(pathlist)
    })

    window.socket.on("data-get-img-plot", function(plot){
       // alert("plot-" + plot)
        const graph = JSON.parse(plot)
        Plotly.newPlot('plt_image_selected', graph,{})
    })

    window.socket.on("data-get-gen-images", function(img_list){
        console.log(img_list)
        //alert("data-get-gen-images")
        generate_tbl_for_gen_images(img_list)
    })


    window.socket.on("data-get-gen-img-plot", function(plot){
        // alert("plot-" + plot)
         const graph = JSON.parse(plot)
         Plotly.newPlot('plot_gen_img', graph,{})
     })

}

function load_imgs(){
    //var socket = io('/data')
    window.socket.emit("data-load-imgs", window.pid, window.expid )
}

function gen_img(){
    //alert("generate img")
    window.socket.emit("data-gen-img", window.pid, window.expid)
}

7//********* */
// delete methods
/****************** */
function del_img(){
  
    window.socket.emit("data-delete-img", window.pid, window.expid , this.value)
    
}

function del_gen_img(){
    window.socket.emit("data-delete-gen-img", window.pid, window.expid , this.value)
}


function show_img(){
   // alert("show img")
    window.socket.emit("data-show-img", this.value)
}

function show_gen_img(){
    console.log("gen imgs")
    window.socket.emit("data-show-gen-img", this.value)
}




function request_gan_gen_images(){
    window.socket.emit("data-request-gan-gen-images", window.pid, window.expid)
}


// For generating image list
function createImageList(imgpathlist){

    var ol = document.getElementById("ol_images");
    ol.innerHTML = "";
    
    for (var i=0; i < imgpathlist.length ; i++){
       // var span = document.createElement("SPAN");

        var ol_item = document.createElement("LI")
       // ol_item.setAttribute("value", imgpathlist[i])
       // var textnode = document.createTextNode("Image")
        //ol_item.appendChild(textnode)

        var btn_img = document.createElement("BUTTON")
        var btn_text = document.createTextNode("Show Image")
        btn_img.setAttribute("value", imgpathlist[i])
        //btn_img.setAttribute("onclick", "click_del_img(this.value)")
        btn_img.onclick = show_img;
        btn_img.appendChild(btn_text)

        var btn_del = document.createElement("BUTTON")
        var btn_text = document.createTextNode("Delete")
        btn_del.setAttribute("value", imgpathlist[i])
        btn_del.onclick = del_img;//test_fn;
        //btn_del.addEventListener('click', )
        btn_del.appendChild(btn_text)

        //span.appendChild(ol_item)
        //span.appendChild(btn_del)


        ol_item.appendChild(btn_img)
        ol_item.appendChild(btn_del)

        ol.appendChild(ol_item)

    }

    
}

// Generate a table for generated images
function generate_tbl_for_gen_images(img_list){
    
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
        btn_del.onclick =  del_gen_img;       
        btn_del.appendChild(btn_text)

        var btn_show = document.createElement("BUTTON");
        var btn_text = document.createTextNode("Show")
        btn_show.setAttribute("value",img_list[i].imgpath)
        btn_show.onclick =  show_gen_img;       
        btn_show.appendChild(btn_text)
  

        cell1.innerHTML = img_list[i].iter;
        cell2.appendChild(btn_del)  
        cell3.appendChild(btn_show)        
       // alert(i)
  
    }
    
    // alert("table updated")
  }