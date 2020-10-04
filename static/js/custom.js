function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function to_bookmarks()
{
    var current = $(this);
    var type = current.data('type');
    var pk = current.data('id');
    var action = current.data('action');
 
    $.ajax({
        url : "/bookmark/" + pk,
        type : 'POST',
        data : { 'comic_id' : pk },
 
        success : function (json) {
            if ($("[data-count='" + pk + "bookmark']").length) {
                $("[data-count='" + pk + "bookmark']").text("  "+json.count);
            } else {
                $(".custom_line_" + pk).css('display','none');
            }

        }
    });
 
    return false;
}

$(function() {
    $('[data-action="bookmark"]').click(to_bookmarks);
});


$('.comic_link').hover(function(){
    var set_bg_img = $(this).find( $('.comic_link_hide') ).attr("src");
    $('.custom-bg-img').css('transform', 'scaleX(1)');
    $('.custom-bg-img').css('background-image', 'url(' + set_bg_img + ')');
});


function to_barf() {
    var barf = $( "#barf" ).val();
    
    if (barf.length > 3) {
        $.ajax({
            url : "/search/" + barf,
            type : 'POST',
            data : { 'searching' : barf },

            success : function (json) {
                $(".dropdown-item").remove();
                jQuery.each(json.result, function(k,v) {
                    $(".dropdown-menu").append("<a class='dropdown-item' href='#'>"+v+"</a>");
                });
                if ($("#barf").is(":focus")) {
                    $(".dropdown-menu").css("display", "block");
                    $(".dropdown-menu").css("left", "auto");
                    $(".dropdown-menu").css("top", "45px");
                    $(".dropdown-menu").css("width", $("#barf").outerWidth());
                }
            }
        });
    };
};

$(document).on("mouseenter", ".dropdown-item", function() {
    $("#barf").val($(this).text());
});
$("#barf").on("input focus", to_barf);
$("#barf").focusout(function() {
    $(".dropdown-menu").css("display", "none");
});
$("#button_barf").on("click", function() {
    if ($( "#barf" ).val().length != 0) {
        window.location.href = "/search/" + $( "#barf" ).val();
    }
});
