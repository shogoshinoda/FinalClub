/* jshint esversion: 6 */
/* jshint node: true */
window.addEventListener('DOMContentLoaded', function (){

    "use strict";

    const search_input = document.getElementById("search_input");
    const search_result = document.getElementById("search_result");
    const search_box = document.getElementById("search_box");

    // 検索の時他のボタンが押された場合（通知と設定のところで同じことをすればいい）
    document.addEventListener('click', function(e){
        if(!(e.target == search_box || e.target == search_result || e.target == search_input)){
            search_box.classList.add("none");
            search_result.classList.add("none");
            search_input.value = '';
        }
    })

    var csrf = document.getElementsByName("csrfmiddlewaretoken")
    // イベントリスナーでイベント[input]を登録　検索ボックスに入力したとき
    search_input.addEventListener("input", function (){
        while(search_result.firstChild){
            search_result.removeChild(search_result.firstChild)
        }
        search_box.classList.remove("none");
        search_result.classList.remove("none");
        console.log(this.value);
        var fd = new FormData()
        fd.append('csrfmiddlewaretoken', csrf[0].value)
        fd.append('search_text', this.value)
        fd.append('action_type', 'search_user')
        $.ajax({
            type: 'POST',
            url: '',
            enctype: 'multipart/form-data',
            data: fd,
            success(responce){
                console.log(responce.users[0])
                if(!responce.users[0]){
                    console.log('uuuu')
                    var result_none = document.createElement('div')
                    result_none.className = 'result-none'
                    result_none.innerText = '検索結果はありません'
                    search_result.insertBefore(result_none, null)
                }
                for(var user of responce.users){
                    var result_content = document.createElement('div')
                    result_content.className = 'result-content'
                    var result_user = document.createElement('div')
                    result_user.className = 'result-user'
                    result_content.insertBefore(result_user, null)
                    var user_icon = document.createElement('div')
                    user_icon.className = 'user-icon'
                    result_user.insertBefore(user_icon, null)
                    var user_icon_a = document.createElement('a')
                    user_icon_a.href = user.user_home_url
                    user_icon.insertBefore(user_icon_a, null)
                    var user_icon_img = document.createElement('img')
                    user_icon_img.src = user.user_icon
                    user_icon_a.insertBefore(user_icon_img, null)
                    var user_info = document.createElement('div')
                    user_info.className = 'user-info'
                    result_user.insertBefore(user_info, null)
                    var user_id = document.createElement('div')
                    user_id.className = 'user-id'
                    user_info.insertBefore(user_id, null)
                    var user_id_a = document.createElement('a')
                    user_id_a.href = user.user_home_url
                    user_id_a.innerText = user.username
                    user_id.insertBefore(user_id_a, null)
                    var user_name = document.createElement('div')
                    user_name.className = 'user-name'
                    user_info.insertBefore(user_name, null)
                    var user_name_a = document.createElement('a')
                    user_name_a.href = user.user_home_url
                    user_name_a.innerText = user.nickname
                    user_name.insertBefore(user_name_a, null)
                    search_result.insertBefore(result_content, null)  
                }
            },
            cache: false,
            contentType: false,
            processData: false
        })
    });

    // イベントリスナーでイベント「クリック」を登録　初めに検索ボックスにクリックしたとき
    search_input.addEventListener("click", function (){
        if (!this.value) {
            search_box.classList.remove('none')
            search_result.classList.remove('none')
        }
    });


    const notice_icon = document.querySelector(".notice-icon img");
    const notice_wrap = document.getElementById("notice-wrap");
    const notice_box = document.getElementById("notice-box");
    notice_icon.addEventListener("click", function () {
        notice_box.classList.toggle("none");
        notice_wrap.classList.toggle("none");
    });
    document.addEventListener('click', function(e){
        if(!(e.target == notice_wrap || e.target == notice_box || e.target == notice_icon)){
            notice_wrap.classList.add("none");
            notice_box.classList.add("none");
        }
    })
    

    const my_icon_box = document.getElementById("my-icon-box");
    const my_icon_description = document.getElementById("my-icon-description");
    const my_icon_contain = document.querySelector('.my-icon-contain img')

    my_icon_contain.addEventListener("click", function () {
       my_icon_box.classList.toggle("none");
       my_icon_description.classList.toggle("none");
    });
    document.addEventListener('click', function(e){
        if(!(e.target == my_icon_box || e.target == my_icon_description || e.target == my_icon_contain)){
            my_icon_box.classList.add("none");
            my_icon_description.classList.add("none");
        }
    })

});