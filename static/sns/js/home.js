/* jshint esversion: 6 */

/* jshint node: true */
window.addEventListener('DOMContentLoaded', function (){

    "use strict";

    document.addEventListener('click', function (e){
        if (e.target.classList.value === 'next') {
            let board = e.target.parentNode.previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling;
            let boardPictureCount = board.childElementCount;
            let position = 0;
            for(let i=0; i<boardPictureCount; i++) {
	            if (board.children[i].classList.value === "target"){
                    break;
                }
                position += 1;
            }
            let styleLeft = board.style.left;
            let left = Number(styleLeft.replace(/%/g, ""));
            board.style.left = (left-100) + "%";
            board.children[position].classList.remove("target");
            board.children[position + 1].classList.add("target");
            e.target.parentNode.nextElementSibling.children[position].classList.remove("blue");
            e.target.parentNode.nextElementSibling.children[position + 1].classList.add("blue");
            e.target.parentNode.previousElementSibling.previousElementSibling.classList.remove("none");
            e.target.parentNode.previousElementSibling.previousElementSibling.previousElementSibling.classList.remove("none");
            if (position+2 === boardPictureCount) {
                e.target.parentNode.classList.add("none");
                e.target.parentNode.previousElementSibling.classList.add("none");
            }
        }
        if (e.target.classList.value === 'before') {
            let board = e.target.parentNode.previousElementSibling.previousElementSibling;
            let boardPictureCount = board.childElementCount;
            let position = 0;
            for(let i=0; i<boardPictureCount; i++) {
	            if (board.children[i].classList.value === "target"){
                    break;
                }
                position += 1;
            }
            let styleLeft = board.style.left;
            let left = Number(styleLeft.replace(/%/g, ""));
            board.style.left = (left+100) + "%";
            board.children[position].classList.remove("target");
            board.children[position - 1].classList.add("target");
            e.target.parentNode.nextElementSibling.nextElementSibling.nextElementSibling.children[position].classList.remove("blue");
            e.target.parentNode.nextElementSibling.nextElementSibling.nextElementSibling.children[position - 1].classList.add("blue");
            e.target.parentNode.nextElementSibling.classList.remove("none");
            e.target.parentNode.nextElementSibling.nextElementSibling.classList.remove("none");
            if (position-1 === 0){
                e.target.parentNode.classList.add("none");
                e.target.parentNode.previousElementSibling.classList.add("none");
            }
        }
    });

    let post = document.getElementById("post");

    post.addEventListener('click', function() {
        let select_post_type_container = document.getElementById("select-post-type-container");
        let cancel = document.getElementById("cancel-btn");
        let photo_type = document.getElementById("photo-type");

        select_post_type_container.classList.remove("none");
        document.body.classList.add("overflow-hidden");

        photo_type.addEventListener('click', function () {
            let crop_image_container = document.getElementById("crop-image-container");
            let back = document.getElementById("back-page");
            let next = document.getElementById("next-page");
            let cancel_s = document.getElementById("cancel-s-btn");

            select_post_type_container.classList.add("none");
            crop_image_container.classList.remove("none");
            
            var image_workspace = document.querySelector('.image-workspace img')
            var actionButton = document.querySelectorAll('.action-button button')
            var hiddenUpload = document.querySelector('.action-button .hidden-upload')
            var image_workspaceSpan = document.querySelector('.image-workspace span')
            var csrf = document.getElementsByName("csrfmiddlewaretoken")
            console.log(actionButton)
            console.log(actionButton[0])
            console.log(actionButton[1])
            // upload image
            // actionButton[0].onclick = () => hiddenUpload.click()
            hiddenUpload.onchange = () => {
                var file = hiddenUpload.files[0]
                var url = window.URL.createObjectURL(new Blob([file], {type: 'image/jpg'}))
                image_workspace.src = url
                image_workspaceSpan.style.display = 'none'

                var options = {
                    dragMode: 'move',
                    preview: '',
                    viewMode: 2,
                    modal: false,
                    background: false,
                    ready: function(){
                        console.log(image_workspace)
                        cropper.getCroppedCanvas().toBlob((blob) => {
                            console.log(blob)
                        })
                        actionButton[1].onclick = () => {
                            cropper.getCroppedCanvas().toBlob((blob) => {
                                
                                fd.append('csrfmiddlewaretoken', csrf[0].value)
                                fd.append('picture1', blob, 'picture1.png')
                                $.ajax({
                                    type: 'POST',
                                    url: '',
                                    enctype: 'multipart/form-data',
                                    data: fd,
                                    success() {
                                        console.log('Upload success');


                                    },
                                    error() {
                                        console.log('Upload error');
                                    },
                                    cache: false,
                                    contentType: false,
                                    processData: false,
                                })
                            })
                        }
                    }
                }

                var cropper = new Cropper(image_workspace, options)
            }


            back.addEventListener('click', function () {
                select_post_type_container.classList.remove("none");
                crop_image_container.classList.add("none");
            });

            next.addEventListener('click', function () {

            });

            cancel_s.addEventListener('click', function() {
                crop_image_container.classList.add("none");
                document.body.classList.remove("overflow-hidden");
                });
        });

        cancel.addEventListener('click', function() {
            select_post_type_container.classList.add("none");
            document.body.classList.remove("overflow-hidden");
        });


    });

});
