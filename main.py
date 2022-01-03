from settings import BOT_TOKEN, GUILD_ID
from typing import Sequence, Iterable
import discord
import asyncio


class RoleSelection(discord.ui.Select):

    def __init__(self, user: discord.Member):
        all_roles = user.guild.roles
        user_role_ids = {role.id for role in user.roles}
        user_has_role = [(role, role.id in user_role_ids) for role in all_roles]
        options = [
            discord.SelectOption(label=role.name,
                                 value=str(role.id),
                                 default=has_role)
            for role, has_role in user_has_role
        ]
        super().__init__(placeholder='Select the roles you want to have...',
                         min_values=0,
                         max_values=len(user_has_role),
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        all_roles = interaction.guild.roles
        print(all_roles)
        to_add = [role for role in all_roles if str(role.id) in self.values]
        await interaction.user.add_roles(*to_add,
                                         reason='User updated their roles.')
        to_remove = [
            role for role in all_roles
            if str(role.id) not in self.values and role.name != 'everyone'
        ]
        await interaction.user.remove_roles(*to_remove)


class RoleEditView(discord.ui.View):

    def __init__(self, ctx):
        self.context = ctx
        super().__init__()
        self.add_item(RoleSelection(ctx.author))

    async def interaction_check(self, interaction):
        return self.context.author == interaction.user


class PollData:

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


bot = discord.Bot()


@bot.slash_command(guild_ids=[GUILD_ID])
async def edit_roles(ctx):
    view = RoleEditView(ctx)
    await ctx.respond('Role selection', view=view)


@bot.slash_command(guild_ids=[GUILD_ID])
async def poll(ctx):
    view = PollView(ctx, ['option a', 'option b', 'option c'])
    await ctx.respond('Role selection', view=view)


@bot.slash_command(guild_ids=[GUILD_ID])
async def anon(ctx, message: discord.commands.Option(str)):
    """Send a message anonymously."""
    await ctx.respond('Ok, I\'ll send that message on your behalf.',
                      ephemeral=True)
    await ctx.send(f'I have a message:\n> {message}')


@bot.message_command(guild_ids=[GUILD_ID])
async def snipe(ctx, message: discord.Message):
    await ctx.respond(f'Haha! {message.author.display_name} said: \n' +
                      f'```\n{message.content}\n```')


@bot.message_command(name='mOcK', guild_ids=[GUILD_ID])
async def mock(ctx, message: discord.Message):
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


@bot.user_command(guild_ids=[GUILD_ID])
async def monkey(ctx, user: discord.User):
    print(f'Someone wanted to monkey {user.display_name}')
    await ctx.respond()


bot.run(BOT_TOKEN)