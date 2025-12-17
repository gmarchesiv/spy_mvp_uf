# ====================
#  - Librerias -
# ====================
import asyncio
from datetime import datetime
import time


from config.IB.options import sellOptionContract
from database.repository.repository import writeDayTrade

from functions.broadcasting import comparar_precios, send_sell, verificar_regla
from functions.labels import generar_label
from functions.logs import printStamp, read_rentabilidad, read_sell, readIBData_action
from functions.notifications import sendError
from functions.saveVars import saveVars

# ====================
#  - Funciones -
# ====================


# INICIO DE LAS REGLAS DE VENTA
def sellOptions(app,varsBc,varsLb,vars,params,debug_mode):

    #---------------------------------------------------
    '''
    En la venta de opciones va verificando los precios 
    de las demas maquinas para alinearlas a que salgan
    por las mismas reglas.Depende del tipo de opcion
    pueden ser de tipo CALL o PUT.

    '''
    #---------------------------------------------------

    if vars.minutos_trade <=params.tiempo_contulta and debug_mode==False: 

        asyncio.run(comparar_precios(vars, params))
 
    if vars.call:
        # sell_obligatoria(app,varsBc,varsLb,vars,params,"C",debug_mode)
        sellCall(app,varsBc,varsLb,vars,params,debug_mode)
        return
    elif vars.put:
        # sell_obligatoria(app,varsBc,varsLb,vars,params,"P",debug_mode)
        sellPut(app,varsBc,varsLb,vars,params,debug_mode)
        return
    else:
        return

def sell_obligatoria(app,varsBc,varsLb,vars,params,tipo):
    #---------------------------------------------------
    '''
    Fuerza la Venta de la opcion.
    '''
    #---------------------------------------------------
    params.max_askbid_venta_abs=params.max_askbid_venta_forzada
    if tipo == "C":
        val = 1
        if vars.askbid_call > params.max_askbid_venta_abs or vars.cbid <= 0:
            return False
    elif tipo == "P":
        val = 2
        if vars.askbid_put > params.max_askbid_venta_abs or vars.pbid <= 0:
            return False
    else:
        print("-ERROR SELL OBLIGATORIO-")
        return
    vars.venta_intentos=params.intentos
    sell_forzada(
            app,varsBc,varsLb,vars,params,
            tipo,
            "FORZADO",
            app.options[val]["contract"],
            app.options[val]["symbol"],
        )
    return
 

