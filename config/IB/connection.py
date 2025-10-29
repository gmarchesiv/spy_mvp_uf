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

    #---------------------------------------------------
    '''
    Intentara conectarse una N cantidad de veces a 
    interactive Broker Gateway y luego de generar la 
    conexión, pedira informacion del cliente 
    ( # de cuenta , cash ,etc).
    '''
    #---------------------------------------------------
    
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

    #---------------------------------------------------
    '''
    Intentara conectarse una N cantidad de veces a 
    interactive Broker Gateway para hacer un test 
    de conexión.
    '''
    #---------------------------------------------------

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

    #---------------------------------------------------
    '''
    Guardara informacion de los test de conexión 
    '''
    #---------------------------------------------------

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
def load_app_vars(app, varsApp):

    #---------------------------------------------------
    '''
    Carga de las variables de APP de las funciones
    internas del IB-Gateway, para recuperar estados de
    transacciones en un nuevo reinicio.
    '''
    #---------------------------------------------------

    app.cash = varsApp.cash
    app.statusIB = varsApp.statusIB
    app.execution_details = varsApp.execution_details
    app.commissions = varsApp.commissions
    app.sendError = varsApp.sendError
    app.Error = varsApp.Error
    app.Error_buy = varsApp.Error_buy
