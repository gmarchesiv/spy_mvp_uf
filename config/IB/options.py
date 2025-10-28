# ====================
#  - Librerias -
# ====================

from datetime import datetime, timedelta
from ib_insync import Contract
import time
from ibapi.order import *

from config.IB.wallet import wallet_cash
from functions.logs import printStamp


# =======================
#  - Funciones Options-
# =======================


# Logica de Peticion de Data de opciones
def req_Options(app, params, vars, etf):

    requestContract(app, etf, vars.strike_c, vars.exp, "C", vars.exchange)
 
    requestContract(app, etf, vars.strike_p, vars.exp, "P", vars.exchange)

    requestContract(app, etf, vars.strike_c_2, vars.exp_2, "C", vars.exchange)
 
    requestContract(app, etf, vars.strike_p_2, vars.exp_2, "P", vars.exchange)
 

# Creacion de contratos de Opciones
def create_contract_OPT(
    symbol, secType, exchange, currency, strike, expirations, typeOpt
):

    contract = Contract()
    contract.symbol = symbol  # Símbolo del subyacente
    contract.secType = secType  # Tipo de seguridad (opción)
    contract.exchange = exchange  # Intercambio
    contract.currency = currency  # Divisa
    contract.lastTradeDateOrContractMonth = (
        expirations  # Fecha de vencimiento en formato YYMMDD
    )

    contract.right = typeOpt  # Tipo de opción (C para call, P para put)
    contract.strike = strike  # Precio de ejercicio

    return contract


 


# Funcion que busca el strike mas proximo
def strikeNear(numero, lista):
    return min(lista, key=lambda x: abs(x - numero))


 

# peticion de data de un contrato
def requestContract(app, etf, strikes, expirations, tipo, exchange):

    contracts = [
        create_contract_OPT(etf, "OPT", exchange, "USD", strikes, expirations, tipo)
    ]

    for i, contract in enumerate(contracts, start=(len(app.options) + 1)):

        app.reqContractDetails(i, contract)
        time.sleep(3)
        tiker = app.tikerOption(contract, i)
        tiker = tiker.replace(" ", "")

        app.reqMktData(i, contract, "", False, False, [])
         
        app.options[i] = {
            "symbol": tiker,
            "strike": contract.strike,
            "expirations": contract.lastTradeDateOrContractMonth,
            "ASK": 0,
            "BID": 0,
            "contract": contract,
            "BID_SIZE": 0,
            "ASK_SIZE": 0,
            "etf": contract.symbol,
            "tipo": contract.right,
        }
    return i


# ==================================
#  - Funciones de Compra y Venta -
# ==================================


def sellOptionContract(params, app, vars, tipo, contract, tiker):
    # ESTRUCTURA DE LA ORDEN DE VENTA
    order = Order()
    order.action = "SELL"  # Venta
    order.orderType = "MKT"  # Tipo de orden: Mercado
    order.totalQuantity = vars.quantity  # Cantidad de contratos
    order.eTradeOnly = ""
    order.firmQuoteOnly = ""
    if app.num_cuenta != "-":
        order.account = app.num_cuenta

    # SOLICITUD DE ID
    app.reqIds(-1)
    time.sleep(1)

    # ULTIMA VERIFICACION
    printStamp(f"- ULTIMA REVISION -")
    if tipo == "P":
        printStamp(f"BID :{app.options[2]['BID']} | ASK/BID_PUT  :{round((app.options[2]['ASK'] / app.options[2]['BID'] - 1)*100,2)}%")
        if (
            params.max_askbid_venta_abs
            < (app.options[2]["ASK"] / app.options[2]["BID"] - 1)
            or app.options[2]["BID"] <= 0
        ):
            printStamp(f"NO VENTA -> BID :{app.options[2]['BID']} | ASK/BID_PUT  :{round((app.options[2]['ASK'] / app.options[2]['BID'] - 1)*100,2)}%")
            return False
    if tipo == "C":
        printStamp(f"BID :{app.options[1]['BID']} | ASK/BID_CALL :{round((app.options[1]['ASK'] / app.options[1]['BID'] - 1)*100,2)}%")
        if (
            params.max_askbid_venta_abs
            < (app.options[1]["ASK"] / app.options[1]["BID"] - 1)
            or app.options[1]["BID"] <= 0
        ):
            printStamp(f"NO VENTA -> BID :{app.options[1]['BID']} | ASK/BID_CALL :{round((app.options[1]['ASK'] / app.options[1]['BID'] - 1)*100,2)}%")
            return False

    # EJECUCION DE LA ORDEN
    app.execution_details[app.nextOrderId] = {
        "id": app.nextOrderId,
        "action": "Sell",
        "tiker": tiker,
        "type": tipo,
        "status": "",
        "symbol": "",
        "execId": 0,
        "price": 0,
        "shares": vars.quantity,
        "commission": 0,
        "save": False,
    }
    app.placeOrder(app.nextOrderId, contract, order)
    # REGISTRO
    vars.trade_hour = datetime.now(params.zone)

    return True


