function generate_diff() {
    var ref_a = $('#ref_a').val();
    var ref_b = $('#ref_b').val();
    $.get("/generate",
          {ref_a: ref_a, ref_b: ref_b},
          function( data ) {
            $("#diff_contents").html( data );
    });

    var uri = new URI(window.location.href);
    uri.query({ref_a:ref_a, ref_b:ref_b});

    history.pushState(null, null, uri.toString());
}


function refresh_repo() {
    var refresh = $("#refresh_repo_icon");
    if (!refresh.hasClass("fa-spin")) {
        refresh.addClass("fa-spin");
    }
    $.get("/refresh",
        {},
        function( data ) {
            setTimeout(function() {
                if (refresh.hasClass("fa-spin")) {
                    refresh.removeClass("fa-spin");
                }
            }, 300);
        });
}


function update_branch_autocomplete() {
    $.get('/branches', function(data){
        $('#ref_a').typeahead({ source:data });
        $('#ref_b').typeahead({ source:data });
    },'json');
}


function read_url_refs() {
        $.urlParam = function(name){
            var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
            if (results === null){
               return null;
            }
            else{
               return results[1] || 0;
            }
        }

        var ref_a = $.urlParam('ref_a');
        var ref_b = $.urlParam('ref_b');

        if (ref_a !== null && ref_b !== null) {
            $('#ref_a').val(ref_a);
            $('#ref_b').val(ref_b);

            generate_diff();
        }
}