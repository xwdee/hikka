__version__ = (1, 3, 2)
#
# ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░       ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░▒▓████████▓▒░▒▓██████▓▒░  
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓███████▓▒░░▒▓███████▓▒░░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓████████▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
#                                                                                                                             
#                                                                                                                             
# meta banner:
# meta developer: @tgXunta
from .. import loader, utils
from hikkatl.tl.types import InputMessagesFilterMusic
import random

@loader.tds
class Meloman(loader.Module):
    """Модуль для відправки випадкових пісень у чат"""

    strings = {
        "name": "MelomanMod",
        "no_songs": "<b>🎵 Немає доступних пісень у вказаних чатах.</b>",
        "song_sent": "<b>🎵 Відправлено випадкову пісню!</b>",
        "invalid_chat_id": "<b>❌ Неправильний ID чату в конфігу.</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "sources",
                [],
                "Список ID чатів, звідки брати пісні (ID мають починатися з -100), добавляючи через «,»",
            ),
        )

    async def rmscmd(self, message):
        """Відправити випадкову пісню"""
        sources = self.config["sources"]

        if not isinstance(sources, list):
            sources = [sources]

        if not all(isinstance(chat_id, int) and str(chat_id).startswith("-100") for chat_id in sources):
            return await utils.answer(message, self.strings("invalid_chat_id"))

        if not sources:
            return await utils.answer(
                message, "<b>🎵 Ви не вказали джерело пісень у конфігу.</b>"
            )

        audio_messages = []
        for chat_id in sources:
            try:
                async for msg in self.client.iter_messages(chat_id, filter=InputMessagesFilterMusic()):
                    if msg.audio:
                        audio_messages.append(msg)
            except Exception as e:
                await utils.answer(
                    message,
                    f"<b>❌ Не вдалося отримати повідомлення з чату {chat_id}: {e}</b>",
                )
                continue

        if not audio_messages:
            return await utils.answer(message, self.strings("no_songs"))

        random_song = random.choice(audio_messages)
        await random_song.forward_to(message.chat_id)
        await utils.answer(message, self.strings("song_sent"))
