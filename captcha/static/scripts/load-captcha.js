function loadCaptcha() {
	$.get('http://localhost:8000/captcha/', function(data) {
		$('.captcha').html(data);
	});
}

$(document).ready(function() {
	loadCaptcha();
});