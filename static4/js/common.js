$(".people_search_btn").click(function(){
    var name = $('#people_search_input').val();

    if (name.length == 0){
        
    }
    else{
        $('#search-form').submit();  
    }

});