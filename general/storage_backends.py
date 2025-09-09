import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class PrivateMediaStorage(FileSystemStorage):
    """
    Simple storage backend for private media files.
    In production, this should be replaced with proper cloud storage.
    """

    def __init__(self, location=None, base_url=None):
        if location is None:
            location = os.path.join(settings.BASE_DIR, "private_media")
        if base_url is None:
            base_url = "/private_media/"
        super().__init__(location, base_url)

    def _save(self, name, content):
        # Ensure directory exists
        full_path = self.path(name)
        directory = os.path.dirname(full_path)
        os.makedirs(directory, exist_ok=True)
        return super()._save(name, content)
