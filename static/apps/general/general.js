$("js-reload").on('click', function(){
	location.reload();
});

function sw_mensaje(texto,titulo='',icono=''){
	Swal.fire({
		icon: icono,
		title: titulo,
		html: texto
	})
}

function abrir_imagen_modal(url,titulo=""){	
	title_modal = $("#GeneralModalImage").find(".modal-title")[0]
	img_modal = $("#GeneralModalImage").find("img")[0]
	$(title_modal).html(titulo)
	$(img_modal).attr("src",url)
	$("#GeneralModalImage").modal('show')
}