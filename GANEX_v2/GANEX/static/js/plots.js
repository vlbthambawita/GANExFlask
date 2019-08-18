

function test(){
    alert("test function is running")
    console.log(window.pid)
    console.log(window.expid)
}

function init_socket_ons(){
    window.socket.on("plot-get-plots-data", function(plots){
       // alert("plot get plot data")
        const graphs = JSON.parse(plots) //| safe;
                       
        Plotly.newPlot('plots_2',graphs,{});

    })
}

function update_plot_settings(){

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