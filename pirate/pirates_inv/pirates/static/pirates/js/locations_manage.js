
function validateBuilding(){
    let error = null
    let type = document.getElementById('newType').innerHTML;
    let room = ''

    if (type === 'new_room'){
        building = document.getElementById('newModalTitle').innerHTML
        room = document.getElementById('roomNumber').value
        errorMessage = document.getElementById('errorMessageRoom')

        console.log('Building: ' + building)
        console.log('Room: ' + document.getElementById('roomNumber').value)
        console.log('Type: ' + document.getElementById('newType').innerHTML)
    }
    else {
        building = document.getElementById('newBuildingName').value;
        errorMessage = document.getElementById('errorMessageBuilding')
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
    let warningMessage = document.getElementById('warningMessage')
    let type = document.getElementById('type').innerHTML;

    if(type ==='room')
        errorMessage = document.getElementById('errorMessageRoom')
    else
        errorMessage = document.getElementById('errorMessageBuilding')


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


//Adds new room by taking information from the #newLocationForm
//and sending it to validate_building()
function addRoom(building){
    let newRoomNum = document.getElementById('')
    errorMessage = document.getElementById('addingRoomError')
    type = 'room'

    $('#addRoom').click(function(){
        let room = document.getElementById('roomNumber').value

        console.log('addRoom()') //for testing delete later
        console.log(building)
        console.log(room)
        console.log(type)


        $.ajax({
            type: "POST",
            url: '/ajax/validate_building',
            async: false,
            data: {
            'building': building,
            'room': room,
            'type': type
            },

            dataType: 'json',
            success: function (data){
                if(data.exist){
                    errorMessage.style.display = 'block'
                    errorMessage.innerHTML = `${building}[${room}] already exist.`
                    console.log("Item Did not Delete")

                }
                else if (data.isNull){
                    errorMessage.style.display = 'block'
                    errorMessage.innerHTML = 'Entry Cannot be null'
                }
                else{
                    document.location.reload()
                    errorMessage.style.display = 'none'
                }

                setTimeout(function wait(){
                    $(errorMessage).fadeOut('slow');
                }, 3000);

            }


        })
    })
}

function editBuilding(){
    let showModi = document.getElementById('modifiedVersion');
    let checkBox = document.getElementById('confirmChange');
    let default_option = document.getElementById('defaultChoice').innerHTML;
    errorMessage = document.getElementById('updateBuildingError')





    //Location to Edit
    $('#curr').click(function(){
        curr = this.value
        let isChecked = document.getElementById('confirmChange').checked
        let newName = document.getElementById('newName').value;

        if (curr != default_option){
            document.getElementById('deleteName').style.display = 'block'
            if (isChecked && newName != '')
                document.getElementById('updateBuilding').style.display = 'block'
        }

        else{
            document.getElementById('deleteName').style.display = 'none'
            document.getElementById('updateBuilding').style.display = 'none'
        }

        showModi.value = curr + ' -----> ' + newName
        console.log('Building to edit Selected')
   })

    //Input Box For New Name
   $('#newName').keyup(function(){
        let newName = this.value
        let isChecked = document.getElementById('confirmChange').checked
        let curr = document.getElementById('curr').value;


        if (newName != '' && isChecked && curr != default_option)
            document.getElementById('updateBuilding').style.display = 'block'
        else
            document.getElementById('updateBuilding').style.display = 'none'

        showModi.value = curr + ' -----> ' + newName

        console.log('Name Changed')
   })

    //Check box to confirm it
   $('#confirmChange').click(function(){
        let isChecked = document.getElementById('confirmChange').checked
        let newName = document.getElementById('newName').value;
        let curr = document.getElementById('curr').value;

        if (isChecked && newName != '' && curr != default_option)
            document.getElementById('updateBuilding').style.display = 'block'
        else
            document.getElementById('updateBuilding').style.display = 'none'

        console.log('Check Box Clicked')

   })


   $('#updateBuilding').click(function(){
        $.ajax({
            type: "POST",
            url: '/ajax/update_building',
            async: false,
            data: {
                'newRoom' : newName.value,
                'oldRoom' : curr,
                'type' : 'building'
            },

            dataType: 'json',

            success: function (data){
                if(data.exist){
                    errorMessage.style.display = 'block'
                    errorMessage.innerHTML = `${newName} already exist.`
                    console.log("Item Did not Delete")

                }
                else if (data.isNull){
                    errorMessage.style.display = 'block'
                    errorMessage.innerHTML = 'Entry Cannot be null'
                }
                else{
                    document.location.reload()
                    errorMessage.style.display = 'none'
                }

                setTimeout(function wait(){
                    $(errorMessage).fadeOut('slow');
                }, 3000);

            }


        })
    })

}

function editRoom(building, room){
    errorMessage = document.getElementById('errorUpdateRoom')

    document.getElementById('editRoomTitle').innerHTML = building
    document.getElementById('roomNum').placeholder = room
    type = 'room'

    $('#updateRoom').click(function(){
        let newName = document.getElementById('roomNum').value

         $.ajax({
            type: "POST",
            url: '/ajax/update_building',
            async: false,
            data: {
            'building': building,
            'newRoom': newName,
            'oldRoom': room,
            'type': type
            },
            dataType: 'json',
            success: function (data){
                if(data.exist){
                    errorMessage.style.display = 'block'
                    errorMessage.innerHTML = `${building} ${newName} already exist.`
                    console.log("Item Did not Delete")

                }
                else if (data.isNull){
                    errorMessage.style.display = 'block'
                    errorMessage.innerHTML = 'Entry Cannot be null'
                }
                else{
                    document.location.reload()
                    errorMessage.style.display = 'none'
                }

                setTimeout(function wait(){
                    $(errorMessage).fadeOut('slow');
                }, 3000);

            }


        })
    })

}



