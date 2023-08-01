import asyncio
import threading

import click
from dotenv import load_dotenv

from tuicord.core import DiscordClient
from tuicord.core import Interface

load_dotenv()


class TUICord:
    def __init__(self, token: str):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the Discord client and interface, as well as setting a
        title for the interface.

        :param self: Represent the instance of the class
        :param token: str: Store the token for the bot
        :return: None
        """
        self.discord_client: DiscordClient = DiscordClient()
        self.interface: Interface = Interface(self.discord_client)
        self.interface.title = 'TUICord'
        self._discord_token: str = token

    def run_client(self, loop):
        """
        The run_client function is a coroutine that runs the discord client.
            It takes in a loop as an argument and uses it to run the discord
            client until completion.
            The loop is used to run the asyncio event loop, which allows
            for asynchronous programming.

        :param self: Represent the instance of the class
        :param loop: Run the client until it is complete
        :return: None
        """
        loop.run_until_complete(
            self.discord_client.run(self._discord_token))

    def run_interface(self):
        """
        The run_interface function is the main function of this program.
        It starts a new thread that runs the discord client, and then it runs
        the interface in the main thread. The reason for this is that if we
        run both on one thread, they will block each other from running.

        :param self: Represent the instance of the class
        :return: None
        """
        threading.Thread(
            target=self.run_client,
            args=[asyncio.new_event_loop()],
            daemon=True
        ).start()
        while True:
            if self.discord_client.is_ready():
                self.interface.run()
                break


@click.group()
def cli():
    """
    The cli function is the entry point for the command line interface.
    It takes no arguments and returns nothing.


    :return: None
    """
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
    """
    The run function is the main function of TUICord. It starts the application
    and runs it until it is closed by a user.


    :param token: str: User discord token
    :return: None
    """
    click.echo(click.style('Starting...', fg='green'))
    app = TUICord(token)
    app.run_interface()


if __name__ == '__main__':
    cli()
