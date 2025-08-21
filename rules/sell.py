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
from functions.saveJson import saveJson

# ====================
#  - Funciones -
# ====================


# INICIO DE LAS REGLAS DE VENTA
def sellOptions(app, vars, params):
    if vars.minutos_trade <=params.tiempo_contulta :

        asyncio.run(comparar_precios(vars, params))
 
    if vars.call:
        # sell_obligatoria(app, vars, params,"C")
        sellCall(app, params, vars)
        return
    elif vars.put:
        # sell_obligatoria(app, vars, params,"P")
        sellPut(app, params, vars)
        return
    else:
        return

def sell_obligatoria(app, vars, params,tipo):
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
            app,
            vars,
            params,
            tipo,
            "FORZADO",
            app.options[val]["contract"],
            app.options[val]["symbol"],
        )
    return
 

def sellCall(app, params, vars):

    timeNow = datetime.now(params.zone).time()

    # CALCULAR RENTABILIDAD
    if vars.askbid_call > params.max_askbid_venta_abs:
        vars.rentabilidad = vars.cbid / vars.priceBuy - 1
        read_rentabilidad(vars)
        return
    if vars.cbid <= 0:
        return
    
 

    vars.rentabilidad = vars.cbid / vars.priceBuy - 1

    read_rentabilidad(vars)

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
            app,
            vars,
            params,
            "C",
            name,
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )
        return

    # REGLA DE PROTECCION
    if (
        vars.pico > params.umbral_no_perdida_c
        and vars.rentabilidad < (vars.pico - params.perdida_maxima_c)
        and vars.manifesto == False and vars.tipo == "R2" 
    ):
        sell(
            app,
            vars,
            params,
            "C",
            "PROTECCION",
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        return
    

    # REGLA DE PROTECCION
    if (
        vars.pico > params.umbral_no_perdida_c
        and vars.rentabilidad < params.perdida_maxima_c_abs
        and vars.manifesto == False and vars.tipo != "R2" 
    ):
        sell(
            app,
            vars,
            params,
            "C",
            "PROTECCION",
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        return

    #########################################################
    ################      CALL  R1    ##################
    #########################################################
    if vars.tipo == "R1"  :

        # MANIFIESTA
        if vars.manifesto:
            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_cr1)):
                if round(vars.pico, 3) > params.diamante_cr1[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break
            # MAXIMA RENTABILIDAD
            if vars.rentabilidad <= (vars.pico - params.resta_cr1[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    name,
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:

            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_cR1:
                vars.manifesto = True
                vars.minutos = 0

            # STOP LOSS
            elif vars.rentabilidad <= params.sl_cr1:
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "SL",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return
            
    #########################################################
    ################      CALL  R1  E      ##################
    #########################################################
    elif vars.tipo == "R1-E"  :

        # MANIFIESTA
        if vars.manifesto:
            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_cr1_e)):
                if round(vars.pico, 3) > params.diamante_cr1_e[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break
            # MAXIMA RENTABILIDAD
            if vars.rentabilidad <= (vars.pico - params.resta_cr1_e[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    name,
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:

            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_cR1_e:
                vars.manifesto = True
                vars.minutos = 0

            # STOP LOSS
            elif vars.rentabilidad <= params.sl_cr1_e:
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "SL",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

    #########################################################
    ################      CALL  R3         ##################
    #########################################################
    elif vars.tipo == "R3"  :

        # MANIFIESTA
        if vars.manifesto:
            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_cr3)):
                if round(vars.pico, 3) > params.diamante_cr3[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break
            # MAXIMA RENTABILIDAD
            if vars.rentabilidad <= (vars.pico - params.resta_cr3[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    name,
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:

            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_cR3:
                vars.manifesto = True
                vars.minutos = 0

            # STOP LOSS
            elif vars.rentabilidad <= params.sl_cr3:
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "SL",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

    #########################################################
    ################      CALL  R1  E2      ##################
    #########################################################
    elif vars.tipo == "R1-E2"  :

        # MANIFIESTA
        if vars.manifesto:
            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_cr1_e2)):
                if round(vars.pico, 3) > params.diamante_cr1_e2[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break
            # MAXIMA RENTABILIDAD
            if vars.rentabilidad <= (vars.pico - params.resta_cr1_e2[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    name,
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:

            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_cR1_e2:
                vars.manifesto = True
                vars.minutos = 0

            # STOP LOSS
            elif vars.rentabilidad <= params.sl_cr1_e2:
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "SL",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return
                 
    
    #########################################################
    ################      CALL  R1  FAST   ##################
    #########################################################
    elif vars.tipo == "R1-FAST":  

        # MANIFIESTA
        if vars.manifesto:
            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_cr1_fast)):
                if round(vars.pico, 3) > params.diamante_cr1_fast[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break
            # MAXIMA RENTABILIDAD
            if vars.rentabilidad <= (vars.pico - params.resta_cr1_fast[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    name,
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:

            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_cR1_fast:
                vars.manifesto = True
                vars.minutos = 0

            # STOP LOSS
            elif vars.rentabilidad <= params.sl_cr1_fast:
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "SL",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return
    #########################################################
    ################      CALL    R2    ##################
    #########################################################
    elif vars.tipo == "R2":

        # MANIFIESTA
        if vars.manifesto:
            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_cr2)):
                if round(vars.pico, 3) > params.diamante_cr2[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break
            # MAXIMA RENTABILIDAD
            if vars.rentabilidad <= (vars.pico - params.resta_cr2[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    name,
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:

            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_cR2:
                vars.manifesto = True
                vars.minutos = 0

            # STOP LOSS
            elif vars.rentabilidad <= params.sl_cr2:
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "SL",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return


    #########################################################
    ################      CALL  R1  INV    ##################
    #########################################################
    elif vars.tipo == "R1-I":

        # MANIFIESTA
        if vars.manifesto:
            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_cr1_i)):
                if round(vars.pico, 3) > params.diamante_cr1_i[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break
            # MAXIMA RENTABILIDAD
            if vars.rentabilidad <= (vars.pico - params.resta_cr1_i[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    name,
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:

            # vars.manifesto
            if vars.rentabilidad >= params.sl_cr1_i:
                vars.manifesto = True
                vars.minutos = 0

            # STOP LOSS
            elif vars.rentabilidad <= params.sl_cr1_fast:
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "SL",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

    #########################################################
    ################      CALL  R1  C      ##################
    #########################################################
    elif vars.tipo ==  "R1-C":

        # MANIFIESTA
        if vars.manifesto:
            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_cr1_c)):
                if round(vars.pico, 3) > params.diamante_cr1_c[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break
            # MAXIMA RENTABILIDAD
            if vars.rentabilidad <= (vars.pico - params.resta_cr1_c[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    name,
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:

            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_cR1_c:
                vars.manifesto = True
                vars.minutos = 0

            # STOP LOSS
            elif vars.rentabilidad <= params.sl_cr1_c:
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "SL",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return
            
    

    #########################################################
    ################      CALL  R1  F      ##################
    #########################################################
    elif vars.tipo == "F"  :

        # MANIFIESTA
        if vars.manifesto:
            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_cr1_f)):
                if round(vars.pico, 3) > params.diamante_cr1_f[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break
            # MAXIMA RENTABILIDAD
            if vars.rentabilidad <= (vars.pico - params.resta_cr1_f[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    name,
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:

            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_cR1_f:
                vars.manifesto = True
                vars.minutos = 0

            # STOP LOSS
            elif vars.rentabilidad <= params.sl_cr1_f:
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "SL",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return
    
    

    else:pass

    vars.venta_intentos=0
    vars.regla_broadcasting=""

def sellPut(app, params, vars):

    timeNow = datetime.now(params.zone).time()

    # CALCULAR RENTABILIDAD
    if vars.askbid_put > params.max_askbid_venta_abs:
        vars.rentabilidad = vars.pbid / vars.priceBuy - 1
        read_rentabilidad(vars)
        return
    if vars.pbid <= 0:
        return
    
 

    vars.rentabilidad = vars.pbid / vars.priceBuy - 1
    read_rentabilidad(vars)
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
            app,
            vars,
            params,
            "P",
            "FD",
            app.options[2]["contract"],
            app.options[2]["symbol"],
        )

        return

    # REGLA PROTECCION
    if (
        vars.pico > params.umbral_no_perdida_p
        and vars.rentabilidad < (vars.pico - params.perdida_maxima_p)
        and vars.manifesto == False and vars.tipo == "R2"
    ):
        sell(
            app,
            vars,
            params,
            "P",
            "PROTECCION",
            app.options[2]["contract"],
            app.options[2]["symbol"],
        )

        return

    # REGLA PROTECCION
    if (
        vars.pico > params.umbral_no_perdida_p
        and vars.rentabilidad < params.perdida_maxima_p_abs
        and vars.manifesto == False and vars.tipo != "R2"
    ):
        sell(
            app,
            vars,
            params,
            "P",
            "PROTECCION",
            app.options[2]["contract"],
            app.options[2]["symbol"],
        )

        return

    #########################################################
    ####################      PUT  R1     ###################
    #########################################################
    if vars.tipo == "R1":
        # MANIFIESTA
        if vars.manifesto:

            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_pr1)):
                if round(vars.pico, 3) > params.diamante_pr1[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr1[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR1:
                vars.manifesto = True
                vars.minutos = 0

 

            # SL
            elif vars.rentabilidad <= params.sl_pr1:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return
    #########################################################
    ####################      PUT  R1  I  ###################
    #########################################################
    elif vars.tipo == "R1-I":
        # MANIFIESTA
        if vars.manifesto:

            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_pr1_i)):
                if round(vars.pico, 3) > params.diamante_pr1_i[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr1_i[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR1_i:
                vars.manifesto = True
                vars.minutos = 0

 

            # SL
            elif vars.rentabilidad <= params.sl_pr1_i:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

    #########################################################
    ####################      PUT  R1  C  ###################
    #########################################################
    elif vars.tipo == "R1-C":
        # MANIFIESTA
        if vars.manifesto:

            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_pr1_c)):
                if round(vars.pico, 3) > params.diamante_pr1_c[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr1_c[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR1_c:
                vars.manifesto = True
                vars.minutos = 0

 

            # SL
            elif vars.rentabilidad <= params.sl_pr1_c:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return
                 
    #########################################################
    ####################      PUT  R1  E  ###################
    #########################################################
    elif vars.tipo == "R1-E":
        # MANIFIESTA
        if vars.manifesto:

            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_pr1_e)):
                if round(vars.pico, 3) > params.diamante_pr1_e[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr1_e[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR1_e:
                vars.manifesto = True
                vars.minutos = 0

 

            # SL
            elif vars.rentabilidad <= params.sl_pr1_e:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return
            
    #########################################################
    ####################      PUT  R1  FAST   ###############
    #########################################################
    elif vars.tipo == "R1-FAST":
        # MANIFIESTA
        if vars.manifesto:

            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_pr1_fast)):
                if round(vars.pico, 3) > params.diamante_pr1_fast[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr1_fast[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR1_fast:
                vars.manifesto = True
                vars.minutos = 0

 

            # SL
            elif vars.rentabilidad <= params.sl_pr1_fast:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

    #########################################################
    ####################      PUT  R2         ###############
    #########################################################
    elif vars.tipo == "R2":
        # MANIFIESTA
        if vars.manifesto:

            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_pr2)):
                if round(vars.pico, 3) > params.diamante_pr2[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr2[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR2:
                vars.manifesto = True
                vars.minutos = 0

         
 

            # SL
            elif vars.rentabilidad <= params.sl_pr2:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

    #########################################################
    ####################      PUT  R2 E       ###############
    #########################################################
    elif vars.tipo == "R2-E":
        # MANIFIESTA
        if vars.manifesto:

            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_pr2_e)):
                if round(vars.pico, 3) > params.diamante_pr2_e[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr2_e[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR2_e:
                vars.manifesto = True
                vars.minutos = 0

 

            # SL
            elif vars.rentabilidad <= params.sl_pr2_e:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return



    #########################################################
    ####################      PUT  R1  F      ###############
    #########################################################
    elif vars.tipo =="F":
        # MANIFIESTA
        if vars.manifesto:

            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_pr1_f)):
                if round(vars.pico, 3) > params.diamante_pr1_f[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr1_f[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR1_f:
                vars.manifesto = True
                vars.minutos = 0

 

            # SL
            elif vars.rentabilidad <= params.sl_pr1_f:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return
            
    #########################################################
    ####################      PUT  R1  F2      ###############
    #########################################################
    elif vars.tipo =="F2":
        # MANIFIESTA
        if vars.manifesto:

            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_pr1_f2)):
                if round(vars.pico, 3) > params.diamante_pr1_f2[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr1_f2[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR1_f2:
                vars.manifesto = True
                vars.minutos = 0

 

            # SL
            elif vars.rentabilidad <= params.sl_pr1_f2:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return
            
    else:pass
    vars.venta_intentos=0
    vars.regla_broadcasting=""
     
def sell(app, vars, params, tipo, regla, contract, symbol):
    from rules.routine import calculations
    
    if vars.rentabilidad<0:
        
        if vars.venta_intentos>=params.intentos:
            pass   
        else:
            vars.venta_intentos+=1
            return
 

    vars.regla_broadcasting = regla
    if vars.sell_broadcasting ==False:
        asyncio.run(send_sell(app, vars, params, tipo,regla))
 
 

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
            if vars.flag_minuto_label:
                generar_label(params, vars,app)
                vars.flag_minuto_label=False
                time.sleep(0.5)
        else:
            vars.flag_minuto_label=True
        if int(timeNow.second) in params.frecuencia_muestra:
            calculations(app, vars, params)
            # ESPERANDO Y REGISTRANDO
            vars.status = "SELLING"
            saveJson(vars, app, params, False)
            writeDayTrade(app, vars, params)

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

def sell_forzada(app, vars, params, tipo, regla, contract, symbol):
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
            if vars.flag_minuto_label:
                generar_label(params, vars,app)
                vars.flag_minuto_label=False
                time.sleep(0.5)
        else:
            vars.flag_minuto_label=True
        if int(timeNow.second) in params.frecuencia_muestra:
            calculations(app, vars, params)
            # ESPERANDO Y REGISTRANDO
            vars.status = "SELLING"
            saveJson(vars, app, params, False)
            writeDayTrade(app, vars, params)

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
