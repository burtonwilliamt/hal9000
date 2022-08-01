import discord

import settings


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


class BoaCog(discord.Cog):

  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @discord.slash_command(guild_ids=[settings.GUILD_ID])
  async def edit_roles(self, ctx: discord.ApplicationContext):
    view = RoleEditView(ctx)
    await ctx.respond('Role selection', view=view)
