$(document).ready(function () {
    // Function to get CSRF cookie value
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to handle both "nope" and "like" actions
    function handleAction(button, action) {
        // Get the user ID from the card (replace 'user-id' with the actual identifier in your HTML)
        var userId = button.closest(".card").data("user-id");

        // Get the dynamic URL
        var dynamicUrl = "{% url 'record_action' %}";

        // Send an AJAX request to record the action
        $.ajax({
            type: "POST",
            url: dynamicUrl, // Replace with the actual URL to handle the action
            data: {
                'user_id': userId,
                'action': action,
                'csrfmiddlewaretoken': getCookie('csrftoken')  // Include CSRF token here
            },
            success: function (data) {
                // Handle success if needed
                console.log("User action recorded successfully");
                // Remove the card from the DOM for "nope" action
                if (action === 'nope') {
                    button.closest(".card").remove();
                }
            },
            error: function (error) {
                // Handle error if needed
                console.error("Error recording user action", error);
            }
        });
    }

    // Click event for "nope" button
    $("#nope1").on("click", function () {
        handleAction($(this), 'nope');
    });

    // Click event for "like" button
    $("#love1").on("click", function () {
        handleAction($(this), 'like');
    });
});
