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
from functions.saveVars import saveVars


# INICIO DE LAS REGLAS DE COMPRA
def buyOptions(app,varsBc,varsLb,vars,params,debug_mode):

    #---------------------------------------------------
    '''
    En la compra de opciones, realizamos calculos y
    verificamos si esta en parametros de compra.
    '''
    #---------------------------------------------------
    
    calculos_previos(vars,varsLb, params,debug_mode)

    vars.promedio_call  = sum(vars.askbid_call_prom) / len(vars.askbid_call_prom) if len(vars.askbid_call_prom)!=0 else 0
    if vars.askbid_call < params.max_askbid_compra_abs and vars.cask > 0 and vars.promedio_call < params.max_askbid_compra_prom :
        calculos_call(vars, params,varsLb,debug_mode )
        buy_Call(app,varsBc,varsLb,vars,params,debug_mode)

    vars.promedio_put  = sum(vars.askbid_put_prom) / len(vars.askbid_put_prom) if len(vars.askbid_put_prom)!=0 else 0
    if vars.askbid_put < params.max_askbid_compra_abs and vars.pask > 0 and  vars.promedio_put < params.max_askbid_compra_prom :
        calculos_put(vars, params )
        buy_Put(app,varsBc,varsLb,vars,params,debug_mode)
    vars.label_ant=varsLb.label
