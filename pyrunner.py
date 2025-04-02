import os
import subprocess
from .. import loader, utils

@loader.tds
class PythonRunner(loader.Module):
    """Модуль для запуску та зупинки Python-скрипта."""

    strings = {
        "name": "PythonRunner",
        "started": "✅ Скрипт запущено!",
        "stopped": "⛔ Скрипт зупинено!",
        "not_running": "⚠ Скрипт не запущено!",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "python_path",
                "/usr/bin/python3",
                "Шлях до Python"
            ),
            loader.ConfigValue(
                "script_path",
                "script.py",
                "Шлях до скрипта"
            ),
            loader.ConfigValue(
                "log_file",
                "/dev/null",
                "Файл логування"
            ),
            loader.ConfigValue(
                "work_dir",
                ".",
                "Директорія виконання скрипта"
            ),
            loader.ConfigValue(
                "autostart",
                False,
                "Автоматичний запуск при старті юзбота",
                validator=loader.validators.Boolean(),
            ),
        )
        self.process = None

    async def client_ready(self, client, db):
        """Автозапуск при старті юзбота, якщо включено в конфіг."""
        if self.config["autostart"]:
            await self.pystartcmd(None)

    async def pystartcmd(self, message):
        """Запустити Python-скрипт."""
        if self.process and self.process.poll() is None:
            return await utils.answer(message, "⚠ Скрипт вже запущено!")
        python_path = self.config['python_path']
        script_path = self.config['script_path']
        work_dir = self.config['work_dir']
        log_file = self.config['log_file']
        cmd = f"cd {work_dir} && {python_path} {script_path} 1> {log_file} 2>&1"
        self.process = subprocess.Popen(cmd, shell=True)
        if message:
            await utils.answer(message, self.strings("started"))

    async def pystopcmd(self, message):
        """Зупинити Python-скрипт."""
        if self.process and self.process.poll() is None:
            os.system(f"kill -9 {self.process.pid}")
            self.process = None
            return await utils.answer(message, self.strings("stopped"))
        await utils.answer(message, self.strings("not_running"))
