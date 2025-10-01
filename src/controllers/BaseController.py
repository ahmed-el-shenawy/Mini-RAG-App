from core.config import Settings, settings
from typing import LiteralString
import os
import random
import string


class BaseController:

    def __init__(self) -> None:
        # global settings
        self.settings: Settings = settings
        # Define paths
        self.src_path: str = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        self.files_path: str = os.path.join(self.src_path, "assets", "files")

    # Generate a random string
    def generate_random_string(self, length=12):
        """Generate a random string of fixed length."""
        letters: LiteralString = string.ascii_letters + string.digits
        return "".join(random.choice(letters) for i in range(length))
