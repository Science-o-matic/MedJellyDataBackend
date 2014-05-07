function toggleSubmitButton() {
  var span_button = $('.ui-submit span.ui-btn-inner'),
    submit_button = $('.ui-submit input[type=submit]'),
    span_text = $(".ui-submit .ui-btn-text");

  if (submit_button.attr('disabled')) {
    submit_button.removeAttr('disabled');
    span_button.removeClass('ui-disabled');
    span_text.text(this.text);
  } else {
    this.text = span_text.text();
    submit_button.attr('disabled', 'disabled');
    span_button.addClass('ui-disabled');
    span_text.text("Enviando...");
  }
}


$(document).ready(function () {

  $("form").submit(function (e) {
    toggleSubmitButton();

    if ($("#id_var_63").val().trim() === "") {
      var errorMessage = "<p class=\"input-error\">Has d'indicar la temperatura de l'aigua</p>"

      $(".input-error").remove();
      $("input[type=submit]").parent().parent().append(errorMessage);
      e.preventDefault();
      toggleSubmitButton();
    }
  });

  $.mobile.ajaxEnabled = true;

  if ($("#message").length) {
    $("#message").fadeOut(2400);
  }

});