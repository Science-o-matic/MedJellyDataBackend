$(document).ready(function () {
        $.mobile.ajaxEnabled = true;

        if ($("#message").length) {
            $("#message").fadeOut(2400);
        }

        prepareJellyFishesFieldset();

        $("form").submit(function (e) {
                toggleSubmitButton();

                if ($("#id_var_63").val().trim() === "") {
                    var errorMessage = "<p class=\"input-error\">Has d'indicar la temperatura de l'aigua</p>";

                    $(".input-error").remove();
                    $("input[type=submit]").parent().parent().append(errorMessage);
                    e.preventDefault();
                    toggleSubmitButton();
                }
            });
});

$(document).on("click", "#add_jelly", function () {
        $(this).before($("#id_jellyfishes").parents("ul").clone());
        $(this).before("<hr/>");
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
    if (jellyfishes_presence.is(':checked')) {
        $(".jellyfishes").show();
        renderJellyfishes($(".jellyfishes"), jellyfishes);
    } else {
        $(".jellyfishes").hide();
        $(".jellyfishes .jellyfish").remove();
    }
}

function renderJellyfishes(target, jellyfishes) {
    var that = this;

    if (!this.hasOwnProperty("template")) {
        $.get('/static/js/jellyfish.mst', function(template) {
                Mustache.parse(template);
                that.template = template;
                target.append(Mustache.render(template, jellyfishes));
        });
    } else {
        target.append(Mustache.render(this.template, jellyfishes));
    }
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
}
