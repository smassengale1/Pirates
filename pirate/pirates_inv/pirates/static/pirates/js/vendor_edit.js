function addVendor(){
    let vendorName = document.getElementById("vendorName").value;
    let vendorID = document.getElementById("vendorID").value;


    $(document).ready(function () {
        $.ajax({
            method: 'POST',
            url:  '/dashboard/vendors',
            data: JSON.stringify({
                'vendor_name': vendorName,
                'vendor_id': vendorID,

            }),
            success: function (data) {
                alert('success')

            },
            error: function (e) {
                alert('error')
            },
            dataType: "json",
            contentType: "application/json"

        });
    });

}
        //$('#null_value').removeClass('d-none');

