# ---------------------------------------------------------------------------------
#
# ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░       ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░▒▓████████▓▒░▒▓██████▓▒░  
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓███████▓▒░░▒▓███████▓▒░░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓████████▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
#                                                                                                                             
# Name: YouTube DownLoader
# Forker: Xunta
# Commands: ripv ripa
# ---------------------------------------------------------------------------------
# meta banner:
# meta developer: @tgXunta
__version__ = (1,2,2)
import os

from telethon.tl.types import DocumentAttributeAudio
from yt_dlp import YoutubeDL
from yt_dlp.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from .. import loader, utils  # type: ignore


@loader.tds
class YtDlMod(loader.Module):
    """YouTube Downloader Module"""

    strings = {
        "name": "YtDl",
        "preparing": "<b>[YtDl]</b> Preparing...",
        "downloading": "<b>[YtDl]</b> Downloading...",
        "working": "<b>[YtDl]</b> Working...",
        "exporting": "<b>[YtDl]</b> Exporting...",
        "reply": "<b>[YtDl]</b> No link!",
        "noargs": "<b>[YtDl]</b> No args!",
        "content_too_short": "<b>[YtDl]</b> Downloading content too short!",
        "geoban": (
            "<b>[YtDl]</b> The video is not available "
            "for your geographical location due to geographical "
            "restrictions set by the website!"
        ),
        "maxdlserr": '<b>[YtDl]</b> The download limit is as follows: " oh ahah"',
        "pperr": "<b>[YtDl]</b> Error in post-processing!",
        "noformat": (
            "<b>[YtDl]</b> Media is not available in the requested format"
        ),
        "xameerr": "<b>[YtDl]</b> {0.code}: {0.msg}\n{0.reason}",
        "exporterr": "<b>[YtDl]</b> Error when exporting video",
        "err": "<b>[YtDl]</b> {}",
        "err2": "<b>[YtDl]</b> {}: {}",
    }

    async def ripvcmd(self, m):
        """<link/reply-link> - download video"""
        await self.riper(m, "video")

    async def ripacmd(self, m):
        """<link/reply-link> - download audio"""
        await self.riper(m, "audio")

    async def riper(self, m, type):
        reply = await m.get_reply_message()
        args = utils.get_args_raw(m)
        url = args or reply.raw_text
        if not url:
            return await utils.answer(m, self.strings("noargs", m))
        m = await utils.answer(m, self.strings("preparing", m))
        if type == "audio":
            opts = {
                "format": "bestaudio",
                "addmetadata": True,
                "key": "FFmpegMetadata",
                "writethumbnail": True,
                "prefer_ffmpeg": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }
                ],
                "outtmpl": "%(id)s",
                "quiet": True,
                "logtostderr": False,
            }
            video = False
            song = True
        elif type == "video":
            opts = {
                "format": "bestvideo+bestaudio/best",
                "addmetadata": True,
                "key": "FFmpegMetadata",
                "prefer_ffmpeg": True,
                "merge_output_format": "mp4",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "postprocessors": [],
                "outtmpl": "%(id)s.%(ext)s",
                "logtostderr": False,
                "quiet": True,
            }
            song = False
            video = True
        try:
            await utils.answer(m, self.strings("downloading", m))
            with YoutubeDL(opts) as rip:
                rip_data = rip.extract_info(url)
        except DownloadError as DE:
            return await utils.answer(m, self.strings("err", m).format(str(DE)))
        except ContentTooShortError:
            return await utils.answer(m, self.strings("content_too_short", m))
        except GeoRestrictedError:
            return await utils.answer(m, self.strings("geoban", m))
        except MaxDownloadsReached:
            return await utils.answer(m, self.strings("maxdlserr", m))
        except PostProcessingError:
            return await utils.answer(m, self.strings("pperr", m))
        except UnavailableVideoError:
            return await utils.answer(m, self.strings("noformat", m))
        except XAttrMetadataError as XAME:
            return await utils.answer(m, self.strings("xameerr", m).format(XAME))
        except ExtractorError:
            return await utils.answer(m, self.strings("exporterr", m))
        except Exception as e:
            return await utils.answer(
                m, self.strings("err2", m).format(str(type(e)), str(e))
            )
        if song:
            u = rip_data["uploader"] if "uploader" in rip_data else "Northing"
            await utils.answer(
                m,
                open(f"{rip_data['id']}.mp3", "rb"),
                supports_streaming=True,
                reply_to=reply.id if reply else None,
                attributes=[
                    DocumentAttributeAudio(
                        duration=int(rip_data["duration"]),
                        title=str(rip_data["title"]),
                        performer=u,
                    )
                ],
            )
            os.remove(f"{rip_data['id']}")
        elif video:
            await utils.answer(
                m,
                open(f"{rip_data['id']}.{rip_data['ext']}", "rb"),
                reply_to=reply.id if reply else None,
                supports_streaming=True,
                caption=rip_data["title"],
            )
            os.remove(f"{rip_data['id']}.{rip_data['ext']}")
