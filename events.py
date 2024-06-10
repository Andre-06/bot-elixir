from discord.utils import get

from main import client

from functions import *
from interactions import Button, ButtonStyle
import discord


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.'):
        await client.process_commands(message)

    elif message.content.lower().startswith('desv'):
        dado = message.content.lower().replace('desv ', '')

        rolar_dado = rolagem_tag(dado)
        rolar_dado1 = rolagem_tag(dado)
        primeiro = rolar_dado[1]
        segundo = rolar_dado1[1]
        primeiro_ctx = rolar_dado[0]
        segundo_ctx = rolar_dado1[0]

        if segundo < primeiro:
            primeiro_ctx = f'~~{primeiro_ctx}~~'
        elif primeiro < segundo:
            segundo_ctx = f'~~{segundo_ctx}~~'

        await message.reply(primeiro_ctx + '\n' + segundo_ctx)

    elif message.content.lower().startswith('van'):
        dado = message.content.lower().replace('van ', '')

        rolar_dado = rolagem_tag(dado)
        rolar_dado1 = rolagem_tag(dado)
        primeiro = rolar_dado[1]
        segundo = rolar_dado1[1]
        primeiro_ctx = rolar_dado[0]
        segundo_ctx = rolar_dado1[0]

        if segundo > primeiro:
            primeiro_ctx = f'~~{primeiro_ctx}~~'
        elif primeiro > segundo:
            segundo_ctx = f'~~{segundo_ctx}~~'

        await message.reply(primeiro_ctx + '\n' + segundo_ctx)


    elif 'd' in message.content.lower() and len(message.content) <= 32 and any(
            chr.isdigit() for chr in message.content):
        try:
            print('*************** ' + str(message.channel) + ' *****************')
            print('*************** ' + str(message.guild.name) + ' *****************')
            dado = rolagem_tag(message.content.lower())[0]
        except ValueError:
            return
        else:
            if message.author.id == 621664265907994624:
                add = ''
            else:
                add = ''

            await message.reply(dado + add, mention_author=True)


@client.event
async def on_ready():
    print(f"Bot ON\nUser: {client.user} | Name: {client.user.name} | ID: {client.user.id}")

    await client.change_presence(activity=discord.Game(name=f".help | Melhor Bot de RPG confia"))


@client.event
async def on_button_click(interaction):
    contents = interaction.custom_id.split('.')

    ctx = interaction.message

    if interaction.custom_id.startswith("help"):

        if int(contents[3]) != interaction.user.id:
            print(f'contents[3]: {contents[3]}')
            print(f"interaction.user.id: {interaction.user.id}")
            print('Retornou')
            return

        pages = [secao1(ctx), secao2(ctx), secao3(ctx), secao4(ctx), secao5(ctx)]

        if contents[1] == 'pass_left' and int(contents[2]) > 0:
            print("pá tras")
            print(f'contents[2]: {contents[2]}')
            page = int(contents[2]) - 1
        elif contents[1] == 'pass_right' and int(contents[2]) < len(pages):
            print('pá frente')
            print(f'contents[2]: {contents[2]}')
            page = int(contents[2]) + 1
            print(f'page: {page}')
        else:
            print('pá rado')
            print(f'contents[2]: {contents[2]}')
            print(f"len(pages): {len(pages)}")
            page = int(contents[2])
            print(f'page: {page}')

        buttons = [
            Button(style=ButtonStyle.PRIMARY, emoji="◀️", custom_id=f'help.pass_left.{page}.{interaction.user.id}'),
            Button(style=ButtonStyle.PRIMARY, emoji="▶️", custom_id=f'help.pass_right.{page}.{interaction.user.id}')
        ]
        await ctx.edit(embed=pages[page], components=[buttons])

    elif interaction.custom_id.startswith("server_info"):
        contents = interaction.custom_id.split('.')
        ctx = interaction.message
        if contents[1] == 'raphakawai':
            await ctx.reply('RAPHAEL KAWAAAIIIIIIIIIIII')
        if contents[1] == 'bolo':
            await ctx.reply('BOOOOOLOOOO :cake: :cake::cake: :cake: :birthday: :birthday: :birthday: ')
        if contents[1] == 'festim':
            await ctx.reply('É FEXXXTAAAA :tada: :partying_face: :tada: :partying_face: :tada: :partying_face:')
    else:
        return


@client.event
async def on_member_join(discord_member: discord.Member):
    embed = discord.Embed(
        title=f'Olá {discord_member.name} :man_mage:',
        description=f'Seja muito bem viado, {discord_member.mention}\n.\nSinta-se a vontade para explorar o sevidor.\nQualquer dúvida fique livre para perguntar, \nsempre tem gente online para responder\n',
        color=corConvert('roxo')
    )

    embed.set_author(name=discord_member.guild.name, icon_url=discord_member.guild.icon.url)
    embed.set_thumbnail(url=discord_member.avatar.url)
    embed.set_footer(
        text='Meu criador: Mestre dos magos#0112 (que não ganhou meio centavo pra faze esse bot cof cof mextre cof cof)')
    embed.set_image(
        url="https://media3.giphy.com/media/3oriNPdeu2W1aelciY/giphy.gif?cid=790b7611fe70bf47d18dd4dd5b087742f07aaee586385d44&rid=giphy.gif&ct=g")
    channel = client.get_guild(discord_member.guild.id).get_channel(
        get(discord_member.guild.text_channels, position=0).id)
    print(channel)
    print(embed)
    await channel.send(embed=embed)
