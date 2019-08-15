function test(pid){
    alert(pid);
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

        cell1.innerHTML = para_list[i].para_name;
        cell2.innerHTML = para_list[i].para_key;
        cell3.innerHTML = para_list[i].para_value;
       // alert(i)

    }
    

}