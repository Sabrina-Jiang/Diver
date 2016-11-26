$(window).bind('load', function() {

    $('.searcher').bind('keydown', function(e) {

    });


    $('.fa-search').bind('click', function() {

        $('#main-frame').attr('src', $('.searcher').val());
        $('#main-frame').toggleClass('active');


        var targetUrl = {
            url: $('.searcher').val()
        }

        $.ajax({
                url: '/direct',
                method: 'POST',
                data: targetUrl
        })
        .done(function(res) {
            $('.svg-container').html(res);
            $('.svg-container').toggleClass('active');
            $('.svg-container').scrollLeft($('.svg-container > svg').width() / 1.9);
        })
        .fail(function(err) {
            alert("Ajax request failed with error " + err);
        });

    });


});