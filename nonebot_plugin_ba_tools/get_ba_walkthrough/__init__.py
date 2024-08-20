from nonebot import require

from ..utils.wiki import get_img_from_url, get_wiki_url_from_title

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (  # noqa: E402
    Alconna,
    Args,
    Image,  # noqa: E402
    Match,  # noqa: E402
    UniMessage,
    on_alconna,
)

# TODO: 添加命令别名
walkthrough = Alconna("ba关卡攻略", Args["index", str])
get_walkthrough = on_alconna(walkthrough, use_cmd_start=True)


@get_walkthrough.assign("index")
async def _(index: Match[str]):
    if index.available:
        url: str | None = await get_wiki_url_from_title(index.result)
        if url:
            imgs_url: list[str] = await get_img_from_url(url)
            if len(imgs_url):
                msg: UniMessage[Image] = UniMessage()
                for img_url in imgs_url:
                    msg.append(Image(url=img_url))
                await get_walkthrough.finish(msg)
            else:
                await get_walkthrough.finish("获取攻略失败惹🥺")
        else:
            await get_walkthrough.finish("未找到对应关卡攻略哦～")
