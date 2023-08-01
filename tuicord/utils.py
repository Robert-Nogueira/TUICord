import os
import string

import discord


def format_name(name: str):
    """
    The format_name function takes a string as input and returns the same
    string with all non-alphabetic characters removed.

    :param name: str: Name to be passed into the function
    :return: A formatted version of the name parameter
    """
    for char in name:
        if char not in string.ascii_letters + ' ':
            name = name.replace(char, '')
    return name


async def consume_history(channel) -> list[discord.Message]:
    """
    The consume_history function takes a channel as an argument and returns a
    list of messages in that channel.
    The function uses the async for loop to iterate over the history of
    the given channel, which is then reversed
    and returned as a list.

    :param channel: Specify the channel to get the history from
    :return: A list of messages, in reverse order
    """
    return list(reversed([message async for message in channel.history()]))


def search_cogs():
    """search the extensions files"""
    for file in os.listdir('./events'):
        if file.endswith('.py') and file != '__init__.py':
            yield f'extensions.commands.{file[:-3]}'
