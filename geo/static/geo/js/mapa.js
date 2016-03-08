$(document).ready(function() {
	boton();
	//$(".bs-example-modal-lg").modal('show');
	abrir();
});


function boton () {
	 // body...
	 $(".object-tools").append('<button type="button" id="mapa" class="btn btn-info"data-toggle="modal">Mapa</button>');
	 $("body").append('<div id="myModal" class="modal hide fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="myModalLabel">Mapa</h3></div><div class="modal-body"><div id="map"></div></div><div class="modal-footer"><button class="btn" data-dismiss="modal" aria-hidden="true">Close</button></div></div>');
}

function abrir () {
	 // body...
	 $("#mapa").click(function(event) {
	 	console.log('click');
	 	/* Act on the event */
	 	$("#myModal").modal('show');
	 	markers();
	 	//google.maps.event.addDomListener(window,'load', initMap);
	 });
}

function markers () {
	 // body...
	$.ajax({
		url: '/geo/list/map/',
		type: 'GET',
		dataType: 'json',
		success: function (response) {
			 /* body... */
			 var data = response.object_list;
			 console.log(data);
			 initMap(data);
		}
	})
	.done(function() {
		console.log("success");
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});
}

function initMap(data) {
	var myLatLng = {lat:10.3996338, lng:-75.5315906};

	var map = new google.maps.Map(document.getElementById('map'), {
	zoom: 12,
	center: myLatLng
	});
	for (var i = 0; i < data.length; i++) {
		var contentString = "<div>"+data[i].descripcion+"</div>";
		var infowindow = new google.maps.InfoWindow({
	    	content: contentString
	  	});
	 	var marker = new google.maps.Marker({
			position: {lat:data[i].lat, lng:data[i].lon},
			map: map,
			title: data[i].nombre,
		});
		marker.addListener('click', listener(infowindow, marker));
	}
	function listener(info, mark) {
		info.open(map, mark);
	}
}
