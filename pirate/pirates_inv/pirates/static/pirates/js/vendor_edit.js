function showDate(){
    var rd = document.getElementById('replacementDate')

    $('#purchaseDate').keyup(function(){

            let date = this.value

            if (date.length > 1){
                let month = date.slice(5,7)
                let year = parseInt(date.slice(0,4))

                switch(month){
                    case '01' :
                        month = 'January';
                        break;
                    case '02':
                        month = 'February';
                        break;
                    case 'March':
                        month = 'March';
                        break;
                    case '04':
                        month = 'April';
                        break;
                    case '05':
                        month = 'May';
                        break;
                    case '06':
                        month = 'June';
                        break;
                    case '07':
                        month = 'July';
                        break;
                    case '08':
                        month = 'August';
                        break;
                    case '09':
                        month = 'September';
                        break;
                    case '10':
                        month = 'October';
                        break;
                    case '11':
                        month = 'November';
                        break;
                    case '12':
                        month = 'December';
                        break;
                    default:
                        month = '';
                        break;

                }
                replacementYear = year + 5

                rd.value = month + " " + replacementYear

            }
    })
}

function convertIntToMonth(month){

    switch(month){
        case '1' :
            month = 'January';
            break;
        case '2':
            month = 'February';
            break;
        case 'March':
            month = 'March';
            break;
        case '4':
            month = 'April';
            break;
        case '5':
            month = 'May';
            break;
        case '6':
            month = 'June';
            break;
        case '7':
            month = 'July';
            break;
        case '8':
            month = 'August';
            break;
        case '9':
            month = 'September';
            break;
        case '10':
            month = 'October';
            break;
        case '11':
            month = 'November';
            break;
        case '12':
            month = 'December';
            break;
        default:
            month = '';
            break;

    }

    return month;
}

function convertMonthToInt(month){

    if (month.length > 1){
        switch(month){
            case 'January' :
                month = 1;
                break;
            case 'February':
                month = 2;
                break;
            case 'March':
                month = 3;
                break;
            case 'April':
                month = 4;
                break;
            case 'June':
                month = 5;
                break;
            case 'July':
                month = 6;
                break;
            case 'July':
                month = 7;
                break;
            case 'August':
                month = 8;
                break;
            case 'September':
                month = 9;
                break;
            case 'October':
                month = 10;
                break;
            case 'November':
                month = 11;
                break;
            case 'December':
                month = 12;
                break;
            default:
                month = '';
                break;

        }
        return month
    }
}

// Fires when the edit button is clicked. This will allow the user to make
// changes to the vendor name and vendor id when it was initially assigned.
// The Jquery statement will fire upon the selected box change, and will
// modify the boxes for the user to edit
function editVendor(){
    //Initial click of the edit button
    let vendorType = document.getElementById('vendorToEdit').value;
    let changed = document.getElementById('modifiedVersion');
    let errorMessage = document.getElementById('updateVendorError')
    document.getElementById('vendorChanged').value = vendorType.split(':')[0];
    document.getElementById('vendorIDChanged').value = vendorType.split(':')[1];



    //Jquery to modify boxes as user changes
    $('#vendorToEdit').on('change', function(){
        type = 'vendor'
        let vendor = document.getElementById('vendorToEdit').value.split(':')[0]
        let id = document.getElementById('vendorToEdit').value.split(':')[1]
        modiName = document.getElementById('vendorChanged').value = vendor;
        modiID = document.getElementById('vendorIDChanged').value = id;



        console.log(`${vendor} : ${id}`)

        //Modified box
        changed.value = `${vendor} : ${id} ----> `

    })

    //Fires when name changes
    $('#vendorChanged').on('keyup', function(){
        vendor = document.getElementById('vendorToEdit').value.split(':')[0];
        id = document .getElementById('vendorToEdit').value.split(':')[1];

        modiName = document.getElementById('vendorChanged').value;
        modiID = document.getElementById('vendorIDChanged').value


        changed.value =  `${vendor} : ${id} ----> ${modiName} : ${modiID}`
    })

    //Fires when ID changes
    $('#vendorIDChanged').on('keyup', function(){
        vendor = document.getElementById('vendorToEdit').value.split(':')[0];
        id = document .getElementById('vendorToEdit').value.split(':')[1];

        modiName = document.getElementById('vendorChanged').value;
        modiID = document.getElementById('vendorIDChanged').value


        changed.value =  `${vendor} : ${id} ----> ${modiName} : ${modiID}`


    })

    //Pushing change to views
    $('#updateName').on('click', function(){
        vendor = document.getElementById('vendorToEdit').value.split(':')[0].trim();
        id = document .getElementById('vendorToEdit').value.split(':')[1].trim();

        modiName = document.getElementById('vendorChanged').value.trim();
        modiID = document.getElementById('vendorIDChanged').value.trim();

        if(modiName && modiID){
            if(modiName != vendor || modiID != id){
                $.ajax({
                    type: "POST",
                    url: '/ajax/update_vendor',
                    async: false,
                    data: {
                    'oVendor' : vendor,
                    'oID' : id,
                    'nVendor' : modiName,
                    'nID' : modiID
                    },

                    dataType: 'json',
                    success: function (data){
                        if(data.exist){
                            errorMessage.style.display = 'block'
                            errorMessage.innerHTML = `${modiName} : ${modiID}  --already exists.`
                            console.log("Duplicate In Database")
                        }
                        else
                            document.location.reload()
                    }
               })
            }
            else{
                errorMessage.style.display = 'block'
                errorMessage.innerHTML = vendor + ' will not be updated. There was no change.'
                console.log('values are the same')
            }
        }
        else{
            errorMessage.style.display = 'block';
            errorMessage.innerHTML = "Values cannot be null."
            console.log('null')
        }


         setTimeout(function wait(){
               $(errorMessage).fadeOut('slow');
         }, 3000);


    })


    $('#deleteV').on('click', function(){
        vendor = document.getElementById('vendorToEdit').value.split(':')[0].trim();
        id = document .getElementById('vendorToEdit').value.split(':')[1].trim();
        toDelete = document.getElementById('toDelete').value = vendor + ' : ' + id

    })

     //Removes vendor from table
    $('#removeVendorConfirmation').on('click', function(){
        checkbox = document.getElementById('confirmVendorDeletion').checked
        toDelete = document.getElementById('toDelete').innerHTML


        if(checkbox){
             $.ajax({
                type: "POST",
                url: '/ajax/remove_vendor',
                async: false,
                data: {
                'type' : type,
                'vendor' : vendor,
                'id' : id,
                },

                dataType: 'json',
                success: function (data){
                    if(!data.exist){
                        errorMessage.style.display = 'Block'
                        errorMessage.innerHTML = 'Unable to remove vendor'
                    }
                    else
                        document.location.reload()
                }
           })
            //let user know there is nothing ot delete
        }
        //let user know check box is null

    })


}


