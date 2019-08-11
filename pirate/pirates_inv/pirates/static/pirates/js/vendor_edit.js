function filterVendors(){
    let input, filter, table, tr, td, i, txtValue;

    input = document.getElementById("myInput").value;
    table = document.getElementById("v_table");
    tr = table.getElementsByTagName("tr");


    for (i=0; i<tr.length; i++){
        vendorName = tr[i].getElementsByTagName("td")[0];
        vendorID = tr[i].getElementsByTagName("td")[1];



        if(vendorName || vendorID){
            vName = vendorName.textContent || vendorName.innerText;
            isvName = vName.toLowerCase().indexOf(input.toLowerCase())>-1;

            vID = vendorID.textContent || vendorID.innerText;
            isvID = vID.indexOf(input)>-1;

            if(isvName || isvID){
                tr[i].style.display="";
            }
            else{
                tr[i].style.display ="none"
            }
        }
    }
}


function addVendor(){
    vendor_name = document.getElementById("vendorName").value;
    vendor_id =  document.getElementById("vendorID").value;

    ajax_queue.ajax_dispatch({
        type: 'POST',
        url: '/dashboard/vendors',
        data: {
            'vendorName': vendor_name,
            'vendorID': vendor_id,

        },
        success: function () {
        },
        error: function (e) {
            console.log(e);
        },
        dataType: "json",
        contentType: "application/json"
    });
}

