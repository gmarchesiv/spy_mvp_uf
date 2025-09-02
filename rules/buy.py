# ====================
#  - Librerias -
# ====================


import asyncio
from datetime import datetime
import time
 
from config.IB.options import buyOptionContract
from database.repository.repository import writeDayTrade

# from functions.broadcasting import broadcasting_buy, send_buy
from functions.broadcasting import send_buy
from functions.labels import generar_label
from functions.logs import printStamp, read_buy, readIBData_action
from functions.notifications import sendError
from functions.saveJson import saveJson


# INICIO DE LAS REGLAS DE COMPRA
def buyOptions(app, vars, params):
    vars.promedio_call  = sum(vars.askbid_call_prom) / len(vars.askbid_call_prom) if len(vars.askbid_call_prom)!=0 else 0
    if vars.askbid_call < params.max_askbid_compra_abs and vars.cask > 0 and vars.promedio_call < params.max_askbid_compra_prom :
        calculos_call(vars, params)
        buy_Call(app, vars, params)

    vars.promedio_put  = sum(vars.askbid_put_prom) / len(vars.askbid_put_prom) if len(vars.askbid_put_prom)!=0 else 0
    if vars.askbid_put < params.max_askbid_compra_abs and vars.pask > 0 and  vars.promedio_put < params.max_askbid_compra_prom :
        calculos_put(vars, params)
        buy_Put(app, vars, params)
 


def buy_Call(app, vars, params):
    timeNow = datetime.now(params.zone).time()
    #########################################################
    ####################      CALL R2     ###################
    #########################################################

    if (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r2[0] and timeNow < params.timeCall_r2[1])
        and (vars.dcall >= params.dcall_r2[0] and vars.dcall < params.dcall_r2[1])
        and (vars.docall >= params.docall_r2[0] and vars.docall <= params.docall_r2[1])
        and  (vars.label==params.labelCall_r2 ) #and vars.flag_Call_R2
    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "C",
            "R2",
            vars.cask,
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        if flag_buy == False:
            return

    #########################################################
    ####################      CALL R1     ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra_call_r1[0] and timeNow < params.proteccion_compra_call_r1[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1[0] and timeNow < params.timeCall_r1[1])
        and (vars.dcall >= params.dcall_r1[0] and vars.dcall < params.dcall_r1[1])
        and (vars.docall >= params.docall_r1[0] and vars.docall <= params.docall_r1[1])
        and  (vars.label==params.labelCall_r1 )and vars.flag_Call_reset_r1
    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "C",
            "R1",
            vars.cask,
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        if flag_buy == False:
            return

    #########################################################
    ###################    CALL R1 FAST   ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_fast[0] and timeNow < params.timeCall_r1_fast[1])
        and (vars.dcall >= params.dcall_r1_fast[0] and vars.dcall < params.dcall_r1_fast[1])
        and (vars.docall >= params.docall_r1_fast[0] and vars.docall <= params.docall_r1_fast[1])
        and  (vars.label==params.labelCall_r1_fast ) 
    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "C",
            "R1-FAST",
            vars.cask,
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        if flag_buy == False:
            return 
    #########################################################
    ####################      CALL R3     ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra_call_r1[0] and timeNow < params.proteccion_compra_call_r1[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r3[0] and timeNow < params.timeCall_r3[1])
        and (vars.dcall >= params.dcall_r3[0] and vars.dcall < params.dcall_r3[1])
        and (vars.docall >= params.docall_r3[0] and vars.docall <= params.docall_r3[1])
        and  (vars.label==params.labelCall_r3 )and vars.flag_Call_R2==False and vars.flag_Call_reset_r3 
    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "C",
            "R3",
            vars.cask,
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        if flag_buy == False:
            return
    
    #########################################################
    ####################      CALL R1  E  ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_e[0] and timeNow < params.timeCall_r1_e[1])
        and (vars.dcall >= params.dcall_r1_e[0] and vars.dcall < params.dcall_r1_e[1])
        and (vars.docall >= params.docall_r1_e[0] and vars.docall <= params.docall_r1_e[1])
        and  (vars.label==params.labelCall_r1_e ) and vars.flag_Call_reset_r1_e
    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "C",
            "R1-E",
            vars.cask,
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        if flag_buy == False:
            return
        
    #########################################################
    ####################      CALL R1  E2  ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_e2[0] and timeNow < params.timeCall_r1_e2[1])
        and (vars.dcall >= params.dcall_r1_e2[0] and vars.dcall < params.dcall_r1_e2[1])
        and (vars.docall >= params.docall_r1_e2[0] and vars.docall <= params.docall_r1_e2[1])
        and  (vars.label==params.labelCall_r1_e2 ) and vars.flag_Call_reset_r1_e2
    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "C",
            "R1-E2",
            vars.cask,
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        if flag_buy == False:
            return
    #########################################################
    ####################      CALL R1  I  ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_i[0] and timeNow < params.timeCall_r1_i[1])
        and (vars.dcall >= params.dcall_r1_i[0] and vars.dcall < params.dcall_r1_i[1])
        and (vars.docall >= params.docall_r1_i[0] and vars.docall <= params.docall_r1_i[1])
        and  (vars.label==params.labelCall_r1_i ) 
    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "C",
            "R1-I",
            vars.cask,
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        if flag_buy == False:
            return
    #########################################################
    ####################      CALL R1 C   ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_c[0] and timeNow < params.timeCall_r1_c[1])
        and (vars.dcall >= params.dcall_r1_c[0] and vars.dcall < params.dcall_r1_c[1])
        and (vars.docall >= params.docall_r1_c[0] and vars.docall <= params.docall_r1_c[1])
        and  (vars.label==params.labelCall_r1_c ) 
    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "C",
            "R1-C",
            vars.cask,
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        if flag_buy == False:
            return
        
    #########################################################
    ####################      CALL R1  F  ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_f[0] and timeNow < params.timeCall_r1_f[1])
        and (vars.dcall >= params.dcall_r1_f[0] and vars.dcall < params.dcall_r1_f[1])
        and (vars.docall >= params.docall_r1_f[0] and vars.docall <= params.docall_r1_f[1])
        and  (vars.label==params.labelCall_r1_f ) 
    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "C",
            "F",
            vars.cask,
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        if flag_buy == False:
            return
