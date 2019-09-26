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
                    case '03':
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


function editClass(d_type, d_brand, d_model, d_vendor, d_qb, d_pm, d_py, d_rm, d_ry, id){

    let defaultType = document.getElementById("selectedType");
    let defaultBrand = document.getElementById("deviceBrand");
    let defaultModel = document.getElementById("deviceModel");
    let defaultVendor = document.getElementById("deviceVendor");
    let defaultQb = document.getElementById("quantityBought");
    let defaultPurchaseD = document.getElementById('purchaseDate');
    let defaultReplacementD = document.getElementById('replacementDate');

    let optionsType = document.getElementById(d_type)

    if (optionsType.value === d_type)
       optionsType.style.display = "none";

    if(d_pm.length === 1)
       d_pm = 0 + d_pm


    getPdate = `${d_py}-${d_pm}`
    getRdate = convertMonth(d_rm) + ' ' + d_ry;


    defaultType.innerHTML = d_type;
    defaultBrand.value = d_brand;
    defaultModel.value = d_model;
    defaultVendor.value = d_vendor;
    defaultQb.value = d_qb;
    defaultPurchaseD.defaultValue = getPdate
    defaultReplacementD.value = getRdate;

}



function convertMonth(m){
    switch(m){
        case '1':
            month = 'January';
            break;
        case '2':
            month = 'February';
            break;
        case '3':
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

    return month
}
