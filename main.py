import discord
from settings import BOT_TOKEN
import src.cogs.bureau_of_administration
import src.cogs.bureau_of_fun
import src.cogs.bureau_of_voting

bot = discord.Bot()

bot.add_cog(src.cogs.bureau_of_administration.BoaCog(bot))
bot.add_cog(src.cogs.bureau_of_fun.BofCog(bot))
bot.add_cog(src.cogs.bureau_of_voting.BovCog(bot))

bot.run(BOT_TOKEN)
