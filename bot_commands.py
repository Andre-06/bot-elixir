# -------------BIBLIOTECAS---------#
from functions import *
from main import client


@client.command(aliases=['r'])
async def roll(ctx, *, dado):
    await ctx.send(rolagem_tag(dado))


@client.command()
async def count(ctx, num, *, frase):
    x = 0
    if frase == 'x':
        num_m = int(num) + 1
        while x < num_m:
            print(x)
            await ctx.send(x)
            x = x + 1
    else:
        num_m = int(num) + 1
        while x < num_m:
            print(x)
            await ctx.send(frase)
            x = x + 1


@client.command(help='Comando Para testes')
async def teste(ctx, test):
    await ctx.send("Testando..." + test)


@client.command()
async def planilha(ctx):
    await ctx.reply(
        "Opa, aqui está o link da planilha: https://docs.google.com/spreadsheets/d/1VfS-zj3nG_nIyK"
        "-O56sRfdn7e7OHeORGVYK6-90TyB4/edit#gid=0\nFaça uma cópia da planilha para poder editá-la indo nos **Menus > "
        "Arquivo > Fazer uma Cópia**. E para adicionar a ficha no bot você deve compartilhar a cópia de sua planilha "
        "com o email **elixiraccount@bot-elixir.iam.gserviceaccount.com** dando a permissão de Editor e usar o "
        "comando `.ficha <personagem> <link>`\n`.help` para mais informações :)")


@client.command(aliases=['conv'])
async def conversor(ctx, metro: int):
    conv_m = round(metro / 3.281 - 0.5)
    conv_f = round(metro * 3.281 - 0.5)

    await ctx.send(f"{metro} metros == {conv_f} pés\n{metro} pés == {conv_m} metros")


@client.command()
async def icon_user(ctx, user: discord.Member):
    await ctx.send(user.avatar.url)


@client.command(aliases=['iconServer'])
async def icon_server(ctx):
    await ctx.send(ctx.guild.icon_url)


@client.command(aliases=['ini'])
async def iniciativa(ctx, *, iniciativa_text):
    # cria uma lista com o que passram na iniciativa e seta as variaveis
    jogador = iniciativa_text.split(',')
    ordem = []
    ordem_to_next = list()
    print(f'jogador: {jogador}')

    # verifica se estao pedindo uma iniciativa com a galera da call
    if 'call' in iniciativa_text:
        # deleta call da lista e acha a call em que a pessoa esta conectada
        del (jogador[item_lista(jogador, 'call')])
        id_canal = ctx.author.voice.channel.id
        print(id_canal)
        canal = client.get_guild(ctx.guild.id).get_channel(id_canal)
        print(canal.members[3].nick)
        for member in canal.members:
            if (member.nick is None or '|' not in member.nick or 'MESTRE' in member.nick.upper() or 'ESPECTANDO'
                    in member.nick.upper() or 'ESPECTADOR' in member.nick.upper() or 'OUVINTE' in member.nick.upper()
                    or 'OUVINDO' in member.nick.upper()):
                pass
            else:
                jogador.append(acharNoNick(member.nick, 'nome').replace(' |', '').replace('|', ''))

    # verifica se tem mais de um elemebnto e coloca a quantiade que tiver
    if '-' in iniciativa_text:
        count = 0
        while count < len(jogador):
            print('AAAAAAAAAAAAAAAAAAA' + jogador[count])
            if '-' in jogador[count]:
                inmigos = jogador[count]
                quantidade = int(jogador[count].split('-')[1])
                print(quantidade)
                countinho = 0
                del (jogador[count])
                while countinho < quantidade:
                    jogador.append(f'{inmigos.split("-")[0]} {countinho + 1}')
                    countinho = countinho + 1
            else:
                count = count + 1

    # remove os espaços que tem no inicio e final e também remove os caracteres especiais
    for i in range(0, len(jogador)):
        player = jogador[0]
        print(f"player: {player}")
        p = player
        player = remover(player, ['all'])
        del (jogador[jogador.index(p)])
        jogador.append(player)
        print(f"jogador: {jogador}")
    # definia a ordem de iniciativa aleatoriamente sem deixar que se repita
    print(f'jogador: {jogador}')
    ini = dict()

    for i in range(0, len(jogador)):
        i = jogador[0]
        print(f'i: {i}')

        dex = await ctx.reply(i.title() + ':\n' + rolagem_tag('1d20')[0], mention_author=False)
        print(f"dex: {dex.content.split(i.title() + ':')[1].split('⟵')[0].replace('`', '')}")
        ini[i] = int(dex.content.split(':\n')[1].split('⟵')[0].replace('`', ''))

        del (jogador[jogador.index(i)])
        jogador.append("passou")
        print(f'jogador: {jogador}')

    print(f'jogador: {jogador}')
    print(f'ini: {ini}')
    ordem_list = list()
    maior = 0
    count = 0
    name = ''
    for i in range(0, len(ini)):
        for i in ini:
            print(f"i: {i}")
            if ini[i] > maior and 'passou' not in i:
                maior = ini[i]
                name = i
                print(f'name: {name}')

        ordem.append(f'{name.title()} ({ini[name]}), ')
        ordem_to_next.append(f'{name.title()} \n')
        print(f'ordem_list: {ordem}')

        ini['passou' + str(count)] = 0
        del ini[name]
        print(f"ini: {ini}")

        maior = 0
        count += 1

    # muda o ultimo item para '.' ao inves de ','
    ordem[len(ordem) - 1] = ordem[len(ordem) - 1].replace(',', '.')

    # coloca, em negritro, a ordem de iniciativa no docs
    ordinha = ''.join(ordem)
    arq = open('iniciativa temp.txt', 'a')
    arq.truncate(0)
    celula = ordem_to_next[0]
    caracter = len(celula) - 2
    ordem_to_next[0] = f'**{celula[:caracter]}** \n'
    arq.writelines(ordem_to_next)

    # envia a ordem de iniciativa
    await ctx.reply(f'Ordem de iniciativa: {str(ordinha)}', mention_author=True)


