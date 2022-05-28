# ignora gli import extra, copia e incollati da altri miei bot per risparmiare tempo
import asyncio
import json
import time

import discord
import requests
from discord import Embed
from discord.ext import commands
import interactions

# import discord_slash
# from discord_slash import SlashCommand, SlashContext


# token del bot, posso rigenerarlo se necessario, su github verrà censurato
bt = 'OTc1NzU1NTE2MzgwODYwNDg5.GInrx7.NIHOZud47cie5wHD12h1eyzn4nL-**********'

print("Applicazione avviata")

b = commands.Bot(command_prefix="!")
b.remove_command("help")


# bs = SlashCommand(b, sync_commands=True)


# https://python.plainenglish.io/how-to-change-discord-bot-status-with-discord-py-39219c8fceea
@b.event
async def on_ready():
    await b.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!help per i comandi'))


# °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
@b.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Un permesso specifico è richiesto per eseguire questo comando')
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Missing Argument!**', color=discord.Color.red())
        embed.add_field(name="Argomento mancante!", value='Digita !help per  maggiori informazioni', inline=False)
        await ctx.send(embed=embed, delete_after=15)
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title='**Comando non trovato!**', color=discord.Color.red())
        embed.add_field(name='**Command Not Found**', value='!help per la lista di comandi', inline=False)
        await ctx.send(embed=embed, delete_after=15)


# ho aggiunto la cosa più utile di questo mondo la delete_after in modo tale che il bot cancelli i messaggi di errore
# tutti questi parametri sono ovviamente configurabili a piacimento

# ----------------------------------------------------------------------------------------------------------------

# TICKET BOT (parte del codice riciclata da un mio vecchio progetto)


# ---------------------------------------------------------------------------------------------------
# TUTTI STI AFFARI NON SERVONO, IL BOT FUNZIONA CON LE REAZIONI E VA MOLTO MEGLIO

@b.command(name='ticket', help='Crea un canale per parlare con gli admin del server')
async def ticket(ctx, *, args):
    guild = b.get_guild(975496826369237062)
    c = guild.get_channel(977937133094449222)
    if ctx.message.channel == c:

        embed = discord.Embed(title='**Ticket creato!**',
                              color=discord.Color.green())
        embed.add_field(name="**Autore del ticket**: ", value=ctx.message.author.mention, inline=True)
        embed.add_field(name='**Segnalazione**: ', value=str(args), inline=False)
        embed.add_field(name='**Come funziona il ticket**?',
                        value='Il bot creerà un canale apposito in cui potrai parlare con lo staff per discutere riguardo la tua segnalazione',
                        inline=False)
        embed.add_field(name='Recati qua: ', value='Canale {}'.format("#" + ctx.message.author.name + "-ticket"))
        embed.set_footer(text="Ticket made by DiStRuTtOrE_Tm#6449", icon_url=b.user.avatar_url)
        await ctx.send(embed=embed)
        category = discord.utils.get(ctx.guild.channels, id=975762506641444884)
        ticket_channel = await ctx.guild.create_text_channel(name='{}-ticket'.format(ctx.message.author.name),
                                                             category=category)

        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
        await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)
        # da qua non funziona più un cazzo, provvedere a sistemare
        s = discord.utils.get(ctx.guild.channels, id=ticket_channel.id)

        cembed = discord.Embed(title='Hai creato un nuovo ticket!', color=discord.Color.red())
        cembed.add_field(name="**Autore del ticket**: ", value=ctx.message.author.mention, inline=True)
        cembed.add_field(name="Argomento/richiesta: ", value=str(args), inline=False)
        cembed.set_thumbnail(url=ctx.message.author.avatar_url)
        cembed.set_footer(text="Ticket made by DiStRuTtOrE_Tm#6449", icon_url=b.user.avatar_url)
        await s.send(embed=cembed)
        # funziona di nuovo da qua

        lembed = discord.Embed(title='Ticket creato/comando ticket utilizzato', color=discord.Color.blue())
        lembed.add_field(name='Messaggio di: ', value=ctx.author.mention)
        channel_to_log = b.get_channel(977885168687808542)
        await channel_to_log.send(embed=lembed)

    else:
        await ctx.send(
            str(ctx.message.author.mention) + 'Utilizza il canale **apertura-ticket** per richiedere supporto',
            delete_after=15)





# -----------------------------------------------------------------------------------------------------------------------
# Sezione log ticket bot

# @b.event
# async def on_message(message):
# if message.content.startswith('!ticket'):
# embed=discord.Embed(title='Ticket creato/comando ticket utilizzato', color=discord.Color.blue())
# embed.add_field(name='Messaggio di: ', value=message.author.mention)
# channel_to_log = b.get_channel(977885168687808542)
# await channel_to_log.send(embed=embed)
# else:
# print('!')

# ----------------------------------------------------------------------------------------------------------------------
# il bot inizia effettivamente da qua, non mi aggrada il fatto di dover mettere gli ID a mano

