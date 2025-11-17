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
    sleep_time = random.uniform(1, 15)
    time.sleep(sleep_time)
    await send_message(text=msg, chat_id=chat_id, bot=bot)


def sendTelegram(params, msg):
    bot = telegram.Bot(token=params.token)
    asyncio.run(main(msg, params.tele, bot))


def sendStart(app, params):
    #---------------------------------------------------
    '''
    Envio de mensaje de Inicio de sesión.
    '''
    #---------------------------------------------------
 
    msg = f"""
======================
- INICIO DE RUTINA -
USER: {params.name}
ETF:{params.etf}
TRADING MODE: {params.typeIB} 
======================
"""
    try:
      
        sendTelegram(params, msg)
    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("-ERROR AL ENVIAR TELEGRAM: sendStart-")


def sendEnd(app, params):

    #---------------------------------------------------
    '''
    Envio de mensaje de Fin de sesión.
    '''
    #---------------------------------------------------

    msg = f"""
======================
- FIN DE RUTINA -
USER: {params.name}
SETTLED CASH: $ {app.wallet["SettledCash"]}
TOTAL CASH : $ {app.wallet["TotalCashValue"]}
======================
"""
    try:
        
        sendTelegram(params, msg)
    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("-ERROR AL ENVIAR TELEGRAM: sendEnd-")


def sendBuy(app, params, detail, vars):

    #---------------------------------------------------
    '''
    Envio de mensaje de Compra de opciones.
    '''
    #---------------------------------------------------

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
  
        sendTelegram(params, msg)
    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("-ERROR AL ENVIAR TELEGRAM: sendBuy-")


def sendSell(app, params, detail, vars):

    #---------------------------------------------------
    '''
    Envio de mensaje de Venta de opciones.
    '''
    #---------------------------------------------------


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
        
        sendTelegram(params, msg)
    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("-ERROR AL ENVIAR TELEGRAM: sendSell-")


def sendError(params, razon):

    #---------------------------------------------------
    '''
    Envio de mensaje de Alerta de Error.
    '''
    #---------------------------------------------------

    msg = f"""
======================
- Alerta de Error -
USER: {params.name}
ETF:{params.etf}
TIPO: {razon}
======================
"""
    try:
         
        sendTelegram(params, msg)
    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("-ERROR AL ENVIAR TELEGRAM: sendError-")
