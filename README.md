# Poll-Twitch-Notify-Discord

This Python script monitors a specified Twitch user's stream status and sends notifications to a Discord channel when the user starts streaming.

## Features

- Monitors a Twitch user's stream status in real-time
- Sends notifications to a specified Discord channel when the stream starts
- Handles brief interruptions in streams to avoid false notifications
- Command-line interface for easy usage

## How It Works

1. The script uses the Twitch GraphQL API to check the streaming status of a specified user.
2. It runs a Discord bot that can send messages to a specified channel.
3. The stream status is checked every 10 seconds.
4. To avoid false positives, the script requires two consecutive positive checks before considering a stream as "started".
5. To handle brief interruptions, the script requires three consecutive negative checks before considering a stream as "ended".

## Requirements

- Python 3.7 or higher
- `discord.py` library
- `requests` library

## Installation

1. Clone this repository or download the script.
2. Install the required libraries:
   ```
   pip install discord.py requests
   ```

## Configuration

Before running the script, you need to set up the following:

1. Discord Bot Token
2. Discord Guild (Server) ID
3. Discord Channel ID

These should be set as environment variables in a file `.env` in the same directory as the script.

- `DISCORD_BOT_TOKEN=` is found in the Discord developer console after [creating a bot](https://discordpy.readthedocs.io/en/stable/discord.html)

- `DISCORD_CHANNEL_ID=` is found by right-clicking a channel in Discord and selecting "Copy channel ID" from the context menu.

- `DISCORD_GUILD_ID=` is found by right-clicking a server (also called guilds) in Discord and selecting "Copy server ID"
POLL_INTERVAL_IN_SECONDS=5

## Usage

Run the script from the command line, specifying the Twitch username to monitor:

```
python twitch_stream_notifier.py USERNAME --poll-interval SECONDS
```

Replace `USERNAME` with the Twitch username you want to monitor.

### Command-line Arguments

- `username`: (Required) The Twitch username to monitor.
- `--poll-interval`: (Optional)
Time in seconds to wait before polling twitch again. Avoid using low values such as 1-2 seconds as you will get rate limited.

## Example

```
python twitch_stream_notifier.py Ninja
```

This will start monitoring the Twitch user "Ninja" and send a Discord notification when they start streaming.

## Notes

- Make sure your Discord bot has the necessary permissions to send messages in the specified channel.
- The script uses a client ID for the Twitch API that may need to be updated if it becomes invalid.
- The script runs indefinitely until manually stopped.

## Troubleshooting

- If you're not receiving notifications, check that your Discord bot token, guild ID, and channel ID are correct.
- Ensure that your Discord bot has been invited to your server and has the necessary permissions.
- Check your internet connection, as the script requires constant internet access to function properly.

## Contributing

Feel free to fork this repository and submit pull requests with any enhancements.

## License

This project is open source and available under the [MIT License](LICENSE).