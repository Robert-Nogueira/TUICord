import os
import string

import discord


def format_name(name: str):
    for char in name:
        if char not in string.ascii_letters + ' ':
            name = name.replace(char, '')
    return name


async def consume_history(channel) -> list[discord.Message]:
    return list(reversed([message async for message in channel.history()]))


def search_cogs():
    """search the extensions files"""
    for file in os.listdir('./events'):
        if file.endswith('.py') and file != '__init__.py':
            yield f'extensions.commands.{file[:-3]}'
