/* jshint esversion: 6 */

/* jshint node: true */
window.addEventListener('DOMContentLoaded', function (){

    "use strict";

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
            board.style.transform += "translateX(-100%)";
            board.children[position].classList.remove("target");
            board.children[position + 1].classList.add("target");
            e.target.parentNode.previousElementSibling.previousElementSibling.classList.remove("none");
            e.target.parentNode.previousElementSibling.previousElementSibling.previousElementSibling.classList.remove("none")
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
            board.style.transform += "translateX(100%)";
            board.children[position].classList.remove("target");
            board.children[position - 1].classList.add("target");
            e.target.parentNode.nextElementSibling.classList.remove("none");
            e.target.parentNode.nextElementSibling.nextElementSibling.classList.remove("none");
            if (position-1 === 0){
                e.target.parentNode.classList.add("none");
                e.target.parentNode.previousElementSibling.classList.add("none");
            }
        }
    });
    let before = document.getElementById("before");
    console.log(before);
});