def buy_Call(app,varsBc,varsLb,vars,params,debug_mode):
    if debug_mode:
        timeNow=vars.df["HORA"][vars.i]
    else:
        timeNow = datetime.now(params.zone).time()

    #---------------------------------------------------
    '''
    Reglas de compras de CALL.
    '''
    #---------------------------------------------------
 
    #########################################################
    ####################      CALL R2     ###################
    #########################################################

    if (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r2[0] and timeNow < params.timeCall_r2[1])
        and (vars.dcall >= params.dcall_r2[0] and vars.dcall < params.dcall_r2[1])
        and (vars.docall >= params.docall_r2[0] and vars.docall <= params.docall_r2[1])
        and  (varsLb.label==params.labelCall_r2 )  #and vars.flag_Call_reset_r2  
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C","R2" ,debug_mode
        )
    
    #########################################################
    ####################      CALL R2-2   ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r2_2[0] and timeNow < params.timeCall_r2_2[1])
        and (vars.dcall >= params.dcall_r2_2[0] and vars.dcall < params.dcall_r2_2[1])
        and (vars.docall >= params.docall_r2_2[0] and vars.docall <= params.docall_r2_2[1])
        and  (varsLb.label==params.labelCall_r2_2 )  #and vars.flag_Call_reset_r2  
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C","R2-2" ,debug_mode
        )

    #########################################################
    ####################      CALL R1     ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra_call_r1[0] and timeNow < params.proteccion_compra_call_r1[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1[0] and timeNow < params.timeCall_r1[1])
        and (vars.dcall >= params.dcall_r1[0] and vars.dcall < params.dcall_r1[1])
        and (vars.docall >= params.docall_r1[0] and vars.docall <= params.docall_r1[1])
        and  (varsLb.label==params.labelCall_r1 )and vars.flag_Call_reset_r1
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C","R1" ,debug_mode
        )
    
    #########################################################
    ####################      CALL R1-2   ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra_call_r1[0] and timeNow < params.proteccion_compra_call_r1[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_2[0] and timeNow < params.timeCall_r1_2[1])
        and (vars.dcall >= params.dcall_r1_2[0] and vars.dcall < params.dcall_r1_2[1])
        and (vars.docall >= params.docall_r1_2[0] and vars.docall <= params.docall_r1_2[1])
        and  (varsLb.label==params.labelCall_r1_2 ) 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C","R1-2" ,debug_mode
        )

    #########################################################
    ####################      CALL R1  E  ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_e[0] and timeNow < params.timeCall_r1_e[1])
        and (vars.dcall >= params.dcall_r1_e[0] and vars.dcall < params.dcall_r1_e[1])
        and (vars.docall >= params.docall_r1_e[0] and vars.docall <= params.docall_r1_e[1])
        and  (varsLb.label==params.labelCall_r1_e ) and vars.flag_Call_reset_r1_e 
        and not vars.flag_bloqueo_r1_e
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C","R1-E" ,debug_mode
        )

    #########################################################
    ####################      CALL R1  E2  ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_e2[0] and timeNow < params.timeCall_r1_e2[1])
        and (vars.dcall >= params.dcall_r1_e2[0] and vars.dcall < params.dcall_r1_e2[1])
        and (vars.docall >= params.docall_r1_e2[0] and vars.docall <= params.docall_r1_e2[1])
        and  (varsLb.label==params.labelCall_r1_e2 ) and vars.flag_Call_reset_r1_e2 and not vars.flag_bloqueo_r1_e
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C","R1-E2" ,debug_mode
        )

    #########################################################
    ####################      CALL R1  I  ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_i[0] and timeNow < params.timeCall_r1_i[1])
        and (vars.dcall >= params.dcall_r1_i[0] and vars.dcall < params.dcall_r1_i[1])
        and (vars.docall >= params.docall_r1_i[0] and vars.docall <= params.docall_r1_i[1])
        and  (varsLb.label==params.labelCall_r1_i )  and vars.dput <params.dcall_r1_i_dput
        and vars.flag_Call_reset_r1_inv
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C", "R1-I" ,debug_mode
        )

    #########################################################
    ####################      CALL R1 C   ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_c[0] and timeNow < params.timeCall_r1_c[1])
        and (vars.dcall >= params.dcall_r1_c[0] and vars.dcall < params.dcall_r1_c[1])
        and (vars.docall >= params.docall_r1_c[0] and vars.docall <= params.docall_r1_c[1])
        and  (varsLb.label==params.labelCall_r1_c ) and vars.flag_Call_reset_r1_c
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C", "R1-C" ,debug_mode
        )
 
    #########################################################
    ###################    CALL R1 FAST   ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_fast[0] and timeNow < params.timeCall_r1_fast[1])
        and (vars.dcall >= params.dcall_r1_fast[0] and vars.dcall < params.dcall_r1_fast[1])
        and (vars.docall >= params.docall_r1_fast[0] and vars.docall <  params.docall_r1_fast[1])
        and  (varsLb.label==params.labelCall_r1_fast ) and vars.flag_cambio_fast and vars.flag_Call_R2==False
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C","R1-FAST" ,debug_mode
        )
  
    #########################################################
    ####################      CALL R3     ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra_call_r1[0] and timeNow < params.proteccion_compra_call_r1[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r3[0] and timeNow < params.timeCall_r3[1])
        and (vars.dcall >= params.dcall_r3[0] and vars.dcall < params.dcall_r3[1])
        and (vars.docall >= params.docall_r3[0] and vars.docall <= params.docall_r3[1])
        and  (varsLb.label==params.labelCall_r3 )and vars.flag_Call_R2==False 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C","R3" ,debug_mode
        )
  
    #########################################################
    ####################      CALL R1  F  ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_f1[0] and timeNow < params.timeCall_r1_f1[1])
        and (vars.dcall >= params.dcall_r1_f1[0] and vars.dcall < params.dcall_r1_f1[1])
        and (vars.docall >= params.docall_r1_f1[0] and vars.docall <= params.docall_r1_f1[1])
        and  (varsLb.label==params.labelCall_r1_f1 ) and vars.flag_Call_F_1
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C", "F" ,debug_mode
        )

    #########################################################
    ####################      CALL R1  F2  ################## 
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (timeNow >= params.timeCall_r1_f2[0] and timeNow < params.timeCall_r1_f2[1])
        and (vars.dcall >= params.dcall_r1_f2[0] and vars.dcall < params.dcall_r1_f2[1])
        and (vars.docall >= params.docall_r1_f2[0] and vars.docall <= params.docall_r1_f2[1])
        and  (varsLb.label==params.labelcall_r1_f2 )  and vars.flag_Call_F_2
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C", "F2" ,debug_mode
        )
 
 
