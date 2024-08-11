$("#show_password").on("click", function(){
    if($(this).is(':checked')){
    	$("#new_password").attr("type", "text");
    	$("#repeat_password").attr("type", "text");      
    }
    else{
    	$("#new_password").attr("type", "password");
    	$("#repeat_password").attr("type", "password");	
    }
});