@client.command(aliases=['v'])
async def view(ctx):
    arq = open('iniciativa temp.txt').readlines()
    msg = 'Ordem de iniciativa:  ' + ', '.join(arq).replace('\n', '') + '.'
    await ctx.send(msg)


@client.command(aliases=['addIni'])
async def addIniciativa(ctx, *, player):
    player = player.title()
    arq = open('iniciativa temp.txt', 'a')
    arq2 = open('iniciativa temp.txt')
    lista = arq2.readlines()

    if 'aleatorio:sim' in player.lower().replace(" ", ''):
        player = player.lower().replace('aleatorio:sim', '').title()
        count = random.randint(0, len(lista))
        lista.insert(count, player + ' \n')
        arq.truncate(0)
        arq.writelines(lista)
    else:
        arq.writelines(player + ' \n')
    await ctx.send('**' + player + '**' + ' adicionado a iniciativa')


@client.command(aliases=['remIni'])
async def remIniciativa(ctx, *, playerRemove):
    arq = open('iniciativa temp.txt', 'r')
    iniciativa = arq.readlines()
    count = 0
    removido = ''
    while count < len(iniciativa):
        print(iniciativa[count].upper())
        print(playerRemove.upper())
        if playerRemove.lower().replace(' ', '') in iniciativa[count].lower().replace(' ', ''):
            if '**' in iniciativa[count]:
                print('tava com **')
                await Next(ctx)
                iniciativa = open('iniciativa temp.txt', 'r').readlines()
                removido = iniciativa[count].replace('\n', '')
                del (iniciativa[count])
                break
            else:
                removido = '**' + iniciativa[count].replace('\n', '') + '**'
                del (iniciativa[count])
                break
        else:
            count = count + 1
            print('num achei nn')
    arq2 = open('iniciativa temp.txt', 'w')
    arq2.truncate(0)
    arq2.writelines(iniciativa)
    await ctx.send(f"{removido} foi removido")


@client.command()
async def paror(ctx):
    await ctx.send('parorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr meoooooooooooooooooooooooooooo')


