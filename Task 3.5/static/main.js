// Declaring all the constants and getting data from index.html file
const audio = document.getElementById('audio');
const video = document.getElementById('video');
const loadingDiv = document.getElementById('loading');
const uploadForm = document.getElementById('upload-form');
const mediaTypeSelect = document.getElementById('media-type');
let currentMediaType = 'audio';
let mediaPlaying = false;

// Terminating the previous media when user uploads new media
function stopMedia() {
    if (mediaPlaying) {
        if (currentMediaType === 'audio') {
            audio.pause();
            audio.currentTime = 0;
        } else if (currentMediaType === 'video') {
            video.pause();
            video.currentTime = 0;
        }
        mediaPlaying = false;
    }
}

// Function to change the speed of the media 
function changeSpeed() {
    const speed = prompt('Enter speed (0.5 to 2.0):');
    if (speed !== null) {
        if (currentMediaType === 'audio') {
            audio.playbackRate = parseFloat(speed);
        } else if (currentMediaType === 'video') {
            video.playbackRate = parseFloat(speed);
        }
    }
}

// Function to set the cursor to the entered time stamp in the format [hh:mm:ss]
function setMediaCursor() {
    // Prompting the user about the format of the time stamp while input
    const timestamp = prompt('Enter timestamp (hh:mm:ss):');
    if (timestamp !== null) {
        // Getting the value of hours, minutes and seconds by splitting on ':'
        const timeComponents = timestamp.split(':');
        // Checking if user has entered the time stamp in correct format
        if (timeComponents.length === 3) {
            const hours = parseInt(timeComponents[0]);
            const minutes = parseInt(timeComponents[1]);
            const seconds = parseInt(timeComponents[2]);

            // Converting the entered time stamp to seconds for easy movement of the cursor
            const totalSeconds = hours * 3600 + minutes * 60 + seconds;

            // Setting the cursor to the user input time stamp for audio file as well as video file
            // Also checking if the entered time stamp in seconds is less than the total duration of media 
            if (currentMediaType === 'audio' && totalSeconds <= audio.duration) {
                audio.currentTime = totalSeconds;
            } else if (currentMediaType === 'video' && totalSeconds <= video.duration) {
                video.currentTime = totalSeconds;
            } else {
                alert('Invalid timestamp. Exceeds media duration.');
            }
        } else {
            alert('Invalid timestamp format.');
        }
    }
}

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    stopMedia();
    loadingDiv.style.display = 'block';
    const formData = new FormData(e.target);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    
    // Checking if the uploaded file is Audio or Video and accordingly displaying
    const filename = await response.text();
    if (filename.toLowerCase().endsWith('.mp3') || filename.toLowerCase().endsWith('.wav')) {
        audio.src = `/play/${filename}`;
        audio.style.display = 'block';
        video.style.display = 'none';
        currentMediaType = 'audio';
    } else if (
        filename.toLowerCase().endsWith('.mp4') ||
        filename.toLowerCase().endsWith('.avi') ||
        filename.toLowerCase().endsWith('.mkv') ||
        filename.toLowerCase().endsWith('.mov')
    ) {
        video.src = `/play/${filename}`;
        video.style.display = 'block';
        audio.style.display = 'none';
        currentMediaType = 'video';
    }

    // Event listener to check when metadata has loaded (including duration)
    if (currentMediaType === 'audio') {
        audio.addEventListener('loadedmetadata', () => {
            // Once metadata is loaded, start playing
            audio.play();

            // Check playback progress
            audio.addEventListener('timeupdate', () => {
                // Assuming 0.1 second as a sufficient duration to consider media "playing"
                // Displaying Uploading status till 0.1 second
                if (audio.currentTime > 0.1) {
                    loadingDiv.style.display = 'none';
                    mediaPlaying = true;
                }
            });
        });
    } else if (currentMediaType === 'video') {
        video.addEventListener('loadedmetadata', () => {
            // Once metadata is loaded, start playing
            video.play();

            // Check playback progress
            video.addEventListener('timeupdate', () => {
                // Assuming 0.1 second as a sufficient duration to consider media "playing"
                // Displaying Uploading status till 0.1 second
                if (video.currentTime > 0.1) {
                    loadingDiv.style.display = 'none';
                    mediaPlaying = true;
                }
            });
        });
    }
});


