from core.config import settings

class BaseController:
	def __init__(self) -> None:
		self.settings = settings