@client.command(aliases=['eéaqui'])
async def eeaqui(ctx):
    await ctx.send(
        'E é aqui.........................................................................................................................................................................')


@client.command()
async def hm(ctx):
    await ctx.send(
        'HUMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM')


@client.command()
async def analise(ctx):
    await ctx.send('Ué, Analisekkkkkk')


@client.command()
async def Next(ctx):
    arq = open('iniciativa temp.txt', 'r')
    lerArq = arq.readlines()
    print(lerArq)

    count = 0
    vezAtual = 0
    while count < len(lerArq):
        if f"**" in lerArq[count]:
            print(f'entramnos {lerArq[count]}')
            vezAtual = count
            count = count + len(lerArq) + 1
        else:
            print(lerArq[count])
            count = count + 1
            vezAtual = 0

    vezProx = vezAtual + 1
    print(vezAtual)
    lerArq[vezAtual] = lerArq[vezAtual].replace('*', '')
    print(vezProx)
    if vezAtual >= len(lerArq) - 1:
        vezAtual = 0
        vezProx = 0

    celula = lerArq[vezProx]
    caracter = len(celula) - 2
    lerArq[vezProx] = f'**{celula[:caracter]}** \n'
    print(lerArq)
    arq = open('iniciativa temp.txt', 'a')
    count = 0
    ordemToNext = list()
    ordemToNext.append(lerArq)
    arq.truncate(0)
    arq.writelines(lerArq)
    ordem = ''.join(lerArq)
    while count < len(lerArq):
        celula = lerArq[count]
        caracter = len(celula) - 2
        lerArq[count] = f'{celula[:caracter]}, '
        count = count + 1
    print(lerArq)
    lerArq[len(lerArq) - 1] = lerArq[len(lerArq) - 1].replace(',', '.')
    await ctx.reply(
        f"Ordem de Iniciativa: {''.join(lerArq)} \nVez Passada: {''.join(lerArq[vezAtual]).replace(',', '').replace('*', '')}\nVez Atual: {''.join(lerArq[vezProx]).replace(',', '')}",
        mention_author=True)


@client.command(pass_context=True)
async def end(ctx):
    arq = open('iniciativa temp.txt', 'a')
    arq.truncate(0)
    await ctx.send("Combate encerrado")


@client.command(pass_context=True, aliases=['d'])
async def dano(ctx, dado, member: discord.Member):
    print(member)
    rolarDado = rolagem(ctx, dado)
    danoDado = rolarDado[1]
    nickAtual = member.nick

    if "|" in nickAtual:
        partesNick = nickAtual.split('|')
        print(partesNick)
    else:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = acharNoNick(nickAtual, 'nome')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    hpSubtraido = int(hpAtual) - int(danoDado)
    hpFinal = f" {hpSubtraido}/{hpTotal}|"
    flechas = acharNoNick(nickAtual, 'flechas')
    mana = acharNoNick(nickAtual, 'mana')

    nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
    print(nickFinal)

    if hpSubtraido < -6:
        await ctx.reply(
            f"**Dano:** {rolarDado[2]} \n **HP:** {hpAtual} - {danoDado} = **{hpSubtraido}**\n*Press F to pay respect*")
    else:
        await ctx.reply(f"**Dano:** {rolarDado[2]} \n **HP:** {hpAtual} - {danoDado} = **{hpSubtraido}**")

    await member.edit(nick=nickFinal)


