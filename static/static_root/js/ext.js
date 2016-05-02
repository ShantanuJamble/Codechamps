function start_countdown(milliseconds,quiz) {
    $("#countdown").countdown({date: new Date(milliseconds)},
        function () {
            window.location.replace("/end/"+quiz)
        });
}

//Unix Timestramp