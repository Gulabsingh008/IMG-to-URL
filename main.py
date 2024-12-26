import os, time, math, json
import string, random, traceback
import asyncio, datetime, aiofiles
import requests, aiohttp, logging
from random import choice 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid, UserNotParticipant, UserBannedInChannel
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from database import Database

logging.basicConfig(
    level=logging.INFO,  # Log level set to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Log to the console
)

UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "-1002051166250")
BOT_OWNER = int(os.environ["BOT_OWNER", "7170452349"])
IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY", "")
DATABASE_URL = os.environ["DATABASE_URL" , "mongodb+srv://lokendrasaini9galaxy:f0TVDwu5pVrHn5i6@cluster0.zseht.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"]
db = Database(DATABASE_URL, "mediatourl")


Bot = Client(
    "Media To Url Bot",
    bot_token = os.environ["BOT_TOKEN" ,"7793828619:AAHnY60vTcElNV_Trmd_DE6pKi7y_RKqRO8"],
    api_id = int(os.environ["API_ID","26494161"]),
    api_hash = os.environ["API_HASH", "55da841f877d16a3a806169f3c5153d3"],
)

START_TEXT = """**{},

ɪ ᴀᴍ ᴍᴇᴅɪᴀ ᴛᴏ ᴜʀʟ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ. 

ɪ ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ᴀɴʏ ᴍᴇᴅɪᴀ (ᴘʜᴏᴛᴏ/ᴠɪᴅᴇᴏ/ɢɪғ) ᴜɴᴅᴇʀ 𝟷𝟶ᴍʙ ɪɴᴛᴏ ʟɪɴᴋs.

ᴊᴜsᴛ sᴇɴᴛ ᴍᴇ ᴍᴇᴅɪᴀ ᴅᴏɴᴛ ɴᴇᴇᴅ ᴛᴏ ᴇɴᴛᴇʀ ᴜsᴇ ʟᴇss ᴄᴏᴍᴍᴀɴᴅ ᴀɴᴅ sᴇᴇ ᴍʏ ᴍᴀɢɪᴄ

ᴍʏ ᴄʀᴇᴀᴛᴏʀ : <a href='https://telegram.me/silicon_bot_Update'>sɪʟɪᴄᴏɴ ᴅᴇᴠᴇʟᴏᴘᴇʀ ⚠️</a>**"""

ABOUT_TEXT = """**{},

🤖 ɪ ᴀᴍ : ᴍᴇᴅɪᴀ ᴛᴏ ᴜʀʟ ʙᴏᴛ
⚙️ ᴄʜɪʟʟɪɴɢ ᴏɴ : <a href="https://www.heroku.com/">ʜᴇʀᴏᴋᴜ</a>
🍿 ʙʀᴀɪɴ ꜰᴜᴇʟᴇᴅ : <a href="https://www.mongodb.com/">ᴍᴏɴɢᴏ ᴅʙ</a>
😚 ᴄᴏᴅɪɴɢ ᴍᴜsᴄʟᴇs : <a href="https://www.python.org/">ᴘʏᴛʜᴏɴ 3</a>
👨‍💻 ᴍʏ ᴄʀᴇᴀᴛᴏʀ : <a href='https://telegram.me/silicon_bot_Update'>sɪʟɪᴄᴏɴ ᴅᴇᴠᴇʟᴏᴘᴇʀ ⚠️</a>
**"""

DONATE_TXT = """<blockquote>❤️‍🔥 𝐓𝐡𝐚𝐧𝐤𝐬 𝐟𝐨𝐫 𝐬𝐡𝐨𝐰𝐢𝐧𝐠 𝐢𝐧𝐭𝐞𝐫𝐞𝐬𝐭 𝐢𝐧 𝐃𝐨𝐧𝐚𝐭𝐢𝐨𝐧</blockquote>

<b><i>💞  ɪꜰ ʏᴏᴜ ʟɪᴋᴇ ᴏᴜʀ ʙᴏᴛ ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴅᴏɴᴀᴛᴇ ᴀɴʏ ᴀᴍᴏᴜɴᴛ ₹𝟷𝟶, ₹𝟸𝟶, ₹𝟻𝟶, ₹𝟷𝟶𝟶, ᴇᴛᴄ.</i></b>

❣️ 𝐷𝑜𝑛𝑎𝑡𝑖𝑜𝑛𝑠 𝑎𝑟𝑒 𝑟𝑒𝑎𝑙𝑙𝑦 𝑎𝑝𝑝𝑟𝑒𝑐𝑖𝑎𝑡𝑒𝑑 𝑖𝑡 ℎ𝑒𝑙𝑝𝑠 𝑖𝑛 𝑏𝑜𝑡 𝑑𝑒𝑣𝑒𝑙𝑜𝑝𝑚𝑒𝑛𝑡

💖 𝐔𝐏𝐈 𝐈𝐃 : <code>pay-to-yash-singh@fam</code>
"""

