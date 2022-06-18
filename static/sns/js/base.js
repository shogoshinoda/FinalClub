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

    // イベントリスナーでイベント[input]を登録　検索ボックスに入力したとき
    search_input.addEventListener("input", function (){
        search_box.classList.remove("none");
        search_result.classList.remove("none");
        console.log(this.value);
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