# - COMPRA DE CONTRATOS -
def buyOptionContract(app, params, vars, price, tipo, contract, tiker):

    # CALCULOS DE CANTIDAD DE CONTRATOS
    app.cash = wallet_cash(app, params)

    vars.quantity = (float(app.cash)) / ((float(price) * params.slippage * 100))

    # CALCULO DE CANTIDADES
    if vars.quantity < 1:
        vars.quantity = 0
        printStamp(f"-ERROR POR CANTIDAD DE CONTRATOS A COMPRAR: {vars.quantity }  -")
        return False

    elif int(vars.quantity) == 1:
        if (vars.quantity - int(vars.quantity)) >= 0.2:
            vars.quantity = 1
        else:
            vars.quantity = 0
            printStamp(
                f"-ERROR POR CANTIDAD DE CONTRATOS A COMPRAR: {vars.quantity }  -"
            )
            return False
    elif (vars.quantity - int(vars.quantity)) < 0.2:
        vars.quantity = int(vars.quantity - 1)
    else:
        vars.quantity = int(vars.quantity)
    if vars.quantity == 1 and app.Error_buy:
        vars.quantity = 0
        printStamp(f"-ERROR POR CANTIDAD DE CONTRATOS A COMPRAR: {vars.quantity }  -")
        return False
    elif app.Error_buy:
        vars.quantity = vars.quantity - 1
    else:
        pass

    # ESTRUCTURA DE LA ORDEN DE COMPRA
    order = Order()
    order.action = "BUY"  # Comprar
    order.orderType = "MKT"  # Tipo de orden: Mercado
    order.totalQuantity = int(vars.quantity)  # Cantidad de contratos
    order.eTradeOnly = ""
    order.firmQuoteOnly = ""
    if app.num_cuenta != "-":
        order.account = app.num_cuenta

    # SOLICITUD DE ID
    app.reqIds(-1)
    time.sleep(1)

    # ULTIMA VERIFICACION
    printStamp(f"- ULTIMA REVISION -")
    if tipo == "P":
        printStamp(f"ASK :{app.options[2]['ASK']} | ASK/BID_PUT :{round((app.options[2]['ASK'] / app.options[2]['BID'] - 1)*100,2)}%")
        if (
            params.max_askbid_compra_abs
            < (app.options[2]["ASK"] / app.options[2]["BID"] - 1)
            or app.options[2]["ASK"] <= 0
        ):
            printStamp(f"NO COMPRA -> ASK :{app.options[2]['ASK']} | ASK/BID_PUT :{round((app.options[2]['ASK'] / app.options[2]['BID'] - 1)*100,2)}%")
          
            return False
    if tipo == "C":
        printStamp(f"ASK :{app.options[1]['ASK']} | ASK/BID_CALL :{round((app.options[1]['ASK'] / app.options[1]['BID'] - 1)*100,2)}%")
        if (
            params.max_askbid_compra_abs
            < (app.options[1]["ASK"] / app.options[1]["BID"] - 1)
            or app.options[1]["ASK"] <= 0
        ):
            printStamp(f"NO COMPRA -> ASK :{app.options[1]['ASK']} | ASK/BID_CALL :{round((app.options[1]['ASK'] / app.options[1]['BID'] - 1)*100,2)}%")
         
            return False

    # EJECUCION DE LA ORDEN

    app.execution_details[app.nextOrderId] = {
        "id": app.nextOrderId,
        "action": "Buy",
        "tiker": tiker,
        "type": tipo,
        "status": "",
        "symbol": "",
        "execId": 0,
        "price": 0,
        "shares": vars.quantity,
        "commission": 0,
        "save": False,
    }
    app.placeOrder(app.nextOrderId, contract, order)
    # REGISTRO
    vars.priceBuy = price
    vars.trade_hour = datetime.now(params.zone)
    return True

