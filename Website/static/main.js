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



// main.js


// main.js

    function performSearch(searchText) {
      var jobCards = document.getElementsByClassName("job-card");
      var noResultsMessage = document.getElementById("no-results-message");
      var hasResults = false;

      for (var i = 0; i < jobCards.length; i++) {
        var jobCard = jobCards[i];
        var companyName = jobCard.getElementsByClassName("company-name")[0].textContent.toLowerCase();
        var location = jobCard.getElementsByClassName("job-details")[0].textContent.toLowerCase();

        if (searchText === "" || companyName.includes(searchText) || location.includes(searchText)) {
          jobCard.style.display = "block";
          hasResults = true;
        } else {
          jobCard.style.display = "none";
        }
      }

      if (hasResults) {
        noResultsMessage.style.display = "none";
      } else {
        noResultsMessage.style.display = "block";
      }
    }

    document.getElementById("search-form").addEventListener("submit", function(event) {
      event.preventDefault();
      var searchText = document.getElementById("search-input").value.trim().toLowerCase();
      performSearch(searchText);
    });

    document.getElementById("search-input").addEventListener("input", function(event) {
      var searchText = event.target.value.trim().toLowerCase();
      performSearch(searchText);
    });
  