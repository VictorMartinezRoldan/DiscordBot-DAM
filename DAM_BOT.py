import discord
import requests
import json
import re
import time

# ---------------------------------------------------------------------------------

webhook_url = '' # CAMBIALO POR TU URL DEL WEBHOOK DE TU SERVIDOR DE DISCORD

bot_token = "" # CAMBIALO POR EL TOKEN DE TU BOT REGISTRADO EN: https://discord.com/developers

# ---------------------------------------------------------------------------------

payload = {
    "content": "@everyone",
    "embeds": [
        {
            "title": "**Se ha detectado un lenguaje humano!!!**."
        }
    ]
}

# pip install discord
def limpiar():
    clear_screen = "\033[H\033[J"
    print(clear_screen)
def ExtraerTexto(code):
    text = re.search(r'```(.*?)```', code, re.DOTALL)
    return text.group(1).strip()
def DetectarLenguaje(code):
    # ---------------------------------------------------------------------
    code = '\n'.join(line for line in code.splitlines())
    code_words = re.findall(r'\b\w+\b|[^\w\s]', code)
    contadorPYTHON=0
    contadorJAVA=0
    # ES PYTHON ?
    for elemento in code_words:
        if "#" in elemento:
            contadorPYTHON+=1
        if "lambda" in elemento:
            contadorPYTHON+=1
        if "pandas" in elemento:
            contadorPYTHON+=1
        if "print" in elemento:
            contadorPYTHON+=1
        if "def" in elemento:
            contadorPYTHON+=1
        if "(" and ")" and "input" in elemento:
            contadorPYTHON+=1
        if "str" in elemento:
            contadorPYTHON+=1
    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # Declarativa que se debe cambiar cuando estemos dando JAVA.
    # Este detector es TERMINAL, es decir, lo encuentra y entiende que es python directamente sin comparar nada.
    for elemento in code_words:
        if "=" in elemento:
            for elemento in code_words:
                if "[" in elemento:
                    for elemento in code_words:
                        if "]" in elemento:
                            contadorPYTHON="Se a detectado una LISTA de python."
                            return "python"
                            #contadorPYTHON+=1
    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # Herramienta para buscar funciones de python:
    x1=0
    x2=0
    x3=0
    intentos=0
    for posición, elemento in enumerate(code_words):
        if elemento == "(":
            x1 = posición
        if elemento == ')':
            x2 = posición
        if elemento == ':':
            x3 = posición
        if x1 > 0 and x2 > 0 and x3 > 0 and x1 == x2-1 and x2 == x3-1 and x1 == x3-2:
            contadorPYTHON+=1
            x1=0
            x2=0
            x3=0
        if elemento != ')' and elemento != '(' and elemento != ':':
            intentos+=1
        elif x1 > 0 and x2 > 0 and x3 > x2 == x3-1 and x3 == x2+1:
            contadorPYTHON+=1
            x1=0
            x2=0
    # Buscar list( en python
    x1=0
    x2=0
    intentos=0
    for posición, elemento in enumerate(code_words):
        if elemento == "list":
            x1 = posición
        if elemento == '(':
            x2 = posición
        if x1 > 0 and x2 > 0 and x1 == x2-1 and x2 == x1+1:
            contadorPYTHON+=1
            x1=0
            x2=0
        if elemento != 'list' and elemento != '(':
            intentos+=1
    # Buscar = range y in range en python
    x1=0
    x2=0
    intentos=0
    for posición, elemento in enumerate(code_words):
        if elemento == "=":
            x1 = posición
        if elemento == 'range':
            x2 = posición
        if x1 > 0 and x2 > 0 and x1 == x2-1 and x2 == x1+1:
            contadorPYTHON+=1
            x1=0
            x2=0
        if elemento != '=' and elemento != 'range':
            intentos+=1
    for posición, elemento in enumerate(code_words):
        if elemento == "in":
            x1 = posición
        if elemento == 'range':
            x2 = posición
        if x1 > 0 and x2 > 0 and x1 == x2-1 and x2 == x1+1:
            contadorPYTHON+=1
            x1=0
            x2=0
        if elemento != 'in' and elemento != 'range':
            intentos+=1
    #-----------------------------------------------
    # Buscadores mixtos:
    # Diferenciador entre while de python y de java:
    if "while" in code_words and not ";" in code_words:
        if not "println" in code_words:
            contadorPYTHON+=1
    elif "while" in code_words and "{" in code_words and "}" in code_words and ";" in code_words:
        if not "print" in code_words and not "def" in code_words:
            contadorJAVA+=1
    #-----------------------------------------------
    # ES JAVA?
    for elemento in code_words:
        if ";" in elemento:
            contadorJAVA+=1
        if "//" in elemento:
            contadorJAVA+=1
        if "println" in elemento:
            contadorJAVA+=1
        if "scanner" in elemento:
            contadorJAVA+=1
        if "Scanner" in elemento:
            contadorJAVA+=1
        if "void" in elemento:
            contadorJAVA+=1
        if "java" in elemento:
            contadorJAVA+=1
        if "args" in elemento:
            contadorJAVA+=1
    # Buscador de ") {" presente en java:
    x1=0
    x2=0
    for posición, elemento in enumerate(code_words):
        if elemento == ")":
            x1 = posición
        if elemento == '{':
            x2 = posición
        if x1 == x2-1 and x2 == x1+1:
            contadorJAVA+=1
            x1=0
            x2=0
    # Buscador de "= variable ;" presente en java:
    x1=0
    x2=0
    for posición, elemento in enumerate(code_words):
        if elemento == "=":
            x1 = posición
        if elemento == ';':
            x2 = posición
        if x1 > 0 and x1 == x2-2 and x2 == x1+2:
            contadorJAVA+=1
            x1=0
            x2=0
        # Buscador de "public class" presente en java:
        x1=0
        x2=0
        for posición, elemento in enumerate(code_words):
            if elemento == "public":
                x1 = posición
            if elemento == 'class':
                x2 = posición
            if x1 == x2-1 and x2 == x1+1:
                contadorJAVA+=1
                x1=0
                x2=0
        print("-------------------------------")
        print("Coincidencias con python: ", contadorPYTHON)
        print("Coincidencias con java: ", contadorJAVA)
        print("-------------------------------")
        if contadorPYTHON > 1 and contadorPYTHON > contadorJAVA:
            print("Lenguaje detectado: Python")
            return "python"
        elif contadorJAVA > 1 and contadorJAVA > contadorPYTHON:
            print("Lenguaje detectado: Java")
            return "java"
        else:
            limpiar()
            PintarCara2()
            print("---------------------------------------------------")
            print("Se a detectado lenguaje humano")
            requests.post(webhook_url,data=json.dumps(payload),headers={'Content-Type': 'application/json'})
            print("---------------------------------------------------")
            print("Tengo una preguntilla para asegurarme...     ")
            print("---------------------------------------------------")
            Decisión = input("Es lenguaje humano? [s], en caso contrario indica el idioma con [p] o [j]: ")
            if Decisión == "s":
                limpiar()
                PintarCara()
                return "lenguaje humano"
            elif Decisión == "p":
                return "python"
            elif Decisión == "j":
                return "java"
            # La variable se queda con texto.

