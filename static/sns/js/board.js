/* jshint esversion: 6 */

/* jshint node: true */
window.addEventListener('DOMContentLoaded', function(){
    
    "use strict";

    document.addEventListener('click', function (e){
        if (e.target.classList.value === 'navigator-next next') {
            let board = e.target.parentNode.parentNode.previousElementSibling;
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
            e.target.parentNode.parentNode.nextElementSibling.children[position].classList.remove("blue");
            e.target.parentNode.parentNode.nextElementSibling.children[position + 1].classList.add("blue");
            e.target.parentNode.previousElementSibling.children[0].classList.add("before");
            e.target.parentNode.previousElementSibling.style.opacity = 0.6;
            e.target.parentNode.previousElementSibling.children[0].style.opacity = 0;
            if (position+2 === boardPictureCount) {
                e.target.classList.remove("next");
                e.target.parentNode.style.opacity = 0;
            }
        }
        if (e.target.classList.value === 'navigator-before before') {
            let board = e.target.parentNode.parentNode.previousElementSibling;
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
            e.target.parentNode.parentNode.nextElementSibling.children[position].classList.remove("blue");
            e.target.parentNode.parentNode.nextElementSibling.children[position - 1].classList.add("blue");
            e.target.parentNode.nextElementSibling.children[0].classList.add("next");
            e.target.parentNode.nextElementSibling.style.opacity = 0.6;
            e.target.parentNode.nextElementSibling.children[0].style.opacity = 0;
            if (position-1 === 0){
                e.target.classList.remove("before");
                e.target.parentNode.style.opacity = 0;
            }
        }
    })

    var csrf = document.getElementsByName("csrfmiddlewaretoken")

    document.addEventListener('click', function(e){
        console.log(e.target.classList.value)
        if(e.target.classList.value === 'favorite-action'){
            var fd = new FormData()
            fd.append('csrfmiddlewaretoken', csrf[0].value)
            fd.append('board_id', e.target.dataset.boardid)
            fd.append('action_type', 'like')
            $.ajax({
                type: 'POST',
                url: '',
                data: fd,
                success(responce){
                    if(responce.liked){
                        e.target.setAttribute('src', '/static/sns/img/home/favorite_t.svg')
                    }
                    else{
                        e.target.setAttribute('src', '/static/sns/img/home/favorite.svg')
                    }
                    if(responce.type == 0){
                        e.target.parentNode.parentNode.parentNode.nextElementSibling.children[0].innerText = ''
                        e.target.parentNode.parentNode.parentNode.nextElementSibling.children[0].innerHTML = '<span class="strong">「いいね！」</span>した人がまだいません'
                    } else if(responce.type == 1){
                        e.target.parentNode.parentNode.parentNode.nextElementSibling.children[0].innerText = ''
                        e.target.parentNode.parentNode.parentNode.nextElementSibling.children[0].innerHTML = '<span class="strong">' + responce.first_like + '</span>が「いいね！」しました'
                    } else{
                        e.target.parentNode.parentNode.parentNode.nextElementSibling.children[0].innerText = ''
                        e.target.parentNode.parentNode.parentNode.nextElementSibling.children[0].innerHTML = '<span class="strong">' + responce.first_like + '、その他</span>が「いいね！」しました'
                    }
                },
                cache: false,
                contentType: false,
                processData: false
            })
        }
        if(e.target.classList.value === 'comment-submit'){
            var fd = new FormData()
            fd.append('csrfmiddlewaretoken', csrf[0].value)
            fd.append('board_id', e.target.dataset.boardid)
            fd.append('action_type', 'comment')
            fd.append('comment', e.target.previousElementSibling.value)
            $.ajax({
                type: 'POST',
                url: '',
                data: fd,
                success(responce){
                    console.log(responce.username)
                    console.log(responce.user_home_url)
                    console.log(responce.comment)
                    e.target.previousElementSibling.value = ''
                    var position = e.target.parentNode.previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling
                    var comments_container = document.createElement('div')
                    comments_container.className = 'comments-container'
                    var comments_wrap = document.createElement('div')
                    comments_wrap.className = 'comments-wrap'
                    comments_container.insertBefore(comments_wrap, null)
                    var comment_user_icon = document.createElement('div')
                    comment_user_icon.className = 'comment-user-icon'
                    comments_wrap.insertBefore(comment_user_icon, null)
                    var comment_user_icon_a = document.createElement('a')
                    comment_user_icon_a.href = responce.user_home_url
                    comment_user_icon.insertBefore(comment_user_icon_a, null)
                    var comment_user_icon_img = document.createElement('img')
                    comment_user_icon_img.setAttribute('src', responce.user_icon_url)
                    comment_user_icon_a.insertBefore(comment_user_icon_img, null)
                    var comment_username = document.createElement('div')
                    comment_username.className = 'comment-username'
                    comments_wrap.insertBefore(comment_username, null)
                    var comment_username_a = document.createElement('a')
                    comment_username_a.href = responce.user_home_url
                    comment_username_a.innerText = responce.username
                    comment_username.insertBefore(comment_username_a, null)
                    var comment_text = document.createElement('div')
                    comment_text.className = 'comment-text'
                    comment_text.innerText = responce.comment
                    comment_username.insertBefore(comment_text, null)
                    position.insertBefore(comments_container, null)
                },
                cache: false,
                contentType: false,
                processData: false
            })
        }
    })
})