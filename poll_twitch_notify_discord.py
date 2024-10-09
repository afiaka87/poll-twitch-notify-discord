import asyncio
import logging
import argparse
import requests
import discord
from discord import TextChannel
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("poll-twitch-notify-discord")

load_dotenv()

# Configuration from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")  # bot test
GUILD_ID = os.getenv("DISCORD_GUILD_ID")  # bot test

class TwitchAPI:
    @staticmethod
    def get_stream_url(username: str) -> str:
        return f"https://twitch.tv/{username}"

    @staticmethod
    def check_if_user_is_streaming(username: str) -> bool:
        url = "https://gql.twitch.tv/gql"
        query = f'query {{ user(login: "{username}") {{ stream {{ id }} }} }}'
        response = requests.post(
            url,
            json={"query": query, "variables": {}},
            headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"},
        )
        return response.json()["data"]["user"]["stream"] is not None


class DiscordBot(discord.Client):
    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")

    async def send_notification(self, username: str):
        if not all([GUILD_ID, CHANNEL_ID, username]):
            logger.error(
                "Missing required configuration. Please check your environment variables."
            )
            return

        guild = await self.fetch_guild(GUILD_ID)
        if guild:
            channel = await guild.fetch_channel(CHANNEL_ID)
            if isinstance(channel, TextChannel):
                message = f"{username} has started streaming at {TwitchAPI.get_stream_url(username)}"
                await channel.send(message)
                logger.info(f"Notification sent: {message}")
            else:
                logger.error(
                    f"Channel with ID {CHANNEL_ID} not found or is not a TextChannel."
                )
        else:
            logger.error(f"Guild with ID {GUILD_ID} not found.")


class StreamMonitor:
    def __init__(self, username: str, bot: DiscordBot, poll_interval_in_seconds: int = 10):
        self.username = username
        self.bot = bot
        self.poll_interval_in_seconds = poll_interval_in_seconds
        self.previously_streaming = False
        self.consecutive_streaming_checks = 0
        self.consecutive_not_streaming_checks = 0

    async def monitor_stream(self):
        while True:
            is_streaming = TwitchAPI.check_if_user_is_streaming(self.username)

            if is_streaming:
                self.consecutive_streaming_checks += 1
                self.consecutive_not_streaming_checks = 0
            else:
                self.consecutive_not_streaming_checks += 1
                self.consecutive_streaming_checks = 0

            if self.consecutive_streaming_checks == 2 and not self.previously_streaming:
                await self.bot.send_notification(self.username)
                self.previously_streaming = True
                logger.info(f"{self.username} started streaming.")
            elif self.consecutive_not_streaming_checks >= 3:
                self.previously_streaming = False
                logger.info(f"{self.username} is not streaming.")

            await asyncio.sleep(self.poll_interval_in_seconds)


async def main(username: str, poll_interval_in_seconds: int = 10):
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True

    bot = DiscordBot(intents=intents)

    # Start the bot in the background
    bot_task = asyncio.create_task(bot.start(DISCORD_TOKEN))

    # Start the stream monitor
    monitor = StreamMonitor(username, bot, poll_interval_in_seconds)
    monitor_task = asyncio.create_task(monitor.monitor_stream())

    # Wait for both tasks to complete (which they never will in this case)
    await asyncio.gather(bot_task, monitor_task)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Monitor a Twitch user's stream and send Discord notifications."
    )
    parser.add_argument("username", help="Twitch username to monitor")
    parser.add_argument("--poll-interval", type=int, default=10, help="Poll interval in seconds")
    args = parser.parse_args()

    asyncio.run(main(args.username, args.poll_interval))
