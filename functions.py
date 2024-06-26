import random
import discord


def rolagem_tag(dado):
    dado = dado.replace(" ", '')
    finalFinal = []
    resultadoFinal = []
    monteDeDadosSFinal = []
    limite = f"` XXXX ` ⟵  [Limite Alcançado]"

    if '#' in dado:
        rollSeparado = int(dado.split("#")[0])
        dado = dado.split('#')[1]
        if rollSeparado > 100: return limite
    else:
        rollSeparado = 1

    for i in range(0, rollSeparado):

        ###################### PRIMEIRA PARTE SÓ ############

        dadoS = []
        dadoM = []
        soma = []
        min = []

        dados = dado.split('+')
        print(f'dados: {dados}')
        for d in dados:
            print(f'd: {d}')
            if 'd' in d and '-' not in d:
                print('entrou 1: dado puro')
                dadoS.append(d)
            elif '-' in d:
                newDados = d.split('-')
                print(f'newDados: {newDados}')
                if 'd' in newDados[0]:
                    print('entrou 2: primeiro dado do split -')
                    dadoS.append(newDados[0])
                elif newDados[0] != '':
                    print('entrou 3: primeiro numero do split -')
                    soma.append(int(d.split('-')[0]))
                del (newDados[0])
                print(f"newDados new: {newDados}")
                for newD in newDados:
                    print(f'newD: {newD}')
                    if newD == '':
                        print('entrou 4: vazio antes do split -')
                        pass
                    elif 'd' in newD:
                        print('entrou 5: dado puro negativo')
                        dadoM.append(newD)
                    else:
                        print('entrou 6: numero negativo')
                        min.append(int(newD))
            else:
                print('entrou 7: numero positivo')
                soma.append(int(d))

        if len(dadoS) > 10 or len(dadoM) > 10:
            return limite

        #######################   ROLAGEM RANDOMICA   ######################

        monteDeDadosS = []
        monteDeDadosM = []

        if dadoS != []:
            for d in dadoS:
                qntD = d.split('d')[0]
                if qntD == '':
                    qntD = 1
                else:
                    qntD = int(qntD)
                numD = int(d.split('d')[1])

                if qntD > 100 or numD > 500: return limite

                for i in range(0, qntD):
                    ran = random.randint(1, numD)
                    if ran == numD:
                        monteDeDadosS.append(ran + 10000)
                    else:
                        monteDeDadosS.append(ran)
            else:
                monteDeDadosS.sort(reverse=True)

        if dadoM != []:
            for d in dadoM:
                qntD = d.split('d')[0]
                if qntD == '':
                    qntD = 1
                else:
                    qntD = int(qntD)
                numD = int(d.split('d')[1])

                if qntD > 100 or numD > 500: return limite

                for i in range(0, qntD):
                    ran = random.randint(1, numD)
                    if ran == numD:
                        monteDeDadosM.append(ran + 10000)
                    else:
                        monteDeDadosM.append(ran)
            else:
                monteDeDadosM.sort(reverse=True)

        print(f'monteDeDadosS: {monteDeDadosS}')
        print(f'monteDeDadosM: {monteDeDadosM}')
        print(f'sum: {soma}')
        print(f'min: {min}')

        #######################  TOTAIS  ######################

        totalS = 0
        for i in monteDeDadosS:
            if i > 10000:
                totalS = totalS + i - 10000
            else:
                totalS = totalS + i

        totalM = 0
        for i in monteDeDadosM:
            if i > 10000:
                totalM = totalM + i - 10000
            else:
                totalM = totalM + i

        totalSum = sum(soma)

        totalMin = sum(min)

        resultado = totalS - totalM + totalSum - totalMin

        #######################  STR DO SUM E MIN  ######################

        sumStrComp = []
        if soma == []:
            sumStrComp = ''
        else:
            for i in soma:
                sumStrComp.append(str(i))

        minStrComp = []
        if min == []:
            minStrComp = ''
        else:
            for i in min:
                minStrComp.append(str(i))

        #######################  EXTREMO DESASTRE  ######################

        count = 0
        while count < len(monteDeDadosM):
            i = monteDeDadosM[count]
            try:
                if i > 10000:
                    monteDeDadosM[count] = '**' + str(i - 10000) + '**'
                elif i == 1:
                    monteDeDadosM[count] = '**' + str(i) + '**'
            except TypeError:
                pass
            count = count + 1

        count = 0
        while count < len(monteDeDadosS):
            i = monteDeDadosS[count]
            try:
                if i > 10000:
                    monteDeDadosS[count] = '**' + str(i - 10000) + '**'
                elif i == 1:
                    monteDeDadosS[count] = '**' + str(i) + '**'
            except TypeError:
                pass
            count = count + 1

        #######################  FINALIZAÇÕES  ######################

        if totalSum != 0:
            finalSoma = f" + {' + '.join(sumStrComp)}"
        else:
            finalSoma = ''

        if totalMin != 0:
            finalMenos = f" - {' - '.join(minStrComp)}"
        else:
            finalMenos = ''

        if totalM != 0:
            finalDadosNegativos = f" - {monteDeDadosM} {'-'.join(dadoM)}"
        else:
            finalDadosNegativos = ''

        if totalS != 0:
            finalBasico = f"{monteDeDadosS} {'+'.join(dadoS)}"
        else:
            finalBasico = ''

        final = f"` {resultado} ` ⟵  " + finalBasico + finalDadosNegativos + finalSoma + finalMenos
        resultadoFinal.append(resultado)
        monteDeDadosSFinal.append(monteDeDadosS)
        finalFinal.append(final)

    return ('\n'.join(finalFinal), sum(resultadoFinal), monteDeDadosSFinal, resultadoFinal)


