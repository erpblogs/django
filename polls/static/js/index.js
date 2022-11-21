$(document).ready(function () {
    let number_of_record = 2
    let expand = false

    const settings = {
        "async": true, "crossDomain": true, "method": "GET", "headers": {
            "X-RapidAPI-Key": "ed7276993bmsh6ebcf60e623573bp197815jsn2d56512b9625",
            "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
        }, "url": "", beforeSend: function () {
            if (!expand) {
                $('#response_id').html(`<div class='loading'>Loading</div> `);
            }
        }, success: function (result) {
            let inputTxt = $('[name=input_txt]').val()
            $('#response_id').empty();

            if (!(result.list && result.list.length)) {
                $('#response_id').append("<strong>No data found!</strong>")
            } else {
                // $('.loading').hide();
                $('#clear_btn').show(); //removeClass("d-none");
                $('#response_id').append(`<p>Translate value for <strong>${inputTxt}</strong></p><p><ul class="list-group">`)
                $.each(result.list, function (key, value) {
                    if (!expand && key == number_of_record) {
                        return false;
                    }
                    $('#response_id').append(`<li class="list-group-item"><div><strong>${value.definition} </strong><br /> ${value.example}</div></li>`);
                })
                $('#response_id').append(`</ul></p>`)
            }
        },
    };

    function do_translate() {
        //$.ajax(settings).done();
        // $.ajax(settings)
        const requestUrl = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        let inputTxt = $('[name=input_txt]').val()
        settings["url"] = `${requestUrl}?term=${inputTxt}`
        //$(".expand").hide()

        /* this code using done method on ajax success
        $.ajax(settings).done(function (result) {
            $('#response_id').empty();
            if (!(result.list && result.list.length)) {
                $('#response_id').append("<strong>No data found!</strong>")
            } else {
                // $('.loading').hide();
                $('#clear_btn').show(); //removeClass("d-none");
                $('#response_id').append(`<p>Translate value for <strong>${inputTxt}</strong></p>`)
                $.each(result.list, function (key, value) {
                    $('#response_id').append(
                        `<p><strong>${value.definition} </strong><br /> ${value.example}</p>`
                    );
                })
            }
        });
         */

        // move event from done to ajax success event
        $.ajax(settings);

    }

    $("#translate_btn").click(function () {
        first_translate_request()
        do_translate()
    });
    /* multiple on event
    $("#clear_btn").on("click", () => $('#response_id').empty()).on("mouseup", function () {
        //$('#clear_btn').addClass("d-none")
        $('#clear_btn').hide();
    });

     */
    $("#clear_btn").on({
        "click": () => {
            $('#response_id').empty();
            $(".expand ").hide();
            $('[name=input_txt]').val('')
            //$(".expand span").slideToggle('slow'); //.hide();
        }
    });
    $(".expand").on({
        // get more item on expand clicked
        "click": function () {
            //var options = {
            //   opacity: 0.25, top: '100%', height: "toggle"
            //}

            expand = true
            $(this).hide();
            do_translate()

            // $(this).slideToggle('slow');
            //$(this).animate(options, 1000);
        }, /*
        "mouseenter": function () {
            $(this).hide();
        },
        "mouseout": function () {
            $(this).show();
        },
            */
    });


    let typingTimer;                //timer identifier
    let doneTypingInterval = 5000;  //time in ms (5 seconds)

    // function doneTyping() {
    //    alert("Do translate!")
    // }

    $('[name=input_txt]').on({
        /* this event will translate after input finished after typing interval
        'keyup': () => {
            return
            clearTimeout(typingTimer);
            if ($('[name=input_txt]').val()) {
               typingTimer = setTimeout(do_translate, doneTypingInterval);
            }

        },*/
        'keypress': function (event) {
            // this event do translate on enter press
            first_translate_request()
            clearTimeout(typingTimer);
            if (event.which === 13) {
                do_translate()
            }
        },
    });

    function first_translate_request() {
        $(".expand").show()
        expand = false
    }

});