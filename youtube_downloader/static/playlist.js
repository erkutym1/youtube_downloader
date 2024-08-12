document.addEventListener('DOMContentLoaded', function() {
    var fetchPlaylistInfoButton = document.getElementById('fetch-playlist-info');
    var downloadPlaylistButton = document.getElementById('download-playlist');
    var playlistUrlInput = document.getElementById('playlist_url');
    var downloadTypeSelect = document.getElementById('download-type');
    var resolutionSelect = document.getElementById('resolution');
    var playlistInfoDiv = document.getElementById('playlist-info');
    var titleElement = document.getElementById('playlist-title');
    var loadingDiv = document.getElementById('loading');
    var downloadingMessageDiv = document.getElementById('downloading-message');
    var statusMessageDiv = document.getElementById('status-message');

    if (fetchPlaylistInfoButton && downloadPlaylistButton && playlistUrlInput && downloadTypeSelect && resolutionSelect && playlistInfoDiv && titleElement && loadingDiv && downloadingMessageDiv && statusMessageDiv) {
        fetchPlaylistInfoButton.addEventListener('click', function() {
            var playlistUrl = playlistUrlInput.value;
            if (playlistUrl) {
                loadingDiv.style.display = 'block';
                fetch(`/get_playlist_info?playlist_url=${encodeURIComponent(playlistUrl)}`)
                    .then(response => response.json())
                    .then(data => {
                        loadingDiv.style.display = 'none';
                        if (data.title) {
                            titleElement.textContent = `Playlist: ${data.title}`;
                            playlistInfoDiv.style.display = 'block';
                        }
                    })
                    .catch(error => {
                        loadingDiv.style.display = 'none';
                        console.error('Error fetching playlist info:', error);
                    });
            }
        });

        downloadTypeSelect.addEventListener('change', function() {
            var downloadType = downloadTypeSelect.value;
            if (downloadType === 'video') {
                resolutionSelect.style.display = 'block';
            } else {
                resolutionSelect.style.display = 'none';
            }
        });

        downloadPlaylistButton.addEventListener('click', function() {
            var playlistUrl = playlistUrlInput.value;
            var downloadType = downloadTypeSelect.value;
            var resolution = resolutionSelect.value;

            if (playlistUrl && downloadType) {
                var downloadUrl = `/download_playlist?playlist_url=${encodeURIComponent(playlistUrl)}&type=${encodeURIComponent(downloadType)}&resolution=${encodeURIComponent(resolution)}`;
                statusMessageDiv.style.display = 'none';
                downloadingMessageDiv.style.display = 'block';
                fetch(downloadUrl)
                    .then(response => response.json())
                    .then(data => {
                        downloadingMessageDiv.style.display = 'none';
                        if (data.success) {
                            statusMessageDiv.textContent = 'Download completed successfully.';
                            statusMessageDiv.style.color = 'green';
                            statusMessageDiv.style.display = 'block';
                            statusMessageDiv.style.textAlign = 'center';
                        } else {
                            statusMessageDiv.textContent = `Error: ${data.error}`;
                            statusMessageDiv.style.display = 'block';
                        }
                    })
                    .catch(error => {
                        downloadingMessageDiv.style.display = 'none';
                        statusMessageDiv.textContent = 'An error occurred during the download.';
                        statusMessageDiv.style.display = 'block';
                        console.error('Error during download:', error);
                    });
            } else {
                alert('Please select a download type and enter a playlist URL.');
            }
        });
    } else {
        console.error('One or more DOM elements not found.');
    }
});
