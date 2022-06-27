// window.addEventListener("DOMContentLoaded" , function (){
//     $("#submit").submit(function(event){ submit(event); });
// });

// function submit(event){
//     event.preventDefault();

//     var serializedData = $("create_boards_form").serialize();

//     $.ajax({
//         type: 'post',
//         url: $("create_boards_form").data('url'),
//         data: {'content': serializedData,
//                'csrfmiddlewaretoken': '{{ csrf_token }}',},
//         success: function(responce) {
//             $(".a").append(responce.board)
//         }
//     });;
    
// }

// $("#create_boards_form").click( function(event) {
//     event.preventDefault();

//     var form = $(this);
//     console.log('fjajfdjafjafkjasfkajfka')
//     $.ajax({
//         url: form.data("url"),
//         method: form.prop("method"),
//         data: form.serialize(),
//         timeout: 10000,
//         dataType: 'json'
//     })
//     .done( function(data) {
//         alert("done");
//         $("#content").append(data);
//     });
// });

// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// var csrftoken = getCookie('csrftoken');

// function csrfSafeMethod(method) {
//     // these HTTP methods do not require CSRF protection
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }

// $.ajaxSetup({
//     beforeSend: function (xhr, settings) {
//         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     }
// });

// $('#create_boards_form').on('submit', function(e) {
//     e.preventDefault();

//     form = $(this)

//     $.ajax({
//         'url': form.data("url"),
//         'type': 'POST',
//         'data': form.serialize(),
//         'dataType': 'json'
//     })
//     .done(function(response){
//         console.log('done')
//         $("#content").append(response.board)
//     });
// });
// $(document).ready(function(event){

//     setInterval(function(){
//         $.ajax({
//             type: 'GET',
//             url: "/",
//             success: function(responce){
//                 console.log(responce.boards);
//             },
//             error: function(responce){
//                 alert("An Error Occured");
//             }
//         });
//     }, 1000);
// });

$(document).on('submit', '#create_boards_form', function(e){
    e.preventDefault();

    const csrf = $("input[name=csrfmiddlewaretoken]").val();
    const form = $("#create_boards_form");

    $.ajax({
        type: 'POST',
        url: "/",
        enctype: "multipart/form-data",
        data: {
            board: form.serialize(),
            csrfmiddlewaretoken: csrf,
        },
        success: function(responce){
            console.log(responce.description);
        }
    });
});