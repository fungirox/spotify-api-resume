window.onload = function(){ 
var modalAlbum = document.getElementById("modal-album");
var btnSelectAlbum = document.getElementById("btn-select-album");
var spanClose = document.getElementsByClassName("close")[0];

    btnSelectAlbum.onclick = function(){
        modalAlbum.style.display = "block";
    }
    spanClose.onclick = function(){
        modalAlbum.style.display = "none";
    }
    window.onclick = function(event){
        if(event.target == modalAlbum){
            modalAlbum.style.display = "none";
        }
    }
};