FORCE_SUBSCRIBE_TEXT = """ 
<i><b>🙁 ꜰɪʀꜱᴛ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴜʀʟ, ᴏᴛʜᴇʀᴡɪꜱᴇ ʏᴏᴜ ᴡɪʟʟ ɴᴏᴛ ɢᴇᴛ ɪᴛ.

ᴄʟɪᴄᴋ ᴊᴏɪɴ ɴᴏᴡ ʙᴜᴛᴛᴏɴ 👇</b></i>"""

START_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇ', url='https://t.me/Silicon_Bot_Update')
    ],[
        InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('ꜱᴜᴘᴘᴏʀᴛ', url='https://telegram.me/Silicon_Botz')
    ]]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('👨‍💻 ᴏᴡɴᴇʀ', url='https://telegram.me/CodexBro'),
        InlineKeyboardButton('⋞ ʙᴀᴄᴋ', callback_data='home')
    ]]
)

async def send_msg(user_id, message):
        try:
                await message.copy(chat_id=user_id)
                return 200, None
        except FloodWait as e:
                await asyncio.sleep(e.x)
                return send_msg(user_id, message)
        except InputUserDeactivated:
                return 400, f"{user_id} : deactivated\n"
        except UserIsBlocked:
                return 400, f"{user_id} : user is blocked\n"
        except PeerIdInvalid:
                return 400, f"{user_id} : user id invalid\n"
        except Exception as e:
                return 500, f"{user_id} : {traceback.format_exc()}\n"



@Client.on_callback_query(filters.regex(r'^imgbb$'))
async def imgbb_upload(bot, update):
    message = update.message
    await update.answer_callback_query(text="Processing...", show_alert=False)

    try:
        replied = message.reply_to_message
        if not replied:
            await message.reply_text("Reply to a photo or video under 5MB.")
            return

        if not (replied.photo or replied.video or replied.animation):
            await message.reply_text("Please reply to a photo, video, or GIF.")
            return

        text = await message.reply_text("Downloading to My Server ...", disable_web_page_preview=True)

        # Download the media
        media = await message.reply_to_message.download()

        await text.edit_text("Downloading Completed. Now I am Uploading to imgbb ...", disable_web_page_preview=True)

        # Uploading to imgbb
        try:
            with open(media, 'rb') as file:
                response = requests.post(
                    f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}",
                    files={"image": file}
                )
                response_data = response.json()

                if response_data['success']:
                    image_url = response_data['data']['url']
                else:
                    raise Exception(response_data['error']['message'])
        except Exception as error:
            print(error)
            await text.edit_text(f"Error: {error}", disable_web_page_preview=True)
            return

        # Clean up the downloaded file
        try:
            os.remove(media)
        except Exception as error:
            print(error)

        await text.edit_text(
            text=f"Link:\n\n{image_url}",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Open Link", url=image_url),
                    InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={image_url}")
                ],
                [
                    InlineKeyboardButton(text="✗ Close ✗", callback_data="close")
                ]
            ])
        )

    except Exception as e:
        logging.exception(f"Error in imgbb upload: {e}")
        await message.reply_text(f"Error: {e}", disable_web_page_preview=True)

@Bot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        ) 
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT.format(update.from_user.mention),
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
   

@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
            await db.add_user(update.from_user.id)
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
            reply_markup=START_BUTTONS
    )

