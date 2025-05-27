###################################################
################### LIBRERIAS  ####################
###################################################
 
import random
from config.IB.etf import req_ETFs
from config.IB.options import (
    dic_checkStrike,
    list_checkExpirations,
    req_Options,
    snapshot,
)
from config.IB.wallet import wallet_cash, wallet_load
from database.repository.repository import writeDayTrade, writeTransactions, writeWallet
from functions.broadcasting import broadcasting_Aliniar
from functions.logs import printStamp
from datetime import datetime

from functions.notifications import sendBuy, sendSell
from datetime import time as dt_time
import random

import time

from functions.saveJson import saveJson

# ====================
#  - Funciones -
# ====================


# REALIZA LA SUSCIPCION DE DATOS
def data_susciption(app, params, vars):

    printStamp(" - Cargando Data de ETFs - ")
    req_ETFs(app, params.etf)
    printStamp(" - FIN de Cargando Data de ETFs - ")

    printStamp(" - Cargando Data de Opciones - ")
    req_Options(app, params, vars, params.etf)
    printStamp(" - FIN de Cargando Data de Opciones - ")


# ACTUALIZA LOS STATUS
def update_status(app, vars,params):
    if app.alerta:
        vars.status = "DESCONEXION"
    else:
        vars.status = "ON"
        if vars.call:
            vars.status = "CALL"

        elif vars.put:
            vars.status = "PUT"

        elif vars.call == False and vars.put == False and vars.compra == False:
            vars.status = "SLEEP"
        else:
            pass
    timeNow = datetime.now(params.zone).time()
    if params.fd < timeNow:
        vars.status = "FD"


# ACTUALIZACION Y y REGISTRO DE JSON Y DB
def registration(app, vars, params):
    wallet_load(app, params)
    update_status(app, vars,params)
    saveJson(vars, app, params, False)
    writeDayTrade(app, vars, params)
    vars.regla = ""
    if vars.call == False and vars.put == False:
        vars.pico = 0
        vars.caida = 0
        vars.rentabilidad = 0


# Calculos


def calculations(app, vars, params):

    # ================================
    #  -CALCULOS-
    # ================================
    timeNow = datetime.now(params.zone).time()

    if int(timeNow.second) == 0:
        vars.minutos += 1
        vars.n_minutos += 1
        vars.minutos_trade += 1

    # DATOS
    vars.cask = app.options[1]["ASK"]
    vars.cbid = app.options[1]["BID"]
    vars.pask = app.options[2]["ASK"]
    vars.pbid = app.options[2]["BID"]
    vars.vix= app.etfs[6]['price']
    broadcasting_Aliniar(vars)

    # CALCULOS
    vars.askbid_call = vars.cask / vars.cbid - 1
    vars.askbid_put = vars.pask / vars.pbid - 1
    vars.dcall = vars.cbid / vars.call_close - 1
    vars.dput = vars.pbid / vars.put_close - 1
    vars.docall = vars.cbid / vars.call_open - 1
    vars.doput = vars.pbid / vars.put_open - 1
    if vars.askbid_call >0 and params.umbral_askbid>vars.askbid_call:
        vars.askbid_call_prom.append(vars.askbid_call)

    if vars.askbid_put >0 and params.umbral_askbid>vars.askbid_put:
        vars.askbid_put_prom.append(vars.askbid_put)

     
    if vars.rule:
        if vars.dcall >= params.umbral_cr2:
            vars.flag_Call_R2 = True
        if vars.dput >= params.umbral_pr2:
            vars.flag_Put_R2 = True
 
        vars.rule = False
        vars.hora_inicio = str(timeNow)
 


# GUARDADO DE TRANSACCIONES
def saveTransaction(app, params, vars):
    for idreq in app.execution_details:

        if (
            app.execution_details[idreq]["save"] == False
            and app.execution_details[idreq]["status"] == "Filled"
        ):

            if app.execution_details[idreq]["action"] == "Sell":
                if vars.accion_mensaje == 1:
                    sendSell(app, params, app.execution_details[idreq], vars)
                    vars.accion_mensaje = 2

                if app.execution_details[idreq]["price"] != 0:
                    wallet_load(app, params)

                    app.cash = wallet_cash(app, params)
                    app.execution_details[idreq]["shares"] = vars.quantity

                    writeTransactions(app, idreq, vars)
                    app.execution_details[idreq]["save"] = True

                    vars.trades.append(5)

                    vars.priceBuy = 0
                    writeWallet(app)
            else:
                vars.quantity= app.execution_details[idreq]["shares"] 
                if vars.accion_mensaje == 0:
                    sendBuy(app, params, app.execution_details[idreq], vars)

                    vars.accion_mensaje = 1
                    vars.minutos_trade = 0

                if app.execution_details[idreq]["price"] != 0:
                    writeTransactions(app, idreq, vars)
                    app.execution_details[idreq]["save"] = True
                    vars.priceBuy = app.execution_details[idreq]["price"]
                    vars.real_priceBuy= app.execution_details[idreq]["price"]
                    app.execution_details[idreq]["shares"] = vars.quantity
                    writeWallet(app)


