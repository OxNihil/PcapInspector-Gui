$(document).ready(function(){
	var pktcount = $('#packet-table tr').length;
	var npages = Math.ceil(pktcount/10);
	console.log(npages);
	for (i = 1; i < npages; i++) { 
		var p = document.createElement("p");
		p.className = "paginas";
		p.id = i;
		p.onclick = function(){changepage($(this)[0].id)};
		var pag = document.createTextNode(i);
		p.appendChild(pag);
		const element = document.getElementById("pages");
		element.appendChild(p);
	};
	changepage(1);
});


function changepage(pag){
	var table = document.getElementById("packet-table");
	var active = document.getElementById(pag);
	const pagesize = 10;
	var liminf = (pag-1) * pagesize;
	var limsup = liminf+pagesize;
	var count=0;
	$('#packet-table tr').each(function(){
		var pktid = $(this).attr("id");
		if (count < liminf){
			count++;
			if (pktid != "table-header"){
				$(this).fadeOut('normal').addClass('hidden');
			}
			return;
		}
		if (count >= liminf && count < limsup){
			if (pktid != "table-header"){
				$(this).fadeIn('slow').removeClass('hidden');
			}
		} else{
			$(this).fadeOut('normal').addClass('hidden');
		}	
		count++;
	});
	count=0;
}