@Bot.on_message(filters.private & filters.command(["donate"]))
async def donation(bot, message):
    btn = [[
        InlineKeyboardButton(text="❌  ᴄʟᴏsᴇ  ❌", callback_data="close")
    ]]
    yt=await message.reply_photo(photo='https://envs.sh/wam.jpg', caption=DONATE_TXT, reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()



@Bot.on_message(filters.media & filters.private)
async def upload(client, message):
    try:
        if not await db.is_user_exist(message.from_user.id):
            await db.add_user(message.from_user.id)
            logging.info(f"New user added to database: {message.from_user.id}")

        if UPDATE_CHANNEL:
            try:
                user = await client.get_chat_member(UPDATE_CHANNEL, message.chat.id)
                if user.status == "kicked":
                    await message.reply_text("You are banned!")
                    logging.warning(f"User {message.chat.id} is banned.")
                    return
            except UserNotParticipant:
                await message.reply_text(
                    text=FORCE_SUBSCRIBE_TEXT,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⛔️ ᴊᴏɪɴ ɴᴏᴡ ⛔️", url=f"https://telegram.me/{UPDATE_CHANNEL}")]]
                    )
                )
                logging.info(f"User {message.chat.id} is not part of the update channel.")
                return
            except Exception as error:
                logging.exception(f"Error checking user subscription: {error}")
                await message.reply_text(
                    "<b>ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. Contact <a href='https://telegram.me/Silicon_Official'>Creator</a>.</b>", 
                    disable_web_page_preview=True
                )
                return

        file_size_limit = 10 * 1024 * 1024  # 10 MB in bytes
        if (message.document and message.document.file_size > file_size_limit) or (message.photo and message.photo.file_size > file_size_limit):
            await message.reply_text("<b>⚠️ ᴘʟᴇᴀsᴇ sᴇɴᴛ ғɪʟᴇ ᴜɴᴅᴇʀ 10 ᴍʙ</b>")
            logging.warning(f"User {message.chat.id} tried to send a file larger than 10 MB.")
            return

        # Send a message to choose the upload service
        await client.send_message(
            chat_id=message.chat.id,
            text="<b>Sᴇʟᴇᴄᴛ Tʜᴇ Uᴘʟᴏᴀᴅ Sᴇʀᴠɪᴄᴇ:</b>\n\n<code>Pʟᴇᴀsᴇ Cʜᴏᴏsᴇ Oᴘᴛɪᴏɴ Fʀᴏᴍ Bᴇʟᴏᴡ </code>",
            reply_markup=InlineKeyboardMarkup(
                                [[
                    InlineKeyboardButton(text="ᴇɴᴠs.sʜ", callback_data="envs.sh"),
                    InlineKeyboardButton(text="ɪᴍɢʙʙ", callback_data="imgbb")
                                ]]
                        ),
            reply_to_message_id=message.id
        )
        logging.info(f"Presented upload options to user {message.chat.id}.")

    except Exception as e:
        logging.exception(f"Error in upload message handler: {e}")




@Bot.on_message(filters.private & filters.command("users") & filters.user(BOT_OWNER))
async def users(bot, update):
    total_users = await db.total_users_count()
    text = "Bot Status\n"
    text += f"\nTotal Users: {total_users}"
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast(bot, update):
        broadcast_ids = {}
        all_users = await db.get_all_users()
        broadcast_msg = update.reply_to_message
        while True:
            broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
            if not broadcast_ids.get(broadcast_id):
                break
        out = await update.reply_text(text=f"Broadcast Started! You will be notified with log file when all the users are notified.")
        start_time = time.time()
        total_users = await db.total_users_count()
        done = 0
        failed = 0
        success = 0
        broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
        async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
            async for user in all_users:
                sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)
                if msg is not None:
                    await broadcast_log_file.write(msg)
                if sts == 200:
                    success += 1
                else:
                    failed += 1
                if sts == 400:
                    await db.delete_user(user['id'])
                done += 1
                if broadcast_ids.get(broadcast_id) is None:
                    break
                else:
                    broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
        if broadcast_ids.get(broadcast_id):
            broadcast_ids.pop(broadcast_id)
        completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
        await asyncio.sleep(3)
        await out.delete()
        if failed == 0:
            await update.reply_text(text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.", quote=True)
        else:
            await update.reply_document(document='broadcast.txt', caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.")
        os.remove('broadcast.txt')


Bot.run()
