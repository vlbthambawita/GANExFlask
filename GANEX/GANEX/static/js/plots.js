



function init_socket_ons(){
    window.socket.on("plot-get-plots-data", function(plots){
       // alert("plot get plot data")
       var div_plots = document.getElementById("plots")
       div_plots.innerHTML = "";
       for (var i=0; i < plots.length ; i++){
        var div_p = document.createElement("DIV"); 
        const graphs = JSON.parse(plots[i])
        Plotly.newPlot(div_p,graphs,{});

        div_plots.appendChild(div_p)

       }

       // const graphs = JSON.parse(plots) //| safe;
                       
      //  Plotly.newPlot('plots_2',graphs,{});

    })

    window.socket.on("plt-get-plt-settings", function(settings_list){
        console.log(settings_list)
        generate_tbl_plt_settings(settings_list)
    })
}

function request_plt_settings(){
    window.socket.emit("plt-rqst-plt-setttings", window.pid, window.expid)
}

function update_plot_settings(){ //  add plot key function

    var statlist_elem = document.getElementById("plot_stat");
    var plotid_elem = document.getElementById("plot_id");

    var plot_stat_name  = statlist_elem.options[statlist_elem.selectedIndex].text;
    var plot_id = plotid_elem.options[plotid_elem.selectedIndex].text;

    window.socket.emit("plot-update-plot-settings",window.expid, plot_stat_name, plot_id)
}

function reset_interval(){
    window.plot_timer = setInterval( update_plots_repeat, 1000)
}

function update_plots_repeat(){
    window.socket.emit("plot-update-plots", window.expid)
}


function update_plot_id_list(){

    var sel = document.getElementById("plot_id");
    var i;
    
    for (i=1; i < 21; i++){
            var opt = document.createElement('option');
            opt.text = i;
            opt.value = i;
            sel.add(opt);

    }
}


function del_plt_stat(){

    // To delete plt stat from plotsettings table
    var plt_values = this.value.split(',')
    

    window.socket.emit("plt-rqst-del-plt-setting", window.pid, window.expid, plt_values)
}

// Clear timer when clicked on plot settings
function click_plt_settings(){
    clearInterval( window.plot_timer);
}


function generate_tbl_plt_settings(settings_list){ // settings_list -> a list of tuples (plotstat, plotid)
    
    var tbl = document.getElementById("tbl_plt_settings")
    tbl.innerHTML = ""
  
    var header = tbl.createTHead();
  
    var row = header.insertRow(0)
  
    var cell0 = row.insertCell(0)
    var cell1 = row.insertCell(1)
    
    
  
    cell0.innerHTML = "<b>Plot Stat Name</b>"
    cell1.innerHTML = "<b>Plot ID</b>"
    
    
  
    var i ;
    for (i= 0; i < settings_list.length; i++){
  
        var row = tbl.insertRow(i+1);
  
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        
  
        var btn_del = document.createElement("BUTTON");
        var btn_text = document.createTextNode("Delete")
        btn_del.setAttribute("value",[settings_list[i][0],settings_list[i][1]]) //settings_list[i][0]
        btn_del.onclick =  del_plt_stat;       
        btn_del.appendChild(btn_text)
        btn_del.className = "btn btn-danger"

        
  

        cell1.innerHTML = settings_list[i][0];
        cell2.innerHTML = settings_list[i][1];
        cell3.appendChild(btn_del)  
        //cell3.appendChild(btn_show)        
       // alert(i)
  
    }
    
    // alert("table updated")
  }