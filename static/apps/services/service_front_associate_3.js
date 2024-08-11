$('[data-number]').on("click", function(){
	let money_str=$("#money_verify").val()
	if($(this).attr("data-number")==="----"){
		money_str = money_str.slice(0, -1);
		$("#money_verify").val(money_str);
		$("#money_text").html(money_str);  
		if(money_str==""){
			$("#money_text").html("------");
		}
	}
	else{
		if(money_str.length<=5){
			let elements=money_str+$(this).attr("data-number");
			$("#money_verify").val(elements);
			$("#money_text").html(elements);
		}
	}
});


$(".js-collection").on("click", function(){
	let array_check=[]
	$(".js-collection:checked").each(function(){
	    array_check.push($(this).val());
	});
	$("#prefix_service").val(array_check);
});

$('.js-quantity').each(function() {
   if($(this).val()==""){
   	$(this).val(1);
   }
});