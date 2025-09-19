from core.config import settings
import os
import random
import string

class BaseController:
	def __init__(self) -> None:
		self.settings = settings
		# Get the absolute path to the 'src' directory (parent of 'controllers')
		self.src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
		self.files_path = os.path.join(self.src_path, 'assets', 'files')
	def generate_random_string(self, length=12):
		"""Generate a random string of fixed length."""
		letters = string.ascii_letters + string.digits
		return ''.join(random.choice(letters) for i in range(length))
