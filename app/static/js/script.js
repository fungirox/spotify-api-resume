window.onload = function () {
    const modalAlbum = document.getElementById("modal-album");
    const btnSelectAlbum = document.getElementById("btn-select-album");
    const spanClose = document.getElementsByClassName("close")[0];

    btnSelectAlbum.onclick = function () {
        modalAlbum.style.display = "block";
    }
    spanClose.onclick = function () {
        modalAlbum.style.display = "none";
    }
    window.onclick = function (event) {
        if (event.target == modalAlbum) {
            modalAlbum.style.display = "none";
        }
    }

};
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modal-album');
    const albumListContainer = document.getElementById('album-list');

    const albumDisplay = document.getElementById('album-display');
    const selectContainer = document.getElementById('select-album-container');

    const selectedImage = document.getElementById('selected-album-image');
    const selectedInfo = document.getElementById('selected-album-info');
    const selectedYear = document.getElementById('selected-album-year');


    albumListContainer.addEventListener('click', function (event) {
        const clickedImage = event.target.closest('.album-choice');

        if (clickedImage) {
            const imgSrc = clickedImage.dataset.imgSrc;
            const name = clickedImage.dataset.name;
            const year = clickedImage.dataset.year;

            selectedImage.src = imgSrc;
            selectedInfo.textContent = `${name} - ${artist}`;
            selectedYear.textContent = `[${year}]`;

            albumDisplay.style.display = 'block';
            selectContainer.style.display = 'none';

            modal.style.display = 'none';
        }
    });

});
