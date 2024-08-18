from apscheduler.triggers.base import random
from nonebot import logger, require
from nonebot.adapters.onebot.v11 import Bot

from ..config import plugin_config
from ..utils.wiki import get_img_from_url, get_max_manga_index, get_wiki_urls_from_title

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Image  # noqa: E402
from nonebot_plugin_alconna import Match  # noqa: E402
from nonebot_plugin_alconna import Alconna, Args, UniMessage, on_alconna  # noqa: E402

manga = Alconna("ba漫画", Args["index", str])
get_manga = on_alconna(manga, use_cmd_start=True)


# TODO: 修复部分漫画加载失败的bug
@get_manga.assign("index")
async def _(bot: Bot, index: Match):
    if index.available:
        pre_msg: dict[str, int] = {"message_id": -1}
        max_index: int = await get_max_manga_index()
        logger.debug(f"最大话数为第{max_index}话")
        random_index: int = random.randint(1, max_index)
        title: str = f"第{random_index}话" if index.result == "抽取" else index.result
        urls: list[str] = await get_wiki_urls_from_title(title)
        logger.debug(f"漫画话数为：{title}")
        if len(urls):
            url: str = urls[0]
            imgs_url: list[str] = await get_img_from_url(url)
            if len(imgs_url):
                if plugin_config.is_open_notice:
                    pre_msg = await get_manga.send("正在努力加载图片中……")
                msg: UniMessage[Image] = UniMessage()
                for img_url in imgs_url:
                    msg.append(Image(url=img_url))
                await get_manga.send(msg)
                if plugin_config.is_open_notice:
                    await bot.delete_msg(message_id=pre_msg["message_id"])
                await get_manga.finish()
            else:
                await get_manga.finish("加载漫画出错了🥺")
        else:
            await get_manga.finish("是找不到的话数呢～")
