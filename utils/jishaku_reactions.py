# Credit to Stella

import contextlib
import io
import os
import jishaku.shell
import jishaku.paginators
import jishaku.exception_handling
import jishaku.repl.compilation
import discord
import pathlib
import sys
import asyncio
import subprocess
import re
import inspect
from jishaku.functools import AsyncSender
from typing import Union
from collections import namedtuple

EmojiSettings = namedtuple('EmojiSettings', 'start back forward end close')


class FakeEmote(discord.PartialEmoji):
    """
    Due to the nature of jishaku checking if an emoji object is the reaction, passing raw str into it will not work.
    Creating a PartialEmoji object is needed instead.
    """
    @classmethod
    def from_name(cls, name):
        emoji_name = re.sub("|<|>", "", name)
        a, name, id = emoji_name.split(":")
        return cls(name=name, id=int(id), animated=bool(a))


emote = EmojiSettings(
    start=FakeEmote.from_name("<:purple_stop_button:821290308766924812>"),
    back=FakeEmote.from_name("<:emoji_6:821299409316347904>"),
    forward=FakeEmote.from_name("<:emoji_5:821298149371936809>"),
    end=FakeEmote.from_name("<:emoji_4:821298104133091348>"),
    close=FakeEmote.from_name("<:purple_stop_button:821290308766924812>")
)
jishaku.paginators.EMOJI_DEFAULT = emote  # Overrides jishaku emojis


async def attempt_add_reaction(msg: discord.Message, reaction: Union[str, discord.Emoji]):
    """
    This is responsible for every add reaction happening in jishaku. Instead of replacing each emoji that it uses in
    the source code, it will try to find the corresponding emoji that is being used instead.
    """
    reacts = {
        "\N{WHITE HEAVY CHECK MARK}": "<:emoji_8:825288282962133043>",
        "\N{BLACK RIGHT-POINTING TRIANGLE}": emote.forward,
        "\N{HEAVY EXCLAMATION MARK SYMBOL}": "<:error_purple_emoji:825289358957346816>",
        "\N{DOUBLE EXCLAMATION MARK}": "<:crossmark:753620331851284480>",
        "\N{ALARM CLOCK}": emote.end
    }
    react = reacts[reaction] if reaction in reacts else reaction
    with contextlib.suppress(discord.HTTPException):
        return await msg.add_reaction(react)


jishaku.exception_handling.attempt_add_reaction = attempt_add_reaction


async def traverse(self, func):
    std = io.StringIO()
    with contextlib.redirect_stdout(std):
        if inspect.isasyncgenfunction(func):
            async for send, result in AsyncSender(func(*self.args)):
                if content := std.getvalue():
                    std.seek(0)
                    std.truncate(0)
                    yield content
                send((yield result))
        else:
            yield await func(*self.args)
            if content := std.getvalue():
                yield content
jishaku.repl.compilation.AsyncCodeExecutor.traverse = traverse

WINDOWS = sys.platform == "win32"
SHELL = os.getenv("SHELL") or "/bin/bash"
def shell_init(self, code: str, timeout: int = 90, loop: asyncio.AbstractEventLoop = None):
        if WINDOWS:
            if pathlib.Path(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe").exists():
                sequence = [r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe", code]
                self.ps1 = "PS >"
                self.highlight = "powershell"
            else:
                sequence = ['cmd', '/c', code]
                self.ps1 = "cmd >"
                self.highlight = "cmd"
        else:
            sequence = [SHELL, '-c', code]
            self.ps1 = "$"
            self.highlight = "sh"

        self.process = subprocess.Popen(sequence, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.close_code = None

        self.loop = loop or asyncio.get_event_loop()
        self.timeout = timeout

        self.stdout_task = self.make_reader_task(self.process.stdout, self.stdout_handler)
        self.stderr_task = self.make_reader_task(self.process.stderr, self.stderr_handler)

        self.queue = asyncio.Queue(maxsize=250)

# This override is to fix ShellReader.__init__ unable to find powershell path.
jishaku.shell.ShellReader.__init__ = shell_init