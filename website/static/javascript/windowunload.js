window.addEventListener('beforeunload', function() {
    // Make an AJAX request to Django when the window loses focus
    $.ajax({
        url: "{% url 'window_blur_method' temp_url %}",  // The Django URL to trigger the method
        type: 'POST',  // Use POST if you're modifying server-side data
        data: {
            'csrfmiddlewaretoken': '{{ csrf_token }}',  // CSRF token for security
            'message': 'Window Closed'  // Optional data you can send to the server
        },
        success: function(response) {
            console.log("Django method triggered successfully!");
        },
        error: function(xhr, status, error) {
            console.error("Error in AJAX request", error);
        }
    });
});