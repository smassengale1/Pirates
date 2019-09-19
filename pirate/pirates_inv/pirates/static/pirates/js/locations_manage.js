function editClass(buildings, roomID){

    let defaultLoc = document.getElementById("selectedLoc")
    let defaultRoom = document.getElementById('roomNumber')


    defaultLoc.innerHTML = buildings

    if (roomID != 'new_room'){
        defaultRoom.placeholder = roomID
    }
    else{
        defaultRoom.placeholder = ' '
    }




    }








