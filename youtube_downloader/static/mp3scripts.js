document.addEventListener('DOMContentLoaded', function() {
    var fetchAudioInfoButton = document.getElementById('fetch-audio-info');
    var downloadAudioButton = document.getElementById('download-audio');
    var audioUrlInput = document.getElementById('audio_url');
    var bitrateSelect = document.getElementById('bitrate');
    var audioInfoDiv = document.getElementById('audio-info');
    var titleElement = document.getElementById('audio-title');
    var loadingDiv = document.getElementById('loading');
    var statusMessageDiv = document.getElementById('status-message');
    var downloadingMessageDiv = document.getElementById('downloading-message'); // Eklenen div

    if (fetchAudioInfoButton && downloadAudioButton && audioUrlInput && bitrateSelect && audioInfoDiv && titleElement && loadingDiv && statusMessageDiv && downloadingMessageDiv) {
        fetchAudioInfoButton.addEventListener('click', function() {
            var audioUrl = audioUrlInput.value;
            if (audioUrl) {
                loadingDiv.style.display = 'block';
                fetch(`/get_audio_info?video_url=${encodeURIComponent(audioUrl)}`)
                    .then(response => response.json())
                    .then(data => {
                        loadingDiv.style.display = 'none';
                        if (data.title) {
                            titleElement.textContent = `Title: ${data.title}`;
                            audioInfoDiv.style.display = 'block';
                        }
                    })
                    .catch(error => {
                        loadingDiv.style.display = 'none';
                        console.error('Error fetching audio info:', error);
                    });
            }
        });

        downloadAudioButton.addEventListener('click', function() {
            var audioUrl = audioUrlInput.value;
            var bitrate = bitrateSelect.value;
            if (audioUrl && bitrate) {
                var downloadUrl = `/download_audio?video_url=${encodeURIComponent(audioUrl)}&bitrate=${encodeURIComponent(bitrate)}`;
                statusMessageDiv.style.display = 'none';  // Initially hide the status message
                loadingDiv.style.display = 'none'; // Hide loading for the fetch
                downloadingMessageDiv.style.display = 'block'; // Download için "Downloading..." mesajını göster
                fetch(downloadUrl)
                    .then(response => response.json())
                    .then(data => {
                        downloadingMessageDiv.style.display = 'none'; // "Downloading..." mesajını gizle
                        if (data.success) {
                            statusMessageDiv.textContent = 'Download completed successfully.';
                            statusMessageDiv.style.display = 'block';
                            statusMessageDiv.style.color = 'green';
                        } else {
                            statusMessageDiv.textContent = `Error: ${data.error}`;
                            statusMessageDiv.style.display = 'block';
                        }
                    })
                    .catch(error => {
                        downloadingMessageDiv.style.display = 'none'; // "Downloading..." mesajını gizle
                        statusMessageDiv.textContent = 'An error occurred during the download.';
                        statusMessageDiv.style.display = 'block';
                        console.error('Error during download:', error);
                    });
            } else {
                alert('Please select a bitrate and enter a video URL.');
            }
        });
    } else {
        console.error('One or more DOM elements not found.');
    }
});