NumVálidos=[1,2,3,4,5,6,7,8,9,10]

# Aquí puedes cambiar los nombres de los canales y su ID

def ID_ChannelSearch(n):
    if n == 1:
        ResponseAsigAndID=[':bell:Exámenes:bell:', ID]
        return ResponseAsigAndID
    if n == 2:
        ResponseAsigAndID=['General', ID]
        return ResponseAsigAndID
    if n == 3:
        ResponseAsigAndID=['Alumnos', ID]
        return ResponseAsigAndID
    if n == 4:
        ResponseAsigAndID=['Dudas-Clase', ID]
        return ResponseAsigAndID
    if n == 5:
        ResponseAsigAndID=['Programación:computer:', ID]
        return ResponseAsigAndID
    if n == 6:
        ResponseAsigAndID=['Lenguaje de Marcas', ID]
        return ResponseAsigAndID
    if n == 7:
        ResponseAsigAndID=['Base de Datos', ID]
        return ResponseAsigAndID
    if n == 8:
        ResponseAsigAndID=['Fol', ID]
        return ResponseAsigAndID
    if n == 9:
        ResponseAsigAndID=['Entornos de Desarrollo', ID]
        return ResponseAsigAndID
    if n == 10:
        ResponseAsigAndID=['Sistemas Informáticos', ID]
        return ResponseAsigAndID

