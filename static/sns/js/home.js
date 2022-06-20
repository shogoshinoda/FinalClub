/* jshint esversion: 6 */
/* jshint node: true */
window.addEventListener('DOMContentLoaded', function (){

    "use strict";
    const viewportWidth = 420;
    const viewportHeight = 560;
    const boundaryWidth = 700;
    const boundaryHeight = 700;

    const img = document.getElementById("board-picture");
    const image_crop = img.croppie({
        enableExif: ture,
        viewport: {
            width: viewportWidth,
            height: viewportHeight,
            type: 'square'
        },
        boundary: {
            width: boundaryWidth,
            height: boundaryHeight
        }
    });

    const upload_image = document.getElementById("upload_image");

    upload_image.addEventListener("change", function (){
        image_crop.croppie('bind', {
            url: event.target.result
        }).then(function (){

        });
        bo
    });

});