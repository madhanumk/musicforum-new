//Follow and unfollow
     $('.people_div').on('click','.follow_unfollow',function(){  
        event.preventDefault();    

        url = $(this).attr('data-url');
        id = $(this).attr('user_id');   

        $.ajax({
            url : url,                        
            success:function(output)
                {
                  if (output.followed)
                      {
                        $('.people_div .user_id_'+id).html('Following');  
                       

                        //home page my network
                        $('.people_div_home .user_id_'+id).removeClass('fa fa-user-check');  
                        $('.people_div_home .user_id_'+id).addClass('fa fa-user-minus');

                        count = $('#following').attr('count');
                        newCount = Number(count)+1;
                        $('#following').attr('count',newCount);
                        $('#following').html('&nbsp;'+newCount);

                        flwc = $('.people_div #user_id'+id).attr('count');
                        fnewCount = Number(flwc)+1;
                        $('.people_div #user_id'+id).attr('count',fnewCount);
                        $('.people_div #user_id'+id).html(fnewCount);


                        

                        
                      }
                  else{
                      $('.people_div .user_id_'+id).html('Follow'); ;
                      //home page my network

                     // $('.people_div_home .user_id_'+id).removeClass('fa fa-user-minus');
                     // $('.people_div_home .user_id_'+id).addClass('fa fa-user-check');

                      count = $('#following').attr('count');
                      newCount = Number(count)-1;
                      $('#following').attr('count',newCount);
                      $('#following').html('&nbsp;'+newCount);


                      flwc = $('.people_div #user_id'+id).attr('count');
                      fnewCount = Number(flwc)-1;
                      $('.people_div #user_id'+id).attr('count',fnewCount);
                      $('.people_div #user_id'+id).html(fnewCount);


                  }    
               },
        });
    });