Canales = '''
- **1**  = :bell:Exámenes:bell:
- **2**  = **General**
- **3**  = Alumnos
- **4**  = Dudas-Clase
- **5**  = **Programación**:computer:
- **6**  = Lenguaje de Marcas
- **7**  = Base de datos
- **8**  = Fol
- **9**  = Entornos de Desarrollo
- **10** = Sistemas Informáticos
'''

def PintarCara():
    print('''
    ⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀
    ⠀⣸⣿⣧⣶⣶⠿⠿⠿⠿⢿⣿⢿⣶⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⣿⡇⣀⣠⣤⣶⣶⡿⠿⠿⠿⢿⣿⢿⣶⣶⣤⣄⡘⣿⡆⠀
    ⢸⣿⡏⠁⠀⠀⠀⠀⠀⠀⢻⣧⡀⣠⣿⠉⠙⠛⠀⠀⠀⠀⠀⠀⣿⡿⠛⠉⠉⠀⠀⠀⠀⠀⠀⢺⣯⡀⣠⣿⠉⠙⠛⢻⣿⡄
    ⣼⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠁⠀⠀⠀⠀⣿⣧
    ⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿
    ⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿
    ⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿
    ⢻⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⣦⣤⣴⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡏
    ⠘⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠁⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⠁
    ⠀⠸⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠻⢷⣶⣤⣤⣄⣀⣀⣀⣀⣀⣀⣤⣤⣴⣶⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠃⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠛⠛⠛⠛⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ''')
def PintarCara2():
    print('''
    ⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀
    ⠀⣸⣿⣧⣶⣶⠿⠿⠿⠿⢿⣿⢿⣶⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⣿⡇⣀⣠⣤⣶⣶⡿⠿⠿⠿⢿⣿⢿⣶⣶⣤⣄⡘⣿⡆⠀
    ⢸⣿⡏⠁⠀⠀⠀⠀⠀⠀⢻⣧⡀⣠⣿⠉⠙⠛⠀⠀⠀⠀⠀⠀⣿⡿⠛⠉⠉⠀⠀⠀⠀⠀⠀⢺⣯⡀⣠⣿⠉⠙⠛⢻⣿⡄
    ⣼⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠁⠀⠀⠀⠀⣿⣧
    ⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿
    ⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿
    ⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿
    ⢻⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⣦⣤⣴⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡏
    ⠘⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⡀⠀⠀⠀  ⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⠁
    ⠀⠸⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠻⢷⣶⣤⣤⣄⣀⣀⣀⣀⣀⣀⣤⣤⣴⣶⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠃⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠛⠛⠛⠛⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ''')
