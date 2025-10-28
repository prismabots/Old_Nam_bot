import discord
import random
import re
import logging
from discord import app_commands

# Assuming cddb and other dependencies will be handled as we refactor.
# For now, some functions might need adjustment if they depend on main.py state.

logger = logging.getLogger(__name__)


def encode(cddb_func, table=None, num=6):
    """
    Generates a random numerical slug of a specified length, checking for uniqueness.
    """
    logger.info("encode called with table=%s, num=%s", table, num)
    start = int(f"1{'0' * (num - 1)}")
    end = int(f"1{'0' * num}") - 1
    slug = random.randint(start, end)

    if table:
        dbs = cddb_func(fun="co")
        try:
            dbs[1].execute(f"SELECT id FROM {table} WHERE id = ?", (slug,))
            if dbs[1].fetchone():
                return encode(cddb_func, table, num)  # Recurse if slug exists
        finally:
            cddb_func(fun="cn", db=dbs[0], cr=dbs[1])
    return slug


def get_hex_color(input_text: str) -> int | None:
    """
    Converts a hexadecimal color string into an integer.
    """
    logger.info("get_hex_color called with input_text=%s", input_text)
    if input_text:
        try:
            return int(input_text, 16)
        except (ValueError, TypeError):
            return None
    return None


def getBiggerLenght(values: list) -> int:
    """
    Calculates the maximum string length from a list of values.
    """
    logger.info("getBiggerLenght called")
    biggerLenth = 0
    for value in values:
        if len(str(value)) > biggerLenth:
            biggerLenth = len(str(value))
    return biggerLenth


def format_time(seconds: int) -> str:
    """
    Formats a duration in seconds into a human-readable string.
    """
    logger.info("format_time called with seconds=%s", seconds)
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''}"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''}"
    else:
        days = seconds // 86400
        return f"{days} day{'s' if days > 1 else ''}"


def convert_to_seconds(time_str: str) -> int | None:
    """
    Converts a time string (e.g., "1d2h30m") into a total number of seconds.
    """
    logger.info("convert_to_seconds called with time_str=%s", time_str)
    try:
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800}
        total_seconds = 0
        matches = re.findall(r'(\d+)([smhdw])', time_str.lower())
        if not matches:
            return None
        for value, unit in matches:
            total_seconds += int(value) * time_units[unit]
        return total_seconds
    except:
        return None


class SwitchMessages(discord.ui.View):
    """
    A Discord UI View that provides 'next' and 'last' buttons to navigate through a list of message contents (embeds).
    """
    def __init__(self, embeds):
        super().__init__(timeout=None)
        logger.info("SwitchMessages view initialized")
        self.embeds = embeds
        self.embedIndex = 0

        self.last_button = discord.ui.Button(label="", style=discord.ButtonStyle.red, custom_id="lastB", emoji="⏮", disabled=True)
        self.last_button.callback = self.lastButton
        self.add_item(self.last_button)

        self.next_button = discord.ui.Button(label="", style=discord.ButtonStyle.green, custom_id="nextB", emoji="⏭")
        if len(self.embeds) <= 1:
            self.next_button.disabled = True
        self.next_button.callback = self.nextButton
        self.add_item(self.next_button)

    async def nextButton(self, interaction: discord.Interaction):
        logger.info("SwitchMessages.nextButton clicked by %s", interaction.user)
        try:
            self.last_button.disabled = False
            if self.embedIndex + 1 >= len(self.embeds) - 1:
                self.next_button.disabled = True
            self.embedIndex += 1
            await interaction.response.edit_message(content=self.embeds[self.embedIndex], view=self)
        except Exception as e:
            logger.error("Error in nextButton: %s", e)

    async def lastButton(self, interaction: discord.Interaction):
        logger.info("SwitchMessages.lastButton clicked by %s", interaction.user)
        try:
            self.next_button.disabled = False
            if self.embedIndex - 1 <= 0:
                self.last_button.disabled = True
            self.embedIndex -= 1
            await interaction.response.edit_message(content=self.embeds[self.embedIndex], view=self)
        except Exception as e:
            logger.error("Error in lastButton: %s", e)


async def ClearAllMessages(client: discord.Client, channel_id: int):
    """
    Deletes all messages in a given text channel.
    """
    logger.info("ClearAllMessages called for channel_id=%s", channel_id)
    channel = client.get_channel(channel_id)
    if not channel:
        logger.warning("ClearAllMessages: Channel %s not found.", channel_id)
        return
    await channel.purge(limit=None)