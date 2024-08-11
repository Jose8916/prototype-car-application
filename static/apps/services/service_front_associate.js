$('[data-number]').on("click", function(){
	console.log("entro");
	let code_str=$("#code_verify").val()
	if($(this).attr("data-number")==="----"){
		code_str = code_str.slice(0, -1);
		$("#code_verify").val(code_str);
		$("#code_text").html(code_str);  
		if(code_str==""){
			$("#code_text").html("------");
		}
	}
	else{
		if(code_str.length<=5){
			let elements=code_str+$(this).attr("data-number");
			$("#code_verify").val(elements);
			$("#code_text").html(elements);
		}
	}
});