def rolagem(ctx, dado):
    print(ctx)
    if '+' in dado:
        posicao = dado.split('d')
        print(posicao)
        print(posicao[0])
        print(posicao[1])
        separa = posicao[1].split('+')
        soma = int(separa[1])
        x = posicao[0]
        if x == '':
            x = 1
        else:
            x = int(x)
        y = int(separa[0])
        print(type(x))
        print(x)
        if x > 100:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        elif y > 300:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        else:
            count = 0
            maisDeUmDado = 0
            todosOsDados = []
            while x > count:
                deu = random.randint(1, y)
                maisDeUmDado = maisDeUmDado + deu
                todosOsDados.append(deu)
                count = count + 1
                print(todosOsDados)

        resultado = maisDeUmDado + soma
        print(separa)


    elif '-' in dado:
        posicao = dado.split('d')
        separa = posicao[1].split('-')
        soma = int(separa[1])
        x = posicao[0]
        if x == '':
            x = 1
        else:
            x = int(x)
        y = int(separa[0])
        if x > 100:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        elif y > 300:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        else:
            count = 0
            maisDeUmDado = 0
            todosOsDados = []
            while x > count:
                deu = random.randint(1, y)
                maisDeUmDado = maisDeUmDado + deu
                todosOsDados.append(deu)
                count = count + 1
                print(todosOsDados)

        resultado = int(maisDeUmDado) - soma
        print(separa)

    else:
        soma = 0
        posicao = dado.split('d')
        x = posicao[0]
        if x == '':
            x = 1
        else:
            x = int(x)
        y = int(posicao[1])
        if x > 100:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        elif y > 300:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        else:
            count = 0
            maisDeUmDado = 0
            todosOsDados = []
            while count < x:
                deu = random.randint(1, y)
                maisDeUmDado = maisDeUmDado + deu

                todosOsDados.append(deu)
                count = count + 1
                print(todosOsDados)
            resultado = int(maisDeUmDado)

    if ctx != '1':
        print(posicao)
        if type(todosOsDados) == str:
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            finalNal = ctx.reply(final, mention_author=True)
            return (finalNal, resultado, final, deu)
        else:
            todosOsDados.sort(reverse=True)
            print(todosOsDados)
            count = 0
            while count < len(todosOsDados):
                if todosOsDados[count] == 1 or todosOsDados[count] == y:
                    todosOsDados[count] = f'**{todosOsDados[count]}**'
                    print(todosOsDados[count])
                else:
                    count = count + 1
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            finalNal = ctx.reply(final, mention_author=True)
            return (finalNal, resultado, final, todosOsDados, maisDeUmDado)
    if ctx == '1':
        print(posicao)
        if type(todosOsDados) == str:
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            return (resultado, final, deu)
        else:
            todosOsDados.sort(reverse=True)
            print(todosOsDados)
            count = 0
            while count < len(todosOsDados):
                if todosOsDados[count] == 1 or todosOsDados[count] == y:
                    todosOsDados[count] = f'**{todosOsDados[count]}**'
                    print(todosOsDados[count])
                else:
                    count = count + 1
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            return (resultado, final, todosOsDados, maisDeUmDado)


def item_lista(lista, itemAchar):
    count = 0
    for item in lista:
        if str(itemAchar).lower() in str(item).lower():
            return count
        else:
            count = count + 1
    else:
        return IndexError


def qualSinal(atribute):
    if '+' in atribute and '-' in atribute:
        return 'Ih rapaz'
    elif '+' in atribute:
        return '+'
    elif '-' in atribute:
        return '-'
    elif '>' in atribute:
        return '>'
    elif '<' in atribute:
        return '<'
    elif '+' in atribute:
        return '+'
    elif '*' in atribute:
        return '*'
    elif '/' in atribute:
        return '/'
    elif '^' in atribute:
        return '^'
    else:
        return IndexError