def PintarCara3():
    print('''
    ⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀
    ⠀⣸⣿⣧⣶⣶⠿⠿⠿⠿⢿⣿⣿⣶⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⣿⡇⣀⣠⣤⣶⣶⡿⠿⠿⠿⢿⣿⣿⣶⣶⣤⣄⡘⣿⡆⠀
    ⢸⣿⡏⠁⠀⠀⢻⣧⡀⣠⣿    ⠉⠙⠛⠀⠀⠀⠀⠀⠀⣿⡿⠛⠉⠉⠀⠀⢺⣯⡀⣠⣿    ⠉⠙⠛⢻⣿⡄
    ⣼⣿⠀⠀⠀⠀⠀⠙⠛⠛⠁    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣤⡀⠀⠀⠀⠀⠙⠛⠛⠁    ⠀⠀⠀⠀⣿⣧
    ⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿
    ⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿
    ⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿
    ⢻⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⣦⣤⣴⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡏
    ⠘⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠁⠀⠀⡀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⠁
    ⠀⠸⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠻⢷⣶⣤⣤⣄⣀⣀⣀⣀⣀⣀⣤⣤⣴⣶⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠃⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠛⠛⠛⠛⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ''')



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
limpiar()
@client.event
async def on_ready():
    print(f'Se a iniciado sesión correctamente como: {client.user}')
    activity = discord.Activity(type=discord.ActivityType.watching, name="Programación ;)")
    await client.change_presence(activity=activity)
    channel_id = ID # IMPORTANTE --> CANAL DONDE OPERA EL BOT
    channel = client.get_channel(channel_id)
    if channel is not None:
        PintarCara()
        print(f'DAM 1.0 está preparado.')
    else:
        print('No se encontró el canal con el identificador especificado.')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    channel = message.channel.id
    content = message.content
    bot_channel = ID # IMPORTANTE --> CANAL PARA ADMINISTRAR EL BOT
    if message.author.nick:
        username = message.author.nick
    elif message.author.name:
        username = message.author.name
    # ---------------------------------------------------------------------------------------------------------------
    if message.content.startswith("//help"):
        await message.delete()
        await message.channel.send("Estas son mis funciones disponibles:\n- **//help**\n- **//purge** [nº mensajes] para borrar mensajes.\n- **//talk** [mensaje] Entre dobles comillas ( ` ), Para hablar con el bot por canales del server.\n- **Analizador de sintaxis python y java.**")
    if message.content.startswith("//cls"):
        await message.delete()
        limpiar()
        PintarCara3()
        time.sleep(0.5)
        limpiar()
        PintarCara2()
        print("---------------------------------------------------")
        print("                     Graciass                      ")
        print("---------------------------------------------------")
        time.sleep(1.5)
        limpiar()
        PintarCara()
    if message.content.startswith("//purge"):
        lista = content.split(" ")
        if len(lista) > 2 or len(lista) < 2:
            await message.channel.send("El comando solo consiste en **//purge y el número de mensajes que desea borrar**")
            return
        await message.channel.purge(limit=int(lista[1]) + 1)
    # ---------------------------------------------------------------------------------------------------------------
    # Parte de comando //talk
    if channel == bot_channel and message.content.startswith("//talk"):
        if not "```" in message.content:
            await message.channel.send("La sintaxis correcta del comando se escribe  **//talk** después con las tres comillas ( **```** ), introduces lo que quieres que diga yo por ti  :)  y luego lo cierras con otras tres comillas ( **```** )\nNo sirve para envíar códigos de python, java etc.. Solo texto.")
            return
        await message.channel.send(f"¿A qué canal quieres que envíe el mensaje? Aquí una lista de los canales disponibles:\nResponde con el **número** asociado.\n{Canales}")
        def check(m):
            return m.author == message.author and m.channel.id == bot_channel
        try:
            response = await client.wait_for('message', check=check, timeout=30)  # Espera 30 segundos para una respuesta
        except:
            await message.channel.send("Se acabó el tiempo :confused:. No se ha proporcionado un canal.")
            return
        else:
            resp=int(response.content)
            if resp in NumVálidos:
                ChannelDest = ID_ChannelSearch(resp)
                await client.get_channel(ChannelDest[1]).send(ExtraerTexto(content))
                await message.channel.send(f"Mensaje enviado a {ChannelDest[0]}")
            else:
                await message.channel.send("Número no válido, vuelve a introducir el comando //talk")
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # Parte de sustitución y identificación de código.
    if message.content.startswith(""):
        if message.content.startswith("//"):
            return
        if message.content.startswith("```python"):
            return
        if message.content.startswith("```java"):
            return
        else:
            limpiar()
            PintarCara3()
            time.sleep(0.5)
            limpiar()
            PintarCara()
            print("-------------------------------")
            print(f"Nombre de usuario: {username}")
            Lenguaje=DetectarLenguaje(content)
            if Lenguaje == "python":
                await message.delete()
                # Andrés es nuestro profe de programación, pero lo puedes cambiar por el tuyo
                if username == "Andrés (Programación)":
                    await message.channel.send(f"Código del **[ PROFESOR ]** = **{username}** :\n```python\n# Autor: Profe {username}\n\n{content}```")
                elif "achillon" in username:
                    await message.channel.send(f"Código del **[ PROFESOR ]** = **{username}** :\n```python\n# Autor: Profe {username}\n\n{content}```")
                else:
                    await message.channel.send(f"Código de **{username}** :\n```python\n# Autor: {username}\n\n{content}```")
            elif Lenguaje == "java":
                await message.delete()
                if username == "Andrés (Programación)":
                    await message.channel.send(f"Código del **[ PROFESOR ]** = **{username}** :\n```java\n# Autor: Profe {username}\n\n{content}```")
                elif "achillon" in username:
                    await message.channel.send(f"Código del **[ PROFESOR ]** = **{username}** :\n```java\n# Autor: Profe {username}\n\n{content}```")
                else:
                    await message.channel.send(f"Código de **{username}** :\n```java\n# Autor: {username}\n\n{content}```")
            elif Lenguaje == "lenguaje humano":
                print("---------------------------------------------------")
                print("                      Ya está                      ")
                print("---------------------------------------------------")
client.run(bot_token)