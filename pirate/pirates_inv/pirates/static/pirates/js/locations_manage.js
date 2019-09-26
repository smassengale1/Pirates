function editClass(buildings, roomID){

    //let defaultLoc = document.getElementById("selectedLoc")
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

    let showModi = document.getElementById('modifiedVersion');
    let newName = document.getElementById('newName');
    let checkBox = document.getElementById('confirmChange');

    //Shows if check box is checked or not
    //let isChecked = document.getElementById('confirmChange').checked

    let curr = document.getElementById('curr').value

    let updateButton = document.getElementById('deleteName')
    let deleteButtonOne = document.getElementById('updateName')



    $('#curr').click(function(){
         showModi.value = this.value + ' --> ' + curr

        if(this.value != 'Select...'){
            newName.disabled = false;
            if(newName.value.length <= 1){
                checkBox.disabled = false;
                checkBox.checked = false;
                updateButton.disabled = false;
                deleteButtonOne.disabled = false;
               }
            else
                checkBox.disabled = true;
        }
        else{
            newName.disabled = true;
            checkBox.disabled = true;
            }
   })


   $('#newName').keyup(function(){
    showModi.value = curr + ' --> ' + this.value

    if(curr != 'Select...'){
        checkBox.disabled = false;
        this.disabled = false;
       }
    else{
        checkBox.disabled = true;
        }
    })

}



function removeLocation(id){

    let checkBox = document.getElementById('confirmDeletion');



    if(id = 'deleteRoom'){
        //Get the data pre-filled in text box
        let area = document.getElementById('roomNumber').value
    }
    else{
       let area = document.getElementById('curr').value
       }







    document.getElementById('toDelete').value = area
    checkBox.disabled = false;




}






