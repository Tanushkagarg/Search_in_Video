/*
This content script is responsible for handling user interactions on the browser extension popup.

It listens for the DOMContentLoaded event to ensure the popup HTML is fully loaded before attaching event listeners to elements.

It provides functionality to perform a search action when the search button is clicked and to navigate backward and forward through the video transcript when the corresponding buttons are clicked.

*/



document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');
    const resultsDiv = document.getElementById('results');
  
    searchButton.addEventListener('click', function() {
    // Extracting search sentence from input field
      const sentence = searchInput.value.trim();
      if (sentence !== '') {
        // Querying active tab to get current YouTube video ID
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          const currentTab = tabs[0];
          const youtubeRegex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
          const match = currentTab.url.match(youtubeRegex);
          if (match) {
            const videoId = match[1];
            console.log('Video ID:', videoId);
            // Sending message to background script with video ID and search sentence
            chrome.runtime.sendMessage({ video_id: videoId, sentence: sentence }, function(response) {
              const startTimes = response.start_times;
              console.log('Received start times:', startTimes);
              if (startTimes && startTimes.length > 0) {
                const firstStartTime = startTimes[0];
                console.log('First start time:', firstStartTime);
              } else {
                console.error('No start times found in response');
              }
            });
          } else {
            console.error('No YouTube video found in the current tab.');
          }
        });
      }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');

 // Adding event listeners to navigation buttons [Move to next or prev time stamp]

    prevButton.addEventListener('click', function() {
        console.log('Sending move_backward message');
        chrome.runtime.sendMessage({ action: 'move_backward' });
    });

    nextButton.addEventListener('click', function() {
        console.log('Sending move_forward message');
        chrome.runtime.sendMessage({ action: 'move_forward' });
    });
});

  




  
  