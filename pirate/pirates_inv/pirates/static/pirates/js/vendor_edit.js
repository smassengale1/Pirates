function showDate(){
    var rd = document.getElementById('replacementDate')

    $('#purchaseDate').keyup(function(){
            let date = this.value

            if (date.length > 1){
                let month = date.slice(5,7)
                let year = parseInt(date.slice(0,4))

                switch(month){
                    case '01' :
                        replacementMonth = 'January';
                        break;
                    case '02':
                        replacementMonth = 'February';
                        break;
                    case '03':
                        replacementMonth = 'March';
                        break;
                    case '04':
                        replacementMonth = 'April';
                        break;
                    case '05':
                        replacementMonth = 'May';
                        break;
                    case '06':
                        replacementMonth = 'June';
                        break;
                    case '07':
                        replacementMonth = 'July';
                        break;
                    case '08':
                        replacementMonth = 'August';
                        break;
                    case '09':
                        replacementMonth = 'September';
                        break;
                    case '10':
                        replacementMonth = 'October';
                        break;
                    case '11':
                        replacementMonth = 'November';
                        break;
                    case '12':
                        replacementMonth = 'December';
                        break;
                    default:
                        replacementMonth = '';
                        break;

                }
                replacementYear = year + 5

                rd.value = replacementMonth + " " + replacementYear

            }

    })






}

















function addtoDate(){

    let purchaseDate = document.getElementById('purchaseDate').value;
    let year = parseInt(purchaseDate.slice(0,4))
    let month = purchaseDate.slice(5,7)

   let replacementYear = year + 5
   let replacementMonth = ''
   

    switch(month){
        case '01' :
            replacementMonth = 'January';
            break;
        case 02:
            replacementMonth = 'February';
            break;
        case 03:
            replacementMonth = 'March';
            break;
        case 04:
            replacementMonth = 'April';
            break;
        case 05:
            replacementMonth = 'May';
            break;
        case 06:
            replacementMonth = 'June';
            break;
        case 07:
            replacementMonth = 'July';
            break;
        case 08:
            replacementMonth = 'August';
            break;
        case 09:
            replacementMonth = 'September';
            break;
        case 10:
            replacementMonth = 'October';
            break;
        case 11:
            replacementMonth = 'November';
            break;
        case 12:
            replacementMonth = 'December';
            break;
        default:
            replacementMonth = '';
            break;

    }

    $('#replacementDate').append(`{$replacementMonth} ${replacementYear}`)


}
function filterVendors(){
    let input, filter, table, tr, td, i, txtValue;
    for(table = 0; table < 7; table++){
        let name = 'myInput' + String(table)
        document.getElementById(name)
    }
    document.getElementById("v_table");
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

