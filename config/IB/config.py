# ====================
#  - Librerias -
# ====================

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.execution import ExecutionFilter
from threading import Thread, Event
from ibapi.common import *
from ibapi.account_summary_tags import AccountSummaryTags
from typing import Any
import pandas as pd
import time
from database.repository.repository import writeRoutineFault
from functions.logs import printStamp
from ibapi.contract import ContractDetails
from ibapi.ticktype import TickTypeEnum
from collections import defaultdict


# ====================
# - Clases de IB API -
# ====================
class IBapi(EWrapper, EClient):

    def __init__(self):
        # Llama al constructor de la clase padre EClient
        EClient.__init__(self, self)

        # Eventos para señalizar entre hilos
        self.done = Event()  # Señal para indicar que una operación está completada
        self.connection_ready = Event()  # Señal para indicar que la conexión está lista

        # Variables para ETFs
        self.etfs = {}

        # Variables para Opciones
        self.option_chains = {}
        self.options = {}
        self.listStrikes = []

        # Variables para CASH
        self.typeCash = [
            "TotalCashValue",
            "SettledCash",
            "NetLiquidation",
            "UnrealizedPnL",
            "AvailableFunds",
        ]
        self.wallet = {key: 0 for key in self.typeCash}
        self.cuentas = defaultdict(lambda: {key: 0 for key in self.typeCash})
        self.cash = 0
        # Otras variables
        self.tiker = ""  # Variable para el ticker actual
        self.nextOrderId = None  # ID de orden siguiente
        self.statusIB = False  # Estado de conexión con IB
        self.desconect_count = 0

        # Tipos de tick
        self.tick_types = {
            0: "BID_SIZE",
            1: "BID",
            2: "ASK",
            3: "ASK_SIZE",
            4: "LAST",
            5: "LAST_SIZE",
            6: "HIGH",
            7: "LOW",
            8: "VOLUME",
            9: "CLOSE",
        }
        self.execution_details = {}
        self.commissions = {}
        self.sendError = False

        self.statusFail = ["PendingCancel", "Cancelled", "Inactive"]

        self.Error = False
        self.Error_buy = False
        self.num_cuenta = "-"
        self.alerta = False

        self.executions = []

    # ================= IB CONTROL =================
    def error(
        self, reqId: TickerId, errorCode: int, errorString: str, contract: Any = None
    ):

        if errorCode == 502:  # not connected
            self.done.set()
        elif errorCode == 504:
            self.desconect_count += 1

        else:
            if reqId == -1:
                if errorCode not in [2104, 2106, 2158, 2107, 2119]:
                    printStamp(f"Warnning Code({errorCode}) : {errorString}")
                    writeRoutineFault("Warnning", errorCode, reqId, errorString)

                if errorCode == 1100:
                    self.alerta = True
                elif errorCode == 1102:
                    self.alerta = False
                else:
                    pass

            else:
                if errorCode not in [300]:
                    printStamp(f"Error Code({errorCode}) ID({reqId}): {errorString}")
                    writeRoutineFault("Error", errorCode, reqId, errorString)
                    if errorCode == 201:
                        self.Error_buy = True

    def stop(self):
        self.disconnect()

    def nextValidId(self, orderId: int):
        self.connection_ready.set()
        self.nextOrderId = int(orderId)

        printStamp(f"ID de orden válida recibida:  {self.nextOrderId}")

    def cancelMarketData(self, reqId):
        self.cancelMktData(reqId)

    # ================= IB TICK DATA =================

    def tickPrice(self, reqId, tickType, price, attrib):
        if reqId in self.etfs:

            if tickType == 4 and price > 0:
                self.etfs[reqId]["price"] = price

        elif reqId in self.options:
            if tickType in [4, 1, 2]:
                self.options[reqId][str(self.tick_types[tickType])] = price

    def tickSize(self, reqId, tickType, size):
        if reqId in self.options:
            if tickType == TickTypeEnum.BID_SIZE:
                self.options[reqId]["BID_SIZE"] = size

            elif tickType == TickTypeEnum.ASK_SIZE:
                self.options[reqId]["ASK_SIZE"] = size

    # ================= IB OPTIONS =================

    def tikerOption(self, contract, reqId):
        tiker = self.reqContractDetails(reqId, contract)
        time.sleep(2)
        return self.tiker

    def request_option_chain(self, tiker):
        if tiker == "QQQ":

            self.reqSecDefOptParams(0, "QQQ", "", "STK", 320227571)
        elif tiker == "SPY":
            self.reqSecDefOptParams(0, "SPY", "", "STK", 756733)

        time.sleep(10)

    def securityDefinitionOptionParameter(
        self,
        reqId,
        exchange,
        underlyingConId,
        tradingClass,
        multiplier,
        expirations,
        strikes,
    ):
        chain_key = f"{exchange}_{tradingClass}"
        self.option_chains[chain_key] = {"expirations": expirations, "strikes": strikes}

    def contractDetails(self, reqId, contractDetails: ContractDetails):
        # Aquí puedes procesar los detalles del contrato de opción recibidos

        self.listStrikes.append(contractDetails.contract.strike)
        if reqId < 10:
            self.tiker = contractDetails.contract.localSymbol

    # ================= IB STATUS =================

    def orderStatus(
        self,
        orderId,
        status,
        filled,
        remaining,
        avgFillPrice,
        permId,
        parentId,
        lastFillPrice,
        clientId,
        whyHeld,
        mktCapPrice,
    ):

        printStamp(
            f"Order Status - orderId: {orderId} status: {status}  filled: {filled} remaining: {remaining} "
        )
        self.execution_details[orderId]["status"] = status

        if status == "Filled" and int(remaining) == 0:
            self.statusIB = True
            self.Error = False
            return

        if status in self.statusFail:

            if int(filled)!=0:
                self.execution_details[orderId]["status"] = "Filled"
                self.statusIB = True
                self.Error = False
                self.execution_details[orderId]["shares"] =filled
            else:
                self.Error = True
            return

        if whyHeld:
            printStamp(
                f"Order Status - orderId: {orderId} status: {status}  whyHeld: {whyHeld}  "
            )
        return


    def execDetails(self, reqId, contract, execution):

        try:
            self.execution_details[execution.orderId]["symbol"] = contract.symbol
            self.execution_details[execution.orderId]["execId"] = execution.execId
            self.execution_details[execution.orderId]["price"] = execution.price
        except:
            pass

    def commissionReport(self, commissionReport):

        try:
            for id in self.execution_details:
                if str(commissionReport.execId) == str(
                    self.execution_details[id]["execId"]
                ):
                    self.execution_details[id][
                        "commission"
                    ] = commissionReport.commission

        except:
            pass

    # ================= IB WALLET =================
    def accountSummary(
        self, reqId: int, account: str, tag: str, value: str, currency: str
    ):
        if tag in self.typeCash:

            self.cuentas[account][tag] = value

    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):

        if key in self.typeCash:

            self.cuentas[accountName][key] = val

    def accountSummaryEnd(self, reqId: int):

        self.done.set()
