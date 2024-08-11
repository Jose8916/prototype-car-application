$("#show_password").on("click", function(){
    if($(this).is(':checked')){
    	$("#password").attr("type", "text");      
    }
    else{
    	$("#password").attr("type", "password");	
    }
});