def sellCall(app,varsBc,varsLb,vars,params,debug_mode):

    #---------------------------------------------------
    '''
    Ventas de tipo CALL.
    Realiza calculos de rentabilidad, verifica reglas 
    de proteccion y verifica reglas de salida .
    '''
    #---------------------------------------------------

    if debug_mode:
        timeNow=vars.df["HORA"][vars.i]
    else:
        timeNow = datetime.now(params.zone).time()

    # CALCULAR RENTABILIDAD
    if vars.askbid_call > params.max_askbid_venta_abs:
        vars.rentabilidad = vars.cbid / vars.priceBuy - 1
        if debug_mode==False:
            read_rentabilidad(vars)
        else:
            vars.df.loc[vars.i, "RENT"]=vars.rentabilidad
        return
    if vars.cbid <= 0 or vars.askbid_call<0: 
        return
    
 

    vars.rentabilidad = vars.cbid / vars.priceBuy - 1

    if debug_mode==False:
        read_rentabilidad(vars)
    else:
        vars.df.loc[vars.i, "RENT"]=vars.rentabilidad

    # CALCULAR RENTABILIDAD vars.pico
    if vars.pico < vars.rentabilidad:
        vars.pico = vars.rentabilidad

    vars.caida = vars.rentabilidad - vars.pico

    if vars.askbid_call > params.max_askbid_venta_abs or vars.cbid <= 0 or vars.askbid_call<0 :
        proteccion_askbid_flag=False
        for hora in params.proteccion_ask_bid:
            if (timeNow >= hora[0] and timeNow<= hora[1]):
                proteccion_askbid_flag=True
        if proteccion_askbid_flag:
            return
   
    
    if timeNow >= params.fd:
        
      
        name = "FD"
        sell(
            app,varsBc,varsLb,vars,params,
            "C",
            name ,debug_mode
        )
        return
 
 
    # REGLA DE PROTECCION
    if (
        vars.rentabilidad < (vars.pico - params.perdida_maxima_c_r2)
        and vars.manifesto == False and   (vars.tipo == "R2" or vars.tipo == "R2-2")
    ):
        sell(
            app,varsBc,varsLb,vars,params,
            "C",  "PROTECCION" ,debug_mode
        )

        return
    
    # REGLA DE PROTECCION
    if ( vars.rentabilidad < (vars.pico - params.perdida_maxima_c)
        and vars.manifesto == False and vars.pico>0 and (vars.tipo != "R2" and  vars.tipo != "R2-2" )
    ):
        sell(
            app,varsBc,varsLb,vars,params,
            "C",  "PROTECCION_D" ,debug_mode
        )

        return
        
    # REGLA DE PROTECCION
    # if (
    #     vars.pico > params.umbral_no_perdida_c
    #     and vars.rentabilidad < params.perdida_maxima_c_abs
    #     and vars.manifesto == False and vars.tipo != "R2" 
    # ):
    #     sell(
    #         app,varsBc,varsLb,vars,params,
    #         "C",  "PROTECCION" ,debug_mode
    #     )

    #     return
    
        

    #########################################################
    ################      CALL    R2       ##################
    #########################################################
    if vars.tipo == "R2": 
        diamante=params.diamante_cr2
        resta=params.resta_cr2
        sl=params.sl_cr2
        manifestacion=params.umbral_manifestacion_cR2
        nmt=params.min_desicion_cR2

    #########################################################
    ################      CALL    R2-2     ##################
    #########################################################
    elif vars.tipo == "R2-2": 
        diamante=params.diamante_cr2_2
        resta=params.resta_cr2_2
        sl=params.sl_cr2_2
        manifestacion=params.umbral_manifestacion_cR2_2
        nmt=params.min_desicion_cR2

    #########################################################
    ################      CALL  R1         ##################
    #########################################################
    elif vars.tipo == "R1"  : 
        diamante=params.diamante_cr1
        resta=params.resta_cr1
        sl=params.sl_cr1
        manifestacion=params.umbral_manifestacion_cR1
        nmt=params.inf

    #########################################################
    ################      CALL  R1-2       ##################
    #########################################################
    elif vars.tipo == "R1-2"  : 
        diamante=params.diamante_cr1_2
        resta=params.resta_cr1_2
        sl=params.sl_cr1_2
        manifestacion=params.umbral_manifestacion_cR1_2
        nmt=params.inf

    #########################################################
    ################      CALL  R1  E      ##################
    #########################################################
    elif vars.tipo == "R1-E"  : 
        diamante=params.diamante_cr1_e
        resta=params.resta_cr1_e
        sl=params.sl_cr1_e
        manifestacion=params.umbral_manifestacion_cR1_e
        nmt=params.inf

    #########################################################
    ################      CALL  R1  E2      ##################
    #########################################################
    elif vars.tipo == "R1-E2"  : 
        diamante=params.diamante_cr1_e2
        resta=params.resta_cr1_e2
        sl=params.sl_cr1_e2
        manifestacion=params.umbral_manifestacion_cR1_e2
        nmt=params.inf

    #########################################################
    ################      CALL  R1  INV    ##################
    #########################################################
    elif vars.tipo == "R1-I": 
        diamante=params.diamante_cr1_i
        resta=params.resta_cr1_i
        sl=params.sl_cr1_i
        manifestacion=params.umbral_manifestacion_cr1_i
        nmt=params.inf

    #########################################################
    ################      CALL  R1  C      ##################
    #########################################################
    elif vars.tipo ==  "R1-C": 
        diamante=params.diamante_cr1_c
        resta=params.resta_cr1_c
        sl=params.sl_cr1_c
        manifestacion=params.umbral_manifestacion_cR1_c
        nmt=params.inf

    #########################################################
    ################      CALL  R1  FAST   ##################
    #########################################################
    elif vars.tipo == "R1-FAST":  
        diamante=params.diamante_cr1_fast
        resta=params.resta_cr1_fast
        sl=params.sl_cr1_fast
        manifestacion=params.umbral_manifestacion_cR1_fast
        nmt=params.inf


    #########################################################
    ################      CALL  R3         ##################
    #########################################################
    elif vars.tipo == "R3"  : 
        diamante=params.diamante_cr3
        resta=params.resta_cr3
        sl=params.sl_cr3
        manifestacion=params.umbral_manifestacion_cR3
        nmt=params.inf
    
     
    #########################################################
    ################      CALL  R1  F      ##################
    #########################################################
    elif vars.tipo == "F"  : 
        diamante=params.diamante_cr1_f1
        resta=params.resta_cr1_f1
        sl=params.sl_cr1_f1
        manifestacion=params.umbral_manifestacion_cR1_f1
        nmt=params.inf
    #########################################################
    ################      CALL  R1  F2      ##################
    #########################################################
    elif vars.tipo == "F2"  : 
        diamante=params.diamante_cr1_f2
        resta=params.resta_cr1_f2
        sl=params.sl_cr1_f2
        manifestacion=params.umbral_manifestacion_cR1_f2
        nmt=params.inf
  

    #########################################################
    ####################      VENTA       ###################
    #########################################################

    # MANIFIESTA
    if vars.manifesto:
        # DIAMANTE
        for y in range(vars.ugs_n, len(diamante)):
            if round(vars.pico, 5) > diamante[y]:
                vars.ugs_n = y
                if vars.ugs_n != vars.ugs_n_ant:
                    vars.minutos = 0
                    vars.ugs_n_ant = vars.ugs_n
            else:
                break
        # MAXIMA RENTABILIDAD
        if vars.rentabilidad <= (vars.pico - resta[vars.ugs_n]):

            name = f"T{vars.ugs_n}"
            sell(
                app,varsBc,varsLb,vars,params,
                "C",  name ,debug_mode
            )

            return

        else:
            pass

    # AUN NO MANIFIESTA
    else:

        # vars.manifesto
        if vars.rentabilidad >= manifestacion:
            vars.manifesto = True
            vars.minutos = 0
            # DIAMANTE
            for y in range(vars.ugs_n, len( diamante)):
                if round(vars.pico, 5) >  diamante[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break
            # MAXIMA RENTABILIDAD
            if vars.rentabilidad <= (vars.pico -  resta[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,varsBc,varsLb,vars,params,
                    "C",  name ,debug_mode
                )

                return

        elif vars.minutos >= (nmt+1): 
            sell(
                app,varsBc,varsLb,vars,params,
                "C", "NMT" ,debug_mode
            )

            return
        # STOP LOSS
        elif vars.rentabilidad <= sl:
            sell(
                app,varsBc,varsLb,vars,params,
                "C", "SL" ,debug_mode
            )

            return

    vars.venta_intentos=0
    vars.regla_broadcasting=""

def sellPut(app,varsBc,varsLb,vars,params,debug_mode):

    #---------------------------------------------------
    '''
    Ventas de tipo PUT.
    Realiza calculos de rentabilidad, verifica reglas 
    de proteccion y verifica reglas de salida .
    '''
    #---------------------------------------------------

    if debug_mode:
        timeNow=vars.df["HORA"][vars.i]
    else:
        timeNow = datetime.now(params.zone).time()

    # CALCULAR RENTABILIDAD
    if vars.askbid_put > params.max_askbid_venta_abs:
        vars.rentabilidad = vars.pbid / vars.priceBuy - 1
        if debug_mode==False:
            read_rentabilidad(vars)
        else:
            vars.df.loc[vars.i, "RENT"]=vars.rentabilidad
        return
    if vars.pbid <= 0 or vars.askbid_put<0: 
        return
     
    vars.rentabilidad = vars.pbid / vars.priceBuy - 1
    if debug_mode==False:
        read_rentabilidad(vars)
    else:
        vars.df.loc[vars.i, "RENT"]=vars.rentabilidad
    # CALCULAR RENTABILIDAD vars.pico
    if vars.pico < vars.rentabilidad:
        vars.pico = vars.rentabilidad

    vars.caida = vars.rentabilidad - vars.pico

    if vars.askbid_put > params.max_askbid_venta_abs or vars.pbid <= 0 or vars.askbid_put<0 :
        proteccion_askbid_flag=False
        for hora in params.proteccion_ask_bid:
            if (timeNow >= hora[0] and timeNow<= hora[1]):
                proteccion_askbid_flag=True
        if proteccion_askbid_flag:
            return
        
    # # FIN DE DIA DE TRADE
 
    if timeNow >= params.fd:
         
        sell(
            app,varsBc,varsLb,vars,params,
            "P",
            "FD" ,debug_mode
        )

        return

    # REGLA PROTECCION
    # if (
    #     vars.pico > params.umbral_no_perdida_p_r2
    #     and vars.rentabilidad < (vars.pico - params.perdida_maxima_p_r2)
    #     and vars.manifesto == False and  vars.tipo == "R2"
    # ):
    #     sell(
    #         app,varsBc,varsLb,vars,params,
    #         "P",  "PROTECCION" ,debug_mode
    #     )

    #     return

    # REGLA PROTECCION
    if (
         vars.rentabilidad < (vars.pico - params.perdida_maxima_p)
        and vars.manifesto == False and vars.pico>0  
    ):
        sell(
            app,varsBc,varsLb,vars,params,
            "P",  "PROTECCION_D" ,debug_mode
        )

        return


    # REGLA PROTECCION
    # if (
    #     vars.pico > params.umbral_no_perdida_p
    #     and vars.rentabilidad < params.perdida_maxima_p_abs
    #     and vars.manifesto == False and vars.tipo != "R2" 
    # ):
    #     sell(
    #         app,varsBc,varsLb,vars,params,
    #         "P",  "PROTECCION" ,debug_mode
    #     )

    #     return

    #########################################################
    ####################      PUT  R2         ###############
    #########################################################
    if vars.tipo == "R2": 
        diamante=params.diamante_pr2
        resta=params.resta_pr2
        sl=params.sl_pr2
        manifestacion=params.umbral_manifestacion_pR2
        nmt=params.inf

    #########################################################
    ####################      PUT  R2 E       ###############
    #########################################################
    elif vars.tipo == "R2-E": 
        diamante=params.diamante_pR2_e
        resta=params.resta_pR2_e
        sl=params.sl_pr2_e
        manifestacion=params.umbral_manifestacion_pR2_e
        nmt=params.inf

    #########################################################
    ####################      PUT  R2  FAST   ###############
    #########################################################
    elif vars.tipo == "R2-FAST": 
        diamante=params.diamante_pr2_fast
        resta=params.resta_pr2_fast
        sl=params.sl_pr2_fast
        manifestacion=params.umbral_manifestacion_pR2_fast
        nmt=params.inf

    #########################################################
    ####################      PUT  R3     ###################
    #########################################################
    elif vars.tipo == "R3": 
        diamante=params.diamante_pr3
        resta=params.resta_pr3
        sl=params.sl_pr3
        manifestacion=params.umbral_manifestacion_pR3
        nmt=params.inf

    #########################################################
    ####################      PUT  R1  FAST   ###############
    #########################################################
    elif vars.tipo == "R1-FAST": 
        diamante=params.diamante_pr1_fast
        resta=params.resta_pr1_fast
        sl=params.sl_pr1_fast
        manifestacion=params.umbral_manifestacion_pR1_fast
        nmt=params.inf

    #########################################################
    ####################      PUT  R1  LABEL  ###############
    #########################################################
    elif vars.tipo == "LABEL-I": 
        diamante=params.diamante_pr1_label
        resta=params.resta_pr1_label
        sl=params.sl_pr1_label
        manifestacion=params.umbral_manifestacion_pR1_label
        nmt=params.inf

    #########################################################
    ####################      PUT  R1  LABEL 2###############
    #########################################################
    elif vars.tipo == "LABEL-II": 
        diamante=params.diamante_pr1_label_2
        resta=params.resta_pr1_label_2
        sl=params.sl_pr1_label_2
        manifestacion=params.umbral_manifestacion_pR1_label_2
        nmt=params.inf
    #########################################################
    ####################      PUT  R1     ###################
    #########################################################
    elif vars.tipo == "R1": 
        diamante=params.diamante_pr1
        resta=params.resta_pr1
        sl=params.sl_pr1
        manifestacion=params.umbral_manifestacion_pR1
        nmt=params.inf
 
    #########################################################
    ####################      PUT  R1  I2 ###################
    #########################################################
    elif vars.tipo == "R1-I2": 
        diamante=params.diamante_pr1_i_2
        resta=params.resta_pr1_i_2
        sl=params.sl_pr1_i_2
        manifestacion=params.umbral_manifestacion_pR1_i_2
        nmt=params.inf
    #########################################################
    ####################      PUT  R1  I3 ###################
    #########################################################
    elif vars.tipo == "R1-I3": 
        diamante=params.diamante_pr1_i_3
        resta=params.resta_pr1_i_3
        sl=params.sl_pr1_i_3
        manifestacion=params.umbral_manifestacion_pR1_i_3
        nmt=params.inf
    #########################################################
    ####################      PUT  R1  I4 ###################
    #########################################################
    elif vars.tipo == "R1-I4": 
        diamante=params.diamante_pr1_i_4
        resta=params.resta_pr1_i_4
        sl=params.sl_pr1_i_4
        manifestacion=params.umbral_manifestacion_pR1_i_4
        nmt=params.inf
    #########################################################
    ####################      PUT  R1  I5 ###################
    #########################################################
    elif vars.tipo == "R1-I5": 
        diamante=params.diamante_pr1_i_5
        resta=params.resta_pr1_i_5
        sl=params.sl_pr1_i_5
        manifestacion=params.umbral_manifestacion_pR1_i_5
        nmt=params.inf
   
    #########################################################
    ####################      PUT  R1  F      ###############
    #########################################################
    elif vars.tipo =="F":    
        diamante=params.diamante_pr1_f
        resta=params.resta_pr1_f
        sl=params.sl_pr1_f
        manifestacion=params.umbral_manifestacion_pR1_f
        nmt=params.inf
 

    #########################################################
    ####################      VENTA       ###################
    #########################################################
    # MANIFIESTA
    if vars.manifesto:

        # DIAMANTE
        for y in range(vars.ugs_n, len(diamante)):
            if round(vars.pico, 5) > diamante[y]:
                vars.ugs_n = y
                if vars.ugs_n != vars.ugs_n_ant:
                    vars.minutos = 0
                    vars.ugs_n_ant = vars.ugs_n
            else:
                break

        # RETROCESO
        if vars.rentabilidad <= (vars.pico - resta[vars.ugs_n]):

            name = f"T{vars.ugs_n}"
            sell(
                app,varsBc,varsLb,vars,params,
                "P", name ,debug_mode)

            return

        else:
            pass

    else:
        # vars.manifesto
        if vars.rentabilidad >= manifestacion:
            vars.manifesto = True
            vars.minutos = 0

            # DIAMANTE
            for y in range(vars.ugs_n, len(diamante)):
                if round(vars.pico, 5) > diamante[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - resta[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,varsBc,varsLb,vars,params,
                    "P", name,debug_mode)

                return

            else:
                pass
        

        elif (vars.minutos) >=( nmt+1): 
            sell(
                app,varsBc,varsLb,vars,params,
                "P", "NMT" ,debug_mode
            )

            return

        # SL
        elif vars.rentabilidad <=sl:

            sell(
                app,varsBc,varsLb,vars,params,
                "P", "SL" ,debug_mode
            )

            return


   
    vars.venta_intentos=0
    vars.regla_broadcasting=""
     
def sell(app,varsBc,varsLb,vars,params, tipo, regla,debug_mode ):
   
    #---------------------------------------------------
    '''
    Venta de la opcion, La rutina consta de lo siguiente:
        1) Verifica si la rentabilidad es negativa para
            intentar hacer un rebote.
        2) Realiza Broadcasting de la Regla de venta.
        3) Verifica que la venta se pueda dar sin 
           problemas de ASKBID.
        4) Ejecuta la orden de Venta.
        5)Espera que la transaccion se complete,mientras
          sigue calculando variables.
        6) Al finalizar modifica variables de estado de 
           venta.
    '''
    #---------------------------------------------------
 
    if debug_mode:
        # SET DE VARIABLES
        vars.regla = regla
        vars.regla_ant = vars.regla
        if tipo == "C":
            vars.call = False
        elif tipo == "P":
            vars.put = False

        vars.status = "SLEEP"
        vars.df.loc[vars.i, "REGLA"]=regla
        
 
        # read_sell(vars, tipo)
        return True


    else:
        from rules.routine import calculations

        if tipo =="C":
            contract=app.options[1]["contract"]
            symbol=app.options[1]["symbol"]
        else:
            contract=app.options[2]["contract"]
            symbol=app.options[2]["symbol"]

        

        # REBOTE

        if vars.rentabilidad<0:
            
            if vars.venta_intentos>=params.intentos:
                pass   
            else:
                vars.venta_intentos+=1
                return
    
        varsBc.sell_regla = regla

        # BROADCASTING
        if varsBc.sell ==False:
            asyncio.run(send_sell(  varsBc, params, tipo,regla))
    
        # LECTURA PREVIA
        readIBData_action(app, vars, tipo, regla)

        # ENVIO DE ORDEN DE VENTA
        flag = sellOptionContract(params, app, vars, tipo, contract, symbol)
        if flag == False:
            printStamp("-NO SE PUDO CONCRETAR LA VENTA-")
            return False

        # ESPERA DE LA ORDEN DE VENTA
        app.statusIB = False
        app.Error = False

        printStamp("-wait Status-")

        while app.statusIB == False:

            timeNow = datetime.now(params.zone).time()
            if (timeNow.minute % 10 == 0 or timeNow.minute % 10 == 5):
                if varsLb.flag_minuto_label:
                    generar_label(params, varsLb,app)
                    varsLb.flag_minuto_label=False
                    time.sleep(0.5)
            else:
                varsLb.flag_minuto_label=True
            if int(timeNow.second) in params.frecuencia_accion:
                calculations(app, vars,varsBc, params)
                # ESPERANDO Y REGISTRANDO
                vars.status = "SELLING"
                saveVars(vars, app, params, False)
                writeDayTrade(app, vars,varsLb, params)

            if app.Error:
                break
            time.sleep(1)
        if app.Error:
            printStamp(f"-VENTA NO PROCESADA-")
            sendError(params, "VENTA NO PROCESADA")
            return False

        # SET DE VARIABLES
        vars.regla = regla
        vars.regla_ant = vars.regla
        if tipo == "C":
            vars.call = False
        elif tipo == "P":
            vars.put = False

        vars.status = "SLEEP"
        read_sell(vars, tipo)
        return True

def sell_forzada(app,varsBc,varsLb,vars,params, tipo, regla, contract, symbol):
    from rules.routine import calculations
 
    # LECTURA PREVIA
    readIBData_action(app, vars, tipo, regla)

    # ENVIO DE ORDEN DE VENTA
    flag = sellOptionContract(params, app, vars, tipo, contract, symbol)
    if flag == False:
        printStamp("-NO SE PUDO CONCRETAR LA VENTA-")
        return False

    # ESPERA DE LA ORDEN DE VENTA
    app.statusIB = False
    app.Error = False

    printStamp("-wait Status-")

    while app.statusIB == False:

        timeNow = datetime.now(params.zone).time()
        if (timeNow.minute % 10 == 0 or timeNow.minute % 10 == 5):
            if varsLb.flag_minuto_label:
                generar_label(params,varsLb, app)
                varsLb.flag_minuto_label=False
                time.sleep(0.5)
        else:
            varsLb.flag_minuto_label=True
        if int(timeNow.second) in params.frecuencia_accion:
            calculations(app, vars,varsBc, params) 
            # ESPERANDO Y REGISTRANDO
            vars.status = "SELLING"
            saveVars(vars, app, params, False)
            writeDayTrade(app, vars,varsLb, params)

        if app.Error:
            break
        time.sleep(1)
    if app.Error:
        printStamp(f"-VENTA NO PROCESADA-")
        sendError(params, "VENTA NO PROCESADA")
        return False

    # SET DE VARIABLES
    vars.regla = regla
    vars.regla_ant = vars.regla
    if tipo == "C":
        vars.call = False
    elif tipo == "P":
        vars.put = False

    vars.status = "SLEEP"
    read_sell(vars, tipo)
    return True