def buy_Put(app, vars, params):
    timeNow = datetime.now(params.zone).time()
    #########################################################
    ####################       PUT R2     ###################
    #########################################################
    if (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timePut_r2[0] and timeNow < params.timePut_r2[1])
        and (vars.dput >= params.dput_r2[0] and vars.dput < params.dput_r2[1])
        and (vars.doput >= params.doput_r2[0] and vars.doput < params.doput_r2[1])
        and (vars.label==params.labelPut_r2 )and vars.flag_Put_R2

    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "P",
            "R2",
            vars.pask,
            app.options[2]["contract"],
            app.options[2]["symbol"],
        )

        if flag_buy == False:
            return

    #########################################################
    ####################       PUT R2   E ###################
    #########################################################
    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timePut_r2_e[0] and timeNow < params.timePut_r2_e[1])
        and (vars.dput >= params.dput_r2_e[0] and vars.dput < params.dput_r2_e[1])
        and (vars.doput >= params.doput_r2_e[0] and vars.doput < params.doput_r2_e[1])
        and (vars.label==params.labelPut_r2_e )and vars.flag_Put_R2 and vars.flag_Put_reset_r2_e

    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "P",
            "R2-E",
            vars.pask,
            app.options[2]["contract"],
            app.options[2]["symbol"],
        )

        if flag_buy == False:
            return
        
    #########################################################
    ####################       PUT R1     ###################
    #########################################################
    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timePut_r1[0] and timeNow < params.timePut_r1[1])
        and (vars.dput >= params.dput_r1[0] and vars.dput < params.dput_r1[1])
        and (vars.doput >= params.doput_r1[0] and vars.doput < params.doput_r1[1])
        and (vars.label==params.labelPut_r1 )and vars.flag_Put_reset_r1

    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "P",
            "R1",
            vars.pask,
            app.options[2]["contract"],
            app.options[2]["symbol"],
        )

        if flag_buy == False:
            return
        
    #########################################################
    ####################       PUT R1 E   ###################
    #########################################################
    # elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        # not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
    #     (timeNow >= params.timePut_r1_e[0] and timeNow < params.timePut_r1_e[1])
    #     and (vars.dput >= params.dput_r1_e[0] and vars.dput < params.dput_r1_e[1])
    #     and (vars.doput >= params.doput_r1_e[0] and vars.doput < params.doput_r1_e[1])
    #     and (vars.label==params.labelPut_r1_e )  and vars.flag_Put_reset_r1_e

    # ):
    #     flag_buy = buy(
    #         params,
    #         app,
    #         vars,
    #         "P",
    #         "R1-E",
    #         vars.pask,
    #         app.options[2]["contract"],
    #         app.options[2]["symbol"],
    #     )

    #     if flag_buy == False:
    #         return



    #########################################################
    ###################    PUT R1 C       ###################
    #########################################################
    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timePut_r1_c[0] and timeNow < params.timePut_r1_c[1])
        and (vars.dput >= params.dput_r1_c[0] and vars.dput < params.dput_r1_c[1])
        and (vars.doput >= params.doput_r1_c[0] and vars.doput < params.doput_r1_c[1])
        and (vars.label==params.labelPut_r1_c ) and vars.flag_Put_reset_r1_c
    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "P",
            "R1-C",
            vars.pask,
            app.options[2]["contract"],
            app.options[2]["symbol"],
        )

        if flag_buy == False:
            return
    #    
    #########################################################
    ###################    PUT R1 FAST    ###################
    #########################################################
    # elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        # not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
    #     (timeNow >= params.timePut_r1_fast[0] and timeNow < params.timePut_r1_fast[1])
    #     and (vars.dput >= params.dput_r1_fast[0] and vars.dput < params.dput_r1_fast[1])
    #     and (vars.doput >= params.doput_r1_fast[0] and vars.doput < params.doput_r1_fast[1])
    #     and (vars.label==params.labelPut_r1_fast ) 

    # ):
    #     flag_buy = buy(
    #         params,
    #         app,
    #         vars,
    #         "P",
    #         "R1-FAST",
    #         vars.pask,
    #         app.options[2]["contract"],
    #         app.options[2]["symbol"],
    #     )

    #     if flag_buy == False:
    #         return
        
    #########################################################
    ####################       PUT R1 I   ###################
    #########################################################
    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timePut_r1_i[0] and timeNow < params.timePut_r1_i[1])
        and (vars.dput >= params.dput_r1_i[0] and vars.dput < params.dput_r1_i[1])
        and (vars.doput >= params.doput_r1_i[0] and vars.doput < params.doput_r1_i[1])
        and (vars.label==params.labelPut_r1_i ) and vars.flag_Call_R2 ==False and vars.flag_Put_reset_r1_i

    ):
        flag_buy = buy(
            params,
            app,
            vars,
            "P",
            "R1-I",
            vars.pask,
            app.options[2]["contract"],
            app.options[2]["symbol"],
        )

        if flag_buy == False:
            return
        
    

    # #########################################################
    # ####################       PUT R1 F   ###################
    # #########################################################
    # elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
    #                     not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
    #     (timeNow >= params.timePut_r1_f[0] and timeNow < params.timePut_r1_f[1])
    #     and (vars.dput >= params.dput_r1_f[0] and vars.dput < params.dput_r1_f[1])
    #     and (vars.doput >= params.doput_r1_f[0] and vars.doput < params.doput_r1_f[1])
    #     and (vars.label==params.labelPut_r1_f ) 

    # ):
    #     flag_buy = buy(
    #         params,
    #         app,
    #         vars,
    #         "P",
    #         "F",
    #         vars.pask,
    #         app.options[2]["contract"],
    #         app.options[2]["symbol"],
    #     )

    #     if flag_buy == False:
    #         return
        
    # #########################################################
    # ####################       PUT R1 F2   ###################
    # #########################################################
    # elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
    #                     not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
    #     (timeNow >= params.timePut_r1_f2[0] and timeNow < params.timePut_r1_f2[1])
    #     and (vars.dput >= params.dput_r1_f2[0] and vars.dput < params.dput_r1_f2[1])
    #     and (vars.doput >= params.doput_r1_f2[0] and vars.doput < params.doput_r1_f2[1])
    #     and (vars.label==params.labelPut_r1_f2 ) 

    # ):
    #     flag_buy = buy(
    #         params,
    #         app,
    #         vars,
    #         "P",
    #         "F2",
    #         vars.pask,
    #         app.options[2]["contract"],
    #         app.options[2]["symbol"],
    #     )

    #     if flag_buy == False:
    #         return

