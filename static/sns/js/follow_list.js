/* jshint esversion: 6 */

/* jshint node: true */
window.addEventListener('DOMContentLoaded', function(){
    
    "use strict";

    var csrf = document.getElementsByName("csrfmiddlewaretoken")
    document.addEventListener('click', function(e){
        console.log(e.target.classList.value)
        if(e.target.classList.value == 'follow'){
            var fd = new FormData()
            console.log(e.target.dataset.username)
            fd.append('csrfmiddlewaretoken', csrf[0].value)
            fd.append('username', e.target.dataset.username)
            fd.append('action_type', 'follow')
            $.ajax({
                type: 'POST',
                url: '',
                data: fd,
                success(responce){
                    console.log('success')
                    e.target.classList.remove('follow')
                    e.target.classList.add('clear-follow')
                    e.target.innerText = 'フォロー中'
                },
                cache: false,
                contentType: false,
                processData: false
            })
        }
        if(e.target.classList.value == 'clear-follow'){
            var fd = new FormData()
            fd.append('csrfmiddlewaretoken', csrf[0].value)
            fd.append('username', e.target.dataset.username) 
            fd.append('action_type', 'clear_follow')
            $.ajax({
                type: 'POST',
                url: '',
                data: fd,
                success(responce){
                    e.target.classList.remove('clear-follow')
                    e.target.classList.add('follow')
                    e.target.innerText = 'フォローをする'
                },
                caches: false,
                contentType: false,
                processData: false
            })
        }
    })
})