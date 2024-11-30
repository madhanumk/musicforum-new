

 //Report People
 $('.people_div').on('click','.report_people',function(){  
    //event.preventDefault();     
    url = $(this).attr('data-url');
    $.ajax({
        url : url,                        
        success:function(output)
            {
                $('.popup-content').html(output.form);  
                $("#add-edit-modal").addClass("is-active"); 
                $("#add-edit-modal #model-title").html("Report - " + output.people);   
           },
    });
});


//Ajax update Award
$('#add-edit-modal').on('click','.report_people_btn', function(){
    event.preventDefault();
    formdata = new FormData($('#add-edit-modal #ajax_form')[0]);
    url = $(this).attr('data-url');
    complaint = $('#id_complaint').val();
    report_file = $('#id_report_file').val();

    if( complaint || report_file ){

      $.ajax({
        url : url,
        data : formdata,
        method: 'post',
        processData: false,
        contentType: false,
        beforeSend:function()
        {
            $('#AjaxModal #info_text').text('Please Wait');
            
        },
        
        success:function(output)
        {
            if(output.valid)
            {
                alert('Successfully  Reported..');
                $("#add-edit-modal").removeClass("is-active"); 

            }
            else
            {
                $('..popup-content').html(output.form);
            }
            $('#AjaxModal #info_text').text('');
        },
    });

    }
    else{

      alert('Complete all of the essential fields.');

    }

});
