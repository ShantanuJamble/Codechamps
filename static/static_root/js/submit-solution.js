$("#loader").hide();
// using jQuery
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

//Submission  Ajax query
function submit_solution(problem_id) {
    var editor = ace.edit("inner-editor");
    var source = editor.getValue();
    var lang_chosen = $("#lang_choose").text().toLowerCase();
    if (source.length == 0)
        alert("Source File cannot be empty");
    else {
        $("#loader").show();
        {
            $.ajax({
                type: "POST",
                url: "/submit/",
                data: {"source": source, "lang_chosen": lang_chosen, "problem_id": problem_id  },
                success: updateSuccess,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                dataType: 'html'

            });
        }
    }
    return false;
}

function submit_trial_solution(problem_id) {
    var editor = ace.edit("inner-editor");
    var source = editor.getValue();
    var lang_chosen = $("#lang_choose").text().toLowerCase();
    if (source.length == 0)
        alert("Source File cannot be empty");
    else {
        $("#loader").show();
        {
            $.ajax({
                type: "POST",
                url: "/trial_submit/",
                data: {"source": source, "lang_chosen": lang_chosen, "problem_id": problem_id  },
                success: updateSuccess,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                dataType: 'html'

            });
        }
    }
    return false;
}
function updateSuccess(data, status, jqXHR) {
    $("#loader").hide();
    $("#result").html(data);

}