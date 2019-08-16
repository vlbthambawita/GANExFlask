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
}

function load_imgs(){
    //var socket = io('/data')
    window.socket.emit("data-load-imgs", window.pid, window.expid )
}

function gen_img(){
    //alert("generate img")
    window.socket.emit("data-gen-img", window.pid, window.expid)
}


function del_img(){
    // var socket = io('/data')
    // var path = e.getAttribute("value")
    //alert("delete" + this.value)
    //alert("pid" + window.pid)
    //alert("expid" + window.expid)
   
    window.socket.emit("data-delete-img", window.pid, window.expid , this.value)
    

    
}

function show_img(){
   // alert("show img")
    window.socket.emit("data-show-img", this.value)
}

function test_fn(){
   // alert("test function is working" + this.value)
    //alert(window.pid)
   
}


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