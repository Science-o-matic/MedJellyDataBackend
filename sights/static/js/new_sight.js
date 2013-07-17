$(document).ready(function () {

  $("form").submit(function (e) {
    if ($("#id_var_63").val().trim() === "") {
      var errorMessage = "<p class=\"input-error\">Has d'indicar la temperatura de l'aigua</p>"

      $(".input-error").remove();
      $("input[type=submit]").parent().parent().append(errorMessage);
      e.preventDefault();
    }
  });

  $.mobile.ajaxEnabled = false;

  if ($("#message").length) {
    $("#message").fadeOut(2400);
  }

});