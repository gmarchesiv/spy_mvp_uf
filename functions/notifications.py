import asyncio
import telegram
import time
import random

from functions.logs import printStamp


async def send_message(text, chat_id, bot):
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id)


async def main(msg, chat_id, bot):
    # Sending a message
    await send_message(text=msg, chat_id=chat_id, bot=bot)


def sendTelegram(params, msg):
    bot = telegram.Bot(token=params.token)
    asyncio.run(main(msg, params.tele, bot))


def sendStart(app, params):
    msg = f"""
======================
- INICIO DE RUTINA -
USER: {params.name}
ETF:{params.etf}
TRADING MODE: {params.typeIB} 
======================
"""
    try:
        sleep_time = random.uniform(1, 10)
        time.sleep(sleep_time)
        sendTelegram(params, msg)
    except:
        printStamp("-ERROR AL ENVIAR TELEGRAM: sendStart-")


def sendEnd(app, params):
    msg = f"""
======================
- FIN DE RUTINA -
USER: {params.name}
SETTLED CASH: $ {app.wallet["SettledCash"]}
TOTAL CASH : $ {app.wallet["TotalCashValue"]}
======================
"""
    try:
        sleep_time = random.uniform(1, 10)
        time.sleep(sleep_time)
        sendTelegram(params, msg)
    except:
        printStamp("-ERROR AL ENVIAR TELEGRAM: sendEnd-")


def sendBuy(app, params, detail, vars):

    msg = f"""
======================
- Notificación -
USER: {params.name}
ETF:{params.etf}
TIPO: COMPRA {detail["symbol"]} - {detail["type"]}
CANTIDAD : {detail["shares"]}
ASK : {detail["price"]}
REGLA : {vars.regla_ant}
======================
"""
    try:
        sleep_time = random.uniform(1, 10)
        time.sleep(sleep_time)
        sendTelegram(params, msg)
    except:
        printStamp("-ERROR AL ENVIAR TELEGRAM: sendBuy-")


def sendSell(app, params, detail, vars):
    msg = f"""
======================
- Notificación -
USER: {params.name}
ETF:{params.etf}
TIPO: Venta {detail["symbol"]} - {detail["type"]}
CANTIDAD : {detail["shares"]}
BID : {detail["price"]}
REGLA : {vars.regla_ant}
======================
"""
    try:
        sleep_time = random.uniform(1, 10)
        time.sleep(sleep_time)
        sendTelegram(params, msg)
    except:
        printStamp("-ERROR AL ENVIAR TELEGRAM: sendSell-")


def sendError(params, razon):
    msg = f"""
======================
- Alerta de Error -
USER: {params.name}
ETF:{params.etf}
TIPO: {razon}
======================
"""
    try:
        sleep_time = random.uniform(1, 5)
        time.sleep(sleep_time)
        sendTelegram(params, msg)
    except:
        printStamp("-ERROR AL ENVIAR TELEGRAM: sendError-")
