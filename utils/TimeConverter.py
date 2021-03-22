from contextlib import redirect_stdout
from datetime import datetime as dt
from discord.ext import commands
from typing import NamedTuple
import subprocess
import functools
import datetime
import textwrap
import humanize
import asyncio
import discord
import string
from utils.CustomContext import PacContext
import io
import re
from utils.errors import InvalidTime




class TimeConverter(commands.Converter):
    def convert(self, time):
    	pos = ['s', 'm', 'h', 'd', 'w', 'y']
    	
    	time_dict = {'s': 0, 'm': 60, 'h': 3600, 'd': 8600, 'w': 604800, 'y': 31557600}
    	
    	if str(time).endswith not in pos:
    		return commands.BadArgument("Cannot convert `{}` as it is not valid.")
    	result = pos[str(time.endswith)] * time_dict[str(pos.endswith)]
    	return int(result)