import requests
import os

class Downloader:
    def __init__(self, url, output_path, progress_callback=None, chunk_size=8192):
        """
        :param url: File URL to download
        :param output_path: Local file path to save the downloaded content
        :param progress_callback: Function that receives progress float (0.0 to 1.0)
        :param chunk_size: Size of chunks to download at a time
        """
        self.url = url
        self.output_path = output_path
        self.progress_callback = progress_callback
        self.chunk_size = chunk_size

    def download(self):
        response = requests.get(self.url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        bytes_downloaded = 0

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(f"{self.output_path}.part", 'wb') as f:
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    f.write(chunk)
                    bytes_downloaded += len(chunk)
                    if self.progress_callback and total_size:
                        progress = bytes_downloaded / total_size
                        self.progress_callback(progress)
        os.rename(f"{self.output_path}.part", self.output_path)