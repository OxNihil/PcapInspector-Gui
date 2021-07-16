function filterdatatable(that,n) {
    var txtfilter = $(that).text().toUpperCase().replace(/\s/g,"-");
    var table = $('#packet-table').DataTable();
    if (txtfilter == "ALL"){
        table.column(n).search( '' ).draw();
    }else{
        console.log(that.parent);
        filteredData = table.column(n).search(txtfilter).draw();
    }
}
    
$(document).ready(function(){
	$('.filter h4').on('click', function() {
		$(this).parent().find(".menu-filtrado")[0].classList.toggle('active');
	});
	
    
	$('#filter-ip-src ul.listado li').click( function(){
        filterdatatable(this,3);
    });
    
    $('#filter-ip-dst ul.listado li').click( function(){
        filterdatatable(this,4);
    });

    $('#filter-proto ul.listado li').click( function(){
        filterdatatable(this,7);
    });
    
    $('#filter-mac-src ul.listado li').click( function(){
        filterdatatable(this,1);
    });
    $('#filter-mac-dst ul.listado li').click( function(){
        filterdatatable(this,2);
    });
    
    $('#filter-port ul.listado li').click( function(){
        filterdatatable(this,5);
    });
    
    $('#filter-port-dst ul.listado li').click( function(){
        filterdatatable(this,6);
    });
    
});