def buy(params, app, vars, tipo, regla, ask, contract, symbol):
    from rules.routine import calculations
    #BROADCASTING
    if vars.buy_broadcasting ==False:
        asyncio.run(send_buy(app, vars, params, tipo,regla))
    # LECTURA PREVIA
    readIBData_action(app, vars, tipo, regla)

    # ENVIO DE ORDEN DE COMPRA
    flag = buyOptionContract(app, params, vars, ask, tipo, contract, symbol)
    if flag == False:
        printStamp("-NO SE PUDO CONCRETAR LA COMPRA-")
        return False

    # ESPERA DE LA ORDEN DE COMPRA
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
            vars.status = "BUYING"
            saveJson(vars, app, params, False)
            writeDayTrade(app, vars, params)

        if app.Error:
            break
        time.sleep(1)
    if app.Error:
        printStamp(f"-COMPRA NO PROCESADA-")
        sendError(params, "COMPRA NO PROCESADA")
        return False

    # SET DE VARIABLES
    vars.compra = False
    vars.minutos = 0
    vars.n_minutos = 0
    vars.minutos_trade = 0
    if tipo == "C":
        vars.tipo = regla
        vars.call = True
        vars.regla = f"CALL - {regla}"
        vars.regla_ant = vars.regla
        vars.status = "CALL"
    elif tipo == "P":
        vars.tipo = regla
        vars.put = True
        vars.regla = f"PUT - {regla}"
        vars.regla_ant = vars.regla
        vars.status = "PUT"
    else:
        return False
    read_buy(vars)
    return True

