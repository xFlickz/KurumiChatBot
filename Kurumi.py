print("[KURUMI]: INITIALIZING ...")
import re
import random
from os import path
from asyncio import (gather, get_event_loop, sleep)

from aiohttp import ClientSession
from pyrogram import (Client, filters, idle)
from Python_ARQ import ARQ
from os import environ

bot_token = str(environ.get("TOKEN", None))
ARQ_API_KEY = str(environ.get("ARQ_API_KEY", None))
LANGUAGE = str(environ.get("LANGUAGE", "en"))
bot_id = int(environ.get("BOT_ID", None))
api_id = int(environ.get("API_ID"))
api_hash = str(environ.get("HASH", None))
ARQ_API_BASE_URL = str(environ.get("ARQ_API_BASE_URL", "https://thearq.tech"))

print("[KURUMI]: INITIALIZING BOT CLIENT ...")
luna = Client(":memory:",
              bot_token=bot_token,
              api_id=api_id,
              api_hash=api_hash,
)
arq = None

HELP = """
Here is my help menu and command list.

/help - To See This Message
/repo - Get Repo Link
/about - About My Creator

Im a chatbot designed for chatting with you,
Send me any message then i can reply you!
"""

ABOUT = """
😘 My Darling is @Yoga_CIC
I was born in @YBotsSupport

See List of My Other Brother/Sisters on @SpreadNetworks

Built with ❤ and Pyrogram.
"""

RTEXT = ["I've started...",
         "Ohayou oniichan>///<",
         "What are u doin'?",
         "Sup?",
         "Now what?",
         "How are you?",
         "Kono hentai! -_-",
         "Dameee! *run away",
         "B-baka>///<",
         "You see my cat?",
         "My darling is @Yoga_CIC",
         "FBI Open Up!!",
         "My money, someone stolen my money 😢",
         "Are you lolicon?"
        ]

async def lunaQuery(query: str, user_id: int):
    query = (
        query
        if LANGUAGE == "en"
        else (await arq.translate(query, "en")).result.translatedText
    )
    resp = (await arq.luna(query, user_id)).result
    return (
        resp
        if LANGUAGE == "en"
        else (
            await arq.translate(resp, LANGUAGE)
        ).result.translatedText
    )


async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(2))
    if "Luna" in response:
        respa = response.replace("Luna", "Kurumi")
    else:
        respa = response
    if "Aco" in respa:
        respb = respa.replace("Aco", "Kurumi")
    else:
        respb = respa
    await message.reply_text(respb)
    await message._client.send_chat_action(chat_id, "cancel")


@luna.on_message(filters.command("repo") & ~filters.edited)
async def repo(_, message):
    await message.reply_text(
        "[GitHub](https://github.com/zYxDevs/KurumiChatbot)"
        + " | [Support](t.me/YBotsSupport)"
        + " | [Updates](t.me/SpreadNetworks)",
        disable_web_page_preview=True,
    )


@luna.on_message(filters.command(["help", "help@TokisakiChatBot"]) & ~filters.edited)
async def start(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text(HELP)

@luna.on_message(filters.command(["about", "about@TokisakiChatBot"]) & ~filters.edited)
async def start(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text(ABOUT)

@luna.on_message(
    ~filters.private
    & filters.text
    & ~filters.command(["start", "start@TokisakiChatBot"])
    & ~filters.edited,
    group=69,
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        from_user_id = message.reply_to_message.from_user.id
        if from_user_id != bot_id:
            return
    else:
        match = re.search(
            "[.|\n]{0,}kurumi[.|\n]{0,}",
            message.text.strip(),
            flags=re.IGNORECASE,
        )
        if not match:
            return
    await type_and_send(message)


@luna.on_message(
    filters.private
    & ~filters.command(["start", "start@TokisakiChatBot"])
    & ~filters.edited
)
async def chatpm(_, message):
    if not message.text:
        await message.reply_text("Uff... ignoring...")
        return
    await type_and_send(message)


@luna.on_message(filters.command(["start", "start@TokisakiChatBot"]) & ~filters.edited)
async def startt(_, message):
    rand = random.choice(RTEXT)
    await message.reply_text(rand)


async def main():
    global arq
    session = ClientSession()
    print("[KURUMI] INITIALIZING ARQ CLIENT ...")
    arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

    await luna.start()
    print(
        """
-------------------
| Kurumi Started! |
-------------------
| By Yoga Pranata |
-------------------
"""
    )
    await idle()


loop = get_event_loop()
loop.run_until_complete(main())