import asyncio
import threading

import click
from dotenv import load_dotenv

from tuicord.core import DiscordClient
from tuicord.core import Interface

load_dotenv()


class TUICord:
    def __init__(self, token: str):
        self.discord_client: DiscordClient = DiscordClient()
        self.interface: Interface = Interface(self.discord_client)
        self.interface.title = 'TUICord'
        self._discord_token: str = token

    def run_bot(self, loop):
        loop.run_until_complete(
            self.discord_client.run(self._discord_token))

    def start(self):
        threading.Thread(
            target=self.run_bot,
            args=[asyncio.new_event_loop()],
            daemon=True
        ).start()
        while True:
            if self.discord_client.is_ready():
                self.interface.run()
                break


@click.group()
def cli():
    pass


@cli.command('run')
@click.option(
    '--token', '-t',
    help='User token',
    envvar='DISCORD_TOKEN',
    required=True,
    type=click.STRING,
)
def run(token: str) -> None:
    """ Starts TUICord

    :param token: An User token string to be used to connect to the discord
    :return: None
    """
    click.echo(click.style('Starting...', fg='green'))
    app = TUICord(token)
    app.start()


if __name__ == '__main__':
    cli()
