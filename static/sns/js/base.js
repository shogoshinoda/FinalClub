/* jshint esversion: 6 */
/* jshint node: true */
window.addEventListener('DOMContentLoaded', function (){

    "use strict";
    const search_input = document.getElementById("search_input");
    const search_result = document.getElementById("search_result");
    const search_box = document.getElementById("search_box");

    // イベントリスナーでイベント「change]を登録　検索ボックスから外れたとき
    search_input.addEventListener("change", function (){
        search_box.classList.add("none");
        search_result.classList.add("none");
        this.value = '';
        console.log(this.value);
    });

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
            console.log("aaaa");
            console.log(search_input.value);
        }
    });


    const notice_icon = document.getElementById("notice-icon");
    // const notice_icon_img = document.getElementById("notice-icon-img");
    const notice_box = document.getElementById("notice-box");
    const notice_wrap = document.getElementById("notice-wrap");
    // const notice = document.getElementById("notice");
    // const style_notice_box = document.defaultView.getComputedStyle(notice_box, null).display;
    // //
    notice_icon.addEventListener("click", function () {
        notice_box.classList.toggle("none");
        notice_wrap.classList.toggle("none");
    });
    // // notice_wrap.addEventListener("blur", function () {
    // //         notice_box.classList.add("none");
    // //         notice_wrap.classList.add("none");
    // // });
    // //
    // notice.addEventListener("mouseenter", function () {
    //     notice_icon_img.src = "/static/img/base/notifications_t.svg";
    //     notice_box.classList.remove("none");
    //     notice_wrap.classList.remove("none");
    // });
    // notice_box.addEventListener("mouseleave", function () {
    //     notice_icon_img.src = "/static/img/base/notifications.svg";
    //     notice_box.classList.add("none");
    //     notice_wrap.classList.add("none");
    // });



    // notice_icon.addEventListener("click", function (){
    //     notice_icon_img.src = "/static/img/base/notifications_t.svg";
    // });
    const my_icon_contain = document.getElementById("my-icon-contain");
    const my_icon_box = document.getElementById("my-icon-box");
    const my_icon_description = document.getElementById("my-icon-description");

    my_icon_contain.addEventListener("click", function () {
       my_icon_box.classList.toggle("none");
       my_icon_description.classList.toggle("none");
    });

});