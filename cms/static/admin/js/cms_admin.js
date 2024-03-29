hide = false;
django.jQuery(document).ready(function(){
    if (django.jQuery("#id_root").is(":checked")) {
        django.jQuery(".parent").hide();
        django.jQuery(".content").hide();
        django.jQuery(".url").hide();
        django.jQuery(".template").hide();
        hide = true;
    } else {
        django.jQuery(".parent").show();
        django.jQuery(".content").show();
        django.jQuery(".url").show();
        django.jQuery(".template").show();
        hide = false;
    }
    django.jQuery("#id_root").click(function(){
        hide =! hide;
        if (hide) {
            django.jQuery(".parent").hide();
            django.jQuery(".content").hide();
            django.jQuery(".url").hide();
            django.jQuery(".template").hide();
        } else {
            django.jQuery(".parent").show();
            django.jQuery(".content").show();
            django.jQuery(".url").show();
            django.jQuery(".template").show();
        }
    })
    if (django.jQuery("#id_parent").val()) {
        django.jQuery(".menu").hide();
        django.jQuery(".root").hide();
    }
    django.jQuery("#id_parent").change(function() {
        if (!django.jQuery(this).val()) {
            django.jQuery(".menu").show();
            django.jQuery(".root").show();
        } else {
            django.jQuery(".menu").find('select option:first').prop('selected', true);
            django.jQuery(".menu").hide();
            django.jQuery(".root").hide();
        }
    })
})

