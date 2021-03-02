from discord.ext import commands
		
class ArgumentBaseError(commands.UserInputError):
    def __init__(self, converter=None, **kwargs):
        super().__init__(**kwargs)
        self.converter = converter  	

class MustMember(ArgumentBaseError):
    def __init__(self, _id, **kwargs):
        super().__init__(message=f"{_id} must be in the server.", **kwargs)
        
class NotFound(ArgumentBaseError):
	def __init__(self, _id, **kwargs):
		super().__init__(message=f"{_id} was not found.", **kwargs)
		print(f"{_id} was not found.", **kwargs)