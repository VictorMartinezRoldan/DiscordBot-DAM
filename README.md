# Discord Bot - Analizador de Código y Moderación

## Descripción
Este bot de Discord está diseñado para analizar y detectar código en mensajes de los usuarios, identificando si el código es Python o Java. Además, cuenta con funciones de moderación como purga de mensajes, envío de mensajes a través de comandos y detección de lenguaje humano.

## ¿Por qué se creó este bot?
La necesidad de automatizar el formateo de código surgió debido a que los usuarios enviaban código en texto plano, lo que dificultaba su lectura, copia y prueba en entornos de desarrollo. Para mejorar la visualización y la comodidad a la hora de trabajar con código, se creó este bot, el cual detecta automáticamente fragmentos de código y los encapsula en bloques de código de formato adecuados para una mejor organización y comprensión.

## Características
- 🔍 **Detección de código**: Identifica si un mensaje contiene código Python o Java y lo formatea adecuadamente.
- 🛑 **Moderación**: Permite eliminar mensajes en masa con el comando `//purge`.
- 💬 **Envío de mensajes**: El comando `//talk` permite enviar mensajes a diferentes canales del servidor.
- 🚀 **Interfaz interactiva**: Responde a ciertos comandos y muestra mensajes visuales en consola.
- 🛠 **Personalizable**: Se pueden modificar los canales donde opera el bot y los permisos según necesidad.

## Instalación y Configuración
1. Clona el repositorio:
   ```bash
   git clone https://github.com/VictorMartinezRoldan/DiscordBot-DAM.git
   cd DiscordBot-DAM
   ```
2. Instala las dependencias necesarias:
   ```bash
   pip install discord requests
   ```
3. Configura tu bot:
   - Obtén un **token de bot** desde [Discord Developer Portal](https://discord.com/developers).
   - Configura el **Webhook URL** en el código.
   - **Partes de código importantes que cambiar:**
     - **Línea 9**   → `webhook_url`
     - **Línea 11**  → `bot_token`
     - **Línea 230** → ID de asignaturas y sus nombres
     - **Línea 262** → Nombre de canales
     - **Línea 330** → `channel_id` → CANAL DONDE OPERA EL BOT
     - **Línea 343** → `bot_channel` → CANAL PARA ADMINISTRAR EL BOT
     - **Línea 414** → Nombre del profesor a identificar

4. Ejecuta el bot:
   ```bash
   python DAM-BOT.py
   ```

## Comandos Disponibles
| Comando       | Descripción |
|--------------|------------|
| `//help`     | Muestra la lista de comandos disponibles. |
| `//purge X`  | Elimina los últimos `X` mensajes en el canal. |
| `//talk`     | Permite enviar mensajes a otros canales. |
| `//cls`      | Limpia la consola y muestra animaciones. |

## Funcionamiento del Analizador de Código
El bot analiza cada mensaje enviado en el servidor y determina si contiene código en **Python** o **Java** mediante la detección de palabras clave específicas, como `def`, `print`, `void`, `public class`, etc. Si detecta código, lo formatea y lo envía nuevamente al canal con el nombre del autor.

## Consideraciones
⚠️ **No compartas el token de tu bot públicamente**. Si accidentalmente lo expones, **debes regenerarlo inmediatamente en el portal de Discord**.

## Contribuciones
Si deseas mejorar este proyecto, puedes enviar un **Pull Request** o abrir un **Issue** con sugerencias y correcciones.

---
📌 **Desarrollado por:** Víctor Martínez Roldán