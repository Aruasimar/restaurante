$(document).ready(function () {
    /* $('#cards :checkbox').change(function () {
        if ($(this).is(':checked')) {
            $('.card').hide();
            seleccionado = $(this).val();
            if ($(this).prop("id") == "entradas") {
                $(".entrada").show("slow")
            }

            if ($(this).prop("id") == "Pfuertes") {
                $(".fuerte").show("slow")
            }

            if ($(this).prop("id") == "postres") {
                $(".postre").show("slow")
            }

        } else {
            $('.card').show("slow");
        }
    }); */

    $('input[type=checkbox]').on('change', function () {
        $('.card').hide();
        var n = $( "input:checked" ).length;
        $('input[type=checkbox]:checked').each(function() {

            if ($(this).prop("id") == "entradas") {
                $(".entrada").show("slow")
            }
            
            if ($(this).prop("id") == "Pfuertes") {
                $('.card').hide();
                $(".fuerte").show("slow")
            }
            
            if ($(this).prop("id") == "postres") {
                $('.card').hide();
                $(".postre").show("slow")
            }
            
        });

        if (n==0) {
            $(".card").show("slow")
        }
    });
})