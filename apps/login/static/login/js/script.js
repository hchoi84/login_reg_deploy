$("#first_name").keyup(function(){
    if ($(this).val() < 2){
        $("#first_name_error").html("Must be at least 2 characters")
    }
    else{
        $("#first_name_error").html("")
    }
})

$("#last_name").keyup(function(){
    if ($(this).val() < 2){
        $("#last_name_error").html("Must be at least 2 characters")
    }
    else{
        $("#last_name_error").html("")
    }
})

