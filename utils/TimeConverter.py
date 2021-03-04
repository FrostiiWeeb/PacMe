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
    	
    	time_dict = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, "w": 604800, 'y': 31557600}
    	
    	unit = time[-1]
    	
    	if unit not in pos:
    		raise InvalidTime(time)    		
    		return -1
    	try:
    		val = int(time[:-1])
    	except:
    		return -2
    	
    	return val * time_dict[unit]


		
