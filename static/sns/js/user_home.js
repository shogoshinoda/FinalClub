/* jshint esversion: 6 */

/* jshint node: true */
window.addEventListener('DOMContentLoaded', function(){
    
    "use strict";

    var csrf = document.getElementsByName("csrfmiddlewaretoken")
    document.addEventListener('click', function(e){
        console.log(e.target.classList.value)
        if(e.target.classList.value == 'follow-action follow'){
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
                    e.target.innerText = 'フォローを解除'
                    var follower_count = document.querySelector('.follower-count .strong')
                    console.log(follower_count)
                    follower_count.innerText = responce.count_follower
                },
                cache: false,
                contentType: false,
                processData: false
            })
        }
        if(e.target.classList.value == 'follow-action clear-follow'){
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
                    var follower_count = document.querySelector('.follower-count .strong')
                    follower_count.innerText = responce.count_follower
                },
                caches: false,
                contentType: false,
                processData: false
            })
        }
    })
})