def buy_Put(app,varsBc,varsLb,vars,params,debug_mode):
    if debug_mode:
        timeNow=vars.df["HORA"][vars.i]
    else:
        timeNow = datetime.now(params.zone).time()
    #---------------------------------------------------
    '''
    Reglas de compras de PUT.
    '''
    #---------------------------------------------------
 
    #########################################################
    ####################       PUT R2     ###################
    #########################################################
    if ( 
        (timeNow >= params.timePut_r2[0] and timeNow < params.timePut_r2[1])
        and (vars.dput >= params.dput_r2[0] and vars.dput < params.dput_r2[1])
        and (vars.doput >= params.doput_r2[0] and vars.doput < params.doput_r2[1])
        and (varsLb.label==params.labelPut_r2 )  and vars.flag_Put_reset_R2

    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P", "R2" ,debug_mode
        )
 
    #########################################################
    ####################       PUT R2   E ###################
    #########################################################
    elif ( 
        (timeNow >= params.timePut_r2_e[0] and timeNow < params.timePut_r2_e[1])
        and (vars.dput >= params.dput_r2_e[0] and vars.dput < params.dput_r2_e[1])
        and (vars.doput >= params.doput_r2_e[0] and vars.doput < params.doput_r2_e[1])
        and (varsLb.label==params.labelPut_r2_e ) and vars.flag_Put_reset_R2e

    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P", "R2-E" ,debug_mode
        )
 
    #########################################################
    ###################    PUT R2 FAST    ###################
    #########################################################
    elif ( 
        (timeNow >= params.timePut_r2_fast[0] and timeNow < params.timePut_r2_fast[1])
        and (vars.dput >= params.dput_r2_fast[0] and vars.dput < params.dput_r2_fast[1])
        and (vars.doput >= params.doput_r2_fast[0] and vars.doput < params.doput_r2_fast[1])
        and (varsLb.label==params.labelPut_r2_fast )  and vars.flag_Put_reset_r2_fast

    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P", "R2-FAST" ,debug_mode
        )
    
    #########################################################
    ####################       PUT R3     ###################
    #########################################################
    elif ( (timeNow >= params.timePut_r3[0] and timeNow < params.timePut_r3[1])
        and (vars.dput >= params.dput_r3[0] and vars.dput < params.dput_r3[1])
        and (vars.doput >= params.doput_r3[0] and vars.doput < params.doput_r3[1])
        and (varsLb.label==params.labelPut_r3 )and vars.flag_Put_reset_r3

    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P", "R3" ,debug_mode
        )

    #########################################################
    ###################    PUT R1 FAST    ###################
    #########################################################
    elif ( 
        (timeNow >= params.timePut_r1_fast[0] and timeNow < params.timePut_r1_fast[1])
        and (vars.dput >= params.dput_r1_fast[0] and vars.dput < params.dput_r1_fast[1])
        and (vars.doput >= params.doput_r1_fast[0] and vars.doput < params.doput_r1_fast[1])
        and (varsLb.label==params.labelPut_r1_fast )   and vars.flag_Put_reset_r1_fast

    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P", "R1-FAST" ,debug_mode
        )

    #########################################################
    ###################    PUT R1 LABEL    ###################
    #########################################################
    elif ( 
        (timeNow >= params.timePut_r1_label[0] and timeNow < params.timePut_r1_label[1])
        and (vars.dput >= params.dput_r1_label[0] and vars.dput < params.dput_r1_label[1])
        and (vars.doput >= params.doput_r1_label[0] and vars.doput < params.doput_r1_label[1])
        and (varsLb.label==params.labelPut_r1_label )   and vars.flag_cambio_R1_label  and vars.flag_Put_reset_r1_label

    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P", "LABEL-I" ,debug_mode
        )


    #########################################################
    ###################    PUT R1 LABEL 2  ###################
    #########################################################
    elif ( 
        (timeNow >= params.timePut_r1_label_2[0] and timeNow < params.timePut_r1_label_2[1])
        and (vars.dput >= params.dput_r1_label_2[0] and vars.dput < params.dput_r1_label_2[1])
        and (vars.doput >= params.doput_r1_label_2[0] and vars.doput < params.doput_r1_label_2[1])
        and (varsLb.label==params.labelPut_r1_label_2 )   and vars.flag_cambio_R1_label  and vars.flag_Put_reset_r1_label_2

    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P", "LABEL-II" ,debug_mode
        )

    #########################################################
    ####################       PUT R1 I2   ################## 
    #########################################################
    # elif ( 
    #     (timeNow >= params.timePut_r1_i_2[0] and timeNow < params.timePut_r1_i_2[1])
    #     and (vars.dput >= params.dput_r1_i_2[0] and vars.dput < params.dput_r1_i_2[1])
    #     and (vars.doput >= params.doput_r1_i_2[0] and vars.doput < params.doput_r1_i_2[1])
    #     and (varsLb.label==params.labelPut_r1_i_2 )  
    # ):
    #     buy(
    #         app,varsBc,varsLb,vars,params,
    #         "P", "R1-I2" ,debug_mode
    #     )
 
    #########################################################
    ####################       PUT R1 I3   ###################
    #########################################################
    elif ( 
        (timeNow >= params.timePut_r1_i_3[0] and timeNow < params.timePut_r1_i_3[1])
        and (vars.dput >= params.dput_r1_i_3[0] and vars.dput < params.dput_r1_i_3[1])
        and (vars.doput >= params.doput_r1_i_3[0] and vars.doput < params.doput_r1_i_3[1])
        and (varsLb.label==params.labelPut_r1_i_3 )  

    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P", "R1-I3" ,debug_mode
        )

    #########################################################
    ####################       PUT R1 I4   ###################
    #########################################################
    elif ( 
        (timeNow >= params.timePut_r1_i_4[0] and timeNow < params.timePut_r1_i_4[1])
        and (vars.dput >= params.dput_r1_i_4[0] and vars.dput < params.dput_r1_i_4[1])
        and (vars.doput >= params.doput_r1_i_4[0] and vars.doput < params.doput_r1_i_4[1])
        and (varsLb.label==params.labelPut_r1_i_4 )  

    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P", "R1-I4" ,debug_mode
        )

    #########################################################
    ####################       PUT R1 I5   ###################
    #########################################################
    elif ( 
        (timeNow >= params.timePut_r1_i_5[0] and timeNow < params.timePut_r1_i_5[1])
        and (vars.dput >= params.dput_r1_i_5[0] and vars.dput < params.dput_r1_i_5[1])
        and (vars.doput >= params.doput_r1_i_5[0] and vars.doput < params.doput_r1_i_5[1])
        and (varsLb.label==params.labelPut_r1_i_5 )  

    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P", "R1-I5" ,debug_mode
        )
 
 
    
    ########################################################
    ###################       PUT R1 F   ###################
    ########################################################
    elif ( 
        (timeNow >= params.timePut_r1_f[0] and timeNow < params.timePut_r1_f[1])
        and (vars.dput >= params.dput_r1_f[0] and vars.dput < params.dput_r1_f[1])
        and (vars.doput >= params.doput_r1_f[0] and vars.doput < params.doput_r1_f[1])
        and (varsLb.label==params.labelPut_r1_f ) and vars.flag_cambio_f

    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P",  "F" ,debug_mode
        )

   
  

    
     
