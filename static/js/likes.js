function postLikeSubmit(event, post_id){
	event.preventDefault();
	const form_action = document.getElementById('post-like-form-' + post_id).action

	$.ajaxSetup({
	        headers: {
	           "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
	                   }
	            });
	$.ajax({
		url: form_action,
		type: "POST",
		dataType: "JSON",
		data: {
			'post_id': post_id
		},

		success: function(response){
			likeCounterId = 'likes-counter-' + post_id		
			document.getElementById(likeCounterId).innerText = response['likes_count']
		}
	})
}


function commentLikeSubmit(event, comment_id){
	event.preventDefault();
	const form_action = document.getElementById('comment-like-form-' + comment_id).action

	$.ajaxSetup({
	        headers: {
	           "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
	                   }
	            });
	$.ajax({
		url: form_action,
		type: "POST",
		dataType: "JSON",
		data: {
			'comment_id': comment_id
		},

		success: function(response){
			likeCounterId = 'comments-counter-' + comment_id		
			document.getElementById(likeCounterId).innerText = response['likes_count']
		}
	})
}