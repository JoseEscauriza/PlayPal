// The idea was when pressed like button go to record_action view, saved to DB and don't reload the page
// when pressed nope button go to record_action view, saved to DB as disliked and remove the card
//(or reload the page, in swiping views just add check if card is in disliked then don't display it )
// Problems:  record_action is not being accessed and and not working at all:)
// What i did: added record_action view, added js, made url in user urls.py, directly in swiping.html added vars
//<div id="recordAction" data-url="{% url 'record_action' %}"></div>
//<div id="swipingUrl" data-url="{% url 'swiping' %}"></div>
// while i couldn't access them directly from js using {% url %}.

$(document).ready(function () {
    // Function to handle both "nope" and "like" actions
    function handleAction(button, action) {
        // Get the user ID from the card (replace 'user-id' with the actual identifier in your HTML)
        var userId = button.closest(".card").data("user-id");

        // Get the dynamic URL
        var dynamicUrl = $("#recordAction").data("url");

        // Get the CSRF token directly from the csrfmiddlewaretoken input field
        var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        // Send an AJAX request to record the action
        $.ajax({
            type: "POST",
            url: dynamicUrl,
            data: {
                'user_id': userId,
                'action': action,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (data) {
                // Handle success if needed
                console.log("User action recorded successfully");

                // Remove the card from the DOM for "nope" action
                if (action === 'nope') {
                    button.closest(".card").remove();
                } else if (action === 'like') {
                    // Optionally handle 'like' action, if needed
                    // For example, display a message or update UI
                }

                // Reload the swiping view after removing the card or recording a "like" action
                window.location.href = $("#swipingUrl").data("url");
            },
            error: function (error) {
                // Handle error if needed
                console.error("Error recording user action", error);
            }
        });
    }

    // Click event for "nope" button
    $("#nope1").on("click", function (event) {
        // Prevent the default form submission behavior
        event.preventDefault();
        console.log("Nope button clicked");

        handleAction($(this), 'nope');
    });

    // Click event for "like" button
    $("#love1").on("click", function (event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        console.log("Love button clicked");
        handleAction($(this), 'like');
    });
});
