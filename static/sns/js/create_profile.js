/* jshint esversion: 6 */

/* jshint node: true */
function getRoundedCanvas(sourceCanvas){
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var width = sourceCanvas.width;
    var height = sourceCanvas.height;

    canvas.width = width;
    canvas.height = height;
    context.imageSmoothingEnabled = true;
    context.drawImage(sourceCanvas, 0, 0, width, height);
    context.globalCompositeOperation = 'destination-in';
    context.beginPath();
    context.arc(width / 2, height / 2, Math.min(width, height) / 2, 0, 2 * Math.PI, true);
    context.fill();
    return canvas;
}

window.addEventListener('DOMContentLoaded', function (){

    "use strict";

    const input_icon = document.querySelector('#id_user_icon')
    const workspace_container = document.querySelector('.workspace-container')
    const show_crop_image = document.querySelector('.item-label img')
    var cropper = ''
    input_icon.onchange = () => {
        if(cropper) {
            cropper.destroy();
        }
        workspace_container.classList.remove('none')
        var file = input_icon.files[0]
        var url = window.URL.createObjectURL(new Blob([file], {type: 'image/jpg'}))
        var picture_workspace = document.getElementById("workspace")
        picture_workspace.src = url

        

        var options = {
            dragMode: 'move',
            aspectRatio: 1,
            preview: '',
            viewMode: 2,
            modal: false,
            backgroud: false,
            cropBoxResizable: false,
            minCropBoxHeight: 400,
            minCropBoxWidth: 400,
            ready: function(){
            },
        }
        cropper = new Cropper(picture_workspace, options)
        
        
    }
    

    var result_button = document.getElementById('result-button')
    var croppedCanvas;
    var roundedCanvas;

    result_button.addEventListener('click', function(){
        croppedCanvas = cropper.getCroppedCanvas();
        roundedCanvas = getRoundedCanvas(croppedCanvas);
        workspace_container.classList.add('none')
        show_crop_image.src = roundedCanvas.toDataURL()
    })


    var submit = document.getElementById('submit');
    var csrf = document.getElementsByName('csrfmiddlewaretoken');
    var fd = new FormData()
    var items = document.querySelectorAll('.items')

    submit.addEventListener('click', function() {
        var username = document.getElementById('username').value;
        var nickname = document.getElementById('nickname').value;
        var introduction = document.getElementById('introduction').value;
        console.log(username)
        console.log(nickname)
        console.log(introduction)
        fd.append('csrfmiddlewaretoken', csrf[0].value)
        roundedCanvas.toBlob((blob) => {
            fd.append('user_icon', blob, 'user_icon.png')
            console.log(blob)
        })
        fd.append('usericon', roundedCanvas.toDataURL())
        fd.append('username', username)
        fd.append('nickname', nickname)
        fd.append('introduction', introduction)
        setTimeout(function() {
            $.ajax({
                type: 'POST',
                url: '',
                data: fd,
                success(responce) {
                    if(responce.success){
                        window.location.href = '/';
                    }else{
                        var message = document.createElement('div')
                        message.className = 'message'
                        items[0].before(message)
                        for(let error_message of responce.error_messages){
                            if(error_message == 'only_number_english'){
                                var text = document.createElement('p');
                                text.textContent = '・英数数字、-._の記号のみでusernameを作成してください';
                                message.appendChild(text);
                            }
                            if(error_message == 'not_username_unique'){
                                var text = document.createElement('p');
                                text.textContent = '・既にこのusernameはつかわれています';
                                message.appendChild(text);
                            }
                        }
                    }
                },
                cache: false,
                contentType: false,
                processData: false,
            })
        }, 100)
    })
})