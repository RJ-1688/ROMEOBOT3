import asyncio
import math
import os
import heroku3
import requests
import urllib3
import sys

from os import execl
from time import sleep

from ..sql.gvar_sql import addgvar, delgvar, gvarstat
from . import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY


@hell_cmd(pattern="reload$")
async def rel(event):
    await eor(event, "🇷𝐄𝐋𝐎𝐀𝐃...")
    await reload_RomeoBot()


@hell_cmd(pattern="shutdown$")
async def down(hell):
    event = await eor(hell, "`𝐎𝐅𝐅 𝐑𝐎𝐌𝐄𝐎𝐁𝐎𝐓`")
    await asyncio.sleep(2)
    await event.edit("**[ ⚠️ ]** \n**𝐒𝐇𝐔𝐓𝐃𝐎𝐖𝐍 𝐑𝐎𝐌𝐄𝐎𝐁𝐎𝐓 𝐒𝐓𝐀𝐑𝐓 𝐌𝐀𝐍𝐔𝐀𝐋𝐋𝐘**")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


@hell_cmd(pattern="svar(?:\s|$)([\s\S]*)")
async def sett(event):
    hel_ = event.pattern_match.group(1)
    var_ = hel_.split(" ")[0].upper()
    val_ = hel_.split(" ")[1:]
    valu = " ".join(val_)
    hell = await eor(event, f"**Setting variable** `{var_}` **as** `{valu}`")
    if var_ == "":
        return await eod(hell, f"**Invalid Syntax !!** \n\nTry: `{hl}svar VARIABLE_NAME variable_value`")
    elif valu == "":
        return await eod(hell, f"**Invalid Syntax !!** \n\nTry: `{hl}svar VARIABLE_NAME variable_value`")
    if var_ not in db_config:
        return await eod(hell, f"__There isn't any DB variable named__ `{var_}`. __Check spelling or get full list by__ `{hl}vars`")
    try:
        addgvar(var_, valu)
    except Exception as e:
        return await eod(hell, f"**ERROR !!** \n\n`{e}`")
    await eod(hell, f"**Variable Added Successfully!!** \n\n**• Variable:** `{var_}` \n**» Value:** `{valu}`")


@hell_cmd(pattern="gvar(?:\s|$)([\s\S]*)")
async def gett(event):
    var_ = event.pattern_match.group(1).upper()
    hell = await eor(event, f"**Getting variable** `{var_}`")
    if var_ == "":
        return await eod(hell, f"**Invalid Syntax !!** \n\nTry: `{hl}gvar VARIABLE_NAME`")
    if var_ not in db_config:
        return await eod(hell, f"__There isn't any variable named__ `{var_}`. __Check spelling or get full list by `{hl}vars`")
    try:
        sql_v = gvarstat(var_)
        os_v = os.environ.get(var_) or "None"
    except Exception as e:
        return await eod(hell, f"**ERROR !!** \n\n`{e}`")
    await hell.edit(f"**• OS VARIABLE:** `{var_}`\n**» OS VALUE :** `{os_v}`\n------------------\n**• DB VARIABLE:** `{var_}`\n**» DB VALUE :** `{sql_v}`\n")


@hell_cmd(pattern="dvar(?:\s|$)([\s\S]*)")
async def dell(event):
    var_ = event.pattern_match.group(1).upper()
    hell = await eor(event, f"**Deleting Variable** `{var_}`")
    if var_ == "":
        return await eod(hell, f"**Invalid Syntax !!** \n\nTry: `{hl}dvar VARIABLE_NAME`")
    if var_ not in db_config:
        return await eod(hell, f"__There isn't any variable named__ `{var_}`. Check spelling or get full list by `{hl}vars`")
    if gvarstat(var_):
        try:
            x = gvarstat(var_)
            delgvar(var_)
            await eod(hell, f"**Deleted Variable Successfully!!** \n\n**• Variable:** `{var_}` \n**» Value:** `{x}`")
        except Exception as e:
            await eod(hell, f"**ERROR !!** \n\n`{e}`")
    else:
        await eod(hell, f"**No variable named** `{var_}`")
   

