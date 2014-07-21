$(document).ready(function () {
  $.mobile.ajaxEnabled = false;

  if ($("#message").length) {
    $("#message").fadeOut(2400);
  }

  prepareJellyFishesFieldset();

  $("form").submit(function (e) {
    var errorMessage = '';
    toggleSubmitButton();

    $('input[name^="jellyfishes"]').each(function(){
      if ($(this).val() == "") {
        errorMessage = "<p class=\"input-error\">Haz de indicar todos los datos sobre medusas o indicar que no hay medusas</p>"
      }
    });

    if (errorMessage) {
      $(".input-error").remove();
      $("input[type=submit]").parent().parent().append(errorMessage);
      e.preventDefault();
      toggleSubmitButton();
    }
  });
});

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

function toggleJellyfishesFieldset(jellyfishes_presence, jellyfishes) {
   $(".jellyfishes .jellyfish").remove();
   if (jellyfishes_presence.is(':checked')) {
        $(".jellyfishes").show();
        renderJellyfishes($(".jellyfishes"), jellyfishes);
    } else {
       $(".jellyfishes").hide();
    }
}

function renderJellyfishes(target, jellyfishes) {
    var that = this;

    if (!this.hasOwnProperty("template")) {
        $.get('/static/js/jellyfish.mst', function(template) {
                Mustache.parse(template);
                that.template = template;
                renderJellyfishesTemplate(target, template, jellyfishes);
        });
    } else {
        renderJellyfishesTemplate(target, template, jellyfishes);
    }
}

function renderJellyfishesTemplate(target, template, jellyfishes) {
    target.append(Mustache.render(template, jellyfishes));
    target.css("background", "none");
    $(".jellyfish").trigger("create");
}

function prepareJellyFishesFieldset() {
  var jellyfishes_presence = $("#id_jellyfishes_presence");
  var jellyfishes = {};

  $.getJSON('/sights/jellyfishes.json', function(data) {
          jellyfishes = data;
          toggleJellyfishesFieldset(jellyfishes_presence, jellyfishes);
  });


  jellyfishes_presence.click(function() {
          toggleJellyfishesFieldset($(this), jellyfishes);
  });

  $(document).on("click", "#add_jelly", function () {
    renderJellyfishes($(".jellyfishes"), jellyfishes);
  });

}
