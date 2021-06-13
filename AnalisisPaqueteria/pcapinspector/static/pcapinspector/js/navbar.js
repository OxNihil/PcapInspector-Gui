$(document).ready(function(){

	$('.sidebar-navigation ul li').on('click', function() {
		$('.sidebar-navigation ul li').removeClass('active');
		$(this).addClass('active');
		window.location.href = ($(this).children("span").attr("data-url"));
	});
	
	$('#home-button').on('click', function() {
		$('.sidebar-navigation').classList.toggle('active');
	});
});


