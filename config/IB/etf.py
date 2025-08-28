# ====================
#  - Librerias -
# ====================

from ib_insync import Contract
import time

# ====================
#  - Funciones ETFs-
# ====================


# Creacion de contratos ETFs
def create_contract(symbol, secType, exchange, currency):

    #---------------------------------------------------
    '''
    Genera la estructura del contrato de ETFs.
    '''
    #---------------------------------------------------

    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency
    return contract


# Peticion de Data ETFs
def req_ETFs(app, etf):

    #---------------------------------------------------
    '''
    Suscripcion de datos de ETFs, genera un id y un 
    diccionario para poder ser llamado,
    este cuenta con informacion del ETF.
    '''
    #---------------------------------------------------

    # Contratos iniciales

    contracts = [
        create_contract(etf, "STK", "SMART", "USD"),
        create_contract("VIX", "IND", "CBOE", "USD"),
    ]
    app.reqMarketDataType(1)

    for i, contract in enumerate(contracts, start=5):
        app.reqMktData(i, contract, "", False, False, [])
        # time.sleep(2)
        app.etfs[i] = {
            "symbol": contract.symbol,
            "price": 0,
            "contract": contract,
        }
 