def calculos_call(vars, params):
    #########################################################
    ###################      CALCULOS      ##################
    #########################################################

  

    # RESET CALL R1
    if vars.docall>= params.docall_r1[1]:
        vars.flag_Call_reset_r1 = False
    elif vars.docall < params.docall_r1[0]:
        vars.flag_Call_reset_r1 = True
    else:
        pass


    # RESET CALL R1
    if vars.docall>= params.docall_r1_e[1]:
        vars.flag_Call_reset_r1_e = False
    elif vars.docall < params.docall_r1_e[0]:
        vars.flag_Call_reset_r1_e = True
    else:
        pass

    # RESET CALL E2
    if vars.docall>= params.docall_r1_e2[1]:
        vars.flag_Call_reset_r1_e2 = False
    elif vars.docall < params.docall_r1_e2[0]:
        vars.flag_Call_reset_r1_e2 = True
    else:
        pass


    # RESET CALL E2
    if vars.docall>= params.docall_r3[1]:
        vars.flag_Call_reset_r3 = False
    elif vars.docall < params.docall_r3[0]:
        vars.flag_Call_reset_r3 = True
    else:
        pass
 
 

def calculos_put(vars, params):

    #########################################################
    ###################      CALCULOS      ##################
    #########################################################

 

    # RESET PUT R1
    if vars.doput >= params.doput_r1[1]:
        vars.flag_Put_reset_r1 = False
    elif vars.doput < params.doput_r1[0]:
        vars.flag_Put_reset_r1 = True
    else:
        pass
 
    # RESET PUT R2-E
    if vars.doput >= params.doput_r2_e[1]:
        vars.flag_Put_reset_r2_e = False
    elif vars.doput < params.doput_r2_e[0]:
        vars.flag_Put_reset_r2_e = True
    else:
        pass

    # RESET PUT R1-C
    if vars.doput >= params.doput_r1_c[1]:
        vars.flag_Put_reset_r1_c = False
    elif vars.doput < params.doput_r1_c[0]:
        vars.flag_Put_reset_r1_c = True
    else:
        pass

     # RESET PUT inv
    if vars.doput >= params.doput_r1_i[1]:
        vars.flag_Put_reset_r1_i = False
    elif vars.doput < params.doput_r1_i[0]:
        vars.flag_Put_reset_r1_i = True
    else:
        pass

     # RESET PUT inv
    if vars.doput >= params.doput_r1_c[1]:
        vars.flag_Put_reset_r1_c = False
    elif vars.doput < params.doput_r1_c[0]:
        vars.flag_Put_reset_r1_c = True
    else:
        pass
 