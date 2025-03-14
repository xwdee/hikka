__version__ = (1,1,0)
# meta developer: @tgXunta
from telethon.tl.types import Message
from .. import loader, utils

def register(cb):
    cb(MusicFinder())

@loader.tds
class MusicFinder(loader.Module):
    """Simple module to find music via bot"""

    strings = {
        "name": "Music Finder",
        "no_text": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Provide a name to find music with</b>"
        ),
        "processing": (
            "<emoji document_id=5451646226975955576>⌛️</emoji> <b>Processing...</b>"
        ),
    }


    strings_ru = {
        "name": "Шукалка пісень",
        "no_text": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Вкажіть назву пісні для пошуку</b>"
        ),
        "processing": (
            "<emoji document_id=5451646226975955576>⌛️</emoji> <b>Працюєм...</b>"
        ),
        "_cmd_doc_aniq": "<запрос> - Шукалька пісень через @LyBot",
        "_cls_doc": "ізі модуль по пошуку пісень",
    }

    async def mfindcmd(self, message: Message):
        """<request> - Find music with @LyBot"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_text"))
            return

        message = await utils.answer(message, self.strings("processing"))

        try:
            query = await self._client.inline_query("@LyBot", args)
            await message.respond(file=query[0].document)
        except Exception as e:
            await utils.answer(message, str(e))
            return

        if message.out:
            await message.delete()