@b.event
async def on_reaction_add(em, u):
    if em.emoji == '🎫':
        if u.id == 975755516380860489:
            None
        else:
            if 'apertura-ticket' in em.message.channel.name:
                guild = b.get_guild(975496826369237062)
                category = discord.utils.get(guild.channels, id=977937083387756674)
                ex = discord.utils.get(guild.text_channels, name=u.name.lower()+'-ticket')
                if ex:
                    None
                else:
                    ticket_channel = await guild.create_text_channel(name='{}-ticket'.format(u.name),
                                                             category=category)

                    await ticket_channel.set_permissions(guild.get_role(guild.id), send_messages=False, read_messages=False)
                    await ticket_channel.set_permissions(u, send_messages=True, read_messages=True, add_reactions=True,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)
                    staff_ds = discord.utils.get(guild.roles, id=976147012678479912)
                    staff_cb = discord.utils.get(guild.roles, id=976172571450040330)
                    await ticket_channel.set_permissions(staff_ds, send_messages=True, read_messages=True, add_reactions=True,
                                                     embed_links=True, attach_files=True, read_message_history=True,
                                                     external_emojis=True, manage_messages=True)
                    await ticket_channel.set_permissions(staff_cb, send_messages=True, read_messages=True,
                                                     add_reactions=True,
                                                     embed_links=True, attach_files=True, read_message_history=True,
                                                     external_emojis=True, manage_messages=True)
                    embed = discord.Embed(title='**Ticket creato!**',
                                      color=discord.Color.green())
                    embed.add_field(name="**Autore del ticket**: ", value=u.mention, inline=True)
                    embed.add_field(name='**Come funziona il ticket**?',
                                value='Attendi che uno ' + staff_ds.mention + ' o uno ' + staff_cb.mention + ' ti risponda, nel mentre descrivi il tuo problema',
                                inline=False)
                    embed.add_field(name='Per chiudere il ticket digita: ', value='!close')
                    embed.set_footer(text="Ticket made by DiStRuTtOrE_Tm#6449", icon_url=b.user.avatar_url)
                    await ticket_channel.send(embed=embed)
            else:
                None
    elif em.emoji == '✔️':
        if u.id == 975755516380860489:
            None
        else:
            if '-ticket' in em.message.channel.name:
                time.sleep(5)
                await em.message.channel.delete(reason='Il seguente ticket è stato chiuso')
            else:
                None




@b.command()
async def set(ctx):
    if ctx.message.author.permissions_in(ctx.message.channel).administrator:
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title='**Ticket bot**', color=discord.Color.dark_gold())
        embed.add_field(name='Reagisci a questo messaggio per aprire un ticket e parlare con lo staff!', value='🎫', inline=False)
        embed.set_footer(text="Ticket made by DiStRuTtOrE_Tm#6449", icon_url=b.user.avatar_url)
        e = '🎫'

        em = await ctx.channel.send(embed=embed)
        await em.add_reaction(emoji=e)
    else:
        await ctx.send('Non hai i permessi per eseguire questo comando', delete_after=10)


@b.command()
async def close(ctx):
    if "-ticket" in ctx.message.channel.name:
        embed = discord.Embed(name='Chiusura ticket', color=discord.Color.dark_orange())
        embed.add_field(name='Con questo comando puoi chiudere un ticket aperto', value='Reagisci con ✔️ per chiudere il ticket. Una volta chiuso tutti i messaggi al suo interno verranno eliminati', inline=False)
        ems = await ctx.send(embed=embed)
        mj = '✔️'
        await ems.add_reaction(emoji=mj)

    else:
        await ctx.send('Con questo comando puoi chiudere solamente il tuo ticket')


@b.command()
async def help(ctx):
    embed = discord.Embed(title='Aiuto e Crediti', color=discord.Color.red())
    embed.add_field(name='**Lista Comandi**', value='Lista dei comandi del bot!', inline=False)
    embed.add_field(name='!set', value='SOLO STAFF!!! Utilizza il comando nel canale in cui vuoi che gli utenti aprano i ticket', inline=False)
    embed.add_field(name='Come ottenere supporto?', value='Recati nel canale apertura ticket e aggiungi una reazione al messaggio del bot. Il bot aprirà un ticket a tuo nome in cui fornirà ulteriori spiegazioni', inline=False)
    embed.add_field(name='!close', value="Utilizza il comando in un canale ticket per chiudere il canale. Prima che l'azione avvenga, il bot chiederà una conferma aggiuntiva", inline=False)
    embed.add_field(name='Maggiori info e documentazione del bot: ', value='https://telegra.ph/ParrotBot-05-22', inline=False)
    embed.add_field(name='Creatore del bot: ', value='DiStRuTtOrE_Tm#6449 (ID=586202654087184384)',
                    inline=False)
    embed.set_footer(text="Ticket bot made by DiStRuTtOrE_Tm#6449", icon_url=b.user.avatar_url)
    await ctx.send(embed=embed)


# ----------------------------------------------------------------------------------------------------------------------
# Sezione vocali temporanee, SPERIMENTALE!


@b.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    cc = discord.utils.get(guild.voice_channels, id=980179770849521755)
    category = discord.utils.get(guild.channels, id=980179615656071260)
    if before.channel is None and after.channel is not None:
        for channel in guild.channels:
            if after.channel.name == 'Entra qua:':
                memb_ch = await guild.create_voice_channel(name=member.name, category=category)
                await memb_ch.set_permissions(member, manage_channels=True, mute_members=True)
                await member.move_to(memb_ch)
            else:
                None
    if before.channel is not None and after.channel is None:
        for channel in guild.channels:
            if before.channel.name == member.name:
                await before.channel.delete()



b.run(bt)
