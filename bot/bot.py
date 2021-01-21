import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import numpy
import pickle
import copy
import os


start_str = "Hola! Soc un bot d'enquestes.\nMira /help per més informació"

help_str = """/start inicia la conversa amb el Bot.\n
/help el Bot mostra aquest text.\n
/author dóna el nom i el correu del autor.\n
/quiz <idEnquesta> inicia la enquesta amb el idEnquesta especificat.\n
/bar <idPregunta> el Bot retorna una gràfica de barres mostrant un diagrama de barres de les respostes a la pregunta donada.\n
/pie <idPregunta> el Bot retorna una gràfica de formatget amb el percentatge de les respostes a la pregunta donada.\n
/report el Bot retorna una taula amb el nombre de respostes obtingudes per cada valor de cada pregunta.\n
/abort anulem la enquesta que estem fent per poder fer-ne una altre, tot i que les respostes enviades fins
al moment es guardaran igualment\n"""

contact_str = "Josep Maria Olivé\n_@est.fib.upc.edu"


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=start_str)


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=help_str)


def author(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=contact_str)


def quiz(bot, update, user_data):
    if len(user_data) == 0:
        # Inicialitzem la enquesta
        # Nom de la enquesta borrant el "/quiz "
        name_enquesta = update.message.text[6:]
        if len(name_enquesta) == 0:
            # No ens han enviat el id
            update.message.reply_text('/quiz <idEnquesta>')
        else:
            user_data['enquesta'] = name_enquesta
            user_data['node'] = name_enquesta
            user_data['lastNodeNonAlt'] = []
            update.message.reply_text('Enquesta '+name_enquesta+':')
            generateNextMessage(bot, update, user_data)
    else:
        # Evitem la invocació /quiz quan ja estem executant un
        update.message.reply_text('Ja tens un questionari en marxa, acaba abans!')


def incomingMessage(bot, update, user_data):
    if len(user_data) == 0:
        # Ens envien qualsevol missatge sense estar relacionat amb una comanda
        update.message.reply_text('Consulta /help per les comandes disponibles')
    else:
        generateNextMessage(bot, update, user_data)


# Retorna la seguent pregunta a la que anar,
# basat en el graf G, al node i i amb
# resposta numero n
def getNextNode(G, i, n, user_data):
    node = copy.copy(i)
    for u, v, a in G.edges(data=True):
        if u == i and 'label' in a and a['label'] == str(n) and 'color' in a and a['color'] == 'green':
            user_data['lastNodeNonAlt'] += [u]
            return v, user_data
        elif u == i and len(a) == 0:
            node = v
    return node, user_data


# Retorna el node seguent apuntat per una
# fletxa negra (sequencia llista)
def getNextNodeInSequence(G, i):
    for u, v, a in G.edges(data=True):
        if u == i and len(a) == 0:
            return v


# Retorna el node amb les respostes de la
# pregunta que conte i
def getRespostes(G, i):
    for u, v, a in G.edges(data=True):
        if u == i and 'color' in a and a['color'] == 'blue':
            return v


# Incrementem en 1 el contador de la resposta
# que ens dóna l'usuari
def addResponseCount(idPregunta, m, G, node, update):
    # Augmentem o inicialitzem la entrada
    # de forma general
    file = open('respostes', 'rb')
    llistaRespostes = pickle.load(file)
    file.close()

    exists = False
    for u, v, c in G.nodes[node]['content']:
        if u == m:
            exists = True
    if not exists:
        update.message.reply_text('La resposta no és correcta i no es guardarà 💣\nPassant a la següent pregunta')
        return

    if (idPregunta, m) in llistaRespostes:
        llistaRespostes[(idPregunta, m)] = llistaRespostes[idPregunta, m] + 1
    else:
        llistaRespostes[(idPregunta, m)] = 1

    file = open('respostes', 'wb')
    pickle.dump(llistaRespostes, file)
    file.close()


