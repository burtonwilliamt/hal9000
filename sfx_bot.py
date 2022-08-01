"""Experimental implementation of the SFX bot.

This bot allows multiple sound files to be playing simultaneously.

Another notable change is the implementation of slash commands on this bot.
"""
import datetime
import subprocess
import discord
from settings import BOT_TOKEN, GUILD_ID

bot = discord.Bot()


async def get_voice_client(guild: discord.Guild, channel: discord.VoiceChannel):
  voice_client = guild.voice_client
  if voice_client is None:
    voice_client = await channel.connect()
  elif voice_client.channel != channel:
    await voice_client.move_to(channel)
  return voice_client


@bot.slash_command(guild_ids=[GUILD_ID])
async def introduce(ctx,
                    channel: discord.commands.Option(discord.VoiceChannel)):
  voice_client = await get_voice_client(ctx.guild, channel)

  ffmpeg_options = ''
  start_time = 1000
  end_time = 5000

  # Set the start time.
  ffmpeg_options += f' -ss {datetime.timedelta(milliseconds=start_time)}'

  # Set the duration.
  ffmpeg_options += f' -t {datetime.timedelta(milliseconds=end_time - start_time)}'

  track = discord.FFmpegOpusAudio(
      '/mnt/c/Users/William/Desktop/youtube-rb94S_HIfXw-Meet_The_Sniper_Theme_Song_Fixed_Version.m4a',
      before_options=ffmpeg_options,
      options='-filter:a loudnorm')

  voice_client.play(track)
  await ctx.respond('I shall announce your arrival presently.')


the_input_pipe = None


@bot.slash_command(guild_ids=[GUILD_ID])
async def setup_sfx(ctx,
                    channel: discord.commands.Option(discord.VoiceChannel)):
  voice_client = await get_voice_client(ctx.guild, channel)

  ffmpeg_proc = subprocess.Popen(
      [
          'ffmpeg',
          '-f',
          's16le',
          '-re',
          '-ar',
          '44100',
          '-ac',
          '2',
          '-i',
          'pipe:0',
          # '-listen',
          # '1',
          # 'unix://home/william/github/hal9000/audio_socket',
          # '-type',
          # '2',
          '-f',
          's16le',
          '-ar',
          '48000',
          '-ac',
          '2',
          'pipe:1',
      ],
      stdout=subprocess.PIPE,
      stdin=subprocess.PIPE,
      stderr=subprocess.DEVNULL)
  global the_input_pipe
  the_input_pipe = ffmpeg_proc.stdin

  track = discord.PCMAudio(ffmpeg_proc.stdout)
  voice_client.play(track)
  await ctx.respond('sfx_initialized', ephemeral=True)


current_sfx = None


@bot.slash_command(guild_ids=[GUILD_ID])
async def play_track(ctx):
  global current_sfx
  if current_sfx is not None:
    current_sfx.terminate()
  current_sfx = subprocess.Popen([
      'ffmpeg',
      '-loglevel',
      'error',
      '-re',
      '-ss',
      '00:00:01',
      '-i',
      'sniper.m4a',
      '-to',
      '00:00:05',
      '-f',
      's16le',
      '-ac',
      '2',
      'pipe:1',
  ],
                                 stdout=the_input_pipe)
  await ctx.respond('Started sound effect', ephemeral=True)


bot.run(BOT_TOKEN)
