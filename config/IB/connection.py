# ====================
#  - Librerias -
# ====================

import json
from config.IB.config import IBapi
from functions.logs import printStamp
import time
from threading import Thread
from ibapi.account_summary_tags import AccountSummaryTags

from datetime import datetime
from datetime import time as dt_time


# ============================
#  - Funciones de conexcion-
# ============================
# Bucle de conexcion
def run_loop(app):
    app.run()


# Conexión
def ibkr_connection(params):
    connection_record(params, False)
    for attempt in range(params.time_connection):
        app = IBapi()
        app.connect(params.ip, params.port, clientId=params.client)

        # Iniciar el bucle en un hilo separado
        api_thread = Thread(target=run_loop, args=(app,), daemon=True)
        api_thread.start()

        printStamp(f"Intento {attempt + 1} de conexión...")

        # Esperar hasta que la conexión se establezca o agotar tiempo
        if app.connection_ready.wait(timeout=1):
            printStamp("Conexión exitosa.")
            # Solicitud de la Billetera del cliente
            app.reqAccountSummary(
                9001,
                "All",
                "AvailableFunds,NetLiquidation,SettledCash,UnrealizedPnL,TotalCashValue",
            )
            app.done.wait()
            printStamp(" - Servidor conectado - ")
            connection_record(params, True)
            return app, api_thread, False

        # Si falla, desconectar y esperar antes del próximo intento
        app.disconnect()
        api_thread.join()
        time.sleep(1)  # Pequeña pausa antes del siguiente intento
    connection_record(params, False)
    return None, None, True


def test_ibkr_connection(params):
    connection_record(params, False)
    for attempt in range(params.time_connection):
        app = IBapi()
        app.connect(params.ip, params.port, clientId=params.client)

        # Iniciar el bucle en un hilo separado
        api_thread = Thread(target=run_loop, args=(app,), daemon=True)
        api_thread.start()

        printStamp(f"Intento {attempt + 1} de conexión...")

        # Esperar hasta que la conexión se establezca o agotar tiempo
        if app.connection_ready.wait(timeout=1):
            printStamp("-TEST de Conexión exitosa-")
            connection_record(params, True)
            app.disconnect()
            api_thread.join()
            return

        # Si falla, desconectar y esperar antes del próximo intento

        app.disconnect()
        api_thread.join()
        time.sleep(1)  # Pequeña pausa antes del siguiente intento

    # Si se agotan los intentos
    printStamp("No se pudo conectar después de 3 minutos.")
    connection_record(params, False)
    return


# REGISTRO DE CONEXION EXITOSA
def connection_record(params, val):
    file_name = "/usr/src/app/data/vars.json"
    with open(file_name, "r") as file:
        datos = json.load(file)
        now = datetime.now(params.zone)
        datos["conexion"] = val
        datos["date"] = now.date().isoformat()
        datos["time"] = now.time().isoformat()

    with open(file_name, "w") as file:
        json.dump(datos, file, indent=4)


# CARGA DE DATOS PERDIDOS
def load_app_vars(app, vars):

    app.cash = vars.cash
    app.statusIB = vars.statusIB
    app.execution_details = vars.execution_details
    app.commissions = vars.commissions

    app.sendError = vars.sendError
    app.Error = vars.Error
    app.Error_buy = vars.Error_buy