def corConvert(color):
    if color == 'verde':
        cor = 32768
    elif color == 'azul':
        cor = 255
    elif color == 'roxo':
        cor = 6950317
    elif color == 'rosa':
        cor = 16718146
    elif color == 'preto':
        cor = 000000
    elif color == 'branco':
        cor = 16777215
    elif color == 'laranja':
        cor = 16753920
    elif color == 'amarelo':
        cor = 16776960
    elif color == 'vermelho':
        cor = 16711680
    elif color == 'ciano':
        cor = 3801067

    else:
        cor = 'Desculpe, não achei essa cor. Tente colocar o código decimal. \nSite para a conversão de decimal: https://convertingcolors.com/'

    return cor


def acharNoNick(nick, achar):
    print('---INICIO-----------INICIO-------------INICIO--------------------INICIO---------')

    if "|" in nick:
        partesNick = nick.split('|')
        print(partesNick)
    elif 'I' in nick:
        partesNick = nick.split('I')
        print(partesNick)
    elif 'l' in nick:
        partesNick = nick.split('l')
        print(partesNick)
    else:
        return None

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = partesNick[0] + '|'
    hp = partesNick[1] + '|'
    hpAtual = partesNick[1].split('/')[0]
    hpTotal = partesNick[1].split('/')[1]
    flechas = ''
    flechasAtual = ''
    flechasTotal = ''
    manaTotal = ''
    manaAtual = ''
    mana = ''

    count = 0
    while count < len(partesNick):
        print(f"parte do nick analisado: {partesNick[count]}")
        if partesNick[count].replace(' ', '') == '':
            del (partesNick[count])
            print(f'nick tava vazio')
            count = count + 1
        else:
            print(f'nick nn tava vaio')
            count = count + 1

    if len(partesNick) == 3:
        # Maugrin Maugrin , 40/40 , 500/500
        # Maugrin Maugrin , 40/40 , f 20/20

        if 'f' in partesNick[2]:
            # Maugrin Maugrin , 40/40 , f 20/20
            flechas = partesNick[2]
            flechasAtual = partesNick[2].split('/')[0]
            flechasTotal = partesNick[2].split('/')[1]
        else:
            # Maugrin Maugrin , 40/40 , 500/500
            mana = partesNick[2]
            manaAtual = partesNick[2].split('/')[0]
            manaTotal = partesNick[2].split('/')[1]

    elif len(partesNick) == 4:
        # Maugrin Maugrin , 40/40 , 500/500 , f 20/20

        mana = partesNick[2] + '|'
        manaAtual = partesNick[2].split('/')[0]
        manaTotal = partesNick[2].split('/')[1]
        flechas = partesNick[3]
        flechasAtual = partesNick[3].split('/')[0]
        flechasTotal = partesNick[3].split('/')[1]

    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(f"nome: {nome}")
    print(f"hp: {hp}")
    print(f"hpAtual: {hpAtual}")
    print(f"hpTotal: {hpTotal}")
    print(f"flechas: {flechas}")
    print(f"flechasAtual: {flechasAtual}")
    print(f"flechasTotal: {flechasTotal}")
    print(f"manaTotal: {manaTotal}")
    print(f"manaAtual: {manaAtual}")
    print(f"mana: {mana}")
    print(f"nickFinal: {nickFinal}")

    if achar == 'nome':
        return nome
    elif achar == 'hp':
        return hp
    elif achar == 'hpAtual':
        return hpAtual
    elif achar == 'hpTotal':
        return hpTotal
    elif achar == 'mana':
        return mana
    elif achar == 'manaTotal':
        return manaTotal
    elif achar == 'manaAtual':
        return manaAtual
    elif achar == 'flechas':
        return flechas
    elif achar == 'flechasAtual':
        return flechasAtual
    elif achar == 'flechasTotal':
        return flechasTotal
    elif achar == 'nickFinal':
        return nickFinal
    else:
        return int('aaa')

    print('--FIM------------------------FIM--------------------FIM---------------FIM-----')


def remover(txt: str, char: list = ['all']):
    charList = ['!', '@', '#', '$', '%', '¨', '&', '*', '(', ')', '_', '-', ',', '.', '<', '>',
                '[', ']', '{', '}', '\'', ";", ":", '/', '?', 'º', '"', "'", '|', ' ']

    if char[0] == 'all':
        charUse = charList
    else:
        charUse = char

    for i in charUse:
        txt = txt.replace(i, '')
    else:
        return txt
