import discord
from discord.ext.commands import Bot as BotBase

# Local code

import utils.json_loader
from utils.CustomContext import PacContext

secret_file = utils.json_loader.read_json("secrets")
class PacMe(BotBase):
	def __init__(self, **kwargs):
		super().__init__(
		command_prefix = "!*",
		owner_ids=secret_file["owner_ids"]		
		)
		self.empty_cache = {"prefix:" "!*"}