# REGISTRO DE STRIKES
def registro_strike(app, vars, params):

    # PEDIMOS LA CADENA DE OPCIONES
    app.request_option_chain(app.etfs[5]["symbol"])

    # PEDIMOS EL EXPERI QUE NOS TOCA
    valor_aleatorio_exchange = random.randint(
        0, len(params.exchange) - 1
    )  # SELECCION DEL EXCEHANGE

    vars.exchange = params.exchange[valor_aleatorio_exchange]  # SELECCION DEL EXCEHANGE

    list_exp = list_checkExpirations(app, app.etfs[5]["symbol"], params, vars.exchange)

    # TOMAMOS ALEATORIAMENTE UNO

    # valor_aleatorio = random.randint(0, len(list_exp) - 1)
    valor_aleatorio = 0
    vars.dic_strike = {}
    vars.dic_strike = dic_checkStrike(
        app, list_exp, app.etfs[5]["symbol"], "C", vars.exchange
    )

    exp_escogido = list_exp[valor_aleatorio]

    printStamp(f"EXP: {exp_escogido}")

    vars.strikes = {}

    precio = app.etfs[5]["price"]
    printStamp(f"PRECIO: {app.etfs[5]['price']} $")

    strikes_dic = {}
    n = 0
    for exp in vars.dic_strike:

        call = int(precio * ((100 + params.rangos_strikes[n][1]) / 100))
        put = int(precio * ((100 - params.rangos_strikes[n][1]) / 100))

        call_inf = int(precio * ((100 + params.rangos_strikes[n][0]) / 100))
        put_inf = int(precio * ((100 - params.rangos_strikes[n][0]) / 100))

        printStamp(f"{exp} - RANGOS --> PUT : {put} - {put_inf} | CALL :{call_inf} - {call}")

        strikes_dic[exp] = {"call": [], "put": []}

        put_list = [
            float(x) for x in vars.dic_strike[exp] if put <= float(x) <= put_inf
        ]
        call_list = [
            float(x) for x in vars.dic_strike[exp] if call_inf <= float(x) <= call
        ]

        if len(call_list) > 2:
            call_list = call_list[:2]
        if len(put_list) > 2:
            put_list = put_list[-2:]
        if len(call_list) == 0:
            suma = 1
            while True:
                call_list = [
                    float(x)
                    for x in vars.dic_strike[exp]
                    if (call_inf) <= float(x) <= (call + suma)
                ]
                if len(call_list) != 0:
                    break
                else:
                    suma += 1

        if len(put_list) == 0:
            resta = 1
            while True:
                put_list = [
                    float(x)
                    for x in vars.dic_strike[exp]
                    if (put - resta) <= float(x) <= (put_inf)
                ]
                if len(put_list) != 0:
                    break
                else:
                    resta += 1
        printStamp(f"{exp} - CALL : {call_list}  ")
        printStamp(f"{exp} - PUT : {put_list}  ")

        strikes_dic[exp]["put"] = put_list
        strikes_dic[exp]["call"] = call_list

        break
        # n += 1
        # if len(strikes_dic[exp]["put"]) == 0 or len(strikes_dic[exp]["call"]) == 0:
        #     del strikes_dic[exp]
    vars.dic_exp_strike = strikes_dic

    printStamp(f"RANGOS SELECCIONADOS --> {vars.dic_exp_strike}")
    exp = exp_escogido

    # ESCOGEMOS VALORES ALEATORIOS

    call_list = vars.dic_exp_strike[exp]["call"]
    # valor_aleatorio = random.randint(0, len(call_list) - 1)

    call_strike =  min(call_list)
    # call_strike = float(call_list[valor_aleatorio])

    put_list = vars.dic_exp_strike[exp]["put"]
    # valor_aleatorio = random.randint(0, len(put_list) - 1)

    put_strike = max(put_list)

    app.cancelMarketData(1)
    time.sleep(1)
    del app.options[1]

    app.cancelMarketData(2)
    time.sleep(1)
    del app.options[2]

    snapshot(app, app.etfs[5]["symbol"], [put_strike, call_strike], exp, vars.exchange)
    while True:
        timeNow = datetime.now(params.zone).time()
        if dt_time(16, 30) < timeNow:
            break
        readyOpt = 0

        if app.options[1]["BID"] > 0 and params.max_askbid_venta > (app.options[1]["ASK"] / app.options[1]["BID"] - 1):
            readyOpt += 1
        if app.options[2]["BID"] > 0 and params.max_askbid_venta > (app.options[2]["ASK"] / app.options[2]["BID"] - 1):
            readyOpt += 1
        if readyOpt == 2:
            break

        time.sleep(0.5)

    # if dt_time(16, 30) < timeNow:
    #     return
    vars.exp = exp
    vars.strike_p = put_strike
    vars.strike_c = call_strike
    vars.put_close = app.options[2]["BID"]
    vars.call_close = app.options[1]["BID"]

    printStamp(
        f"GUARDADO: {vars.exp} | PUT-STRIKE: {vars.strike_p} PUT-CLOSE: {vars.put_close} | CALL-STRIKE: {vars.strike_c} CALL-CLOSE: {vars.call_close}  "
    )
    timeNow = datetime.now(params.zone).time()
    vars.hora_inicio = str(timeNow)
