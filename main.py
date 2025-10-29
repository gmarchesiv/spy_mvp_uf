###################################################
################### LIBRERIAS  ####################
###################################################
 
import time
from datetime import datetime
import traceback
# config/
from config.IB.connection import test_ibkr_connection, ibkr_connection, load_app_vars
from config.IB.wallet import wallet_config 
from config.params import parameters
from config.vars.rutina import varsRutina
from config.vars.broadcasting import varsBroadcasting
from config.vars.app import varsApps
from config.vars.label import varsLabel

# DataBase
from database.repository.repository import writeRegister

# funtions/
from functions.broadcasting import *
from functions.clean import clean_broadcasting, clean_vars
from functions.events import countdown, isTradingDay
from functions.labels import generar_label
from functions.logs import *
from functions.notifications import sendError, sendStart
from functions.saveVars import saveVars

# rules/
from rules.buy import buyOptions
from rules.routine import (
    data_option_open,
    calculations,
    data_option_open,
    data_susciption,
    registration,
    registro_strike,
    saveTransaction 
)

# database/
from database.repository.repository import *
from rules.sell import sellOptions


# ====================
#  - Funciones -
# ====================
def main():

    try:

        # ================================
        #     - Variables y Parametros -
        # ================================

        #---------------------------------------------------
        '''
        Aqui inicializamos las variables y 
        parametros antes de comenzar la rutina.
        '''
        #---------------------------------------------------

        # VARIABLES
        vars = varsRutina(debug_mode=False)
 
        varsBc = varsBroadcasting(debug_mode=False)
 
        varsLb=varsLabel(debug_mode=False)
   
        varsApp=varsApps(debug_mode=False)
   
        # PARAMETROS
        params = parameters(debug_mode=False)

        # ====================
        #  - TEST CONNECTION -
        # ====================

        #---------------------------------------------------
        '''
        Generamos antes de iniciar un test de conexión 
        en caso estemos fuera de hora, si estamos por 
        iniciar el trading day este se omitira.
        '''
        #---------------------------------------------------

        timeNow = datetime.now(params.zone).time()

        if timeNow < params.rutina[0] or timeNow >= params.rutina[1]:
            test_ibkr_connection(params)
            return

        # ====================
        #  - Feriados -
        # ====================

        #---------------------------------------------------
        '''
        En caso este sea un dia Feriado , solo genera
        un test de conexión
        '''
        #---------------------------------------------------

        if isTradingDay(params): # TODO MEJORAR LOS FERIADOS NO AGREGADOS
            test_ibkr_connection(params)
            return

        # ---------------------------------

        # ====================
        #  - conexcion a IB -
        # ====================

        #---------------------------------------------------
        '''
        Generamos conexión con el API de Interactive Broker ,
        Esperamos a que comience el trading Day y registramos 
        inicio en nuestra DB.
        '''
        #---------------------------------------------------

        app, api_thread, status = ibkr_connection(params)
  
        if status: # FIN en caso no conecte.
            return

        # Cuenta regresiva para iniciar.
        countdown(params.zone)

        # Registro de sesion.
        writeRegister(params.name, params.zone)
   
        # ==========================
        #  - SUSCRIPCIONES A DATOS -
        # ==========================

        #---------------------------------------------------
        '''
        Suscripcion de datos de ETFs, y 
        contratos de opciones.
        '''
        #---------------------------------------------------

        data_susciption(app, params, vars)
       
        # ====================
        #  -   AL INICIAR   -
        # ====================

        #---------------------------------------------------
        '''
        -Iniciamos con las siguientes tareas en caso sea un
         primer inicio :

            1)Limpieza de variables. 
            2)Cargar datos de Open de las opciones.
            3)Generar el primer Label.
            4)Bloqueo por inicio tardio.

        - En caso sea un inicio por desconexión :
            1)Cargar Variables de Aplicacion.
 
        Inmediatamente sea el primer o 2do caso va a 
        hacer un analisis y configuracion de billetera 
        para iniciar el trading day, finalmente envia la 
        notificacion de inicio de sesion del cliente por la
        aplicacion de Telegram.   
        '''
        #---------------------------------------------------

        now = datetime.now(params.zone).strftime("%Y-%m-%d")

        if vars.fecha != now:
            clean_vars(vars,varsApp)
            data_option_open(app,vars,params)
            generar_label(params, varsLb,app)

            timeNow = datetime.now(params.zone).time()
         
            # Bloqueo por sesion tardia
            if (timeNow.hour >= 9 and timeNow.minute >= 33):
               varsApp.flag_bloqueo_tiempo=True
        else:
            load_app_vars(app, varsApp)
  
        wallet_config(app, params, vars)

        sendStart(app, params)

        printStamp(" - INICIO DE RUTINA - ")
         
        # ====================
        #      - Rutina -
        # ====================

        #---------------------------------------------------
        '''
        La rutina consta de un bucle que mantiene a lo largo
        del dia y se rompe al finalizar el trading day. 
        '''
        #---------------------------------------------------

        while True:

            timeNow = datetime.now(params.zone).time()
             
            # MIENTRAS NO SEA FIN DE DIA

            # ==================================
            #  -        GENERAR LABEL          -
            # ==================================

            #---------------------------------------------------
            '''
            Generamos el Label cada 5 minutos para tener una 
            tendencia a la hora de realizar una transaccion.
            '''
            #---------------------------------------------------
            # GENERAR LABEL
            if (timeNow.minute % 10 == 0 or timeNow.minute % 10 == 5):
                if varsLb.flag_minuto_label:
                    generar_label(params, varsLb,app)
                    varsLb.flag_minuto_label=False

            else:
                varsLb.flag_minuto_label=True

            # ==================================
            #  -        DAY TRADING            -
            # ==================================
            
            if params.fin_rutina >= timeNow:
                #---------------------------------------------------
                '''
                Inicio del Horario de Trading.
                '''
                #---------------------------------------------------
            
                    
                # ==================================
                #  -        BROADCASTING           -
                # ==================================

                #---------------------------------------------------
                '''
                Las Funciones Broadcasting permiten compartir 
                informacion con otras maquinas conectadas a el
                por REST. Esta Funcion cuenta con compra y venta
                inducida por otras maquinas y venta obligatoria
                inducida por una peticion local.
                '''
                #---------------------------------------------------
                # RUTINA DE COMPRA Y VENTA BROADCASTING
                if vars.bloqueo == False and varsApp.flag_bloqueo_tiempo==False:
                    
                    if vars.call or vars.put:
                        broadcasting_sell(varsBc,varsLb,vars,params,app)
                        broadcasting_sell_auto(varsBc,varsLb,vars,params,app)
                    if vars.compra:
                        broadcasting_buy(varsBc,varsLb,vars,params,app)
                    pass
                
                

                # ==================================
                #  -        RUTINA NORMAL          -
                # ==================================
                #---------------------------------------------------
                '''
                La rutina consiste en realizar compras y ventas 
                dandole seguimiento al precio de las opciones
                cada una determinada frecuencia de muestra.
                La rutina va a realizar lo siguiente:
                    1) Ver si ya ocurrio una transaccion
                    2) Calcular variables
                    3) Generar un log
                    4) Verificar COMPRAS y VENTAS
                    5) Registrar el dia
                '''
                #---------------------------------------------------
                if int(timeNow.second) in params.frecuencia_accion:
                    
                    saveTransaction(app, params, vars)  # VERIFICADOR DE TRANSACCIONES
                    calculations(app, vars,varsBc, params)  # CALCULOS DE RUTINA
                    readIBData(app, vars,varsLb)  # LOGS DE LOS CALCULOS

                    # Se Bloquea en caso la configuracion de la wallet te indique
                    if vars.bloqueo == False and varsApp.flag_bloqueo_tiempo==False:
                        # ================================
                        #            -VENTA-
                        # ================================
                        if vars.call or vars.put:
                            sellOptions(app,varsBc,varsLb,vars,params,debug_mode=False )
                        # ================================
                        #            -COMPRA-
                        # ================================
                        if vars.compra and params.fd >= timeNow:
                            buyOptions(app,varsBc,varsLb,vars,params,debug_mode=False )
                        pass
                    
                    # ================================
                    #          - Registro -
                    # ================================
 
                    registration(app, vars,varsApp, varsLb,params)
                
                    time.sleep(0.5)
    
                # ==================================
                #  -          ESPERA               -
                # ==================================
                #---------------------------------------------------
                '''
                Sumando el tiempo de Registro y podemos saltar el 
                segundo.
                '''
                #---------------------------------------------------
                time.sleep(0.5)

            # ==================================
            #  -       FIN DEL DAY TRADING     -
            # ==================================
            else:

                # ================================
                #         - Nuevo STRIKE -
                # ================================

                #---------------------------------------------------
                '''
                Seleccion del Nuevo strike para el siguiente dia y 
                fin del dia.
                '''
                #---------------------------------------------------

                printStamp(" - Registrando Nuevo Strike - ")
                registro_strike(app, vars, params)
                
                vars.status = "OFF"
          
                saveVars(vars, app, params, True) 
         
                break
           

        app.stop()
        api_thread.join()
        printStamp(" - Desconexión completada - ")
        return

    # ----- ERROR POR INTERRUPCION MANUAL -----
    except KeyboardInterrupt:
        #---------------------------------------------------
        '''
        Interrupcion del codigo.
        '''
        #---------------------------------------------------
        try:
            # Corte de conexión con IB
            try:
                vars.status = "ERROR"
                
                saveVars(vars, app, params, False)
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

        #---------------------------------------------------
        '''
        Imprimimos el Error.
        '''
        #---------------------------------------------------


        printStamp(f"Ha ocurrido un error: {e}")
        printStamp(f"Tipo de error: {type(e).__name__}")
        printStamp("Detalles del error:")
        texto="".join(traceback.format_exception(type(e), e, e.__traceback__))
        printStamp(texto)

        # Si la excepción tiene atributos adicionales, como args
        if hasattr(e, "args"):
            printStamp(f"Argumentos del error: {e.args}")
        # Corte de conexión con IB
        try:
            try:
                vars.status = "ERROR"
              
                saveVars(vars, app, params, False)
                error=f"{e}"
                sendError(params, error)
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
    ###########################
    #### INICIO DEL CODIGO ####
    ###########################

    #---------------------------------------------------
    '''
    INICIO
    '''
    #---------------------------------------------------
    main()
