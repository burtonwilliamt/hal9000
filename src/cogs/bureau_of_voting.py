"""Features that allow users to vote, poll, or ask questions."""
from typing import Iterable
import discord

import settings


class PollData:
  """The state of a Poll, tracks the users that responded to each option."""

  def __init__(self, options: Iterable[str]):
    # A mapping from option to a set of user ids that have responded for
    # that option.
    self.responses = {option: set() for option in options}

  def respond(self, user: discord.Member, option: str):
    """Toggle a user response for a given option.

        Args:
            user (discord.Member): The user responding.
            option (str): The option they are either adding or removing
                themselves from.
        """
    if user.id in self.responses[option]:
      self.responses[option].remove(user.id)
    else:
      self.responses[option].add(user.id)


class PollButton(discord.ui.Button):

  def __init__(self, poll_data: PollData, option: str):
    super().__init__(label=option)
    self.poll_data = poll_data
    self.option = option

  async def callback(self, interaction: discord.Interaction):
    self.poll_data.respond(interaction.user, self.option)
    await interaction.message.edit(str(self.poll_data.responses))


class PollView(discord.ui.View):

  def __init__(self, ctx, options: Iterable[str]):
    super().__init__()
    self.context = ctx
    self.poll_data = PollData(options)

    for option in options:
      self.add_item(PollButton(self.poll_data, option))


class BovCog(discord.Cog):

  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @discord.slash_command(guild_ids=[settings.GUILD_ID])
  async def poll(self, ctx: discord.ApplicationContext):
    view = PollView(ctx, ['option a', 'option b', 'option c'])
    await ctx.respond('Role selection', view=view)
