/* jshint esversion: 6 */

/* jshint node: true */
window.addEventListener('DOMContentLoaded', function (){

    "use strict";

    // 提示版写真の移動
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
    let cancel = document.getElementById("cancel-btn");
    let photo_type = document.getElementById("photo-type");
    let select_post_type_container = document.getElementById("select-post-type-container");
    // 提示版投稿クリック
    post.addEventListener('click', function() {
        select_post_type_container.classList.remove("none");
        document.body.classList.add("overflow-hidden");
    })    

    cancel.addEventListener('click', function() {
        select_post_type_container.classList.add("none");
        document.body.classList.remove("overflow-hidden");
    });

    let next = document.getElementById("next-page");
    let cancel_s = document.getElementById("cancel-s-btn");
    let crop_image_container = document.getElementById("crop-image-container");
    let back = document.getElementById("back-page");
    var crop_images_box = document.querySelector(".crop-images-box")
    var work_space = document.querySelectorAll(".workspace img")
    var csrf = document.getElementsByName("csrfmiddlewaretoken")
    var next_page = document.querySelector('.next-page')
    var croppers = []
    var fd = new FormData()

    // 写真を投稿をクリック
    photo_type.addEventListener('click', function () {
        select_post_type_container.classList.add("none");
        crop_image_container.classList.remove("none");
    })

    // クリックが起きた時
    document.addEventListener('click', function(e) {
        // 写真を投稿　トリミング
        if(e.target.classList.value === 'upload') {
            var input_button = e.target.nextElementSibling
            input_button.click()
            input_button.onchange = () => {
                next_page.classList.remove("none")
                e.target.parentNode.parentNode.previousElementSibling.children[1].classList.add('none')
                var file = input_button.files[0]
                var url = window.URL.createObjectURL(new Blob([file], {type: 'image/jpg'}))
                var picture_workspace = e.target.parentNode.parentNode.previousElementSibling.children[0]
                picture_workspace.src = url

                var options = {
                    dragMode: 'move',
                    aspectRatio: 1,
                    preview: '',
                    viewMode: 2,
                    modal: false,
                    background: false,
                    cropBoxResizable: false,
                    ready: function(){

                        back.onclick = () => {
                            var delete_board = window.confirm('削除してもよろしいで')
                            if(delete_board) {
                                cropper1.destroy()
                                picture1_workspace.src = ''
                                image_workspaceSpan.style.display = 'block'
                                select_post_type_container.classList.remove("none");
                                crop_image_container.classList.add("none"); 
                            }
                        }
                    }
                }
                croppers.push(new Cropper(picture_workspace, options))
            }
        }
        // プラスボタンを押された時leftを-100％にする
        if(e.target.classList.value === 'plus') {
            let styleLeft = crop_images_box.style.left;
            let left = Number(styleLeft.replace(/%/g, ""));
            crop_images_box.style.left = (left-100) + "%";
        }
        // backボタンを押された時leftを＋100％にする
        if(e.target.classList.value === 'input-back') {
            let styleLeft = crop_images_box.style.left;
            let left = Number(styleLeft.replace(/%/g, ""));
            crop_images_box.style.left = (left+100) + "%";
        }
    })
                
    // 戻るを押した場合
    back.addEventListener('click', function () {
        select_post_type_container.classList.remove("none");
        crop_image_container.classList.add("none");
    });

    var board_upload = document.getElementById("board-upload")
    var left_container = document.getElementById("left-container")
    var description_input_container = document.getElementById("description-input-container")
    var description_input = document.getElementById("description-input")
    // 次へのボタンが押された場合　-> 掲示版投稿最終ページへ
    next.addEventListener('click', function(){
        description_input_container.classList.remove("none")
        crop_image_container.classList.add("none")
    })
    // コメント追加
    description_input.addEventListener('change', function() {
        var description = description_input.value
        fd.append('description', description)
    })

    // 掲示板投稿最終ボタン
    board_upload.addEventListener('click', function () {
        // 変更を全て初期化
        description_input_container.classList.add("none")
        crop_images_box.style.left = '0%';
        var image_work_span = document.querySelectorAll('.workspace span')
        for(var i = 0; i < image_work_span.length; i++){
            image_work_span[i].classList.remove('none')
        }

        // 写真情報をfdについかする
        var i
        for(i = 0; i < croppers.length; i++){
            let picture = 'picture' + (i+1)
            croppers[i].getCroppedCanvas().toBlob((blob) => {
                fd.append(picture, blob, picture+'.png')
            })
        }
        fd.append('csrfmiddlewaretoken', csrf[0].value)
        fd.append('action_type', 'board')
        setTimeout(function() {
            $.ajax({
                type: 'POST',
                url: '',
                enctype: 'multipart/form-data',
                data: fd,
                success(responce) {
                    console.log('Upload success');
                    console.log(responce)
                    description_input_container.classList.add("none")
                    var board_container = document.createElement('div')
                    board_container.className = 'board-container'
                    var board_wrap = document.createElement('div')
                    board_wrap.className = 'board-wrap'
                    board_container.insertBefore(board_wrap, null)
                    var board_header_wrap = document.createElement('div')
                    board_header_wrap.className = 'board-header-wrap'
                    board_wrap.insertBefore(board_header_wrap, null)
                    var board_picture_wrap = document.createElement('div')
                    board_picture_wrap.className = 'board-picture-wrap'
                    board_wrap.insertBefore(board_picture_wrap, null)
                    var board_fotter = document.createElement('div')
                    board_fotter.className = 'board-fotter'
                    board_wrap.insertBefore(board_fotter, null)
                    var board_header_contents = document.createElement('div')
                    board_header_contents.className = 'board-header-contents'
                    board_header_wrap.insertBefore(board_header_contents, null)
                    var board_user_wrap = document.createElement('div')
                    board_user_wrap.className = 'board-user-wrap'
                    board_header_contents.insertBefore(board_user_wrap, null)
                    var board_icon = document.createElement('div')
                    board_icon.className = 'board-icon'
                    board_user_wrap.insertBefore(board_icon, null)
                    var user_home = document.createElement('a')
                    user_home.href = responce.user_home_url
                    board_icon.insertBefore(user_home, null)
                    var user_img = document.createElement('img')
                    user_img.src = responce.user_img
                    user_home.insertBefore(user_img, null)
                    var board_username = document.createElement('div')
                    board_username.className = 'board-username'
                    board_user_wrap.insertBefore(board_username, null)
                    var username = document.createElement('a')
                    username.href = responce.user_home_url
                    username.innerText = responce.username
                    board_username.insertBefore(username, null)
                    var board_setting = document.createElement('div')
                    board_setting.className = 'board-setting'
                    board_header_contents.insertBefore(board_setting, null)
                    var board_three_point = document.createElement('div')
                    board_three_point.className = 'three-point'
                    board_setting.insertBefore(board_three_point, null)
                    var three_point_img = document.createElement('img')
                    three_point_img.src = '/static/sns/img/home/three_point.svg'
                    board_three_point.insertBefore(three_point_img, null)
                    var board_picture = document.createElement('div')
                    board_picture.className = 'board-picture'
                    board_picture_wrap.insertBefore(board_picture, null)
                    if(responce.picture_count > 1){
                        var navigator_before_shadow = document.createElement('div')
                        navigator_before_shadow.className = 'navigator-before-shadow none'
                        board_picture_wrap.insertBefore(navigator_before_shadow, null)
                        var navigator_before = document.createElement('button')
                        navigator_before.className = 'navigator-before none'
                        board_picture_wrap.insertBefore(navigator_before, null)
                        var before = document.createElement('div')
                        before.className = 'before'
                        navigator_before.insertBefore(before, null)
                        var navigator_next_shadow = document.createElement('div')
                        navigator_next_shadow.className = 'navigator-next-shadow'
                        board_picture_wrap.insertBefore(navigator_next_shadow, null)
                        var navigator_next = document.createElement('button')
                        navigator_next.className = 'navigator-next'
                        board_picture_wrap.insertBefore(navigator_next, null)
                        var next = document.createElement('div')
                        next.className = 'next'
                        navigator_next.insertBefore(next, null)
                    }
                    var position_wrap = document.createElement('div')
                    position_wrap.className = 'position-wrap'
                    board_picture_wrap.insertBefore(position_wrap, null)
                    for(var i = 0; i < responce.picture_count; i++){
                        var picture = 'responce.picture' + (i+1)
                        var picture_img = document.createElement('img')
                        var position = document.createElement('div')
                        var blue_position = document.createElement('div')
                        picture_img.src = eval(picture)
                        position.className = 'position'
                        blue_position.className = 'position blue'
                        if(i === 0){
                            picture_img.className = 'target'
                        }
                        if(i ===1 ){
                            position_wrap.insertBefore(blue_position, null)
                            position_wrap.insertBefore(position, null)
                        }
                        if(i > 1){
                            position_wrap.insertBefore(position, null)
                        }
                        board_picture.insertBefore(picture_img, null)
                    }
                    var board_action_wrap = document.createElement('div')
                    board_action_wrap.className = 'board-action-wrap'
                    board_fotter.insertBefore(board_action_wrap, null)
                    var favorite = document.createElement('div')
                    favorite.className = 'favorite'
                    board_action_wrap.insertBefore(favorite, null)
                    var favorite_img = document.createElement('img')
                    favorite_img.src = '/static/sns/img/home/favorite.svg'
                    favorite_img.className = 'favorite-action'
                    favorite_img.dataset.boardid = responce.board_id
                    favorite.insertBefore(favorite_img, null)
                    var board_like_list = document.createElement('div')
                    board_like_list.className = 'board-like-list'
                    board_fotter.insertBefore(board_like_list, null)
                    var like_list = document.createElement('div')
                    like_list.className = 'like-list'
                    board_like_list.insertBefore(like_list, null)
                    var board_description_container = document.createElement('div')
                    board_description_container.className = 'board-description-container'
                    board_fotter.insertBefore(board_description_container, null)
                    var board_description_wrap = document.createElement('div')
                    board_description_wrap.className = 'board-description-wrap'
                    board_description_container.insertBefore(board_description_wrap, null)
                    var board_description_user = document.createElement('div')
                    board_description_user.className = 'board-description-user'
                    board_description_user.innerText = responce.username
                    board_description_wrap.insertBefore(board_description_user, null)
                    var board_description_text = document.createElement('div')
                    board_description_text.className = 'board-description-text'
                    board_description_text.innerText = responce.description
                    board_description_wrap.insertBefore(board_description_text, null)
                    var board_comment_list_wrap = document.createElement('div')
                    board_comment_list_wrap.className = 'board-comment-list-wrap'
                    board_description_container.insertBefore(board_comment_list_wrap, null)
                    var board_time = document.createElement('div')
                    board_time.className = 'board-time'
                    board_time.innerText = responce.create_at
                    board_fotter.insertBefore(board_time, null)
                    var board_comment_action_wrap = document.createElement('div')
                    board_comment_action_wrap.className = 'board-comment-action-wrap'
                    board_fotter.insertBefore(board_comment_action_wrap, null)
                    var comment_input = document.createElement('input')
                    comment_input.type = 'text'
                    comment_input.placeholder = 'コメント追加...'
                    comment_input.className = 'comment'
                    board_comment_action_wrap.insertBefore(comment_input, null)
                    var comment_submit_input = document.createElement('input')
                    comment_submit_input.className = 'comment-submit'
                    comment_submit_input.type = 'submit'
                    comment_submit_input.value = '投稿'
                    comment_submit_input.dataset.boardid = responce.board_id
                    board_comment_action_wrap.insertBefore(comment_submit_input, null)
                    
                    
                    left_container.insertBefore(board_container, left_container.firstChild)
                    document.body.classList.remove("overflow-hidden")
                    var k
                    for(k = 0; k < croppers.length; k ++){
                        croppers[k].destroy()
                    }
                    for(k = 0; k < work_space.length; k++){
                        work_space[k].src = ''
                    }
                    croppers = []
                    var next_page = document.querySelector('.next-page')
                    next_page.classList.add('none')
                    var description_input = document.getElementById("description-input")
                    description_input.value = ''
                },
                error() {
                    console.log('Upload error');
                },
                cache: false,
                contentType: false,
                processData: false,
            })
        }, 2000);
    });
    

            

    cancel_s.addEventListener('click', function() {
        crop_image_container.classList.add("none");
        document.body.classList.remove("overflow-hidden");
    });

    
    document.addEventListener('click', function(e){
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
                        e.target.parentNode.parentNode.nextElementSibling.children[0].innerText = ''
                        e.target.parentNode.parentNode.nextElementSibling.children[0].innerHTML = '<span class="strong">「いいね！」</span>した人がまだいません'
                    } else if(responce.type == 1){
                        e.target.parentNode.parentNode.nextElementSibling.children[0].innerText = ''
                        e.target.parentNode.parentNode.nextElementSibling.children[0].innerHTML = '<span class="strong">' + responce.first_like + '</span>が「いいね！」しました'
                    } else{
                        e.target.parentNode.parentNode.nextElementSibling.children[0].innerText = ''
                        e.target.parentNode.parentNode.nextElementSibling.children[0].innerHTML = '<span class="strong">' + responce.first_like + '、その他</span>が「いいね！」しました'
                    }
                },
                cache: false,
                contentType: false,
                processData: false
            })
        }
        if(e.target.classList.value === 'comment-submit' && e.target.previousElementSibling.value){
            console.log('comment')
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
                    var position = e.target.parentNode.previousElementSibling.previousElementSibling.children[1]
                    var comment_list = document.createElement('div')
                    comment_list.className = 'comment-list'
                    var comment_username = document.createElement('div')
                    comment_username.className = 'comment-username'
                    comment_list.insertBefore(comment_username, null)
                    var comment_username_a = document.createElement('a')
                    comment_username_a.href = responce.user_home_url
                    comment_username_a.innerText = responce.username
                    comment_username.insertBefore(comment_username_a, null)
                    var half_space = document.createElement('div')
                    half_space.innerHTML = '&nbsp;'
                    comment_list.insertBefore(half_space, null)
                    var comment_text = document.createElement('div')
                    comment_text.innerText = responce.comment
                    comment_text.className = 'comment-text'
                    comment_list.insertBefore(comment_text, null)
                    position.insertBefore(comment_list, null)
                },
                cache: false,
                contentType: false,
                processData: false
            })
        }
    })

    var setting_follow = document.querySelector('.setting-follow')
    var setting_container = document.querySelector('.setting-container')
    var setting_cancel = document.querySelector('.setting-cancel')
    var setting_action_type = ''
    var setting_board_id = ''
    var board_user = ''
    var board
    var board_id;

    // 掲示板編集画面
    var edit_board_container = document.querySelector('.edit-board-container')
    var edit_picture_wrap = document.querySelector('.edit-picture-wrap')
    var edit_navigator = document.querySelector('.edit-navigator')
    var edit_position_wrap = document.querySelector('.edit-position-wrap')
    var edit_board_icon = document.querySelector('.edit-board-icon img')
    var edit_board_username = document.querySelector('.edit-board-username')
    var edit_board_textarea = document.querySelector('.edit-board-textarea textarea')
    var edit_board_header_cancel = document.querySelector('.edit-board-header-cancel')
    var edit_baord_header_submit = document.querySelector('.edit-board-header-submit')

    // スクロール禁止関数
    function disableScroll(event) {
        event.preventDefault();
    }

    document.addEventListener('click', function(e){
        if(e.target.classList.value == 'board-setting-img'){
            setting_container.classList.remove('none')
            var followed = e.target.dataset.followed
            if(followed == 'followed'){
                setting_action_type = 'clear_follow'
            }else if(followed == 'follow'){
                setting_action_type = 'follow'
            }else{
                setting_action_type = 'edit_board'
            }
            board_id = e.target.dataset.boardid
            setting_board_id = board_id
            board_user = e.target.dataset.username
            setting_follow.innerText = ''
            if(followed == 'followed' ){
                var delete_board = document.querySelector('.delete-board')
                if(delete_board){
                    delete_board.remove()
                }
                setting_follow.classList.remove('setting-board-edit-action')
                setting_follow.classList.remove('setting-follow-action')
                setting_follow.innerText = 'フォローをやめる'
                setting_follow.classList.add('setting-follow-clear-action')
            }else if(followed == 'follow'){
                var delete_board = document.querySelector('.delete-board')
                if(delete_board){
                    delete_board.remove()
                }
                setting_follow.classList.remove('setting-follow-clear-action')
                setting_follow.classList.remove('setting-board-edit-action')
                setting_follow.innerText = 'フォローする'
                setting_follow.classList.add('setting-follow-action')
            }else{
                var delete_board = document.querySelector('.delete-board')
                if(delete_board){
                    delete_board.remove()
                }
                setting_follow.classList.remove('setting-follow-clear-action')
                setting_follow.classList.remove('setting-follow-action')
                setting_follow.innerText = '投稿を編集する'
                setting_follow.classList.add('setting-board-edit-action')
                var delete_board = document.createElement('div')
                delete_board.className = 'delete-board'
                delete_board.innerText = '削除する'
                setting_follow.after(delete_board)
            }
            board = e.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode
        }
        if(e.target.classList.value == 'setting-move-board'){
            window.location.href = '/p/' + setting_board_id;
        }
        if(e.target.classList.value == 'setting-follow setting-follow-clear-action'){
            console.log(board_user)
            var fd = new FormData()
            fd.append('csrfmiddlewaretoken', csrf[0].value)
            fd.append('username', board_user)
            fd.append('action_type', setting_action_type)
            $.ajax({
                type: 'POST',
                url: '',
                data: fd,
                success(responce){
                    setting_follow.classList.remove('setting-follow-clear-action')
                    setting_follow.classList.remove('setting-board-edit-action')
                    setting_follow.innerText = 'フォローする'
                    setting_follow.classList.add('setting-follow-action')
                    setting_action_type = 'follow'
                },
                cache: false,
                contentType: false,
                processData: false
            })
        }
        if(e.target.classList.value == 'setting-follow setting-follow-action'){
            console.log(board_user)
            var fd = new FormData()
            fd.append('csrfmiddlewaretoken', csrf[0].value)
            fd.append('username', board_user)
            fd.append('action_type', setting_action_type)
            $.ajax({
                type: 'POST',
                url: '',
                data: fd,
                success(responce){
                    setting_follow.classList.remove('setting-board-edit-action')
                    setting_follow.classList.remove('setting-follow-action')
                    setting_follow.innerText = 'フォローをやめる'
                    setting_follow.classList.add('setting-follow-clear-action')
                    setting_action_type = 'clear_follow'
                },
                cache: false,
                contentType: false,
                processData: false
            })
        }
        if(e.target.classList.value == 'delete-board'){
            var fd = new FormData()
            fd.append('csrfmiddlewaretoken', csrf[0].value)
            fd.append('username', board_user)
            fd.append('board_id', setting_board_id)
            fd.append('action_type', 'setting_delete_board')
            var comfirm_result = window.confirm('削除してもよろしですか？')
            if(comfirm_result){
                $.ajax({
                    type: 'POST',
                    url: '',
                    data: fd,
                    success(responce){
                        if(responce.success){
                            window.confirm('削除しました')
                        }
                        setting_container.classList.add('none')
                        console.log(board)
                        board.remove()
                    },
                    cache: false,
                    contentType: false,
                    processData: false
                })
            }
        }
        if(e.target.classList.value == 'setting-follow setting-board-edit-action'){
            var fd = new FormData()
            fd.append('csrfmiddlewaretoken', csrf[0].value)
            fd.append('board_id', setting_board_id)
            fd.append('action_type', 'setting_board_edit_action')
            $.ajax({
                type: 'POST',
                url: '',
                data: fd,
                success(responce){
                    setting_container.classList.add('none')
                    document.addEventListener('touchmove', disableScroll, { passive: false });
                    document.addEventListener('mousewheel', disableScroll, { passive: false });
                    edit_board_container.classList.remove('none')
                    for(let i =1; i <= responce.len_picture; i++){
                        var picture_url = 'responce.picture' + i + '_url'
                        var picture = document.createElement('img')
                        picture.src = eval(picture_url)
                        if(i==1){
                            picture.className = 'edit-target'
                        }
                        edit_picture_wrap.insertBefore(picture, null)
                        if(i == 2){
                            var edit_board_before = document.createElement('div')
                            edit_board_before.className = 'edit-board-before'
                            var edit_navigator_before = document.createElement('button')
                            edit_navigator_before.className = 'edit-navigator-before'
                            edit_board_before.insertBefore(edit_navigator_before, null)
                            edit_navigator.insertBefore(edit_board_before, null)
                            var edit_board_next = document.createElement('div')
                            edit_board_next.className = 'edit-board-next'
                            var edit_navigator_next = document.createElement('button')
                            edit_navigator_next.className = 'edit-navigator-next'
                            edit_board_next.insertBefore(edit_navigator_next, null)
                            edit_navigator.insertBefore(edit_board_next, null)

                            var edit_position_blue = document.createElement('div')
                            edit_position_blue.className = 'edit-position edit-blue'
                            var edit_position = document.createElement('div')
                            edit_position.className = 'edit-position'
                            edit_position_wrap.insertBefore(edit_position_blue, null)
                            edit_position_wrap.insertBefore(edit_position, null)
                        }else if(i > 2){
                            var edit_position = document.createElement('div')
                            edit_position.className = 'edit-position'
                            edit_position_wrap.insertBefore(edit_position, null)
                        }
                    }
                    edit_board_icon.src = responce.user_icon_url
                    edit_board_username.innerText = responce.username
                    edit_board_textarea.value = responce.description
                },
                cache: false,
                contentType: false,
                processData: false
            })
        }
    })
    setting_cancel.addEventListener('click', function(){
        setting_container.classList.add('none')
    })
    edit_board_header_cancel.addEventListener('click', function(){
        edit_board_container.classList.add('none')
        while(edit_picture_wrap.firstChild){
            edit_picture_wrap.removeChild(edit_picture_wrap.firstChild);
        }
        while(edit_navigator.firstChild){
            edit_navigator.removeChild(edit_navigator.firstChild);
        }
        while(edit_position_wrap.firstChild){
            edit_position_wrap.removeChild(edit_position_wrap.firstChild)
        }
        document.removeEventListener('touchmove', disableScroll, { passive: false });
        document.removeEventListener('mousewheel', disableScroll, { passive: false });
    })

})