def buy(app,varsBc,varsLb,vars,params, tipo, regla ,debug_mode):

    from rules.routine import calculations

    #---------------------------------------------------
    '''
    Compra de la opcion, La rutina consta de lo siguiente:
 
        1) Realiza Broadcasting de compra.
        2) Verifica que la compra se pueda dar sin 
           problemas de ASKBID.
        3) Ejecuta la orden de compra.
        4)Espera que la transaccion se complete,mientras
          sigue calculando variables.
        5) Al finalizar modifica variables de estado de 
           compra.
    '''
    #---------------------------------------------------
    if debug_mode:
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
            vars.priceBuy=vars.cask
        elif tipo == "P":
            vars.tipo = regla
            vars.put = True
            vars.regla = f"PUT - {regla}"
            vars.regla_ant = vars.regla
            vars.status = "PUT"
            vars.priceBuy=vars.pask
        else:
            return False
        
        vars.df.loc[vars.i, "REGLA"]=vars.status
        vars.df.loc[vars.i, "TIPO"]=vars.tipo
        print(vars.df["FECHA"][vars.i],vars.status,vars.tipo)
        return True



    else:

        if tipo =="C":
            ask=vars.cask
            contract=app.options[1]["contract"]
            symbol=app.options[1]["symbol"]
        else:
            ask=vars.pask
            contract=app.options[2]["contract"]
            symbol=app.options[2]["symbol"]

        
        #BROADCASTING
        if varsBc.buy ==False:
            asyncio.run(send_buy(app, varsBc, params, tipo,regla))
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
                if varsLb.flag_minuto_label:
                    generar_label(params, varsLb,app)
                    varsLb.flag_minuto_label=False
                    time.sleep(0.5)
            else:
                varsLb.flag_minuto_label=True

            if int(timeNow.second) in params.frecuencia_accion:
                calculations(app, vars,varsBc, params) 
                # ESPERANDO Y REGISTRANDO
                vars.status = "BUYING"
                saveVars(vars, app, params, False)
                writeDayTrade(app, vars,varsLb, params)
                
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

