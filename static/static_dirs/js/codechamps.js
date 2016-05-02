/**
 * Created by user on 06/09/2015.
 */

$(document).ready(function () {
    $("#picbutton").hide();
    $("#profilepic").mouseenter(function () {
        $("#picbutton").show();
    });
    $("#profilepic").mouseleave(function () {
        $("#picbutton").hide();
    });
});
