import asyncio
import logging
import random
from datetime import datetime

import discord
from discord.abc import PrivateChannel

from rl_interceptor import RLInterceptor
from util import pretty_channel, is_removable_message, delete_message


async def select_channel(private_channels: list[discord.abc.PrivateChannel]) -> discord.abc.PrivateChannel | None:
    print("..| # Groups | @ Direct messages | ? Unknown |..")
    for channel in private_channels:
        print(f"  {pretty_channel(channel)}")

    while True:
        print()
        try:
            # Use to_thread to avoid blocking the event loop
            channel_id_str: str = await asyncio.to_thread(input, "[>>>] Enter channel ID: ")
            selected_channel_id = int(channel_id_str)
        except ValueError:
            print("[!] Invalid channel ID provided")
            continue

        selected_channel = discord.utils.get(private_channels, id=selected_channel_id)
        if selected_channel:
            return selected_channel

        print(f"[!] Invalid channel ID: {selected_channel_id}")


class Client(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.desired_delay: float = 1.0
        self.maximum_delay: float = 8.0
        self.delay: float = 1.0

        self.reduce_after_successful: int = 4
        self.successful_requests: int = 0
        self.reduce_multiplier: float = 0.995

        self._setup_rate_limit_interceptor()

    def _setup_rate_limit_interceptor(self) -> None:
        http_logger = logging.getLogger("discord.http")
        http_logger.addHandler(RLInterceptor(self))
        http_logger.setLevel(logging.WARNING)

    def adjust_dynamic_delay(self, penalty: float | None = None) -> None:
        # Uncomment for debugging!
        # print(f"delay={self.delay}; successful={self.successful_requests}; penalty={penalty}")

        # Handle successful request
        if not penalty:
            self.successful_requests += 1

            # Check if we had enough successful requests to start reducing
            if self.successful_requests < self.reduce_after_successful:
                return

            # Check if we're already at the most desirable (lowest) delay
            if self.delay <= self.desired_delay:
                return

            # Reduce delay
            self.delay *= self.reduce_multiplier
            return

        # Unsuccessful request; increase delay
        self.successful_requests = 0
        self.delay += penalty
        self.delay = min(self.delay, self.maximum_delay)

    async def on_ready(self):
        print(f"Logged in to account {self.user.name}; fetching private channels...")
        print("Note: This will include hidden/closed channels")
        print()

        # Sort channels by last message or creation ID
        private_channels = list(self.private_channels)
        private_channels.sort(key=lambda c: c.last_message_id or c.id, reverse=True)

        # Sanity check; new account?
        if not private_channels:
            print("[!] No private channels detected.")
            return

        selected_channel: PrivateChannel = await select_channel(private_channels)

        print(f"[*] Selected channel: {selected_channel.id}; press any key to begin message deletion...")
        print(
            "[!] If you're feeling nostalgic, I recommend backing up messages beforehand: github.com/Tyrrrz/DiscordChatExporter")
        await asyncio.to_thread(input)

        # Note: we delete oldest first because it can cache-miss/avoid message loggers

        print("[*] Beginning message deletion...")
        async for message in selected_channel.history(limit=None, oldest_first=True):

            if not is_removable_message(message, self.user.id):
                continue

            t1: datetime = datetime.now()
            should_jitter: bool = bool(random.getrandbits(1))

            try:
                asyncio.create_task(delete_message(message))
                await asyncio.sleep(self.delay)

                if should_jitter:
                    await asyncio.sleep(random.uniform(0.0, 0.5))

                self.adjust_dynamic_delay()
            except discord.Forbidden:
                print(f"[!] 403 forbidden within group/direct messages, aborting...")
                return
            except discord.HTTPException as e:
                print(f"[!] Failed to delete message {message.id}: {e}; aborting")
                return
            else:
                time_taken: float = (datetime.now() - t1).total_seconds()
                print(f"| {time_taken:.2f}s | {message.author.name} | {message.clean_content}")

        print("[*] Message deletion completed.")
