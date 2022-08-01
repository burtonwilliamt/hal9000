import json
import http.client
import urllib.parse

import discord

import settings


class BofCog(discord.Cog):
  """A Cog filled with fun nonsense."""

  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @discord.slash_command(guild_ids=[settings.GUILD_ID])
  async def anon(self, ctx: discord.ApplicationContext,
                 message: discord.commands.Option(str)):
    """Send a message anonymously."""
    await ctx.respond('Ok, I\'ll send that message on your behalf.',
                      ephemeral=True)
    await ctx.send(f'I have a message:\n> {message}')

  @discord.message_command(guild_ids=[settings.GUILD_ID])
  async def snipe(self, ctx: discord.ApplicationContext,
                  message: discord.Message):
    await ctx.respond(f'Haha! {message.author.display_name} said: \n' +
                      f'```\n{message.content}\n```')

  @discord.message_command(name='mOcK', guild_ids=[settings.GUILD_ID])
  async def mock(self, ctx: discord.ApplicationContext,
                 message: discord.Message):
    """mAkE fUn Of WhAt ThEy SaId."""
    content = message.content
    mocked = []

    upper = False
    for c in content:
      if not c.isalpha():
        mocked.append(c)
        continue

      if upper:
        mocked.append(c.upper())
      else:
        mocked.append(c.lower())
      upper = not upper

    await ctx.delete()
    await ctx.send(''.join(mocked))

  @discord.user_command(guild_ids=[settings.GUILD_ID])
  async def monkey(self, ctx: discord.ApplicationContext, user: discord.User):
    await ctx.respond(
        f'Someone wanted to monkey {user.display_name} using right click.')

  @discord.slash_command(guild_ids=[settings.GUILD_ID])
  async def ud(self, ctx: discord.ApplicationContext,
               term: discord.commands.Option(str)):
    """Fetches a definition from urban dictionary."""
    conn = http.client.HTTPSConnection('api.urbandictionary.com')
    encoded_term = urllib.parse.quote(term, safe='')
    conn.request('GET', f'/v0/define?term={encoded_term}')
    res = conn.getresponse()

    data_bytes = res.read()
    if len(data_bytes) == 0:
      ctx.respond('Failed to get a definition')
    data = json.loads(data_bytes.decode('utf-8'))
    the_list = data['list']
    first_result = the_list[0]

    word = first_result['word']
    permalink = first_result['permalink']
    definition = first_result['definition'].replace(r'\r\n', '\n')
    e = discord.Embed(description=f'[{word}]({permalink})\n\n' + definition)
    await ctx.respond(embed=e)
