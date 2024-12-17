from .. import loader, utils
from asyncio import sleep

def register(cb):
    cb(DelkrMod())

class DelkrMod(loader.Module):
    """Модуль для надсилання репортів з інтервалом"""
    strings = {"name": 'DelkrMod'}

    async def delkrcmd(self, message):
        """Команда delkr для надсилання повідомлень з інтервалом"""
        try:
            await message.delete()
            args = utils.get_args_raw(message).split(' ')
            if len(args) < 2:
                return await message.client.send_message(message.to_id, 'Використання: <code>delkr <інтервал:int> <кількість:int></code>')

            interval = int(args[0])
            count = int(args[1])
            report_chat_id = message.to_id

            msg = await message.client.send_message(report_chat_id, f"Репорт 0/{count}: Початок відправлення.")

            for i in range(count):
                await sleep(interval)
                await msg.edit(f"Репорт {i + 1}/{count}: Повідомлення надіслано.")
        except Exception as e:
            await message.client.send_message(message.to_id, f"Помилка: {str(e)}")
