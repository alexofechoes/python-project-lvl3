# -*- coding:utf-8 -*-
"""Savers module."""

import os


class FileSaver:
    """FileSaver use with file system."""

    def save(self, content_for_save: bytes, path_to_save: str):
        """Save content to file."""
        mode = 'w' if isinstance(content_for_save, str) else 'wb'
        with open(path_to_save, mode) as file_descriptor:
            file_descriptor.write(content_for_save)

    def create_dir(self, path_to_dir: str):
        """Create dir if dit is not exists."""
        if not os.path.exists(path_to_dir):
            os.mkdir(path_to_dir)
