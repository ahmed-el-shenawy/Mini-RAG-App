from core.config import settings
import os
class BaseController:
	def __init__(self) -> None:
		self.settings = settings
		# Get the absolute path to the 'src' directory (parent of 'controllers')
		self.src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
		self.files_path = os.path.join(self.src_path, 'assets', 'files')