# Llegeix el graf, mira el missatge rebut, i en cas que sigui
# necessari guarda la resposta que rep, a més a més envia el
# seguent missatge de la cadena, i en el cas necessari, fa
# backtracking i continua fina arribar a el node END
def generateNextMessage(bot, update, user_data):
    try:
        file = open('enquestes/'+user_data['enquesta'], 'rb')
    except Exception as e:
        # Avisem al usuari si la enquesta
        # que vol no la tenim disponible
        update.message.reply_text('La enquesta '+user_data['enquesta']+' no existeix 💣')
        user_data.clear()
        return

    # Carreguem el graf
    G = pickle.load(file)
    # Missatge rebut
    m = update.message.text

    if user_data['node'] != user_data['enquesta'] and user_data['node'] != 'END':
        # Hem d'incrementar el comptador de la resposta que ens donen
        # i guardar-lo
        addResponseCount(user_data['node'], m, G, getRespostes(G, user_data['node']), update)

    # Avançem al seguent node, amb preferencia als nodes alternativa
    # basats en la resposta que donem
    i, user_data = getNextNode(G, user_data['node'], m, user_data)

    if i == user_data['node']:
        # Ens quedem al mateix node del que veniem == estem a un node
        # alternativa, que no té cap camí més i hem de fer
        # backtracking i buscar el seguent a node basats en l'ultim cop
        # que vem pendre un camí alternatiu
        i = getNextNodeInSequence(G, user_data['lastNodeNonAlt'][len(user_data['lastNodeNonAlt'])-1])
        user_data['lastNodeNonAlt'].pop()

    if str(i) != 'END':
        # Hem d'enviar la pregunta i respostes
        # del node al que ens trobem
        r = getRespostes(G, i)
        respostes = ''
        for u, v, c in G.nodes[r]['content']:
            respostes += u+': '+v+'\n'
        missatge = user_data['enquesta']+'> '+G.nodes[i]['content']+'\n'+respostes
        update.message.reply_text(missatge)

        # Guardem el ultim node del que hem enviat la
        # informació, i del que hem de guardar la
        # resposta que ens donin amb el seguent missatge
        user_data['node'] = i

    else:
        # Missatge de finalització
        update.message.reply_text(user_data['enquesta']+'> No hi ha més preguntes.\nGràcies pel teu temps!')
        # Borrem les dades per tal de permetre que
        # es comenci una nova enquesta
        user_data.clear()


def bar(bot, update):
    # Carreguem les respostes
    file = open('respostes', 'rb')
    llistaRespostes = pickle.load(file)
    file.close()

    # Missatge rebut, sense el /bar
    m = update.message.text[5:]

    if len(m) == 0:
        update.message.reply_text('/bar <idPregunta>')

    else:
        # Llistes per les barres
        values = []
        counters = []
        for (pregID, valor), count in llistaRespostes.items():
            if pregID == m:
                values.append(str(valor))
                counters.append(int(count))

        # Create bars
        x_pos = list(range(len(values)))
        plt.bar(x=x_pos, height=counters)
        plt.xticks(x_pos, values)
        plt.savefig('bar.png')
        plt.clf()

        # Enviem la foto
        bot.send_photo(chat_id=update.message.chat_id, photo=open('bar.png', 'rb'))
        os.remove('bar.png')


def pie(bot, update):
    # Carreguem les respostes
    file = open('respostes', 'rb')
    llistaRespostes = pickle.load(file)
    file.close()

    # Missatge rebut, sense el /pie
    m = update.message.text[5:]

    if len(m) == 0:
        update.message.reply_text('/pie <idPregunta>')

    else:
        # Llistes per les pie
        values = []
        counters = []
        for (pregID, valor), count in llistaRespostes.items():
            if pregID == m:
                values.append(str(valor))
                counters.append(int(count))

        # Create pie
        x_pos = list(range(len(values)))
        plt.pie(x=counters, labels=values, autopct='%1.1f%%')
        plt.savefig('pie.png')
        plt.clf()

        # Enviem la foto
        bot.send_photo(chat_id=update.message.chat_id, photo=open('pie.png', 'rb'))
        os.remove('pie.png')


def report(bot, update):
    # Missatge a enviar
    missatge = '*pregunta   valor   respostes*\n'

    # Obrim les respostes
    file = open('respostes', 'rb')
    llistaRespostes = pickle.load(file)
    file.close()

    if len(llistaRespostes) > 0:
        # Acumula les respostes
        for (pregID, valor), count in sorted(llistaRespostes.items()):
            missatge += pregID+'   '+valor+'   '+str(count)+'\n'
    else:
        # Indiquem que està buit
        missatge = '*No hi ha cap resposta guardada*'

    # Envia el missatge
    update.message.reply_text(missatge, parse_mode=telegram.ParseMode.MARKDOWN)


def abort(bot, update, user_data):
    # Reset a les dades
    if len(user_data) == 0:
        update.message.reply_text('No tens cap enquesta iniciada')
    else:
        user_data.clear()
        update.message.reply_text('Enquesta parada, ja pots iniciar una de nova')


# CODI MAIN DEL SCRIPT
TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Enllaç de funcions i comandes
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('quiz', quiz, pass_user_data=True))
dispatcher.add_handler(CommandHandler('bar', bar))
dispatcher.add_handler(CommandHandler('pie', pie))
dispatcher.add_handler(CommandHandler('report', report))
dispatcher.add_handler(CommandHandler('abort', abort, pass_user_data=True))
dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=incomingMessage, pass_user_data=True))

# Evitem que s'intentin crear finestres al plt
matplotlib.use('agg')

# Estructura extra per guardar el resultat de totes les enquestes
# cojuntament
# Llista de llistes: estructura
# llistaRespostes['pregunta', 'valor'] = {'respostes': '0'}
try:
    # Obrim el fitxer ja existent, per veure si hi és
    file = open('respostes', 'rb')
    llistaRespostes = pickle.load(file)
    file.close()
except Exception:
    # Inicialitzem el fitxer de 0
    file = open('respostes', 'wb')
    llistaRespostes = {}
    pickle.dump(llistaRespostes, file)
    file.close()
    print("S' ha creat un nou arxiu respostes al directori bot/enquestes/")

# StartUp
updater.start_polling()
