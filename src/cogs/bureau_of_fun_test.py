"""Tests for the BoF."""
import unittest
from unittest import mock
import discord
import src.cogs.bureau_of_fun


class BofTest(unittest.IsolatedAsyncioTestCase):

  def setUp(self):
    self.bot = mock.create_autospec(discord.Bot, instance=True)
    self.cog = src.cogs.bureau_of_fun.BofCog(self.bot)
    self.ctx = mock.create_autospec(discord.ApplicationContext, instance=True)

  async def test_anon(self):
    message_str = 'I am anonymous.'
    await self.cog.anon.callback(self.cog, self.ctx, message_str)
    self.ctx.respond.assert_called_once_with(
        'Ok, I\'ll send that message on your behalf.', ephemeral=True)
    self.ctx.send.assert_called_once_with(
        'I have a message:\n> I am anonymous.')

  async def test_snipe(self):
    message = mock.create_autospec(discord.Message, instance=True)
    message.author.display_name = 'fake_user'
    message.content = 'Something embarassing.'
    await self.cog.snipe.callback(self.cog, self.ctx, message)
    self.ctx.respond.assert_called_once_with(
        'Haha! fake_user said: \n```\nSomething embarassing.\n```')

  async def test_mock(self):
    message = mock.create_autospec(discord.Message, instance=True)
    message.content = 'You can\'t just change capitalization to mock me.'
    await self.cog.mock.callback(self.cog, self.ctx, message)
    self.ctx.delete.assert_called_once_with()
    self.ctx.send.assert_called_once_with(
        'yOu CaN\'t JuSt ChAnGe CaPiTaLiZaTiOn To MoCk Me.')

  async def test_monkey(self):
    user = mock.create_autospec(discord.User, instance=True)
    user.display_name = 'fake_username'
    await self.cog.monkey.callback(self.cog, self.ctx, user)
    self.ctx.respond.assert_called_once_with(
        'Someone wanted to monkey fake_username using right click.')
