/**
 * Created by user on 10/04/2016.
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');


function get_question(question_id) {
    {
        $.ajax({
            type: "POST",
            url: "/mcqs/" + question_id.toString() + '/',
            data: {"quiz": $("h4").text(),
                "sitting_id": $("#sitting_id").text()},
            success: updateQuestion,
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'html'
        });

    }
    return false;
}

function updateQuestion(data, status, jqXHR) {
    $("#question_details").html(data);
}