@hell_cmd(pattern="(set|get|del) var(?: |$)(.*)(?: |$)([\s\S]*)")
async def variable(hell):
    lg_id = Config.LOGGER_ID
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await eor(hell, "**[ HEROKU ]:**\n__Please setup your__ `HEROKU_APP_NAME`")
    exe = hell.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "get":
        event = await eor(hell, "Getting Variable Info...")
        cap = "Logger me chala jaa."
        capn = "Saved in LOGGER_ID !!"
        try:
            xvar = hell.pattern_match.group(2).split()[0]
            variable = xvar.upper()
            if variable in db_config:
                return await eod(event, f"This is a SQL based variable. Do `{hl}gvar {variable}` to get variable info.")
            if variable in ("ROMEOBOT_SESSION", "BOT_TOKEN", "HEROKU_API_KEY"):
                if Config.ABUSE == "ON":
                    await event.client.send_file(hell.chat_id, cjb, caption=cap)
                    await event.delete()
                    await event.client.send_message(lg_id, f"#HEROKU_VAR \n\n`{heroku_var[variable]}`")
                    return
                else:
                    await event.edit(f"**{capn}**")
                    await event.client.send_message(lg_id, f"#HEROKU_VAR \n\n`{heroku_var[variable]}`")
                    return
            if variable in heroku_var:
                return await event.edit(f"**Heroku Var:** \n\n`{variable}` = `{heroku_var[variable]}`\n")
            else:
                return await eod(event, "**Heroku Var:** \n\n__Error:__\n-> I doubt `{variable}` exists!")
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await hell.client.send_file(
                        hell.chat_id,
                        "configs.json",
                        reply_to=hell.id,
                        caption="`Output too large, sending it as a file`",
                    )
                    await event.delete()
                else:
                    await event.edit(
                        "**Heroku Var :**\n\n"
                        "================================"
                        f"\n```{result}```\n"
                        "================================"
                    )
            os.remove("configs.json")
            return
    elif exe == "set":
        event = await eor(hell, "Setting Heroku Variable...")
        xvar = hell.pattern_match.group(2)
        if not xvar:
            return await eod(event, f"`{hl}set var <Var Name> <Value>`")
        variable = xvar.upper()
        value = hell.pattern_match.group(3)
        if not value:
            variable = variable.split()[0]
            try:
                value = hell.pattern_match.group(2).split()[1]
            except IndexError:
                return await eod(event, f"`{hl}set var <Var Name> <Value>`")
        if variable in db_config:
            return await eod(event, f"This is a SQL based variable. Do `{hl}svar {variable} {value}` to set this.")
        if variable in heroku_var:
            await event.edit(f"`{variable}` **successfully changed to**  ->  `{value}`")
        else:
            await event.edit(f"`{variable}` **successfully added with value**  ->  `{value}`")
        heroku_var[variable] = value
    elif exe == "del":
        event = await eor(hell, "Getting info to delete Variable")
        try:
            xvar = hell.pattern_match.group(2).split()[0]
        except IndexError:
            return await eod(event, "`Please specify ConfigVars you want to delete`")
        variable = xvar.upper()
        if variable in db_config:
            return await eod(event, f"This is a SQL based variable. Do `{hl}dvar {variable}` to delete it.")
        if variable in heroku_var:
            await event.edit(f"**Successfully Deleted** \n`{variable}`")
            del heroku_var[variable]
        else:
            return await eod(event, f"`{variable}`  **does not exists**")


@hell_cmd(pattern="usage$")
async def dyno_usage(hell):
    event = await eor(hell, "`Processing...`")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {Config.HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await eod(event, "`Error: something bad happened`\n\n" f">.`{r.reason}`\n")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    cid = await client_id(event)
    hell_mention = cid[2]

    return await event.edit(
        "⚡ **Dyno Usage** ⚡:\n\n"
        f" ➠ __Dyno usage for__ • **{Config.HEROKU_APP_NAME}** • :\n"
        f"     ★  `{AppHours}`**h**  `{AppMinutes}`**m**  "
        f"**|**  `{AppPercentage}`**%**"
        "\n\n"
        " ➠ __Dyno hours remaining this month__ :\n"
        f"     ★  `{hours}`**h**  `{minutes}`**m**  "
        f"**|**  `{percentage}`**%**"
        f"\n\n**Owner :** {hell_mention}"
    )


@hell_cmd(pattern="logs$")
async def _(event):
    if (HEROKU_APP_NAME is None) or (HEROKU_API_KEY is None):
        return await eor(event, f"Make Sure Your HEROKU_APP_NAME & HEROKU_API_KEY are filled correct. Visit {hell_grp} for help.", link_preview=False)
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await event.reply(f"Make Sure Your Heroku AppName & API Key are filled correct. Visit {hell_grp} for help.", link_preview=False)
    cid = await client_id(event)
    hell_mention = cid[2]
    hell_data = app.get_log()
    await eor(event, hell_data, deflink=True, linktext=f"**🗒️ Heroku Logs of 💯 lines. 🗒️**\n\n🌟 **Bot Of :**  {hell_mention}\n\n🚀** Pasted**  ")


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""
    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)


CmdHelp("power").add_command(
  "reload", None, "Reloads the bot DB and SQL variables without deleting any external plugins if installed."
).add_command(
  "shutdown", None, "Turns off RomeoBot. Userbot will stop working unless you manually turn it on."
).add_command(
  "svar", "<variable name> <variable value>", "Sets the variable to SQL variables without restarting the bot.", "svar ALIVE_PIC https://telegra.ph/file/57bfe195c88c5c127a653.jpg"
).add_command(
  "gvar", "<variable name>", "Gets the info of mentioned variable from both SQL & OS.", "gvar ALIVE_PIC"
).add_command(
  "dvar", "<variable name>", "Deletes the mentioned variable from SQL variables without restarting the bot.", "dvar ALIVE_PIC"
).add_info(
  "Power Switch For Bot"
).add_warning(
  "✅ Harmless Module"
).add()

CmdHelp("heroku").add_command(
  "usage", None, "Check your heroku dyno hours status."
).add_command(
  "set var", "<Var Name> <value>", "Add new variable or update existing value/variable\nAfter setting a variable bot will restart so stay calm for 1 minute."
).add_command(
  "get var", "<Var Name>", "Gets the variable and its value (if any) from heroku."
).add_command(
  "del var", "<Var Name>", "Deletes the variable from heroku. Bot will restart after deleting the variable. So be calm for a minute 😃"
).add_command(
  "logs", None, "Gets the app log of 100 lines of your bot directly from heroku."
).add_info(
  "Heroku Stuffs"
).add_warning(
  "✅ Harmless Module"
).add()
