function editClass(buildings, roomID){

    let title = document.getElementById('newModalTitle')
    let defaultRoom = document.getElementById('roomNumber')


    //defaultLoc.innerHTML = buildings

    if (roomID != 'new_room'){
        title.innerHTML = buildings
        defaultRoom.value = roomID
    }
    else{
        defaultRoom.value = ' '
    }
}

function editBuilding(){
    let curr = document.getElementById('curr').value
    let showModi = document.getElementById('modifiedVersion');
    let newName = document.getElementById('newName');
    let checkBox = document.getElementById('confirmChange');

    //Shows if check box is checked or not
    //let isChecked = document.getElementById('confirmChange').checked



    $('#curr').click(function(){
         showModi.value = this.value + ' --> ' + curr

         if(this.value === 'Select...'){
            newName.disabled = true;
            checkBox.disabled = true;
        }
        else
            newName.disabled = false;
   })


}



function removeLocation(type){

    let checkBox = document.getElementById('confirmDeletion').isChecked;
    let deleteButton = document.getElementById('deleteLoc')




    if(type === 'room'){
        var area = document.getElementById('roomNumber').value
        //To do make toRemove = Building: #
    }
    else{

        var area = document.getElementById('curr').value
        //ex. Remove Highschool

    }
    $('#confirmDeletion').click(function(){
        $('#deleteLoc').toggle()

    })


    document.getElementById('toDelete').value = area
}






