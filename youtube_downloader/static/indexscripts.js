document.addEventListener('DOMContentLoaded', function() {
    var fetchInfoButton = document.getElementById('fetch-info');
    var downloadButton = document.getElementById('download');
    var videoUrlInput = document.getElementById('video_url');
    var resolutionSelect = document.getElementById('resolution');
    var videoInfoDiv = document.getElementById('video-info');
    var titleElement = document.getElementById('video-title');
    var loadingDiv = document.getElementById('loading');
    var statusMessageDiv = document.getElementById('status-message');
    var downloadingMessageDiv = document.createElement('div'); // Yeni bir div oluştur
    downloadingMessageDiv.id = 'downloading-message';
    downloadingMessageDiv.style.display = 'none'; // Başlangıçta gizli
    document.body.appendChild(downloadingMessageDiv); // Sayfaya ekle

    if (fetchInfoButton && downloadButton && videoUrlInput && resolutionSelect && videoInfoDiv && titleElement && loadingDiv && statusMessageDiv && downloadingMessageDiv) {
        fetchInfoButton.addEventListener('click', function() {
            var videoUrl = videoUrlInput.value;
            if (videoUrl) {
                loadingDiv.textContent = 'Loading...'; // Get Video Info için "Loading..."
                loadingDiv.style.display = 'block';
                fetch(`/get_resolutions?video_url=${encodeURIComponent(videoUrl)}`)
                    .then(response => response.json())
                    .then(data => {
                        loadingDiv.style.display = 'none';
                        if (data.title && data.resolutions) {
                            titleElement.textContent = `Title: ${data.title}`;
                            resolutionSelect.innerHTML = '<option value="">Select a resolution</option>';
                            data.resolutions.forEach(function(resolution) {
                                var option = document.createElement('option');
                                option.value = resolution;
                                option.text = resolution + 'p';
                                resolutionSelect.add(option);
                            });
                            videoInfoDiv.style.display = 'block';
                        }
                    })
                    .catch(error => {
                        loadingDiv.style.display = 'none';
                        console.error('Error fetching resolutions:', error);
                    });
            }
        });

        downloadButton.addEventListener('click', function() {
            var videoUrl = videoUrlInput.value;
            var resolution = resolutionSelect.value;
            if (videoUrl && resolution) {
                loadingDiv.textContent = 'Downloading...'; // Download için "Downloading..."
                loadingDiv.style.display = 'block';
                var downloadUrl = `/download_video?video_url=${encodeURIComponent(videoUrl)}&resolution=${encodeURIComponent(resolution)}`;
                statusMessageDiv.style.display = 'none';  // Initially hide the status message
                downloadingMessageDiv.style.display = 'block'; // Download için "Downloading..." mesajını göster
                fetch(downloadUrl)
                    .then(response => response.json())
                    .then(data => {
                        downloadingMessageDiv.style.display = 'none'; // "Downloading..." mesajını gizle
                        loadingDiv.style.display = 'none'; // "Downloading..." mesajını gizle
                        if (data.success) {
                            statusMessageDiv.textContent = 'Download completed successfully.';
                            statusMessageDiv.style.textAlign = 'center'
                            statusMessageDiv.style.color = 'white'; // Başarı mesajını yeşil yap
                        } else {
                            statusMessageDiv.textContent = `Error: ${data.error}`;
                            statusMessageDiv.style.color = 'red'; // Hata mesajını kırmızı yap
                            statusMessageDiv.style.display = 'block';
                        }
                    })
                    .catch(error => {
                        downloadingMessageDiv.style.display = 'none'; // "Downloading..." mesajını gizle
                        statusMessageDiv.textContent = 'An error occurred during the download.';
                        statusMessageDiv.style.color = 'red'; // Hata mesajını kırmızı yap
                        statusMessageDiv.style.display = 'block';
                        console.error('Error during download:', error);
                    });
            } else {
                alert('Please select a resolution and enter a video URL.');
            }
        });
    } else {
        console.error('One or more DOM elements not found.');
    }
});
