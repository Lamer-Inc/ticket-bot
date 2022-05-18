# ignora gli import extra, copia e incollati da altri miei bot per risparmiare tempo
import asyncio
import json
import discord
import requests
from discord import Embed
from discord.ext import commands

# import discord_slash
# from discord_slash import SlashCommand, SlashContext


# token del bot, posso rigenerarlo se necessario, su github verrà censurato
bt = 'OTc1NzU1NTE2MzgwODYwNDg5.GInrx7.NI********************************'

print("Applicazione avviata")

b = commands.Bot(command_prefix="!")
#da cambiare il prefisso necessariamente, aggiungere supporto a slash commands
b.remove_command("help")


# bs = SlashCommand(b, sync_commands=True)


# https://python.plainenglish.io/how-to-change-discord-bot-status-with-discord-py-39219c8fceea
@b.event
async def on_ready():
    await b.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!help for commands'))
#cambaire status, preso dal bot: https://github.com/Lamer-Inc/random-stuff/blob/main/anti-scam-bot.py


# °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
@b.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Un permesso specifico è richiesto per eseguire questo comando')
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Missing Argument!**', color=discord.Color.red())
        embed.add_field(name="Argomento mancante!", value='Digita !help per  maggiori informazioni', inline=False)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title='**Comando non trovato!**', color=discord.Color.red())
        embed.add_field(name='**Command Not Found**', value='!help per la lista di comandi', inline=False)
        await ctx.send(embed=embed)


# ----------------------------------------------------------------------------------------------------------------

# TICKET BOT (parte del codice riciclata da un mio vecchio progetto)


# ---------------------------------------------------------------------------------------------------

# name e help da levare avendo disabilitato l'help command di default
@b.command(name='ticket', help='Crea un canale per parlare con gli admin del server')
async def ticket(ctx, *, args):
    guild = b.get_guild(930511259416272917)
    c = guild.get_channel(976158359717810246)
    if ctx.message.channel == c:
        ticket_channel = await ctx.guild.create_text_channel(name='Ticket di ' + str(ctx.author.name))
        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
        await ctx.send(str(ctx.author.mention) + ' controlla il canale **Ticket** per parlare con gli amministratori')
        await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)
        embed = discord.Embed(title='**Ticket di:**' + ctx.author.mention, color=discord.Color.red())
        embed.add_field(name='**Argomento o segnalazione: **', value=args, inline=False)
        await ticket_channel.send(embed)

    else:
        await ctx.send(
            str(ctx.message.author.mention) + 'Utilizza il canale **apertura-ticket** per richiedere supporto')
#da correggere riga 67
#da revisionare permessi
#guild ID e C riferiti al server di prova, da cambiare in base a id effettivi del server in cui si usa il bot, da aggiornare!


##################### NON FINITO, WORK IN PROGRESS


b.run(bt)
