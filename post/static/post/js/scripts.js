$(document).ready(function() {
    $('.like-button').click(function() {
      var button = $(this);
      var postId = $(this).data('post-id');
      var liked = $(this).data('liked');
      if (postId) {
        url = '/insta/posts/' + postId + '/';
      } else {
        url = '/insta/';
      }
  
      // Send the AJAX request
      $.ajax({
        type: 'POST',
        url: url,
        data: {
          liked: liked,
          csrfmiddlewaretoken: '{{ csrf_token }}' // Add the CSRF token here
        },
        success: function(response) {
          // Update the button text and data-liked attribute
          if (response.liked) {
            button.text('Unlike');
            button.data('liked', true);
          } else {
            button.text('Like');
            button.data('liked', false);
          }
  
          // Update the like count
          var likesCountElement = $('#likesCount-' + postId);
          likesCountElement.text(response.count + ' Like' + (response.count !== 1 ? 's' : ''));
        },
        error: function(xhr, textStatus, errorThrown) {
          console.error(errorThrown);
          alert('An error occurred. Please try again later.');
        }
      });
    });
  });