from .. import loader, utils
from telethon.tl.functions.messages import DeleteHistoryRequest

class ClearAllMod(loader.Module):
    """Повністю очищає історію чату"""
    strings = {'name': 'ClearAll'}

    @loader.sudo
    async def clearallcmd(self, message):
        """Очищає історію чату"""
        chat = message.chat
        if not chat:
            await message.edit("<b>Я не можу чистити лс!</b>")
            return

        confirmation_code = str(chat.id + message.sender_id)
        args = utils.get_args_raw(message)

        if args != confirmation_code:
            await message.edit(
                f"<b>Якщо ти впевнений у своїх діях, введи:</b>\n"
                f"<code>.clearall {confirmation_code}</code>"
            )
            return

        try:
            await message.client(DeleteHistoryRequest(
                peer=chat.id,
                just_clear=False,
                revoke=True
            ))
            await message.edit("<b>Історію чату видалено повністю!</b>")
        except Exception as e:
            await message.edit(f"<b>Помилка:</b> {str(e)}")
