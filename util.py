import discord


def pretty_channel(channel: discord.abc.PrivateChannel) -> str:
    """Returns a pretty string representation of a private channel."""

    if isinstance(channel, discord.DMChannel):
        return f"| @ | {channel.id} | {channel.recipient.name}"
    elif isinstance(channel, discord.GroupChannel):
        return f"| # | {channel.id} | {channel.name or ', '.join(r.name for r in channel.recipients)}"
    else:
        return f"| ? | {channel.id} | {channel}"


def is_removable_message(message: discord.Message, self_id: int) -> bool:
    return all((
        message.author.id == self_id,
        message.type in (discord.MessageType.default, discord.MessageType.reply)
    ))


async def delete_message(message: discord.Message) -> None:
    await message.delete()