// Checks to see if the Vendor has any records. If not then a message
// to tell the user to sign up appears.

//Not being used
function isNull(vendor){
    const table = document.getElementById(vendor + "_device_table")
    const nullTable = document.getElementById(vendor + "_null")
    const row = table.rows.length - 2;

    if (row === 0){
        table.style.display = "none";
        nullTable.style.display = "block"

        //Add an add button if null
    }
    else{
    nullTable.style.display = "none";

    }

}

//grabs vendor name when add button gets clicked on {{vendor}}_view modal
// and places it in add_vendor_records vendor spot
function getVendorName(vendor){
    document.getElementById('deviceVendor').value = vendor
}

function addVendorRecord(){
    let type = 'Record' //Tells views function how to handle


    let deviceType = document.getElementById('deviceType').value.trim()
    let make = document.getElementById('deviceBrand').value.trim()
    let model = document.getElementById('deviceModel').value.trim()
    let vendor = document.getElementById('deviceVendor').value.trim()
    let quantity = document.getElementById('quantityBought').value.trim()
    let pd = document.getElementById('purchaseDate').value.trim()
    let rd = document.getElementById('replacementDate').value.trim()

    let purchase_month = parseInt(pd.slice(-2))
    let purchase_year = parseInt(pd.slice(0,5))

    let replacement_month =  convertMonthToInt(rd.slice(0,-5))
    let replacement_year = parseInt(rd.slice(-4))


    if(vendor)

        $.ajax({
            type: "POST",
            url: '/ajax/vendor',
            async: false,
            data: {
            'type' : type,
            'vendor' : vendor,
            'make' : make,
            'deviceType' : deviceType,
            'model' : model,
            'quantity': quantity,
            'purchase_month': purchase_month,
            'purchase_year': purchase_year,
            'replacement_month': replacement_month,
            'replacement_year':replacement_year
            },

            dataType: 'json',
            success: function (data){
                if(data.exist){
                    null
                    //If record already exist

                }
                else
                    document.location.reload()
            }
        })


    else{
        //errorMessage = document.getElementById('addVendorError');
        //errorMessage.innerHTML = "Input cannot be Null";
        //errorMessage.style.display = 'block';
    }


setTimeout(
   function wait(){
        $(errorMessage).fadeOut('slow');
    }, 3000);


}

function newVendor(){
    let type = 'vendor'

    let vendor = document.getElementById('new_vendor').value.trim();
    let id = document.getElementById('new_vendor_id').value.trim();


    $('#addVendor').click(function(){
        //0 is False || anything > 0 True
        if(vendor && id){
            $.ajax({
                type: "POST",
                url: '/ajax/vendor',
                async: false,
                data: {
                'type' : type,
                'vendor' : vendor,
                'vendorID' : id,
                },

                dataType: 'json',
                success: function (data){
                    if(data.exist){
                        errorMessage.style.display = 'block'
                        errorMessage.innerHTML = `${vendor}(${id}) already exists.`
                        console.log("Duplicate In Database")

                    }
                    else
                        document.location.reload()
                }
            })
        }

        else{
            errorMessage = document.getElementById('addVendorError');
            errorMessage.innerHTML = "Input cannot be Null";
            errorMessage.style.display = 'block';
        }




    })

}


function editVendorRecord(vendor, brand, type, model, quantity, pm, py, rm, ry){

    if(pm == 1){
        pm = 0+pm
    }

alert(`${py}-${pm}`)

 document.getElementById('deviceType').value = type
 document.getElementById('deviceBrand').value = ' ';
 document.getElementById('deviceModel').value = model;
 document.getElementById('deviceVendor').value = vendor;
 document.getElementById('quantityBought').value = quantity;
 document.getElementById('purchaseDate').value = `${py}-${pm}`;
 document.getElementById('replacementDate').value = convertIntToMonth(rm) + ' ' + ry;


}
