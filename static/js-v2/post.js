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
                // Select the element by ID and class
                var element = document.querySelector('#post_div .' + postId);

                // Check if the element exists before removing its content
                if (element) {
                    element.innerHTML = '';
                }

                
                if (output.liked)
                    {                        
                        $('#post_div .post_svg_'+id).addClass('social-count-active');
                        $('#post_div .'+postId).html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-heart"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>');
                        $('#post_div .post_like_count_'+id).html(output.like_count);  
                        $('#post_div .post_like_count_words_'+id).html(output.like_count+ "  liked this");  
                    }
                else{
                    $('#post_div .post_svg_'+id).removeClass('social-count-active');
                    $('#post_div .'+postId).html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-heart"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>');
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
  
