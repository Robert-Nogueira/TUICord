import asyncio

from textual import on
from textual.widgets import Input


class InputBox(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @on(Input.Submitted)
    async def on_submit(self, event: Input.Submitted):
        discord_client = self.app.client
        asyncio.run_coroutine_threadsafe(
            self.app.actual_channel.send(event.input.value),
            loop=discord_client.loop)
        event.input.value = ''
