/* jshint esversion: 6 */
/* jshint node: true */
window.addEventListener('DOMContentLoaded', function (){

    "use strict";
    const search_input = document.getElementById("search_input");
    const search_result = document.getElementById("search_result");
    const search_box = document.getElementById("search_box");

    // イベントリスナーでイベント「change]を登録
    search_input.addEventListener("change", function (){
        search_box.classList.add("none");
        search_result.classList.add("none");
        this.value = '';
        console.log(this.value);
    });

    // イベントリスナーでイベント[input]を登録
    search_input.addEventListener("input", function (){
        search_box.classList.remove("none");
        search_result.classList.remove("none");
        console.log(this.value);
    });

    // イベントリスナーでイベント「クリック」を登録
        search_input.addEventListener("click", function (){
            if (!this.value) {
                console.log("aaaa");
                console.log(search_input.value);
            }
    });




});