window.addEventListener("DOMContentLoaded" , function (){
    $("#submit").on("click", function(){ submit(); });
});

function submit(){
    
    var serializedData = $("create_boards_form").serialize();

    $.ajax({
        url: $("create_boards_form").data('url'),
        data: {'content': serializedData,
               'csrfmiddlewaretoken': '{{ csrf_token }}',},
        dataType: json,
        type: 'POST',
    })
    .done(function(response){
        // $(".a").before("<div>" + response.board + "</div>")
    });;
    
}