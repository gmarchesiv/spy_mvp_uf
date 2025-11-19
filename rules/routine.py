###################################################
################### LIBRERIAS  ####################
###################################################
 
import random
from config.IB.etf import req_ETFs
from config.IB.options import (
    checkStrike,
    dic_checkStrike,
    list_checkExpirations,
    list_checkExpirations_2,
    req_Options,
    snapshot,
    snapshot_2,
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
# GUARDAR OPEN DE OPCIONES
def data_option_open(app,   vars,params):

    #---------------------------------------------------
    '''
    Extraccion de los precios de Open de las opciones.
    '''
    #---------------------------------------------------
    
    vars.call_open = -1
    vars.put_open = -1

    while (vars.call_open==-1 or vars.put_open == -1):
        timeNow = datetime.now(params.zone).time()
        c_ask=app.options[1]["ASK"]
        c_bid=app.options[1]["BID"]
        p_ask=app.options[2]["ASK"]
        p_bid=app.options[2]["BID"]
        if vars.call_open==-1 and ((c_ask/c_bid)-1)<params.max_askbid_open:
            vars.call_open = app.options[1]["BID"]

        if vars.put_open==-1 and ((p_ask/p_bid)-1)<params.max_askbid_open:
            vars.put_open = app.options[2]["BID"]
      
        if   params.max_askbid_hora_open <= timeNow:
            vars.call_open = app.options[1]["BID"]
            vars.put_open = app.options[2]["BID"]
            vars.flag_bloqueo_tiempo =True
            break
        time.sleep(0.5)


    vars.call_open_2 = -1
    vars.put_open_2 = -1

    while (vars.call_open_2==-1 or vars.put_open_2 == -1):
        timeNow = datetime.now(params.zone).time()
        c_ask=app.options[3]["ASK"]
        c_bid=app.options[3]["BID"]
        p_ask=app.options[4]["ASK"]
        p_bid=app.options[4]["BID"]
        if vars.call_open_2==-1 and ((c_ask/c_bid)-1)<params.max_askbid_open:
            vars.call_open_2 = app.options[3]["BID"]

        if vars.put_open_2==-1 and ((p_ask/p_bid)-1)<params.max_askbid_open:
            vars.put_open_2 = app.options[4]["BID"]
      
        if   params.max_askbid_hora_open <= timeNow:
            vars.call_open_2 = app.options[3]["BID"]
            vars.put_open_2 = app.options[4]["BID"]
            vars.flag_bloqueo_tiempo =True
            break
        time.sleep(0.5)
        

# REALIZA LA SUSCIPCION DE DATOS
def data_susciption(app, params, vars):

    printStamp(" - Cargando Data de ETFs - ")
    req_ETFs(app, params.etf)
    # printStamp(" - FIN de Cargando Data de ETFs - ")

    printStamp(" - Cargando Data de Opciones - ")
    req_Options(app, params, vars, params.etf)
    # printStamp(" - FIN de Cargando Data de Opciones - ")

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
    while True:
        ready  = 0
  
        if app.options[3]["ASK"] > 0 and app.options[3]["BID"] > 0:
            ready += 1

        if app.options[4]["ASK"] > 0 and app.options[4]["BID"] > 0:
            ready += 1
 
        if ready == 2:
            break

        time.sleep(0.5)
    printStamp(" - Datos Recibidos - ")


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
        elif  vars.flag_bloqueo_tiempo :
            vars.status = "BLOQUEO T."
        elif  vars.bloqueo:
            vars.status = "BLOQUEO"
        else:
            pass
    timeNow = datetime.now(params.zone).time()
    if params.fd < timeNow:
        vars.status = "FD"


# ACTUALIZACION Y y REGISTRO DE JSON Y DB
def registration(app, vars, params):
     
    update_status(app, vars,params)
    saveJson(vars, app, params, False)
    writeDayTrade(app, vars, params)
   

# Calculos


def calculations(app, vars, params):

    # ================================
    #  -CALCULOS-
    # ================================
    timeNow = datetime.now(params.zone).time()

 

    # DATOS
    vars.cask = app.options[1]["ASK"]
    vars.cbid = app.options[1]["BID"]
    vars.pask = app.options[2]["ASK"]
    vars.pbid = app.options[2]["BID"]

 

    vars.vix= app.etfs[6]['price']
 

    # CALCULOS
    vars.askbid_call = vars.cask / vars.cbid - 1
    vars.askbid_put = vars.pask / vars.pbid - 1
    vars.dcall = vars.cbid / vars.call_close - 1
    vars.dput = vars.pbid / vars.put_close - 1
    vars.docall = vars.cbid / vars.call_open - 1
    vars.doput = vars.pbid / vars.put_open - 1
 
    vars.cask_2 = app.options[3]["ASK"]
    vars.cbid_2 = app.options[3]["BID"]
    vars.pask_2 = app.options[4]["ASK"]
    vars.pbid_2 = app.options[4]["BID"]


    # CALCULOS
    vars.askbid_call_2 = vars.cask_2 / vars.cbid_2 - 1
    vars.askbid_put_2 = vars.pask_2 / vars.pbid_2 - 1
    vars.dcall_2 = vars.cbid_2 / vars.call_close_2 - 1
    vars.dput_2 = vars.pbid_2 / vars.put_close_2 - 1
    vars.docall_2= vars.cbid_2 / vars.call_open_2 - 1
    vars.doput_2 = vars.pbid_2 / vars.put_open_2 - 1


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
        print("CALLS:",call_list)
        print("PUTS:",put_list)
        # put_strike = put_list[-2]  
        # call_strike = call_list[1] 

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
    # app.options={}
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



# REGISTRO DE STRIKES
def registro_strike_2(app, vars, params):

    # PEDIMOS LA CADENA DE OPCIONES
    app.request_option_chain(app.etfs[5]["symbol"])

 
    vars.exchange = params.exchange[0]  # SELECCION DEL EXCEHANGE

    list_exp = list_checkExpirations_2(app, app.etfs[5]["symbol"], params, vars.exchange)


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
        print("CALLS:",call_list)
        print("PUTS:",put_list)
        put_strike = put_list[-1]  
        call_strike = call_list[0] 
        exp_escogido = exp
        break
     
    

    printStamp(f"EXP: {exp_escogido}")
 
    printStamp(f"RANGOS SELECCIONADOS --> PUT: {put_strike} /  CALL: {call_strike}")

    app.cancelMarketData(3)
    time.sleep(1)
    del app.options[3]

    app.cancelMarketData(4)
    time.sleep(1)
    del app.options[4]
    time.sleep(1)
    # print("LLEGUE HASTA AQUI")
    snapshot_2(app, app.etfs[5]["symbol"], [put_strike, call_strike], exp, vars.exchange)
    printStamp(f"EXTRAYENDO DATOS DE LA OPCION")
    while True:
        timeNow = datetime.now(params.zone).time()
        if dt_time(16, 30) < timeNow:
            break
        readyOpt = 0
        if int(timeNow.second) in params.frecuencia_accion:
            print("===============================================")
            printStamp(f"CASK: {app.options[3]['ASK'] } | CBID: {app.options[3]['BID'] }")
            printStamp(f"PASK: {app.options[4]['ASK'] } | PBID: {app.options[4]['BID'] }")
        if app.options[3]["BID"] > 0 and params.max_askbid_venta_abs > (app.options[3]["ASK"] / app.options[3]["BID"] - 1):
            readyOpt += 1
     
        if app.options[4]["BID"] > 0 and params.max_askbid_venta_abs > (app.options[4]["ASK"] / app.options[4]["BID"] - 1):
            readyOpt += 1
            
   
        if readyOpt == 2:
            break

        time.sleep(0.5)

    
    vars.exp_2 = exp
    vars.strike_p_2 = put_strike
    vars.strike_c_2 = call_strike
    vars.put_close_2 = app.options[4]["BID"]
    vars.call_close_2 = app.options[3]["BID"]
    print("===============================================")
    printStamp(
        f"GUARDADO: {vars.exp_2} | PUT-STRIKE: {vars.strike_p_2} PUT-CLOSE: {vars.put_close_2} | CALL-STRIKE: {vars.strike_c_2} CALL-CLOSE: {vars.call_close_2}  "
    )
    timeNow = datetime.now(params.zone).time()
    vars.hora_inicio = str(timeNow)
