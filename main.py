###################################################
################### LIBRERIAS  ####################
###################################################
 
import time
import asyncio
from datetime import datetime
 
# config/
from config.IB.connection import test_ibkr_connection, ibkr_connection, load_app_vars


from config.IB.wallet import wallet_config 
from config.params import parameters
from config.vars import variables
from config.broadcasting import broadcasting
# DataBase
from database.repository.repository import writeRegister

# funtions/

from functions.broadcasting import *
from functions.clean import clean_broadcasting, clean_vars
from functions.events import countdown, isTradingDay
from functions.labels import generar_label
from functions.logs import *


from functions.notifications import sendError, sendStart
from functions.saveJson import saveJson

# rules/


from rules.buy import buyOptions
from rules.routine import (
    calculations,
    data_option_open,
    data_susciption,
    registration,
    registro_strike,
    registro_strike_2,
    saveTransaction 
)
# from rules.sell import sell_obligatoria, sellOptions


# database/
from database.repository.repository import *
from rules.sell import sellOptions


# ====================
#  - Funciones -
# ====================
def main():

    try:

        # ================================
        #  - Variables y Parametros -
        # ================================

        # VARIABLES
        vars = variables(debug_mode=False)
 

        # PARAMETROS
        params = parameters(debug_mode=False)

        # ====================
        #  - TEST CONNECTION -
        # ====================

        # PRUEBA DE CONEXION A IBKR AL ARRANQUE
        timeNow = datetime.now(params.zone).time()

        if timeNow < params.rutina[0] or timeNow >= params.rutina[1]:
            test_ibkr_connection(params)
            return

        # ====================
        #  - Feriados -
        # ====================
        if isTradingDay(params):
            test_ibkr_connection(params)
            return

        # ---------------------------------

        # ====================
        #  - conexcion a IB -
        # ====================

        app, api_thread, status = ibkr_connection(params)
        if status:
            return

        # ESPERAR HASTA INICIAR EL DIA
        countdown(params.zone)

        writeRegister(params.name, params.zone)

        # ==========================
        #  - SUSCRIPCIONES A DATOS -
        # ==========================
        data_susciption(app, params, vars)

        # ====================
        #  -   AL INICIAR    -
        # ====================

        # ====================
        #  - LIMPIEZA -
        # ====================
        clean_broadcasting(vars )  # NO PUEDE INICIAR CON DATOS BROADCASTING

        now = datetime.now(params.zone).strftime("%Y-%m-%d")

        if vars.fecha != now:
            clean_vars(vars)
            data_option_open(app,   vars,params)
            generar_label(params, vars,app)
 
        else:
            load_app_vars(app, vars)

        wallet_config(app, params, vars)

        # sendStart(app, params)
        
        printStamp(" - INICIO DE RUTINA - ")
        # # ====================
        # #  - Rutina -
        # # ====================

        while True:

            timeNow = datetime.now(params.zone).time()
            # MIENTRAS NO SEA FIN DE DIA
            if params.fd >= timeNow:
                if (timeNow.minute % 10 == 0 or timeNow.minute % 10 == 5):
                    if vars.flag_minuto_label:
                        generar_label(params, vars,app)
                        vars.flag_minuto_label=False
                        time.sleep(0.5)
                        calculations(app, vars, params)
                        readIBData(app, vars) 
                else:
                    vars.flag_minuto_label=True
            
                if int(timeNow.second) in params.frecuencia_accion:
                    calculations(app, vars, params)  # CALCULOS DE RUTINA
                    # readIBData(app, vars)  # LOGS DE LOS CALCULOS
                  

                    registration(app, vars, params)

                    time.sleep(0.5)
            # ================================
            #  - Fin de Dia -
            # ================================

            if params.fd < timeNow:
                
               
                calculations(app, vars, params)
                readIBData(app, vars)
                registration(app, vars, params)
                vars.status = "FD"
                break

            time.sleep(0.5)

        # ================================
        #  - Registro de Datos de final del dia -
        # ================================
        printStamp(" - Esperando FD - ")
        while True:

            timeNow = datetime.now(params.zone).time()
            if (timeNow.minute % 10 == 0 or timeNow.minute % 10 == 5):
                if vars.flag_minuto_label:
                    generar_label(params, vars,app)
                    vars.flag_minuto_label=False
                    time.sleep(0.5)
            else:
                vars.flag_minuto_label=True
           
            if params.fin_rutina < timeNow:
                printStamp(" - Registrando Nuevo Strike - ")
                registro_strike(app, vars, params)
                registro_strike_2(app, vars, params)
                clean_broadcasting(vars)
                vars.status = "OFF"
                saveJson(vars, app, params, True)
                break
            else:
                if int(timeNow.second) in params.frecuencia_muestra:
                    saveTransaction(app, params, vars)
                    calculations(app, vars, params)
                    saveJson(vars, app, params, False)
                    registration(app, vars, params)

            time.sleep(1)

        app.stop()
        api_thread.join()
        printStamp(" - Desconexión completada - ")
        return

    # ----- ERROR POR INTERRUPCION MANUAL -----
    except KeyboardInterrupt:
        try:
            # Corte de conexión con IB
            try:
                vars.status = "ERROR"
                saveJson(vars, app, params, False)
            except:
                pass
            app.stop()
            api_thread.join()
            printStamp(" - Desconexión completada - ")
        except:
            pass
        return

    # ----- ERROR DE CODIGO -----
    except Exception as e:
        printStamp(f"Ha ocurrido un error: {e}")
        printStamp(f"Tipo de error: {type(e).__name__}")

        # Si la excepción tiene atributos adicionales, como args
        if hasattr(e, "args"):
            printStamp(f"Argumentos del error: {e.args}")
        # Corte de conexión con IB
        try:
            try:
                vars.status = "ERROR"
                saveJson(vars, app, params, False)
                error=f"{e}"
                # sendError(params, error)
            except:
                pass
            app.stop()
            api_thread.join()
            printStamp(" - Desconexión completada - ")
        except:
            pass
        return


# ====================
#  - INICIO -
# ====================

if __name__ == "__main__":
    # ###########################
    # #### INICIO DEL CODIGO ####
    # ###########################
    
    main()
   