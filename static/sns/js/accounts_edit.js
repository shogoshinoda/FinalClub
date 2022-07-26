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

    const input_icon = document.getElementById('user-icon-input');
    const input_icon_button = document.querySelector('.user-icon-edit-button');
    const workspace_container = document.querySelector('.workspace-container');
    const show_crop_image = document.querySelector('.user-icon')
    var cropper = '';
    var submit = document.getElementById('submit');
    var csrf = document.getElementsByName('csrfmiddlewaretoken');
    var fd = new FormData()
    var username = document.getElementById('username');
    var nickname = document.getElementById('nickname');
    var introduction = document.getElementById('introduction');
    var user_home_url = document.querySelector('.profile-text .a')

    input_icon_button.addEventListener('click', function(){
        input_icon.click();
    });
    input_icon.addEventListener('change', function(){
        console.log(input_icon)
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

    })

    var result_button = document.getElementById('result-button')
    var croppedCanvas;
    var roundedCanvas;

    result_button.addEventListener('click', function(){
        croppedCanvas = cropper.getCroppedCanvas();
        roundedCanvas = getRoundedCanvas(croppedCanvas);
        workspace_container.classList.add('none')
        show_crop_image.src = roundedCanvas.toDataURL()
    })

    input_icon.onchange = () => {
        submit.style.backgroundColor = 'rgb(0, 149, 246)'
        submit.disabled = false
    }
    username.onchange = () => {
        submit.style.backgroundColor = 'rgb(0, 149, 246)'
        submit.disabled = false
    }
    nickname.onchange = () => {
        submit.style.backgroundColor = 'rgb(0, 149, 246)'
        submit.disabled = false
    }
    introduction.onchange = () => {
        submit.style.backgroundColor = 'rgb(0, 149, 246)'
        submit.disabled = false
    }

    submit.addEventListener('click', function() {
        var username_val = username.value;
        var nickname_val = nickname.value;
        var introduction_val = introduction.value;
        fd.append('csrfmiddlewaretoken', csrf[0].value)
        if(cropper){
            roundedCanvas.toBlob((blob) => {
                fd.append('user_icon', blob, 'user_icon.png')
            })
            fd.append('usericon', roundedCanvas.toDataURL())
        }
        fd.append('username', username_val)
        fd.append('nickname', nickname_val)
        fd.append('introduction', introduction_val)
        setTimeout(function() {
            $.ajax({
                type: 'POST',
                url: '',
                data: fd,
                success(responce) {
                    if(responce.success){
                        window.confirm('プロフィールが更新されました。');
                        user_home_url.href = `/${responce.username}/`
                    }else{
                        username.value = responce.username
                        for(let error_message of responce.error_messages){
                            if(error_message == 'only_number_english'){
                                window.confirm('半角英数数字、.(ピリオド)、_(アンダースコア)のみでユーザネームを作成してください');
                            }
                            if(error_message == 'not_username_unique'){
                                window.confirm('すでにこのユーザネームを使用しているユーザがいます');
                            }
                        }
                    }
                },
                cache: false,
                contentType: false,
                processData: false,
            })
        }, 100)
        submit.style.backgroundColor = 'rgb(0, 149, 246, .3)'
        submit.disabled = true
    })



})