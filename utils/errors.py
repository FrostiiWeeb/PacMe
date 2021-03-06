from discord.ext import commands

# Base Error	
						
class ArgumentBaseError(commands.UserInputError):
    def __init__(self, converter=None, **kwargs):
        super().__init__(**kwargs)
        self.converter = converter  	
        
# Making the custom errors.

class MustMember(ArgumentBaseError):
    def __init__(self, _id, **kwargs):
        super().__init__(message=f"{_id} must be in the server.", **kwargs)
        
class NotFound(ArgumentBaseError):
	def __init__(self, _id, **kwargs):
		super().__init__(message=f"{_id} was not found.", **kwargs)
		print(f"{_id} was not found.", **kwargs)
		
class InvalidTime(ArgumentBaseError):
	def __init__(self, _id, **kwargs):
		super().__init__(message=f"{_id} is an invalid arg.", **kwargs)
		print(f"{_id} was not found.", **kwargs)

class NotInDB(ArgumentBaseError):
	def __init__(self, _id, **kwargs):
		super().__init__(message=f"{_id} is not in the database.", **kwargs)		