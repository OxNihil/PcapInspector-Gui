$(document).ready(function(){
	$('.filter h4').on('click', function() {
		$(this).parent().find(".menu-filtrado")[0].classList.toggle('active');
	});
	
	$('ul.listado li').click(function() {
		var txtfilter = $(this).text().toUpperCase().replace(/\s/g,"-");
		if (txtfilter == "ALL"){
			$('#packet-table tr').each(function(){
				$(this).fadeIn('slow').removeClass('hidden');
			});
		} else {
			var pktcount = $('#packet-table tr').length;
			$('#packet-table tr').each(function(){
				var pktid = $(this).attr("id");
				if(!$(this).children().hasClass(txtfilter)){
					console.log(pktid);
					if (pktid != "table-header"){
						$(this).fadeOut('normal').addClass('hidden');
					}
				}else{
					$(this).fadeIn('slow').removeClass('hidden');
				}
				
			});
			console.log(pktcount);
		}
	});
	
	$('.post-form').on('submit', function(){
		console.log("aaaa")
	});
});
