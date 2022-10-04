import discord
from discord.ext import commands
from discord.ext.commands import bot
import youtube_dl
import os
import shutil
from google_images_download import google_images_download
import random
from image_cog import image_cog



queues={}

def check_queue(id):
    if queues[id] != []:
        player= queues[id].pop(0)
        players[id] = player
        player.start()



 

client= commands.Bot(command_prefix='$')

@client.command(name='info')
async def version(context):
    print('here')    
    myEmbed = discord.Embed(title="Current Version", description="This bot will notify you when you join vc " , color=0x00ff00)
    myEmbed.add_field(name="Version code", value="v1.0",inline=False)
    myEmbed.add_field(name="Date Released:", value= "January 4th, 2022",inline=False)
    myEmbed.set_footer(text="This is a sample")
    myEmbed.set_author(name= "dollarmyballer")

    await context.message.channel.send(embed=myEmbed)
    

@client.command(name='commands')
async def version(context):
    print('here')
    myEmbed = discord.Embed(title="Current Commands", description="The current commands are $info,$play,$pause,$resume, and $leave" , color=0x00ff00)
    myEmbed.add_field(name="Date Released:", value= "January 4th, 2022",inline=False)
    myEmbed.set_author(name= "Dollarmyballer")

    await context.message.channel.send(embed=myEmbed)

   

@client.command()
async def play(ctx,url:str):
    song_there= os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the stop command")
        return

    voiceChannel= discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice= discord.utils.get(client.voice_clients,guild=ctx.guild)
    

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',

        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"))


    



@client.command()
async def leave(ctx):
    voice= discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()

    else:
        await ctx.sned("The bot is not connected to a voice channel")
   
@client.command()
async def pause(ctx):
    voice= discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no auido is playing")

@client.command()
async def resume(ctx):
    voice= discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()

    else:
        await ctx.send("The auido is not paused")


@client.command(pass_context=True)
async def queue(ctx,url):
    server= ctx.message.server
    voice_client=client.voice_client_in(server)
    player= await voice_client.create_ytdl_player(url)

    if server.id in queues:
        queues[server.id].append(player)

    else:
        queues[server.id]=[player]
    await client.say('Video queued')



    


client.run('OTI4MDg4MDE1MjgzMzA2NTM3.YdTrUQ.lRHKuxt_pHhMHg05vFTY4T6CS6Q')


