import asyncio

from textual import on
from textual.widgets import Input


class InputBox(Input):
    def __init__(self, *args, **kwargs):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and takes arguments that are
        passed to it.

        :param self: Represent the instance of the class
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass in keyword arguments to the parent class
        :return: Nothing, it is a constructor
        """
        super().__init__(*args, **kwargs)

    @on(Input.Submitted)
    async def on_submit(self, event: Input.Submitted):
        """
        The on_submit function is called when the user submits a message.
        It takes the input from the text box and sends it to discord.

        :param self: Refer to the class itself
        :param event: Input.Submitted: Get the input value from the user
        :return: None
        """
        discord_client = self.app.client
        asyncio.run_coroutine_threadsafe(
            self.app.actual_channel.send(event.input.value),
            loop=discord_client.loop,
        )
        event.input.value = ''
