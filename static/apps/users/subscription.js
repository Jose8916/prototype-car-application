$(document).ready(function(){
if($("#amount_subscription").val()!=""){
  pay_wompi();  
}
});

function pay_wompi(){
  let key_wompi='';
  let amount=$("#amount_subscription").val()+'00';
  let reference=$("#invoice_reference").val();
  if(debug_config == false){
    key_wompi= 'pub_prod_Vlm7zuJTqCvBkhezWQZhGr8mhbVcKonm'
  }
  else{
    key_wompi='pub_test_3nY5Jqlp0rLB99qB2BcWrCwsyf721Wp6';
  }
  console.log(key_wompi+" "+reference);
  checkout = new WidgetCheckout({
    currency: 'COP',
    amountInCents: amount,
    reference: reference,
    publicKey: key_wompi,
    redirectUrl: urlapis_config+'/invoice/'+$("#invoice_id").val() // Opcional
  });
  checkout.open(function ( result ) {
      var transaction = result.transaction;
      console.log(transaction);
      if (transaction.status=="APPROVED" || transaction.status=="PENDING"){
        window.location.href=transaction.redirectUrl+"?id="+transaction.id;
      }
  });
}
