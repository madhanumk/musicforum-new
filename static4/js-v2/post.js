




     //post like and unlike
     $('#post_div').on('click','.like_unlike',function(){  
        event.preventDefault();       
        url = $(this).attr('data-url');
        postId =  $(this).attr('id');
        id =  $(this).attr('post_id');      

        $.ajax({
            url : url,                        
            success:function(output)
                {
                  if (output.liked)
                      {                         
                        $('#'+postId).addClass('is-liked');  
                        $('#post_div .post_like_count_'+id).html(output.like_count);  
                        $('#post_div .post_like_count_words_'+id).html(output.like_count+ "  liked this");  
                      }
                  else{
                      $('.'+postId).removeClass('is-liked');
                      $('#post_div .post_like_count_'+id).html(output.like_count);  
                      $('#post_div .post_like_count_words_'+id).html(output.like_count+ "  liked this");  
                    }    
               },
        });
    });



  //delete comment
  $('#post_div').on('click','.delete_comment',function(){
    event.preventDefault();
      
      url = $(this).attr('data-url');
      commentId =  $(this).attr('comment_id');
      postId =  $(this).attr('post_id');
      
      if (confirm('Are you sure to delete your Comment?')) {
            $.ajax({
                url : url,                        
                success:function(output)
                    {
                    if (output.valid)
                        {                       
                            $('.post_comment_section_'+output.post_id).html(output.html);  
                            $('#post_div .post_comment_count2_'+postId).html(output.comment_count);
                            $('#post_div .post_comment_count_'+postId).html("("+output.comment_count+")");

                        }
                    else{
                            alert('Access Denied...!')
                        }    
                    },
            });
      }

  });
  