@client.command(pass_context=True)
async def mute(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        if member.id != ctx.guild.owner.id and member.bot != True:
            await member.edit(mute=True)
            await ctx.send(f'{member.nick} calou a boquinha com sucesso')
    else:
        await ctx.send('Quem você pensa que é?')


@client.command(pass_context=True, aliases=['desmute'])
async def unmute(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        await member.edit(mute=False)
        await ctx.send(f'{member.nick} voltou a falar merda com sucesso')
    else:
        await ctx.send('Quem você pensa que é?')


@client.command(pass_context=True)
async def muteAll(ctx):
    print(ctx.guild.voice_channels)
    canal = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
    print(canal.members)
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        for member in canal.members:
            if member.id != ctx.guild.owner.id and member.bot != True:
                await member.edit(mute=True)
        else:
            await ctx.send('Todo mundo ficou com a boquinha calada')
    else:
        await ctx.send('Quem você pensa que é?')


@client.command(pass_context=True, aliases=['desmuteall'])
async def unmuteAll(ctx):
    canal = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        for member in canal.members:
            await member.edit(mute=False)
        else:
            await ctx.send('Todo mundo voltou a falar merda')
    else:
        await ctx.send('Quem você pensa que é?')


@client.command(pass_context=True, aliases=['c'])
async def cura(ctx, dado, member: discord.Member):
    rolarDado = rolagem(ctx, dado)
    danoDado = rolarDado[1]
    nickAtual = member.nick
    if "|" in nickAtual:
        partesNick = nickAtual.split('|')
        print(partesNick)
    else:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = acharNoNick(nickAtual, 'nome')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    hpAdicionado = int(hpAtual) + int(danoDado)
    hpFinal = f" {hpAdicionado}/{hpTotal}|"
    mana = acharNoNick(nickAtual, 'mana')
    flechas = acharNoNick(nickAtual, 'flechas')

    nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
    print(nickFinal)

    if int(hpAdicionado) >= int(hpTotal):
        hpFinal = f" {hpTotal}/{hpTotal}|"
        nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
        print(nickFinal)
        await ctx.reply(f"**Cura:** {rolarDado[2]} \n **HP:** {hpAtual} + {danoDado} = **{hpAdicionado}**")
    else:
        await ctx.reply(f"**Cura:** {rolarDado[2]} \n **HP:** {hpAtual} + {danoDado} = **{hpAdicionado}**")

    await member.edit(nick=nickFinal)


@client.command(pass_context=True)
async def hp(ctx, dano, member: discord.Member = None):
    if member == None: member = ctx.author
    nickAtual = member.nick

    if 'd' in dano:
        if dano.startswith('-'):
            dano = dano[1:]
            print(dano)
            sinal = '-'
            rolarDado = rolagem_tag(dano)
            danoDado = rolarDado[1] * -1
        else:
            sinal = '+'
            rolarDado = rolagem_tag(dano[1:])
            danoDado = rolarDado[1]
        ctxReturn = rolarDado[0]
    else:
        danoDado = eval(dano)
        sinal = qualSinal(str(danoDado))
        if sinal == IndexError: sinal = '+'
        ctxReturn = str(danoDado).replace(sinal, '')

    if "|" in nickAtual:
        partesNick = nickAtual.split('|')
        print(partesNick)
    else:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) |f flecha/flecha(se tiver flecha)')

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = acharNoNick(nickAtual, 'nome')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    hpSubtraido = int(hpAtual) + int(danoDado)
    if hpSubtraido > int(hpTotal): hpSubtraido = int(hpTotal)
    hpFinal = f" {hpSubtraido}/{hpTotal}|"
    flechas = acharNoNick(nickAtual, 'flechas')
    mana = acharNoNick(nickAtual, 'mana')

    nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
    if hpSubtraido <= 0:
        await ctx.reply(f"**HP:** {hpAtual} {sinal} {ctxReturn} = **{hpSubtraido}**\n*Press F to pay respect*")
    else:
        await ctx.reply(f"**HP:** {hpAtual} {sinal} {ctxReturn} = **{hpSubtraido}**")

    await member.edit(nick=nickFinal)


@client.command(pass_context=True, aliases=['ml'])
async def magiaLeve(ctx, nick: discord.Member = None):
    print(nick)
    rolarDado = rolagem(ctx, '2d10')
    manaGasta = rolarDado[1]
    manaAtual = ''
    manaTotal = ''
    estagio = ''
    nome = ''
    hp = ''
    flechas = ''
    dadoMagia = ''

    c1d6 = [1, 2, 3, 4, 5]
    c1d8 = [6, 7, 8, 9, 10]
    c1d10 = [11, 12, 13, 14, 15]
    c2d8 = [16, 17, 18, 19, 20]
    if manaGasta in c1d6:
        dadoMagia = '1d6'
        estagio = '1/4'
    if manaGasta in c1d8:
        dadoMagia = '1d8'
        estagio = '2/4'
    if manaGasta in c1d10:
        dadoMagia = '1d10'
        estagio = '3/4'
    if manaGasta in c2d8:
        dadoMagia = '2d8'
        estagio = '**4/4**'

    nickAtual = ctx.message.author.nick
    member = ctx.author
    if nick != None:
        print('entrei')
        nickAtual = nick.nick
        member = nick
    try:
        manaAtual = acharNoNick(nickAtual, 'manaAtual')
        manaTotal = acharNoNick(nickAtual, 'manaTotal')
        nome = acharNoNick(nickAtual, 'nome')
        flechas = acharNoNick(nickAtual, 'flechas')
        hp = acharNoNick(nickAtual, 'hp')
    except:
        await ctx.send(
            'Não consegui reconhecer seu nick, verifique se esta no modelo certo: \nNome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    if manaAtual == None or manaTotal == None:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')
        return

    mana = f"{int(manaAtual) - int(manaGasta)}/{manaTotal}|"
    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(nickFinal)
    await ctx.reply(
        f"Mana Gasta: {rolarDado[2]} \nMana Total: {manaAtual} - {manaGasta} = **{int(manaAtual) - int(manaGasta)}** \nEstágio {estagio} = {dadoMagia}")
    await member.edit(nick=nickFinal)


@client.command(pass_context=True, aliases=['mm'])
async def magiaModerada(ctx, nick: discord.Member = None):
    print(nick)
    rolarDado = rolagem(ctx, '2d30')
    manaGasta = rolarDado[1]
    manaAtual = ''
    manaTotal = ''
    estagio = ''
    nome = ''
    hp = ''
    flechas = ''
    dadoMagia = ''

    c1d8 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    c1d10 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    c2d8 = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    c2d10 = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    c2d12 = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    c4d8 = [51, 52, 53, 54, 55, 56]
    c2d20 = [57, 58, 59, 60]
    if manaGasta in c1d8:
        dadoMagia = '1d8'
        estagio = '1/7'
    elif manaGasta in c1d10:
        dadoMagia = '1d10'
        estagio = '2/7'
    elif manaGasta in c2d8:
        dadoMagia = '2d8'
        estagio = '3/7'
    elif manaGasta in c2d10:
        dadoMagia = '2d10'
        estagio = '4/7'
    elif manaGasta in c2d12:
        dadoMagia = '2d12'
        estagio = '5/7'
    elif manaGasta in c4d8:
        dadoMagia = '4d8'
        estagio = '6/7'
    elif manaGasta in c2d20:
        dadoMagia = '2d20'
        estagio = '**7/7**'
    nickAtual = ctx.message.author.nick
    member = ctx.author
    if nick != None:
        nickAtual = nick.nick
        member = nick
    try:
        manaAtual = acharNoNick(nickAtual, 'manaAtual')
        manaTotal = acharNoNick(nickAtual, 'manaTotal')
        nome = acharNoNick(nickAtual, 'nome')
        flechas = acharNoNick(nickAtual, 'flechas')
        hp = acharNoNick(nickAtual, 'hp')
    except:
        await ctx.send(
            'Não consegui reconhecer seu nick, verifique se esta no modelo certo: \nNome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    if manaAtual == None or manaTotal == None:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')
        return

    mana = f"{int(manaAtual) - int(manaGasta)}/{manaTotal}|"

    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(nickFinal)
    await ctx.reply(
        f"Mana Gasta: {rolarDado[2]} \nMana Total: {manaAtual} - {manaGasta} = **{int(manaAtual) - int(manaGasta)}** \nEstágio {estagio} = {dadoMagia}")
    await member.edit(nick=nickFinal)


@client.command(pass_context=True, aliases=['me'])
async def magiaExtrema(ctx, nick: discord.Member = None):
    rolarDado = rolagem(ctx, '2d50')
    manaGasta = rolarDado[1]
    manaAtual = ''
    manaTotal = ''
    estagio = ''
    nome = ''
    hp = ''
    flechas = ''
    dadoMagia = ''
    manaExtrema = ''

    c2d8menos15 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    c2d12menos10 = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    c2d16menos10 = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    c2d20menos5 = [51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
    c2d20mais5 = [61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
    c2d20mais7 = [71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
    c2d20mais10 = [81, 82, 83, 84, 85, 86, 87, 88, 89]
    c1d50menos15 = [90, 91, 92, 93, 94, 95]
    c1d100menos25 = [96, 97, 98, 99, 100]

    if manaGasta in c2d8menos15:
        dadoMagia = '2d8'
        manaExtrema = 15
        estagio = '1/9'
    elif manaGasta in c2d12menos10:
        dadoMagia = '2d12'
        manaExtrema = 10
        estagio = '2/9'
    elif manaGasta in c2d16menos10:
        dadoMagia = '2d16'
        manaExtrema = 10
        estagio = '3/9'
    elif manaGasta in c2d20menos5:
        dadoMagia = '2d20'
        manaExtrema = 5
        estagio = '4/9'
    elif manaGasta in c2d20mais5:
        dadoMagia = '2d20+5'
        manaExtrema = 0
        estagio = '5/9'
    elif manaGasta in c2d20mais7:
        dadoMagia = '2d20+7'
        manaExtrema = 0
        estagio = '6/9'
    elif manaGasta in c2d20mais10:
        dadoMagia = '2d20+10'
        manaExtrema = 0
        estagio = '7/9'
    elif manaGasta in c1d50menos15:
        dadoMagia = '5d10'
        manaExtrema = 15
        estagio = '8/9'
    elif manaGasta in c1d100menos25:
        dadoMagia = '5d20'
        manaExtrema = 25
        estagio = '**9/9**'

    if manaExtrema == 0:
        streManaExtrema = ''
    else:
        streManaExtrema = f'**- {manaExtrema}**'

    nickAtual = ctx.message.author.nick
    member = ctx.author
    if nick != None:
        nickAtual = nick.nick
        member = nick
    try:
        manaAtual = acharNoNick(nickAtual, 'manaAtual')
        manaTotal = acharNoNick(nickAtual, 'manaTotal')
        nome = acharNoNick(nickAtual, 'nome')
        flechas = acharNoNick(nickAtual, 'flechas')
        hp = acharNoNick(nickAtual, 'hp')
    except:
        await ctx.send(
            'Não consegui reconhecer seu nick, verifique se esta no modelo certo: \nNome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    if manaAtual == None or manaTotal == None:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')
        return

    mana = f" {int(manaAtual) - int(manaGasta) - manaExtrema}/{manaTotal}|"

    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(nickFinal)
    await ctx.reply(
        f"Mana Gasta: {rolarDado[2]} \nMana Total: {manaAtual} - {manaGasta} {streManaExtrema} = **{int(manaAtual) - int(manaGasta) - manaExtrema}** \nEstágio {estagio} = {dadoMagia}")
    await member.edit(nick=nickFinal)


@client.command(aliases=['f'])
async def flecha(ctx, quantidade):
    nickAtual = ctx.message.author.nick

    flechaAtual = acharNoNick(nickAtual, 'flechasAtual')
    flechasTotal = acharNoNick(nickAtual, 'flechasTotal')
    nome = acharNoNick(nickAtual, 'nome')
    hp = acharNoNick(nickAtual, 'hp')
    mana = acharNoNick(nickAtual, 'mana')

    flechaOperada = int(flechaAtual) + int(quantidade)
    print(f'flecha operdaa: {flechaOperada}')
    if flechaOperada > int(flechasTotal.replace('f', '')) and int(flechaAtual) >= int(
            flechasTotal.replace('f', '')) and quantidade.count('+') == 1:
        flechaOperada = flechasTotal.replace('f', '')
        await ctx.reply('Sua aljava ja esta cheia')
    elif flechaOperada < 0 and int(flechaAtual) <= 0 and quantidade.count('-') == 1:
        await ctx.reply('Ops, acabaram-se as flechas, taca o arco mesmo')
    else:
        if flechaOperada < 0:
            flechaOperada = 0
        elif flechaOperada > int(flechasTotal.replace('f', '')):
            flechaOperada = int(flechasTotal.replace('f', ''))

        flechaFinal = f' {flechaOperada}/{flechasTotal}'
        nickFinal = f"{nome}{hp}{mana}{flechaFinal}"
        print(nickFinal)
        await ctx.reply(f'{quantidade} flecha na sua aljava\n{flechaAtual}{quantidade} = {flechaOperada}')
        await ctx.member.edit(nick=nickFinal)


@client.command()
async def full(ctx, token: discord.Member = ''):
    if token == '':
        nickAtual = ctx.message.author.nick
        nickEditar = ctx.message.author
    else:
        nickAtual = token.nick
        nickEditar = token

    nome = acharNoNick(nickAtual, 'nome')
    hp = acharNoNick(nickAtual, 'hp')
    mana = acharNoNick(nickAtual, 'mana')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    manaAtual = acharNoNick(nickAtual, 'manaAtual')
    manaTotal = acharNoNick(nickAtual, 'manaTotal')
    flecha = acharNoNick(nickAtual, 'flechas')
    nick = nickAtual
    final = ''

    if hp != '' and mana != '':
        nick = f"{nome} {hpTotal.replace(' ', '')}/{hpTotal}| {manaTotal.replace(' ', '')}/{manaTotal}|{flecha}"
        final = f'Elixir esta enchendo sua HP e mana `glub glub glub`\nHP: {hpAtual} + {int(hpTotal) - int(hpAtual)} = {hpTotal}\nMana: {manaAtual} + {int(manaTotal) - int(manaAtual)} = {manaTotal}'
    elif hp != '' and mana == '':
        nick = f"{nome} {hpTotal.replace(' ', '')}/{hpTotal}|{mana}{flecha}"
        final = f'Elixir esta enchendo sua HP `glub glub glub`\nHP: {hpAtual} + {int(hpTotal) - int(hpAtual)} = {hpTotal}'
    elif hp == '' and mana == '':
        nick1 = f'HP e Mana nao estao em seu nick'
        await ctx.send(nick1)
    print(nickEditar)
    try:
        await nickEditar.edit(nick=nick)
    except discord.errors.Forbidden:
        await ctx.send('Sou fraco, me falta permissão')
    else:
        await ctx.reply(final)


@client.command(aliases=['s'])
async def sorte(ctx):
    coiso = rolagem(ctx, '1d20')
    dado = int(coiso[1])
    dadoRolagem = coiso[2]
    if dado >= 10:
        await ctx.reply(f'Teste de Sorte\n\nSucesso | {dadoRolagem}', mention_author=True)
    elif dado < 10:
        await ctx.reply(f'Teste de Sorte\n\nFracasso | {dadoRolagem}', mention_author=True)
    else:
        await ctx.reply('uékkkkkk', mention_author=True)


@client.command()
async def calc(ctx, *, conta):
    await ctx.send(f'{conta} = `{eval(conta)}`')


@client.command()
async def help(ctx, page="1"):
    help_embed = discord.Embed(
        title=f'Elixir Comandos\nSeção {1}/{2}:',
        description='Passe para a próxima pagina com .help 2',
        color=6950317
    )

    icon = ctx.guild.icon.url if ctx.guild is not None else None
    nome = ctx.guild.name if ctx.guild is not None else None

    help_embed.set_author(name=nome, icon_url=icon)
    help_embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

    help_embed.add_field(name='.planilha', value='Manda o link da ficha planilha'),
    help_embed.add_field(name='.[iniciativa|ini] <personagens>',
                         value='Rola um teste de destreza dos personagens, caso a ficha esteja adicionada ao bot ou um d20 normal caso contrário, e organiza a ordem de iniciativa. Você pode colocar um "-" do lado para adicionar mais de um personagem/inimigo. Exemplo: .iniciativa player 1, player 2, player 3, inimigo -4',
                         inline=False)
    help_embed.add_field(name='.[addIniciativa|addIni] <personagem>',
                         value='Adiciona o personagem no final da ordem de iniciativa. Você pode escrever "aleatorio:sim" ao final do comando para adicionar o personagem em uma poscição aleatória',
                         inline=False)
    help_embed.add_field(name='.[remIniciativa|remIni] <personagem>',
                         value='Remove o personagem da ordem de iniciativa', inline=False)
    help_embed.add_field(name='.next', value='Mostra o próximo na ordem de iniciativa', inline=False)
    help_embed.add_field(name='.end', value='Encerra a iniciativa', inline=False)
    help_embed.add_field(name='.view', value='Mostra a ordem de iniciativa', inline=False)
    help_embed.add_field(name='.[cura|c] <dado> <@player>',
                         value='Rola um dado de cura e altera no nick', inline=False)
    help_embed.add_field(name='.hp <valor> <@player(opicional)>',
                         value='Altera a hp no seu nick ou no nick de outro player', inline=False)
    help_embed.add_field(name='.[dano|d] <dado> <@player>',
                         value='Rola um dado de dano e altera no nick', inline=False)
    help_embed.add_field(name='.[flecha|f] <quantidade>',
                         value='Altera o seu nick adicionando ou removendo a quantidade', inline=False)
    help_embed.add_field(name='.[magiaLeve|ml]',
                         value='Rola 2d10 de magia, tira a mana de seu nick e mostra o dado de dano que deu',
                         inline=False)
    help_embed.add_field(name='.[magiaModerada|mm]',
                         value='Rola 2d30 de magia, tira a mana de seu nick e mostra o dado de dano que deu',
                         inline=False)
    help_embed.add_field(name='.[magiaExtrema|me]',
                         value='Rola 2d50 de magia, tira a mana de seu nick e mostra o dado de dano que deu',
                         inline=False)
    help_embed.add_field(name='.full <@player>', value='Coloca a vida e a mana(se tiver) no máximo',
                         inline=False)
    help_embed.add_field(name='.[roll|r] <dado>', value='Rola um dado', inline=False)
    help_embed.add_field(name='.[sorte|s]', value='Faz um teste de sorte', inline=False)

    help_embed2 = discord.Embed(
        title=f'Elixir Comandos\nSeção {2}/{2}:',
        description='Volte uma página com .help 1',
        color=6950317
    )

    help_embed2.set_author(name=nome, icon_url=icon)
    help_embed2.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

    help_embed2.add_field(name='.icon_server', value='Mostra o icone do servidor', inline=False)
    help_embed2.add_field(name='.icon_user <@membro>', value='Mostra a foto de perfil do membro marcado',
                          inline=False)
    help_embed2.add_field(name='.calc <conta>', value='Realiza uma conta', inline=False)
    help_embed2.add_field(name='.[conversor|conv] <numero>',
                          value='Converte o numero de feet para metro e de metro para feet', inline=False)
    help_embed2.add_field(name='.mute <@membro>', value='Desativa o microfone de um membro em uma call',
                          inline=False)
    help_embed2.add_field(name='.muteAll',
                          value='Desativa o microfone de todos os membros em uma call que você esteja conectado também',
                          inline=False)
    help_embed2.add_field(name='.unmute <@membro>', value='Reativa o microfone de um membro em uma call',
                          inline=False)
    help_embed2.add_field(name='.[unmuteAll|desmuteall]',
                          value='Reativa o microfone de todos os membros em uma call que você esteja conectado também',
                          inline=False)

    help_embed2.add_field(name='.analise', value='Faz uma analise apurada da situação', inline=False)
    help_embed2.add_field(name='.eéaqui', value='Acaba com a seção e infarta os players', inline=False)
    help_embed2.add_field(name='.count <numero de vezes> <mensagem>',
                          value='Repete uma mesma messagem',
                          inline=False)
    help_embed2.add_field(name='.hm', value='HUMMMMMMMMMMMMMMMMM', inline=False)
    help_embed2.add_field(name='.paror', value='para com tudo', inline=False)
    help_embed2.add_field(name='.reliquias', value='Confirma se ele disse reliquias', inline=False)

    embeds = (help_embed, help_embed2)

    await ctx.send(embed=embeds[int(page) - 1])
