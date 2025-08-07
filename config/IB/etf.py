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
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency
    return contract


# Peticion de Data ETFs
def req_ETFs(app, etf):

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

    # loadData = True

    # while loadData:
    #     readyEtf = 0

    #     for i in app.etfs:
    #         if app.etfs[i]["price"] > 0:
    #             readyEtf += 1
    #     if readyEtf == len(app.etfs):
    #         loadData = False
    #     time.sleep(0.5)
