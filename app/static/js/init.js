function flask_moment_render(elem) {
    $(elem).text(eval('moment("' + $(elem).data('timestamp') + '").' + $(elem).data('format') + ';'));
    $(elem).removeClass('flask-moment').show();
}
function flask_moment_render_all() {
    $('.flask-moment').each(function() {
        flask_moment_render(this);
        if ($(this).data('refresh')) {
            (function(elem, interval) { setInterval(function() { flask_moment_render(elem) }, interval); })(this, $(this).data('refresh'));
        }
    })
}
$(document).ready(function() {
    moment.locale("zh-cn");
    flask_moment_render_all();
    //Initial Materialize Scripts.
    $('select').material_select();
    $('.collapsible').collapsible({
      accordion : false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
    });
    $(".button-collapse").sideNav();

});

document.addEventListener("DOMContentLoaded", function() {
    $(".quotes").css("display", "none");

    $.getJSON( "https://api.github.com/gists/a00a44bac1be8c0047af9ba96a26ba03", function(data) {

        fortunes = JSON.parse(data.files["celitea.json"].content);
        randomFortune = fortunes[ Math.floor( Math.random() * fortunes.length ) ];
        if ( randomFortune.author === undefined ) {
            Materialize.toast(randomFortune.content, 4000);
        } else {
            Materialize.toast("<p>"+randomFortune.content+ "<br /> <small>-- " + randomFortune.author + "</small></p>",4000);
        }
    });
});
