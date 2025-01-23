import contextlib
__version__ = (1, 2, 3)
#
# ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░       ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░▒▓████████▓▒░▒▓██████▓▒░  
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓███████▓▒░░▒▓███████▓▒░░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓████████▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
#                                                                                                                             
# meta banner:
# meta developer: @tgXunta
from telethon.tl.types import Message
import requests
import logging
import re

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class Groq(loader.Module):
    """Groq API interaction"""

    strings = {
        "name": "Groq",
        "no_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>No arguments"
            " provided</b>"
        ),
        "question": (
            "<emoji document_id=5974038293120027938>👤</emoji> <b>Question:</b>"
            " {question}\n"
        ),
        "answer": (
            "<emoji document_id=5971808079811972376>🤖</emoji> <b>Answer:</b> {answer}"
        ),
        "loading": "<code>Loading...</code>",
        "no_api_key": (
            "<b>🚫 No API key provided</b>\n<i><emoji"
            " document_id=5971808079811972376>ℹ️</emoji> Get it from official groq"
            " website and add it to config</i>"
        ),
    }

    strings_ru = {
        "no_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Не указаны"
            " аргументы</b>"
        ),
        "question": (
            "<emoji document_id=5974038293120027938>👤</emoji> <b>Вопрос:</b>"
            " {question}\n"
        ),
        "answer": (
            "<emoji document_id=5971808079811972376>🤖</emoji> <b>Ответ:</b> {answer}"
        ),
        "loading": "<code>Загрузка...</code>",
        "no_api_key": (
            "<b>🚫 Не указан API ключ</b>\n<i><emoji"
            " document_id=5971808079811972376>ℹ️</emoji> Получите его на официальном"
            " сайте groq и добавьте в конфиг</i>"
        ),
    }

    strings_es = {
        "no_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>No se han"
            " proporcionado argumentos</b>"
        ),
        "question": (
            "<emoji document_id=5974038293120027938>👤</emoji> <b>Pregunta:</b>"
            " {question}\n"
        ),
        "answer": (
            "<emoji document_id=5971808079811972376>🤖</emoji> <b>Respuesta:</b>"
            " {answer}"
        ),
        "loading": "<code>Cargando...</code>",
        "no_api_key": (
            "<b>🚫 No se ha proporcionado una clave API</b>\n<i><emoji"
            " document_id=5971808079811972376>ℹ️</emoji> Obtenga una en el sitio web"
            " oficial de groq y agréguela a la configuración</i>"
        ),
    }

    strings_fr = {
        "no_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Aucun argument"
            " fourni</b>"
        ),
        "question": (
            "<emoji document_id=5974038293120027938>👤</emoji> <b>Question:</b>"
            " {question}\n"
        ),
        "answer": (
            "<emoji document_id=5971808079811972376>🤖</emoji> <b>Réponse:</b> {answer}"
        ),
        "loading": "<code>Chargement...</code>",
        "no_api_key": (
            "<b>🚫 Aucune clé API fournie</b>\n<i><emoji"
            " document_id=5971808079811972376>ℹ️</emoji> Obtenez-en un sur le site"
            " officiel d'groq et ajoutez-le à la configuration</i>"
        ),
    }

    strings_de = {
        "no_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Keine Argumente"
            " angegeben</b>"
        ),
        "question": (
            "<emoji document_id=5974038293120027938>👤</emoji> <b>Frage:</b>"
            " {question}\n"
        ),
        "answer": (
            "<emoji document_id=5971808079811972376>🤖</emoji> <b>Antwort:</b> {answer}"
        ),
        "loading": "<code>Laden...</code>",
        "no_api_key": (
            "<b>🚫 Kein API-Schlüssel angegeben</b>\n<i><emoji"
            " document_id=5971808079811972376>ℹ️</emoji> Holen Sie sich einen auf der"
            " offiziellen groq-Website und fügen Sie ihn der Konfiguration hinzu</i>"
        ),
    }

    strings_tr = {
        "no_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Argümanlar"
            " verilmedi</b>"
        ),
        "question": (
            "<emoji document_id=5974038293120027938>👤</emoji> <b>Soru:</b> {question}\n"
        ),
        "answer": (
            "<emoji document_id=5971808079811972376>🤖</emoji> <b>Cevap:</b> {answer}"
        ),
        "loading": "<code>Yükleniyor...</code>",
        "no_api_key": (
            "<b>🚫 API anahtarı verilmedi</b>\n<i><emoji"
            " document_id=5971808079811972376>ℹ️</emoji> groq'nın resmi websitesinden"
            " alın ve yapılandırmaya ekleyin</i>"
        ),
    }

    strings_uz = {
        "no_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Argumentlar"
            " ko'rsatilmadi</b>"
        ),
        "question": (
            "<emoji document_id=5974038293120027938>👤</emoji> <b>Savol:</b>"
            " {question}\n"
        ),
        "answer": (
            "<emoji document_id=5971808079811972376>🤖</emoji> <b>Javob:</b> {answer}"
        ),
        "loading": "<code>Yuklanmoqda...</code>",
        "no_api_key": (
            "<b>🚫 API kalit ko'rsatilmadi</b>\n<i><emoji"
            " document_id=5971808079811972376>ℹ️</emoji> Ofitsial groq veb-saytidan"
            " oling</i>"
        ),
    }

    strings_it = {
        "no_args": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Nessun argomento"
            " fornito</b>"
        ),
        "question": (
            "<emoji document_id=5974038293120027938>👤</emoji> <b>Domanda:</b>"
            " {question}\n"
        ),
        "answer": (
            "<emoji document_id=5971808079811972376>🤖</emoji> <b>Risposta:</b> {answer}"
        ),
        "loading": "<code>Caricamento...</code>",
        "no_api_key": (
            "<b>🚫 Nessuna chiave API fornita</b>\n<i><emoji"
            " document_id=5971808079811972376>ℹ️</emoji> Ottienila dal sito ufficiale"
            " di groq e aggiungila al tuo file di configurazione</i>"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                "",
                "API key from groq",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "model",
                "llama3-8b-8192",
                "Model to use the Groq",
                validator=loader.validators.String(),
            ),
        )

    async def _make_request(
            self,
            method: str,
            url: str,
            headers: dict,
            data: dict,
    ) -> dict:
        resp = await utils.run_sync(
            requests.request,
            method,
            url,
            headers=headers,
            json=data,
        )
        return resp.json()

    def _process_code_tags(self, text: str) -> str:
        return re.sub(
            r"`(.*?)`",
            r"<code>\1</code>",
            re.sub(r"```(.*?)```", r"<code>\1</code>", text, flags=re.DOTALL),
            flags=re.DOTALL,
        )

    async def _get_chat_completion(self, prompt: str) -> str:
        resp = await self._make_request(
            method="POST",
            url="https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f'Bearer {self.config["api_key"]}',
            },
            data={
                "model": self.config["model"],
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        if resp.get("error", None):
            return f"🚫 {resp['error']['message']}"
        return resp["choices"][0]["message"]["content"]

    @loader.command(
        ru_doc="<вопрос> - Задать вопрос",
        it_doc="<domanda> - Fai una domanda",
        fr_doc="<question> - Posez une question",
        de_doc="<frage> - Stelle eine Frage",
        es_doc="<pregunta> - Haz una pregunta",
        tr_doc="<soru> - Soru sor",
        uz_doc="<savol> - Savol ber",
    )
    async def groq(self, message: Message):
        """<question> - Ask a question or reply to a message to ask a question"""
        if self.config["api_key"] == "":
            return await utils.answer(message, self.strings("no_api_key"))

        args = utils.get_args_raw(message)

        reply = await message.get_reply_message()
        reply_text = reply.raw_text if reply else ""

        prompt = args if args else reply_text

        if not prompt:
            return await utils.answer(message, self.strings("no_args"))

        await utils.answer(
            message,
            "\n".join(
                [
                    self.strings("question").format(question=prompt),
                    self.strings("answer").format(answer=self.strings("loading")),
                ]
            ),
        )
        
        answer = await self._get_chat_completion(prompt)
        await utils.answer(
            message,
            "\n".join(
                [
                    self.strings("question").format(question=prompt),
                    self.strings("answer").format(
                        answer=self._process_code_tags(answer)
                    ),
                ]
            ),
        )