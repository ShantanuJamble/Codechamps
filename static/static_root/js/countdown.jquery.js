(function($) {
	$.fn.countdown=function countdown(options,callback) {
		var settings ={ 'date':null};

		if (options) {
			$.extend(settings , options);
		}
        var this_sel = $(this);
		function count_exec() {
            var eventDate = Date.parse(settings['date']) / 1000;
            var currentDate = Math.floor($.now() / 1000);

			if(eventDate <=currentDate)
			{
				callback.call(this);
				clearInterval(interval);
			}

            var seconds = eventDate - currentDate;


            var days = Math.floor(seconds / (60 * 60 * 24));
			seconds -= days*60*60*24;


            var hours = Math.floor(seconds / (60 * 60));
			seconds -=hours*60*60;

            var minuits = Math.floor(seconds / 60);
			seconds-= minuits*60;

			days=(String(days).length !=2)?'0'+days:days;
			hours=(String(hours).length !=2)?'0'+hours:hours;
			minuits=(String(minuits).length !=2)?'0'+minuits:minuits;
			seconds=(String(seconds).length !=2)?'0'+seconds:seconds;

			if(!isNaN(eventDate)){
				this_sel.find('.days').text(days);
				this_sel.find('.hours').text(hours);
				this_sel.find('.minuits').text(minuits);
				this_sel.find('.seconds').text(seconds);
			}
		}	

		count_exec();

		interval=setInterval(count_exec,1000);
	}  
})(jQuery);