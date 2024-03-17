/*
This background script is responsible for communicating with the content script and controlling the YouTube video playback in response to user actions.

It listens for messages from the content script and executes appropriate actions based on the received message.

The script maintains an array of start times extracted from the HTML content of the search result page.

It provides functions to move the video pointer forward, backward, and to a specific start time.
*/

// To Check if the Background Script is loaded or not
console.log('Background script loaded');

let startTimes = [];

// Pointer to track current position in startTimes array
let pointer = 0;  


// Listener for messages from content script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.video_id && message.sentence) {
    console.log('Video ID:', message.video_id);
    // Sending POST request to search_sentence endpoint (Flask App On Local Host) with video_id and sentence
    fetch(`http://localhost:5000/search_sentence`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `video_id=${message.video_id}&search-sentence=${message.sentence}` 
    })
    .then(response => response.text())
    .then(htmlContent => {
    // Extracting start times from HTML content
      startTimes = extractStartTimes(htmlContent);
      console.log('Extracted start times:', startTimes);
    
    // Moving video pointer to the first start time if available
      if (startTimes.length > 0) {
        pointer = 0;
        console.log('Moving video pointer to:', startTimes[0]);
        moveVideoPointer(startTimes[0]);
      } else {
        console.error('No start times found');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
    return true;
  }
});

// Listener for messages from content script to move video playback
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log('Message received:', message);
    if (message.action === 'move_forward') {
      moveForward();
    } else if (message.action === 'move_backward') {
      moveBackward();
    }
  });



// Function to move video pointer to a specific start time
function moveVideoPointer(startTime) {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const videoId = tabs[0].url.match(/[?&]v=([^&]+)/)[1];
    const newUrl = `https://www.youtube.com/watch?v=${videoId}&t=${startTime}`;
    chrome.tabs.update(tabs[0].id, { url: newUrl }); // Update tab URL
  });
}

// Move Pointer Forward
function moveForward() {
  if (pointer < 6) {
    pointer++;
    moveVideoPointer(startTimes[pointer]);
} else {
        pointer = -1;
    }
}

// Move Pointer Backward
function moveBackward() {
  if (pointer > 0) {
    pointer--;
    moveVideoPointer(startTimes[pointer]);
} else {
        pointer = 7;
    }
}


// Function to extract start times from HTML content
function extractStartTimes(htmlContent) {
  const startTimesRegex = /var\s+start_times\s*=\s*\[([^\]]+)\]/;
  const match = htmlContent.match(startTimesRegex);
  if (match && match[1]) {
    const startTimesString = match[1];
    const startTimes = startTimesString.split(',').map(time => parseInt(time.trim(), 10));
    return startTimes;
  } else {
    console.error('start_times array not found in HTML content');
    return [];
  }
}