def snapshot_2(app, etf, strike, exp, exchange):

    contracts = [
        create_contract_OPT(etf, "OPT", exchange, "USD", strike[1], exp, "C"),
        create_contract_OPT(etf, "OPT", exchange, "USD", strike[0], exp, "P"),
    ]
   
    for i, contract in enumerate(contracts, start=3):

        app.reqMktData(i, contract, "", False, False, [])
        time.sleep(3)
        app.options[i] = {
            "strike": contract.strike,
            "expirations": contract.lastTradeDateOrContractMonth,
            "ASK": 0,
            "BID": 0,
        }
def snapshot(app, etf, strike, exp, exchange):

    contracts = [
        create_contract_OPT(etf, "OPT", exchange, "USD", strike[1], exp, "C"),
        create_contract_OPT(etf, "OPT", exchange, "USD", strike[0], exp, "P"),
    ]
   
    for i, contract in enumerate(contracts, start=1):

        app.reqMktData(i, contract, "", False, False, [])
        time.sleep(3)
        app.options[i] = {
            "strike": contract.strike,
            "expirations": contract.lastTradeDateOrContractMonth,
            "ASK": 0,
            "BID": 0,
        }

 

# revision del strike disponible
def dic_checkStrike(app, expiri, etf, tipo, exhange):
    dic_strike = {}
    for exp in expiri:

        contract = create_contract_OPT(etf, "OPT", exhange, "USD", "", exp, tipo)

        app.listStrikes = []
        app.reqContractDetails(10, contract)
        time.sleep(10)

        app.listStrikes = list(set(app.listStrikes))

        app.listStrikes.sort()
        dic_strike[exp] = app.listStrikes
    return dic_strike



def checkStrike(app, exp, etf, tipo, exchange):

    contract = create_contract_OPT(etf, "OPT", exchange, "USD", "", exp, tipo)

    app.listStrikes = []
    app.reqContractDetails(10, contract)
    time.sleep(10)

    app.listStrikes.sort()
    return app.listStrikes


def list_checkExpirations(app, etf, params, exchange):
    name = f"{exchange}_{etf}"

    listExpire = list(app.option_chains[name]["expirations"])
    fecha_actual = datetime.now()

    format_str = "%Y%m%d"
    listExpire_dates = [datetime.strptime(date, format_str) for date in listExpire]

    # Ordenar la lista en orden descendente
    listExpire_dates.sort(reverse=False)
    n=0
    lista_exp = []
    for expiry_date in listExpire_dates:
        if expiry_date >= (
            fecha_actual + timedelta(days=params.days_min_exp)
        ) :
            if n!=0:
                lista_exp.append(expiry_date.strftime(format_str))
            if n>=5:
                return lista_exp
            n+=1
    return lista_exp


def list_checkExpirations_2(app, etf, params, exchange):
    name = f"{exchange}_{etf}"

    listExpire = list(app.option_chains[name]["expirations"])
    fecha_actual = datetime.now()

    format_str = "%Y%m%d"
    listExpire_dates = [datetime.strptime(date, format_str) for date in listExpire]

    # Ordenar la lista en orden descendente
    listExpire_dates.sort(reverse=False)
    n=0
    lista_exp = []
    for expiry_date in listExpire_dates:
        if expiry_date >= (
            fecha_actual + timedelta(days=params.days_min_exp )
        ) :
            lista_exp.append(expiry_date.strftime(format_str))
            if n>=5:
                return lista_exp
            n+=1
    return lista_exp