def calculos_call(vars, params,varsLb,debug_mode):
    from datetime import time as dt_time

    if debug_mode:
        timeNow=vars.df["HORA"][vars.i]
    else:
        timeNow = datetime.now(params.zone).time()
    #---------------------------------------------------
    '''
    Calculos de call para bloquear o habilitar reglas 
    de compra.
    '''
    #---------------------------------------------------
    #########################################################
    ###################      CALCULOS      ##################
    #########################################################
 

    # RESET CALL R2
    if vars.docall >= params.docall_r2[1]:
        vars.flag_Call_reset_r2 = False
    elif vars.docall < params.docall_r2[0]:
        vars.flag_Call_reset_r2 = True
    else:
        pass

    # RESET CALL R1
    if vars.docall>= params.docall_r1[1]:
        vars.flag_Call_reset_r1 = False
    elif vars.docall < params.docall_r1[0]:
        vars.flag_Call_reset_r1 = True
    else:
        pass

    # RESET CALL RE1
    if vars.docall>= params.docall_r1_e[1]:
        vars.flag_Call_reset_r1_e = False
    elif vars.docall < params.docall_r1_e[0]:
        vars.flag_Call_reset_r1_e = True
    else:
        pass

    # RESET CALL RE2
    if vars.docall >= params.docall_r1_e2[1]:
        vars.flag_Call_reset_r1_e2 = False
    elif vars.docall < params.docall_r1_e2[0]:
        vars.flag_Call_reset_r1_e2 = True
    else:
        pass

    # RESET CALL RE2
    if vars.docall >= params.docall_r1_c[1]:
        vars.flag_Call_reset_r1_c = False
    elif vars.docall < params.docall_r1_c[0]:
        vars.flag_Call_reset_r1_c = True
    else:
        pass


    if vars.docall >= params.docall_r1_f1[1]:
        vars.flag_Call_F_1 = False
    elif vars.docall < params.docall_r1_f1[0]:
        vars.flag_Call_F_1 = True
    else:
        pass

 
    if vars.docall >= params.docall_r1_f2[1]:
        vars.flag_Call_F_2 = False
    elif vars.docall < params.docall_r1_f2[0]:
        vars.flag_Call_F_2 = True
    else:
        pass


    if vars.docall >= params.docall_r1_i[1]:
        vars.flag_Call_reset_r1_inv = False
    elif vars.docall < params.docall_r1_i[0]:
        vars.flag_Call_reset_r1_inv = True
    else:
        pass
    

    if (vars.flag_cambio_fast==False  and  
        varsLb.label==params.labelCall_r1_fast  and  
       timeNow >= dt_time(9, 33) and  #VITA EL CAMBIO DE NOCHE A MAñana
        varsLb.label!=vars.label_ant):

        vars.flag_cambio_fast=True
  

