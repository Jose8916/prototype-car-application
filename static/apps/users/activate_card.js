$('#modal_activate_card').on('shown.bs.modal', function (event) {
  $("#activation_code").focus();
});
$('#modal_activate_card').on('hidden.bs.modal', function (e) {
    // window.location.replace("/activate_card");
    location.replace(location.href)
 });