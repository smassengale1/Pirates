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

function convertMonthToInt(date){

    if (date.length > 1){
        let month = date.slice(0,-5)

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
        date = year + '-' + month
    }
    return date
}


function isNull(vendor){
    const table = document.getElementById(vendor + "_device_table")
    const nullTable = document.getElementById(vendor + "_null")
    const row = table.rows.length - 1;


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
let deviceType = document.getElementById('deviceType').value.trim()
let make = document.getElementById('deviceBrand').value.trim()
let model = document.getElementById('deviceModel').value.trim()
let vendor = document.getElementById('deviceVendor').value.trim()
let quantity = document.getElementById('quantityBought').value.trim()
let pd = document.getElementById('purchaseDate').value.trim()
let rd = document.getElementById('replacementDate').value.trim()

let month =  rd.slice(0,-5)
let year = parseInt(date.slice(-4))

rm = convertMonthToInt(rd)
ry =


console.log(`${deviceType}`)
console.log(make)
console.log(model)
console.log(vendor)
console.log(quantity)
console.log(pd)
console.log(rd)




}
function newVendor(){
    let vendor = document.getElementById('new_vendor').value.trim();
    let id = document.getElementById('new_vendor_id').value.trim();


    $('#addVendor').click(function(){
        //0 is False || anything > 0 True
        if(vendor && id){
            $.ajax({
                type: "POST",
                url: '/ajax/add_vendor',
                async: false,
                data: {
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

    setTimeout(
       function wait(){
            $(errorMessage).fadeOut('slow');
        }, 3000);
}