def calculos_put(vars, params ):

    #########################################################
    ###################      CALCULOS      ##################
    #########################################################

    # RESET R3
    if vars.doput >= params.doput_r3[1]:
        vars.flag_Put_reset_r3 = False
    elif vars.doput < params.doput_r3[0]:
        vars.flag_Put_reset_r3 = True
    else:
        pass


    if vars.doput >= params.doput_r2[1]:
        vars.flag_Put_reset_R2 = False
    elif vars.doput < params.doput_r2[0]:
        vars.flag_Put_reset_R2 = True
    else:
        pass

    if vars.doput >= params.doput_r2_e[1]:
        vars.flag_Put_reset_R2e = False
    elif vars.doput < params.doput_r2_e[0]:
        vars.flag_Put_reset_R2e = True
    else:
        pass


    if vars.doput >= params.doput_r1_fast[1]:
        vars.flag_Put_reset_r1_fast = False
    elif vars.doput < params.doput_r1_fast[0]:
        vars.flag_Put_reset_r1_fast = True
    else:
        pass

    if vars.doput >= params.doput_r2_fast[1]:
        vars.flag_Put_reset_r2_fast = False
    elif vars.doput < params.doput_r2_fast[0]:
        vars.flag_Put_reset_r2_fast = True
    else:
        pass

 
    # RESET PUT LABEL
    if  vars.doput >= params.doput_r1_label[1]:
        vars.flag_Put_reset_r1_label = False

    elif  vars.flag_Put_reset_r1_label == False and\
    vars.doput_ant  <  vars.doput and \
        ( vars.doput>= params.doput_r1_label[0] and  vars.doput <= params.doput_r1_label[1]):
        vars.flag_Put_reset_r1_label = True

    elif  vars.doput<params. doput_r1_label[0]:
        vars.flag_Put_reset_r1_label = True
    else:
        pass  


    # RESET PUT LABEL
    if  vars.doput >= params.doput_r1_label_2[1]:
        vars.flag_Put_reset_r1_label_2 = False

    elif  vars.flag_Put_reset_r1_label_2 == False and\
    vars.doput_ant  <  vars.doput and \
        ( vars.doput>= params.doput_r1_label_2[0] and  vars.doput <= params.doput_r1_label_2[1]):
        vars.flag_Put_reset_r1_label_2 = True

    elif  vars.doput<params. doput_r1_label_2[0]:
        vars.flag_Put_reset_r1_label_2 = True
    else:
        pass  


    vars.doput_ant = vars.doput  


def calculos_previos(vars,varsLb, params,debug_mode):

    from datetime import time as dt_time

    if debug_mode:
        timeNow=vars.df["HORA"][vars.i]
    else:
        timeNow = datetime.now(params.zone).time()


    if (timeNow < params.bloqueo_cr1_e_hora and (vars.docall>params.bloqueo_cr1_e_docall or
        vars.doput>params.bloqueo_cr1_e_doput
        )):

        vars.flag_bloqueo_r1_e=True
  
 

    if (vars.flag_cambio_f==False and 
        timeNow >= params.timePut_r1_f[0] and
         varsLb.label==params.labelPut_r1_f  and  
         varsLb.label!=vars.label_ant 
        ):
        vars.flag_cambio_f=True

    if  (( timeNow <= params.timePut_r1_label_2[1]) and 
          ( varsLb.label!=vars.label_ant  and
            varsLb.label==params.labelPut_r1_label and 
            vars.flag_cambio_R1_label==False)) :
        vars.flag_cambio_R1_label=True