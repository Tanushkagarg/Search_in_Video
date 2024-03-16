// Declaring all the constants
const video = document.getElementById('video');
const loadingDiv = document.getElementById('loading');
const uploadForm = document.getElementById('upload-form');
const changeSpeedBtn = document.getElementById('changeSpeedBtn');
const setMediaCursorBtn = document.getElementById('setMediaCursorBtn');
const searchform = document.getElementById('sf');
let mediaPlaying = false;

// Terminating the previous media when user uploads new media
function stopMedia() {
    if (mediaPlaying) {
        video.pause();
        video.currentTime = 0;
        mediaPlaying = false;
    }
}

// Function to change the speed of the media 
function changeSpeed() {
    const speed = prompt('Enter speed (0.5 to 2.0):');
    if (speed !== null) {
        video.playbackRate = parseFloat(speed);
    }
}


// Function to set the cursor to the entered time stamp in the format [hh:mm:ss]
function setMediaCursor() {
    // Prompting the user about the format of the time stamp while input
    const timestamp = prompt('Enter timestamp (hh:mm:ss):');
    if (timestamp !== null) {
        // Getting the value of hours, minutes, and seconds by splitting on ':'
        const timeComponents = timestamp.split(':');
        // Checking if user has entered the time stamp in correct format
        if (timeComponents.length === 3) {
            const hours = parseInt(timeComponents[0]);
            const minutes = parseInt(timeComponents[1]);
            const seconds = parseInt(timeComponents[2]);

            // Converting the entered time stamp to seconds for easy movement of the cursor
            const totalSeconds = hours * 3600 + minutes * 60 + seconds;

            // Setting the cursor to the user input time stamp for video file
            // Also checking if the entered time stamp in seconds is less than the total duration of media 
            if (totalSeconds <= video.duration) {
                video.currentTime = totalSeconds;
            } else {
                alert('Invalid timestamp. Exceeds media duration.');
            }
        } else {
            alert('Invalid timestamp format.');
        }
    }
}

// Listening to submit button
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    stopMedia();
    loadingDiv.style.display = 'block';
    const formData = new FormData(e.target);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    
    // Checking if the uploaded file is Video and accordingly displaying
    const filename = await response.text();
    if (
        filename.toLowerCase().endsWith('.mp4') ||
        filename.toLowerCase().endsWith('.avi') ||
        filename.toLowerCase().endsWith('.mkv') ||
        filename.toLowerCase().endsWith('.mov')
    ) {
        video.src = `/play/${filename}`;
        video.style.display = 'block';
         // Event listener to check when metadata has loaded (including duration)
         video.addEventListener('loadedmetadata', () => {
            // Once metadata is loaded, start playing
            video.play();

            // Check playback progress
            video.addEventListener('timeupdate', () => {
                // Displaying "Change Speed" and "Set Media Cursor" buttons when video is playing
                changeSpeedBtn.style.display = 'inline-block';
                setMediaCursorBtn.style.display = 'inline-block';
                searchform.style.display = 'block';
                loadingDiv.style.display = 'none';
                mediaPlaying = true;
            });
        });
    }
     else {
        alert('Invalid file format. Please upload a video file.');
    }
});
