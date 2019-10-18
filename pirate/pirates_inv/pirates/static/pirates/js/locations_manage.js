function editClass(buildings, roomID){
    let title = document.getElementById('newModalTitle')
    let defaultRoom = document.getElementById('roomNumber')

    //May need to be deleted
    title.innerHTML = buildings

    if (roomID != 'new_room'){
        title.innerHTML = buildings
        defaultRoom.value = roomID
    }
    else{
        defaultRoom.value = ' '
        document.getElementById('newType').innerHTML = roomID
    }


}

function validateBuilding(){
    let errorMessage = document.getElementById('errorMessageRoom')
    let error = null
    let type = document.getElementById('newType').innerHTML;
    let room = ''

    if (type === 'new_room'){
        building = document.getElementById('newModalTitle').innerHTML
        room = document.getElementById('roomNumber').value

        console.log('Building: ' + building)
        console.log('Room: ' + document.getElementById('roomNumber').value)
        console.log('Type: ' + document.getElementById('newType').innerHTML)
    }
    else {
        building = document.getElementById('newBuildingName').value;
        console.log('Building: ' + building)
    }

    errorMessage.style.display = 'none'

        $.ajax({
            type: "POST",
            url: '/ajax/validate_building',
            async: false,
            data: {
            'building': building,
            'room': document.getElementById('roomNumber').value,
            'type': document.getElementById('newType').innerHTML,
            },

            dataType: 'json',
            success: function (data){
                if(data.exist){
                    errorMessage.style.display = 'block'
                    errorMessage.innerHTML = building + ' ' + room + ' already exists'
                    console.log("Duplicate In Database")

                }

                else if(data.isNull){
                    errorMessage.style.display = 'block'
                    errorMessage.innerHTML = 'Input Cannot be Null'
                    console.log("Null Value Cannot Be Added")
                }


                else
                    document.location.reload()





            }

        })

        setTimeout(
            function wait(){
                $(errorMessage).fadeOut('slow');
        }, 3000);
}






function editBuilding(){
    let curr = document.getElementById('curr').value
    let showModi = document.getElementById('modifiedVersion');
    let newName = document.getElementById('newName');
    let checkBox = document.getElementById('confirmChange');
    let default_option = document.getElementById('defaultChoice').innerHTML;

    //Shows if check box is checked or not
    //let isChecked = document.getElementById('confirmChange').checked



    $('#curr').click(function(){
        curr = this.value
        let isChecked = document.getElementById('confirmChange').checked
        let newName = document.getElementById('newName').value;

        if (curr != default_option){
            document.getElementById('deleteName').style.display = 'block'
            if (isChecked && newName != '')
                document.getElementById('updateName').style.display = 'block'
        }

        else{
            document.getElementById('deleteName').style.display = 'none'
            document.getElementById('updateName').style.display = 'none'
        }

        showModi.value = curr + ' -----> ' + newName
   })

   $('#newName').keyup(function(){
        let newName = this.value
        let isChecked = document.getElementById('confirmChange').checked
        let curr = document.getElementById('curr').value;


        if (newName != '' && isChecked && curr != default_option)
            document.getElementById('updateName').style.display = 'block'
        else
            document.getElementById('updateName').style.display = 'none'

        showModi.value = curr + ' -----> ' + newName
   })

   $('#confirmChange').click(function(){
        let isChecked = document.getElementById('confirmChange').checked
        let newName = document.getElementById('newName').value;
        let curr = document.getElementById('curr').value;

        if (isChecked && newName != '' && curr != default_option)
            document.getElementById('updateName').style.display = 'block'
        else
            document.getElementById('updateName').style.display = 'none'

   })


}


function removeLocation(type){


    let checkBox = document.getElementById('confirmDeletion').isChecked;
    let deleteButton = document.getElementById('deleteLoc')
    let warningMessage = document.getElementById('warningMessage').innerHTML

    if(type === 'room'){
        var area = document.getElementById('roomNumber').value
        warningMessage.value = "<b>Warning</b>"

        //To do make toRemove = Building: #
    }
    else{

        var area = document.getElementById('curr').value
        //ex. Remove Highschool

    }
    $('#confirmDeletion').click(function(){
        $('#deleteLoc').toggle()

    })


    document.getElementById('toDelete').value = area;
    document.getElementById('type').innerHTML = type;


}

//Actually Deletes Building
function removeBuilding(){
    let errorMessage = document.getElementById('errorMessage')
    let warningMessage = document.getElementById('warningMessage')
    let type = document.getElementById('type').innerHTML;


     $.ajax({
            type: "POST",
            url: '/ajax/remove_building',
            async: false,
            data: {
            'roomBuilding': document.getElementById('newModalTitle').innerHTML,
            'area': document.getElementById('toDelete').value,
            'type': type
            },

            dataType: 'json',
            success: function (data){
                if(data.exist){
                    errorMessage.style.display = 'block'
                    errorMessage.innerHTML = 'Building already exists'
                    console.log("Item Did not Delete")

                }

                else{
                    document.location.reload()
                    errorMessage.style.display = 'none'
                }

            }

  })

}


function updateBuilding(){
    let oldName = document.getElementById('curr').value;
    let newName = document.getElementById('newName').value;
    let errorMessage = document.getElementById('updateBuildingError')

    $.ajax({
            type: "POST",
            url: '/ajax/update_building',
            async: false,
            data: {
            'oldName': oldName,
            'newName' : newName,
            },

            dataType: 'json',
            success: function (data){
                if(data.exist){
                    errorMessage.style.display = 'block'
                    errorMessage.innerHTML = 'Duplicate Names Are Not Allowed.'
                    console.log("Duplicate In Database")
            }
                else{
                    console.log('Successfully Changed Names')
                    document.location.reload();
                }
            }

        })

    setTimeout(
        function wait(){
              $(errorMessage).fadeOut('slow');
        }, 3000);
}


