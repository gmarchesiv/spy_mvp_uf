###################################################
################### LIBRERIAS  ####################
###################################################
 
import asyncio
import random
from config.IB.etf import req_ETFs
from config.IB.options import (
    checkStrike,
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

from functions.saveVars import saveApp, saveVars

# ====================
#  - Funciones -
# ====================

# GUARDAR OPEN DE OPCIONES
def data_option_open(app,   vars):

    #---------------------------------------------------
    '''
    Extraccion de los precios de Open de las opciones.
    '''
    #---------------------------------------------------
    
    # TODO AGREGAR ASK BID FILTER

    vars.call_open = app.options[1]["BID"]
    vars.put_open = app.options[2]["BID"]


# REALIZA LA SUSCIPCION DE DATOS
def data_susciption(app, params, vars):

    #---------------------------------------------------
    '''
    Suscripcion de datos de ETFs, y 
    contratos de opciones , finalmente esperamos a que 
    los datos esten recibiendoce llenos y sin errores.
    '''
    #---------------------------------------------------

    printStamp(" - Cargando Data de ETFs - ")
    req_ETFs(app, params.etf)
 

    printStamp(" - Cargando Data de Opciones - ")
    req_Options(app, vars, params.etf)
  

    printStamp(" - Esperando Datos - ")

    while True:
        ready  = 0
        if app.etfs[5]["price"] > 0:
            ready += 1
        if app.etfs[6]["price"] > 0:
            ready += 1
        if app.options[1]["ASK"] > 0 and app.options[1]["BID"] > 0:
            ready += 1

        if app.options[2]["ASK"] > 0 and app.options[2]["BID"] > 0:
            ready += 1
 
        if ready == 4:
            break

        time.sleep(0.5)

    printStamp(" - Datos Recibidos - ")


# ACTUALIZA LOS STATUS
def update_status(app, vars,varsApp, params):
    #---------------------------------------------------
    '''
    Actualiza la etiqueta de status en el dashboard
    segun sea el caso.
    '''
    #---------------------------------------------------
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
        elif  varsApp.flag_bloqueo_tiempo :
            vars.status = "BLOQUEO T."
        elif  vars.bloqueo:
            vars.status = "BLOQUEO"
        else:
            pass
    timeNow = datetime.now(params.zone).time()
    if params.fd < timeNow:
        vars.status = "FD"


# ACTUALIZACION Y y REGISTRO DE JSON Y DB
def registration(app, vars,varsApp, varsLb,params):
    #---------------------------------------------------
    '''
    Registra y actualiza estados de la maquina.
    '''
    #---------------------------------------------------

    wallet_load(app, params)
    update_status(app, vars,varsApp, params)
    
    asyncio.run(saveVars(vars, app, params, False))
    asyncio.run(saveApp(varsApp, app,  params  ))
    writeDayTrade(app, vars,varsLb, params)
    vars.regla = ""
    if vars.call == False and vars.put == False:
        vars.pico = 0
        vars.caida = 0
        vars.rentabilidad = 0


# Calculos


def calculations(app, vars,varsBc, params):

    #---------------------------------------------------
    '''
    Extrae una muestra de los precios actuales de los 
    ETFs y opciones , tambien puede alinear en caso 
    detecte entrada de datos y realiza algunas 
    operaciones de rutina.
    '''
    #---------------------------------------------------

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
    broadcasting_Aliniar(varsBc,vars)

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

    #---------------------------------------------------
    '''
    Verifica si hubo un cambio de el diccionario de 
    transacciones para poder enviar notificacion y
    guardar los datos reales de la transaccion como
    son el precio real.
    '''
    #---------------------------------------------------

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

 
    vars.exchange = params.exchange[0]  # SELECCION DEL EXCEHANGE

    list_exp = list_checkExpirations(app, app.etfs[5]["symbol"], params, vars.exchange)


    precio = app.etfs[5]["price"]
    printStamp(f"PRECIO: {app.etfs[5]['price']} $")

    call = int(precio * ((100 + params.rangos_strikes[0][1]) / 100))
    put = int(precio * ((100 - params.rangos_strikes[0][1]) / 100))

    call_inf = int(precio * ((100 + params.rangos_strikes[0][0]) / 100))
    put_inf = int(precio * ((100 - params.rangos_strikes[0][0]) / 100))
    
    printStamp(f"RANGOS --> PUT : {put} - {put_inf} | CALL :{call_inf} - {call}")


    for exp in list_exp:
        strikes = checkStrike(
        app, exp, app.etfs[5]["symbol"], "C", vars.exchange
    )
        put_list = [
            float(x) for x in strikes if put <= float(x) <= put_inf
        ]
        call_list = [
            float(x) for x in strikes if call_inf <= float(x) <= call
        ]
        # Ordenar listas
        put_list.sort()
        call_list.sort()
        printStamp(f"EXP: {exp} - PUTs:{put_list} / CALLs:{call_list}")
        if len(put_list)==0 or len(call_list)==0:
            continue 
        put_strike = put_list[-1]  
        call_strike = call_list[0] 
        exp_escogido = exp
        break
     
    

    printStamp(f"EXP: {exp_escogido}")
 
    printStamp(f"RANGOS SELECCIONADOS --> PUT: {put_strike} /  CALL: {call_strike}")

    app.cancelMarketData(1)
    time.sleep(1)
    del app.options[1]

    app.cancelMarketData(2)
    time.sleep(1)
    del app.options[2]

    snapshot(app, app.etfs[5]["symbol"], [put_strike, call_strike], exp, vars.exchange)
    printStamp(f"EXTRAYENDO DATOS DE LA OPCION")
    while True:
        timeNow = datetime.now(params.zone).time()
        if dt_time(16, 30) < timeNow:
            break
        readyOpt = 0
        if int(timeNow.second) in params.frecuencia_accion:
            print("===============================================")
            printStamp(f"CASK: {app.options[1]['ASK'] } | CBID: {app.options[1]['BID'] }")
            printStamp(f"PASK: {app.options[2]['ASK'] } | PBID: {app.options[2]['BID'] }")
        if app.options[1]["BID"] > 0 and params.max_askbid_venta_abs > (app.options[1]["ASK"] / app.options[1]["BID"] - 1):
            readyOpt += 1
     
        if app.options[2]["BID"] > 0 and params.max_askbid_venta_abs > (app.options[2]["ASK"] / app.options[2]["BID"] - 1):
            readyOpt += 1
            
   
        if readyOpt == 2:
            break

        time.sleep(0.5)

    
    vars.exp = exp
    vars.strike_p = put_strike
    vars.strike_c = call_strike
    vars.put_close = app.options[2]["BID"]
    vars.call_close = app.options[1]["BID"]
    print("===============================================")
    printStamp(
        f"GUARDADO: {vars.exp} | PUT-STRIKE: {vars.strike_p} PUT-CLOSE: {vars.put_close} | CALL-STRIKE: {vars.strike_c} CALL-CLOSE: {vars.call_close}  "
    )
    timeNow = datetime.now(params.zone).time()
    vars.hora_inicio = str(timeNow)
