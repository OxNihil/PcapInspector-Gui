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
				if(!$(this).children("#protocol").hasClass(txtfilter)){
					if (pktid != "table-header"){
						$(this).fadeOut('normal').addClass('hidden');
					}
				}else{
					$(this).fadeIn('slow').removeClass('hidden');
				}
				
			});
		}
	});
	
	$('#ipsrc-form').submit(function(event){
		var ipsrc = $("#ipsrc-form").children()[1].value;
		if (ipsrc != ""){
			$('#packet-table tr').each(function(){
				var pktid = $(this).attr("id");
				if(!$(this).children("#ipsrc").hasClass(ipsrc)){
					if (pktid != "table-header"){
						$(this).fadeOut('normal').addClass('hidden');
					}
				}else{
					$(this).fadeIn('slow').removeClass('hidden');
				}
			});
		} else {
			$('#packet-table tr').each(function(){
				$(this).fadeIn('slow').removeClass('hidden');
			});
		}
		event.preventDefault();
	});
	
	$('#ipdst-form').submit(function(event){
		var ipdst = $("#ipdst-form").children()[1].value;
		if (ipsrc != ""){
			$('#packet-table tr').each(function(){
				var pktid = $(this).attr("id");
				if(!$(this).children("#ipdst").hasClass(ipdst)){
					if (pktid != "table-header"){
						$(this).fadeOut('normal').addClass('hidden');
					}
				}else{
					$(this).fadeIn('slow').removeClass('hidden');
				}
			});
		} else {
			$('#packet-table tr').each(function(){
				$(this).fadeIn('slow').removeClass('hidden');
			});
		}
		event.preventDefault();
	});
	
	$('#macsrc-form').submit(function(event){
		var macsrc = $("#macsrc-form").children()[1].value;
		if (macsrc != ""){
			$('#packet-table tr').each(function(){
				var pktid = $(this).attr("id");
				if(!$(this).children("#ethsrc").hasClass(macsrc)){
					if (pktid != "table-header"){
						$(this).fadeOut('normal').addClass('hidden');
					}
				}else{
					$(this).fadeIn('slow').removeClass('hidden');
				}
			});
		} else {
			$('#packet-table tr').each(function(){
				$(this).fadeIn('slow').removeClass('hidden');
			});
		}
		event.preventDefault();
	});
	
	$('#macdst-form').submit(function(event){
		var macdst = $("#macdst-form").children()[1].value;
		if (macdst != ""){
			$('#packet-table tr').each(function(){
				var pktid = $(this).attr("id");
				if(!$(this).children("#ethdst").hasClass(macdst)){
					if (pktid != "table-header"){
						$(this).fadeOut('normal').addClass('hidden');
					}
				}else{
					$(this).fadeIn('slow').removeClass('hidden');
				}
			});
		} else {
			$('#packet-table tr').each(function(){
				$(this).fadeIn('slow').removeClass('hidden');
			});
		}
		event.preventDefault();
	});
});
