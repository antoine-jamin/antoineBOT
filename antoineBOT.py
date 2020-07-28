import discord
from random import randint
import requests
import html

TOKEN = 'myTOKEN'

CHANNEL_TO_LISTEN = "test-salon"
CHANNEL_TO_WRITE = "nsfw-test"

client = discord.Client()
chanListen = None
chanWrite = None


@client.event
async def on_ready():
    global chanListen, chanWrite
    print("antoineBot is Ready")
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.name == CHANNEL_TO_LISTEN:
                chanListen = client.get_channel(channel.id)
            if channel.name == CHANNEL_TO_WRITE:
                chanWrite = client.get_channel(channel.id)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Si le mot "bot" apparait dans le chan sélectionné --> envoyer une blague dans le chan NSFW sélectionné
    if message.channel == chanListen:
        if 'bot' in message.content.lower():
            nb = randint(1, 3)
            if nb == 1:
                response = requests.get('https://bridge.buddyweb.fr/api/blagues/blagues')
                response.encoding = 'utf-8'
                data = response.json()
                nb = len(html.unescape(data))
                url = 'https://bridge.buddyweb.fr/api/blagues/blagues/' + str(randint(1, nb))
                response = requests.get(url)
                response.encoding = 'utf-8'
                data = response.json()
                await chanWrite.send(html.unescape(data["blagues"]) + "\n©[API blagues from bridge.buddyweb.fr]")
            elif nb == 2:
                response = requests.get('https://www.chucknorrisfacts.fr/api/get?data=tri:alea;type:txt;nb:1')
                response.encoding = 'UTF-8'
                data = response.json()
                await chanWrite.send(html.unescape(data[0]["fact"]) + "\n©[chucknorrisfacts.fr]")
            elif nb == 3:
                response = requests.get("https://api.thecatapi.com/v1/images/search?size=full")
                data = response.json()
                url = data[0]["url"]
                file_name = 'chat.' + url.split(".")[-1]
                file = open(file_name, 'wb')
                file.write(requests.get(url).content)
                fi = discord.File(file_name, filename=file_name)
                await chanWrite.send('Allez une petite pause avec un chat...\n©[thecatapi.com]', file=fi)
            else:
                response = requests.get("https://api.thedogapi.com/v1/images/search?size=full")
                data = response.json()
                url = data[0]["url"]
                file_name = 'chien.' + url.split(".")[-1]
                file = open(file_name, 'wb')
                file.write(requests.get(url).content)
                fi = discord.File(file_name, filename=file_name)
                await chanWrite.send('Allez une petite pause avec un chien...\n©[thedogapi.com]', file=fi)

    # Si quelqu'un envoi un message contenant le mot "blague" --> envoi d'une blague trouvée depuis une API
    if 'blague' in message.content.lower():
        response = requests.get('https://bridge.buddyweb.fr/api/blagues/blagues')
        response.encoding = 'utf-8'
        data = response.json()
        nb = len(html.unescape(data))
        url = 'https://bridge.buddyweb.fr/api/blagues/blagues/' + str(randint(1, nb))
        response = requests.get(url)
        response.encoding = 'utf-8'
        data = response.json()
        await message.channel.send(html.unescape(data["blagues"]) + "\n©[API blagues from bridge.buddyweb.fr]")

    # Si quelqu'un envoi un message contenant les mots "chuck" et/ou "norris" --> envoi d'une chuck norris fact trouvée depuis une API
    if any(word in message.content.lower() for word in ["chuck", "norris"]):
        response = requests.get('https://www.chucknorrisfacts.fr/api/get?data=tri:alea;type:txt;nb:1')
        response.encoding = 'UTF-8'
        data = response.json()
        await message.channel.send(html.unescape(data[0]["fact"]) + "\n©[chucknorrisfacts.fr]")

    # Si quelqu'un envoi un message contenant les mots "coronavirus" et/ou "covid" --> envoi du nombre de décès en France trouvé depuis une API
    if any(word in message.content.lower() for word in ["coronavirus", "covid"]):
        try:
            response = requests.get('https://corona.lmao.ninja/countries/france')
            data = response.json()
            await  message.channel.send(
                str(data["cases"]) + " cas et " + str(
                    data["deaths"]) + " morts en France\n[Sources : corona.lmao.ninja]")
        except:
            fi = discord.File("restezchezvous_site_02.png", filename="restezchezvous_site_02.png")
            await message.channel.send('Pour lutter contre le coronavirus :', file=fi)

    # Si envoi de la commande "&monnaie!pays" --> envoi de la monnaie du pays
    if "&monnaie" in message.content.lower():
        pays = message.content.lower().split('!')[1].split(" ")[0]
        url = 'https://restcountries.eu/rest/v2/alpha/' + str(pays)
        response = requests.get(url)
        try:
            data = response.json()
            await message.channel.send(
                "The currency of " + data["name"] + " is " + data["currencies"][0]["name"] + "\n©[restcountries.eu]")
        except:
            await message.channel.send(
                "Indique le code alpha du Pays après le ! (par exemple monnaie!fr pour la France)")

    # Si envoi de la commande "&tel!pays" --> envoi de l'indicatif téléphonique du pays
    if "&tel" in message.content.lower():
        pays = message.content.lower().split('!')[1].split(" ")[0]
        url = 'https://restcountries.eu/rest/v2/alpha/' + str(pays)
        response = requests.get(url)
        try:
            data = response.json()
            await message.channel.send(
                "The calling codes of " + data["name"] + " is +" + str(
                    data["callingCodes"][0]) + "\n©[restcountries.eu]")
        except:
            await message.channel.send(
                "Indique le code alpha du Pays après le ! (par exemple tel!fr pour la France)")

    # Si envoi de la commande "&ville!codepostal" --> envoi du noms des villes correpondant au code postal
    if "&ville" in message.content.lower():
        cp = message.content.lower().split('!')[1].split(" ")[0]
        url = 'http://api.zippopotam.us/fr/' + str(cp)
        response = requests.get(url)
        data = response.json()
        rep_string = ""
        try:
            for i, place in enumerate(data["places"]):
                rep_string += place["place name"] + " ; "
            await message.channel.send(rep_string + "\n©[zippopotam.us]")
        except:
            await message.channel.send("Pas de ville correspondant à ce code postal")

    # Si la commande &chat ou &cat apparait --> envoi d'une image de chat trouvée sur une API
    if any(word in message.content.lower() for word in ["&chat", "&cat"]):
        response = requests.get("https://api.thecatapi.com/v1/images/search?size=full")
        data = response.json()
        url = data[0]["url"]
        file_name = 'chat.' + url.split(".")[-1]
        file = open(file_name, 'wb')
        file.write(requests.get(url).content)
        fi = discord.File(file_name, filename=file_name)
        await message.channel.send('Tu aimes les chats ???\n©[thecatapi.com]', file=fi)

    # Si la commande &chien ou &dog apparait --> envoi d'une image de chat trouvée sur une API
    if any(word in message.content.lower() for word in ["&chien", "&dog"]):
        response = requests.get("https://api.thedogapi.com/v1/images/search?size=full")
        data = response.json()
        url = data[0]["url"]
        file_name = 'chien.' + url.split(".")[-1]
        file = open(file_name, 'wb')
        file.write(requests.get(url).content)
        fi = discord.File(file_name, filename=file_name)
        await message.channel.send('Tu aimes les chiens ???\n©[thedogapi.com]', file=fi)

client.run(TOKEN)
