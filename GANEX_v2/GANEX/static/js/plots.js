

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


function update_plots_repeat(){
    window.socket.emit("plot-update-plots", window.expid)
}