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

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,  # Log level set to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Log to the console
)

UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "")
BOT_OWNER = int(os.environ["BOT_OWNER"])
DATABASE_URL = os.environ["DATABASE_URL"]
db = Database(DATABASE_URL, "mediatourl")
IMGBB_API_KEY = ""

Bot = Client(
    "Media To Url Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START_TEXT = """**{},

ɪ ᴀᴍ ᴍᴇᴅɪᴀ ᴛᴏ ᴜʀʟ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ. 

ɪ ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ᴀɴʏ ᴍᴇᴅɪᴀ (ᴘʜᴏᴛᴏ/ᴠɪᴅᴇᴏ) ᴜɴᴅᴇʀ 𝟷𝟶ᴍʙ.

ᴍʏ ᴄʀᴇᴀᴛᴏʀ : <a href='https://telegram.me/CodeXBro'>ʀᴀʜᴜʟ</a>**"""

ABOUT_TEXT = """**{},

🤖 ɪ ᴀᴍ [ᴍᴇᴅɪᴀ ᴛᴏ ᴜʀʟ ʙᴏᴛ](https://telegram.me/MediaToUrlBot)
⚙️ ᴄʜɪʟʟɪɴɢ ᴏɴ : <a href="https://www.heroku.com/">ʜᴇʀᴏᴋᴜ</a>
🍿 ʙʀᴀɪɴ ꜰᴜᴇʟᴇᴅ : <a href="https://www.mongodb.com/">ᴍᴏɴɢᴏ ᴅʙ</a>
😚 ᴄᴏᴅɪɴɢ ᴍᴜsᴄʟᴇs : <a href="https://www.python.org/">ᴘʏᴛʜᴏɴ 3</a>
👨‍💻 ᴍʏ ᴄʀᴇᴀᴛᴏʀ : <a href="https://telegram.me/CodeXBro">ʀᴀʜᴜʟ</a>
😜 ʀᴇᴘᴏ : <a href="https://github.com/CodeXBots">ʟɪɴᴋ</a>**"""

DONATE_TXT = """<blockquote>❤️‍🔥 𝐓𝐡𝐚𝐧𝐤𝐬 𝐟𝐨𝐫 𝐬𝐡𝐨𝐰𝐢𝐧𝐠 𝐢𝐧𝐭𝐞𝐫𝐞𝐬𝐭 𝐢𝐧 𝐃𝐨𝐧𝐚𝐭𝐢𝐨𝐧</blockquote>

<b><i>💞  ɪꜰ ʏᴏᴜ ʟɪᴋᴇ ᴏᴜʀ ʙᴏᴛ ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴅᴏɴᴀᴛᴇ ᴀɴʏ ᴀᴍᴏᴜɴᴛ ₹𝟷𝟶, ₹𝟸𝟶, ₹𝟻𝟶, ₹𝟷𝟶𝟶, ᴇᴛᴄ.</i></b>

❣️ 𝐷𝑜𝑛𝑎𝑡𝑖𝑜𝑛𝑠 𝑎𝑟𝑒 𝑟𝑒𝑎𝑙𝑙𝑦 𝑎𝑝𝑝𝑟𝑒𝑐𝑖𝑎𝑡𝑒𝑑 𝑖𝑡 ℎ𝑒𝑙𝑝𝑠 𝑖𝑛 𝑏𝑜𝑡 𝑑𝑒𝑣𝑒𝑙𝑜𝑝𝑚𝑒𝑛𝑡

💖 𝐔𝐏𝐈 𝐈𝐃 : <code>RahulReviews@UPI</code>
"""

FORCE_SUBSCRIBE_TEXT = """ 
<i><b>🙁 ꜰɪʀꜱᴛ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴜʀʟ, ᴏᴛʜᴇʀᴡɪꜱᴇ ʏᴏᴜ ᴡɪʟʟ ɴᴏᴛ ɢᴇᴛ ɪᴛ.

ᴄʟɪᴄᴋ ᴊᴏɪɴ ɴᴏᴡ ʙᴜᴛᴛᴏɴ 👇</b></i>"""

START_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('ᴅᴇᴠᴇʟᴏᴘᴇʀ', url='https://youtube.com/@RahulReviews')
    ],[
        InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('ꜱᴜᴘᴘᴏʀᴛ', url='https://telegram.me/CodeXSupport')
    ]]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('🫡 ᴅᴏɴᴀᴛᴇ', url='https://codexbots.github.io/Donate'),
        InlineKeyboardButton('👨‍💻 ᴏᴡɴᴇʀ', url='https://telegram.me/CodexBro')
    ],[
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
    elif update.data == "upload_envs.sh":
                upload_service = update.data.split('_')[1]
                await handle_upload(bot, update, upload_service)

    elif update.data == "upload_imgbb":
                upload_service = update.data.split('_')[1]
                await handle_upload(bot, update, upload_service)

    else:
        await update.message.delete()

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

def upload_image_requests(image_path, upload_service):
    logging.info(f"Initiating upload process for {image_path} to {upload_service}.")

    if upload_service == "envs.sh":
        upload_url = "https://envs.sh"
        logging.info("Using envs.sh for upload.")
    elif upload_service == "imgbb":
        upload_url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}"
        logging.info(f"Using imgbb for upload with URL {upload_url}.")
    else:
        logging.error("Unsupported upload service provided.")
        raise ValueError("Unsupported upload service")

    try:
        logging.info(f"Opening file {image_path} for upload.")
        with open(image_path, 'rb') as file:
            files = {'file': file}
            logging.info(f"Sending POST request to {upload_url}.")
            response = requests.post(upload_url, files=files)

            logging.info(f"Response status code: {response.status_code}")
            if response.status_code == 200:
                if upload_service == "imgbb":
                    response_data = response.json()
                    logging.info(f"Response JSON: {response_data}")
                    if response_data['success']:
                        image_url = response_data['data']['url']
                        logging.info(f"Upload successful. Image URL: {image_url}")
                        return image_url
                    else:
                        error_message = response_data.get('error', {}).get('message', 'Unknown error')
                        logging.error(f"imgbb upload failed: {error_message}")
                        raise Exception(error_message)
                return response.text.strip()  # for envs.sh
            else:
                logging.error(f"Upload failed with status code {response.status_code}")
                raise Exception(f"Upload failed with status code {response.status_code}")

    except Exception as e:
        logging.exception(f"Error during upload: {e}")
        return None

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
                    "<b>ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. Contact <a href='https://telegram.me/CodeXBro'>Creator</a>.</b>", 
                    disable_web_page_preview=True
                )
                return

        file_size_limit = 10 * 1024 * 1024  # 10 MB in bytes
        if (message.document and message.document.file_size > file_size_limit) or (message.photo and message.photo.file_size > file_size_limit):
            await message.reply_text("<b>⚠️ Send a media file under 10 MB</b>")
            logging.warning(f"User {message.chat.id} tried to send a file larger than 10 MB.")
            return

        # Send a message to choose the upload service
        await client.send_message(
            chat_id=message.chat.id,
            text="<b>Select upload service:</b>n<code>Please choose one of the options below:</code>",
            reply_markup=InlineKeyboardMarkup(
                                [[
                    InlineKeyboardButton(text="envs.sh", callback_data="upload_envs.sh"),
                    InlineKeyboardButton(text="imgbb", callback_data="upload_imgbb")
                                ]]
                        ),
            reply_to_message_id=message.id
        )
        logging.info(f"Presented upload options to user {message.chat.id}.")

    except Exception as e:
        logging.exception(f"Error in upload message handler: {e}")

#@Bot.on_callback_query(filters.regex(r"^upload_(envs|imgbb)$"))
async def handle_upload(client, query, upload_service):
    try:
      #  upload_service = query.data.split('_')[1]
        logging.info(f"User {query.from_user.id} selected {upload_service} for upload.")

        # Get the original message that had the media (the message that the buttons were replying to)
        original_message = query.message.reply_to_message
        if not original_message or not (original_message.photo or original_message.document):
            await query.message.reply_text("⚠️ Please reply to a media message to upload.")
            logging.warning(f"User {query.from_user.id} did not reply to a media message.")
            return

        # Download the media
        logging.info(f"Downloading media for user {query.from_user.id}.")
        path = await original_message.download()

        uploading_message = await query.message.reply_text(f"<code>Uploading to {upload_service}...</code>")
        logging.info(f"Uploading media to {upload_service} for user {query.from_user.id}.")

        try:
            image_url = upload_image_requests(path, upload_service)
            if not image_url or not image_url.startswith('http'):
                raise Exception("Failed to upload file or invalid URL.")
        except Exception as error:
            logging.exception(f"Error during file upload for user {query.from_user.id}: {error}")
            await uploading_message.edit_text(f"Upload failed: {error}")
            return

        try:
            os.remove(path)
            logging.info(f"Temporary file {path} deleted after upload.")
        except Exception as error:
            logging.exception(f"Error deleting file {path}: {error}")

        await uploading_message.delete()
        await query.message.reply_photo(
            photo=image_url,
            caption=f"<b>Upload completed to {upload_service} 👇</b>\n\nLink:\n\n<code>{image_url}</code>\n\n<b>ʙʏ - <a href='https://telegram.me/CodeXBro'>ʀᴀʜᴜʟ</a></b>",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(text="• ᴏᴘᴇɴ ʟɪɴᴋ •", url=image_url),
                InlineKeyboardButton(text="• sʜᴀʀᴇ ʟɪɴᴋ •", url=f"https://telegram.me/share/url?url={image_url}")
            ],[
                InlineKeyboardButton(text="❌   ᴄʟᴏsᴇ   ❌", callback_data="close_data")
            ]])
        )
        logging.info(f"Upload link sent to user {query.from_user.id}.")

        await asyncio.sleep(120)
        await query.message.delete()
        logging.info(f"Message deleted after 120 seconds for user {query.from_user.id}.")

    except Exception as e:
        logging.exception(f"Error in callback handler: {e}")

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