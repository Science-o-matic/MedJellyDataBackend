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

function toggleJellyfishesFieldset(jellyfishes_presence) {
  if (jellyfishes_presence.is(':checked')) {
    $(".jellyfishes").show();
  } else {
    $(".jellyfishes").hide();
  }
}



$(document).ready(function () {
  var jellyfishes_presence = $("#id_jellyfishes_presence");

  $.mobile.ajaxEnabled = true;

  if ($("#message").length) {
    $("#message").fadeOut(2400);
  }

  toggleJellyfishesFieldset(jellyfishes_presence);

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

  jellyfishes_presence.click(function() {
    toggleJellyfishesFieldset($(this));
  });

});