/* jshint esversion: 6 */

/* jshint node: true */

window.addEventListener('DOMContentLoaded', function(){

    "use strict";

    var old_password = document.querySelector('.old-password');
    var new_password1 = document.querySelector('.new-password1');
    var new_password2 = document.querySelector('.new-password2');
    var submit = document.getElementById('submit');
    var csrf = document.getElementsByName('csrfmiddlewaretoken');
    var fd = new FormData()

    old_password.addEventListener('change', function() {
        if(old_password.value && new_password1.value && new_password2.value){
            submit.style.backgroundColor = 'rgb(0, 149, 246)'
            submit.disabled = false
        }else{
            submit.style.backgroundColor = 'rgb(0, 149, 246, .3)'
            submit.disabled = true
        }
    })
    new_password2.addEventListener('change', function() {
        if(old_password.value && new_password1.value && new_password2.value){
            submit.style.backgroundColor = 'rgb(0, 149, 246)'
            submit.disabled = false
        }else{
            submit.style.backgroundColor = 'rgb(0, 149, 246, .3)'
            submit.disabled = true
        }
    })
    new_password2.addEventListener('change', function() {
        if(old_password.value && new_password1.value && new_password2.value){
            submit.style.backgroundColor = 'rgb(0, 149, 246)'
            submit.disabled = false
        }else{
            submit.style.backgroundColor = 'rgb(0, 149, 246, .3)'
            submit.disabled = true
        }
    })


    submit.addEventListener('click', function() {
        var old_password_val = old_password.value;
        var new_password1_val = new_password1.value;
        var new_password2_val = new_password2.value;
        fd.append('csrfmiddlewaretoken', csrf[0].value)
        fd.append('old_password', old_password_val)
        fd.append('new_password1', new_password1_val)
        fd.append('new_password2', new_password2_val)
        setTimeout(function() {
            $.ajax({
                type: 'POST',
                url: '',
                data: fd,
                success(responce) {
                    if(responce.error_type){
                        if(responce.error_type == 'not_correct'){
                            window.confirm('パスワードが一致しません')
                        }else if(responce.error_type == 'danger'){
                            window.confirm('6文字以上で半角英語、全角英語、数字を含めてください')
                        }else if(responce.error_type == 'not_authenticate'){
                            window.confirm('旧パスワードが正しくありません')
                        }
                    }else{
                        window.confirm('パスワードが変更されました')
                        old_password_val = ''
                        new_password1_val = ''
                        new_password2_val = ''
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