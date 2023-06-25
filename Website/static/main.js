$(document).ready(function() {
    var isOpen = false;

    // Toggle chat body when the chat header is clicked
    $('.chat-header').on('click', function() {
        $('.chat-body').slideToggle();
        isOpen = !isOpen;
    });

    // Send message to the chatbot when the user submits the form
    $('form').on('submit', function(event) {
        event.preventDefault();
        var userMessage = $('#user-message').val();
        sendMessage(userMessage);
    });

    function sendMessage(message) {
        // Display user message in the chat interface
        $('#chat-log').append('<div class="user-message">' + message + '</div>');

        // Send AJAX request to the /chat route
        $.ajax({
            type: 'POST',
            url: '/chat',
            data: {user_message: message},
            success: function(response) {
                // Display chatbot response in the chat interface
                $('#chat-log').append('<div class="chatbot-message">' + response + '</div>');
                scrollChatToBottom(); // Scroll to the bottom after receiving a response
            },
            error: function(error) {
                console.log(error);
            }
        });

        // Clear the input field
        $('#user-message').val('');

        // If the chat is closed, open it automatically after sending a message
        if (!isOpen) {
            $('.chat-body').slideDown();
            isOpen = true;
        }
    }

    function scrollChatToBottom() {
        var chatBody = $('.chat-body');
        chatBody.scrollTop(chatBody[0].scrollHeight);
    }
});
