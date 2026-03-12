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
        calculos_call(vars, params )
        buy_Call(app,varsBc,varsLb,vars,params,debug_mode)

    vars.promedio_put  = sum(vars.askbid_put_prom) / len(vars.askbid_put_prom) if len(vars.askbid_put_prom)!=0 else 0

    if vars.askbid_put < params.max_askbid_compra_abs and vars.pask > 0 and  vars.promedio_put < params.max_askbid_compra_prom :
        calculos_put(vars, params )
        buy_Put(app,varsBc,varsLb,vars,params,debug_mode)
    
    vars.doput_ant =vars.doput 

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

    if  (
    ( not( 
        (params.proteccion_compra[0]  <= timeNow  < params.proteccion_compra[1]) or
        (params.proteccion_compra_2[0]  <= timeNow  < params.proteccion_compra_2[1]) ))
    and(params.C_r2["TIME"][0] <= timeNow < params.C_r2["TIME"][1])
    and (params.C_r2["D"][0] <=  vars.dcall < params.C_r2["D"][1])
    and (params.C_r2["DO"][0] <= vars.docall < params.C_r2["DO"][1])
    and ((params.C_r2["DPUT"][0] <= vars.dput < params.C_r2["DPUT"][1]) 
    and (vars.askbid_put < params.max_askbid_compra_alt))
    and  (varsLb.label==params.C_r2["LABEL"]   ) 
    and vars.flag_Call_reset["R2"] 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C",params.C_r2 ,debug_mode
        )


        


    #########################################################
    ####################      CALL R1     ###################
    #########################################################

    elif(
        ( not( 
        (params.proteccion_compra_call_r1[0]  <= timeNow  < params.proteccion_compra_call_r1[1]) or
        (params.proteccion_compra_2[0]  <= timeNow  < params.proteccion_compra_2[1]) ))
    
    and(params.C_r1["TIME"][0] <= timeNow < params.C_r1["TIME"][1])
    and (params.C_r1["D"][0] <=  vars.dcall < params.C_r1["D"][1])
    and (params.C_r1["DO"][0] <= vars.docall < params.C_r1["DO"][1])
    and ((params.C_r1["DPUT"][0] <= vars.dput < params.C_r1["DPUT"][1]) 
    and (vars.askbid_put < params.max_askbid_compra_alt))
    and  (varsLb.label==params.C_r1["LABEL"]   ) 
    and vars.flag_Call_reset["R1"] 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C",params.C_r1 ,debug_mode
        )




    #########################################################
    ####################      CALL R1-2   ###################
    #########################################################

    elif(
    (params.C_r1_2["TIME"][0] <= timeNow < params.C_r1_2["TIME"][1])
    and (params.C_r1_2["D"][0] <=  vars.dcall < params.C_r1_2["D"][1])
    and (params.C_r1_2["DO"][0] <= vars.docall < params.C_r1_2["DO"][1])
    and ((params.C_r1_2["DPUT"][0] <= vars.dput < params.C_r1_2["DPUT"][1]) 
    and (vars.askbid_put < params.max_askbid_compra_alt))
    and  (varsLb.label==params.C_r1_2["LABEL"]   ) 
    and vars.flag_Call_reset["R1-2"] 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C",params.C_r1_2 ,debug_mode
        )



    #########################################################
    ####################      CALL R3     ###################
    #########################################################

    elif(
    ( not( 
        (params.proteccion_compra[0]  <= timeNow  < params.proteccion_compra[1]) or
        (params.proteccion_compra_2[0]  <= timeNow  < params.proteccion_compra_2[1]) ))
    and(params.C_r3["TIME"][0] <= timeNow < params.C_r3["TIME"][1])
    and (params.C_r3["D"][0] <=  vars.dcall < params.C_r3["D"][1])
    and (params.C_r3["DO"][0] <= vars.docall < params.C_r3["DO"][1])
    and ((params.C_r3["DPUT"][0] <= vars.dput < params.C_r3["DPUT"][1]) 
    and (vars.askbid_put < params.max_askbid_compra_alt))
    and  (varsLb.label==params.C_r3["LABEL"]   ) 
    and vars.flag_Call_reset["R3"] 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C",params.C_r3 ,debug_mode
        )


    #########################################################
    ####################      CALL R3-2   ###################
    #########################################################

    elif(
    ( not( 
        (params.proteccion_compra[0]  <= timeNow  < params.proteccion_compra[1]) or
        (params.proteccion_compra_2[0]  <= timeNow  < params.proteccion_compra_2[1]) ))
    and(params.C_r3_2["TIME"][0] <= timeNow < params.C_r3_2["TIME"][1])
    and (params.C_r3_2["D"][0] <=  vars.dcall < params.C_r3_2["D"][1])
    and (params.C_r3_2["DO"][0] <= vars.docall < params.C_r3_2["DO"][1])
    and ((params.C_r3_2["DPUT"][0] <= vars.dput < params.C_r3_2["DPUT"][1]) 
    and (vars.askbid_put < params.max_askbid_compra_alt))
    and  (varsLb.label==params.C_r3_2["LABEL"]   ) 
    and vars.flag_Call_reset["R3-2"] 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C",params.C_r3_2 ,debug_mode
        )




    #########################################################
    ####################      CALL R1-E   ###################
    #########################################################

    elif(
    ( not( 
        (params.proteccion_compra[0]  <= timeNow  < params.proteccion_compra[1]) or
        (params.proteccion_compra_2[0]  <= timeNow  < params.proteccion_compra_2[1]) ))
    and(params.C_r1_e["TIME"][0] <= timeNow < params.C_r1_e["TIME"][1])
    and (params.C_r1_e["D"][0] <=  vars.dcall < params.C_r1_e["D"][1])
    and (params.C_r1_e["DO"][0] <= vars.docall < params.C_r1_e["DO"][1])
    and ((params.C_r1_e["DPUT"][0] <= vars.dput < params.C_r1_e["DPUT"][1]) 
    and (vars.askbid_put < params.max_askbid_compra_alt))
    and  (varsLb.label==params.C_r1_e["LABEL"]   ) 
    and vars.flag_Call_reset["R1-E"]
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C",params.C_r1_e ,debug_mode
        )




    #########################################################
    ####################      CALL FAST   ###################
    #########################################################

    elif(
    ( not( 
        (params.proteccion_compra[0]  <= timeNow  < params.proteccion_compra[1]) or
        (params.proteccion_compra_2[0]  <= timeNow  < params.proteccion_compra_2[1]) ))
    and(params.C_fast["TIME"][0] <= timeNow < params.C_fast["TIME"][1])
    and (params.C_fast["D"][0] <=  vars.dcall < params.C_fast["D"][1])
    and (params.C_fast["DO"][0] <= vars.docall < params.C_fast["DO"][1])
    and ((params.C_fast["DPUT"][0] <= vars.dput < params.C_fast["DPUT"][1]) 
    and (vars.askbid_put < params.max_askbid_compra_alt))
    and  (varsLb.label==params.C_fast["LABEL"]   ) 
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C",params.C_fast ,debug_mode
        )




    #########################################################
    ####################      CALL INV    ###################
    #########################################################

    elif(
    ( not( 
        (params.proteccion_compra[0]  <= timeNow  < params.proteccion_compra[1]) or
        (params.proteccion_compra_2[0]  <= timeNow  < params.proteccion_compra_2[1]) ))
    and(params.C_inv_1["TIME"][0] <= timeNow < params.C_inv_1["TIME"][1])
    and (params.C_inv_1["D"][0] <=  vars.dcall < params.C_inv_1["D"][1])
    and (params.C_inv_1["DO"][0] <= vars.docall < params.C_inv_1["DO"][1])
    and ((params.C_inv_1["DPUT"][0] <= vars.dput < params.C_inv_1["DPUT"][1]) 
    and (vars.askbid_put < params.max_askbid_compra_alt))
    and  (varsLb.label==params.C_inv_1["LABEL"]   ) 
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C",params.C_inv_1 ,debug_mode
        )


    
    #########################################################
    ####################      CALL INV-2  ###################
    #########################################################

    elif(
    ( not( 
        (params.proteccion_compra[0]  <= timeNow  < params.proteccion_compra[1]) or
        (params.proteccion_compra_2[0]  <= timeNow  < params.proteccion_compra_2[1]) ))
    and(params.C_inv_2["TIME"][0] <= timeNow < params.C_inv_2["TIME"][1])
    and (params.C_inv_2["D"][0] <=  vars.dcall < params.C_inv_2["D"][1])
    and (params.C_inv_2["DO"][0] <= vars.docall < params.C_inv_2["DO"][1])
    and ((params.C_inv_2["DPUT"][0] <= vars.dput < params.C_inv_2["DPUT"][1]) 
    and (vars.askbid_put < params.max_askbid_compra_alt))
    and  (varsLb.label==params.C_inv_2["LABEL"]   ) 
    and vars.flag_Call_reset["INV-2"]
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C",params.C_inv_2 ,debug_mode
        )

    #########################################################
    ####################      CALL R1  C  ###################
    #########################################################

    elif(
    ( not( 
        (params.proteccion_compra[0]  <= timeNow  < params.proteccion_compra[1]) or
        (params.proteccion_compra_2[0]  <= timeNow  < params.proteccion_compra_2[1]) ))
    and(params.C_r1_c["TIME"][0] <= timeNow < params.C_r1_c["TIME"][1])
    and (params.C_r1_c["D"][0] <=  vars.dcall < params.C_r1_c["D"][1])
    and (params.C_r1_c["DO"][0] <= vars.docall < params.C_r1_c["DO"][1])
    and ((params.C_r1_c["DPUT"][0] <= vars.dput < params.C_r1_c["DPUT"][1]) 
    and (vars.askbid_put < params.max_askbid_compra_alt))
    and  (varsLb.label==params.C_r1_c["LABEL"]   ) 
    and vars.flag_Call_reset["R1-C"]
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "C",params.C_r1_c ,debug_mode
        )

    # #########################################################
    # ####################      CALL R1  F   ################## 
    # #########################################################

    # elif(
    # ( not( 
    #     (params.proteccion_compra[0]  <= timeNow  < params.proteccion_compra[1]) or
    #     (params.proteccion_compra_2[0]  <= timeNow  < params.proteccion_compra_2[1]) ))
    # and(params.C_f1["TIME"][0] <= timeNow < params.C_f1["TIME"][1])
    # and (params.C_f1["D"][0] <=  vars.dcall < params.C_f1["D"][1])
    # and (params.C_f1["DO"][0] <= vars.docall < params.C_f1["DO"][1])
    # and ((params.C_f1["DPUT"][0] <= vars.dput < params.C_f1["DPUT"][1]) 
    # and (vars.askbid_put < params.max_askbid_compra_alt))
    # and  (varsLb.label==params.C_f1["LABEL"]   ) 
    # and vars.flag_Call_reset["F1"]
    # ):
    #     buy(
    #         app,varsBc,varsLb,vars,params,
    #         "C",params.C_f1 ,debug_mode
    #     )
 
 
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
    if   ( 
        (params.P_r2["TIME"][0] <=timeNow  < params.P_r2["TIME"][1])
        and  (params.P_r2["D"][0] <= vars.dput   < params.P_r2["D"][1])
        and   (params.P_r2["DO"][0] <=vars.doput   < params.P_r2["DO"][1])
         and( (params.P_r2["DCALL"][0] <=vars.dcall   < params.P_r2["DCALL"][1])
         and (vars.askbid_call < params.max_askbid_compra_alt))
        and (varsLb.label==params.P_r2["LABEL"]  )
        and vars.flag_Put_reset["R2"]
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P",params.P_r2  ,debug_mode
        )


    ########################################################
    ###################       PUT R2 E    ##################
    ########################################################
    elif ( 
        (params.P_r2_e["TIME"][0] <=timeNow  < params.P_r2_e["TIME"][1])
        and  (params.P_r2_e["D"][0] <= vars.dput   < params.P_r2_e["D"][1])
        and   (params.P_r2_e["DO"][0] <=vars.doput   < params.P_r2_e["DO"][1])
         and( (params.P_r2_e["DCALL"][0] <=vars.dcall   < params.P_r2_e["DCALL"][1])
         and (vars.askbid_call < params.max_askbid_compra_alt))
        and (varsLb.label==params.P_r2_e["LABEL"]  )
        and vars.flag_Put_reset["R2-E"]
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P",params.P_r2_e  ,debug_mode
        )



    ########################################################
    ###################       PUT R1      ##################
    ########################################################
    elif ( 
        (params.P_r1["TIME"][0] <=timeNow  < params.P_r1["TIME"][1])
        and  (params.P_r1["D"][0] <= vars.dput   < params.P_r1["D"][1])
        and   (params.P_r1["DO"][0] <=vars.doput   < params.P_r1["DO"][1])
         and( (params.P_r1["DCALL"][0] <=vars.dcall   < params.P_r1["DCALL"][1])
         and (vars.askbid_call < params.max_askbid_compra_alt))
        and (varsLb.label==params.P_r1["LABEL"]  )
        # and vars.flag_Put_reset["R1"]
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P",params.P_r1  ,debug_mode
        )


    ########################################################
    ###################  PUT R1-LABEL     ##################
    ########################################################
    elif ( 
        (params.P_label_1["TIME"][0] <=timeNow  < params.P_label_1["TIME"][1])
        and  (params.P_label_1["D"][0] <= vars.dput   < params.P_label_1["D"][1])
        and   (params.P_label_1["DO"][0] <=vars.doput   < params.P_label_1["DO"][1])
         and( (params.P_label_1["DCALL"][0] <=vars.dcall   < params.P_label_1["DCALL"][1])
         and (vars.askbid_call < params.max_askbid_compra_alt))
        and (varsLb.label==params.P_label_1["LABEL"]  )
        and vars.flag_Put_reset_esc["LABEL-1"]
        and vars.flag_cambio_R1_label
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P",params.P_label_1  ,debug_mode
        )


    ########################################################
    ###################       PUT INV 1   ##################
    ########################################################
    elif ( 
        (params.P_inv_1["TIME"][0] <=timeNow  < params.P_inv_1["TIME"][1])
        and  (params.P_inv_1["D"][0] <= vars.dput   < params.P_inv_1["D"][1])
        and   (params.P_inv_1["DO"][0] <=vars.doput   < params.P_inv_1["DO"][1])
         and( (params.P_inv_1["DCALL"][0] <=vars.dcall   < params.P_inv_1["DCALL"][1])
         and (vars.askbid_call < params.max_askbid_compra_alt))
        and (varsLb.label==params.P_inv_1["LABEL"]  )
        and vars.flag_Put_reset["INV-1"]
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P",params.P_inv_1  ,debug_mode
        )




    ########################################################
    ###################       PUT INV 2   ##################
    ########################################################
    elif ( 
        (params.P_inv_2["TIME"][0] <=timeNow  < params.P_inv_2["TIME"][1])
        and  (params.P_inv_2["D"][0] <= vars.dput   < params.P_inv_2["D"][1])
        and   (params.P_inv_2["DO"][0] <=vars.doput   < params.P_inv_2["DO"][1])
         and( (params.P_inv_2["DCALL"][0] <=vars.dcall   < params.P_inv_2["DCALL"][1])
         and (vars.askbid_call < params.max_askbid_compra_alt))
        and (varsLb.label==params.P_inv_2["LABEL"]  )
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P",params.P_inv_2  ,debug_mode
        )




    ########################################################
    ###################       PUT INV 3   ##################
    ########################################################
    elif ( 
        (params.P_inv_3["TIME"][0] <=timeNow  < params.P_inv_3["TIME"][1])
        and  (params.P_inv_3["D"][0] <= vars.dput   < params.P_inv_3["D"][1])
        and   (params.P_inv_3["DO"][0] <=vars.doput   < params.P_inv_3["DO"][1])
         and( (params.P_inv_3["DCALL"][0] <=vars.dcall   < params.P_inv_3["DCALL"][1])
         and (vars.askbid_call < params.max_askbid_compra_alt))
        and (varsLb.label==params.P_inv_3["LABEL"]  )
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P",params.P_inv_3  ,debug_mode
        )

    

    ########################################################
    ###################       PUT INV 4   ##################
    ########################################################
    elif ( 
        (params.P_inv_4["TIME"][0] <=timeNow  < params.P_inv_4["TIME"][1])
        and  (params.P_inv_4["D"][0] <= vars.dput   < params.P_inv_4["D"][1])
        and   (params.P_inv_4["DO"][0] <=vars.doput   < params.P_inv_4["DO"][1])
         and( (params.P_inv_4["DCALL"][0] <=vars.dcall   < params.P_inv_4["DCALL"][1])
         and (vars.askbid_call < params.max_askbid_compra_alt))
        and (varsLb.label==params.P_inv_4["LABEL"]  )
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P",params.P_inv_4  ,debug_mode
        )



        
    ########################################################
    ###################       PUT R3   #####################
    ########################################################
    elif ( 
        (params.P_r3["TIME"][0] <=timeNow  < params.P_r3["TIME"][1])
        and  (params.P_r3["D"][0] <= vars.dput   < params.P_r3["D"][1])
        and   (params.P_r3["DO"][0] <=vars.doput   < params.P_r3["DO"][1])
         and( (params.P_r3["DCALL"][0] <=vars.dcall   < params.P_r3["DCALL"][1])
         and (vars.askbid_call < params.max_askbid_compra_alt))
        and (varsLb.label==params.P_r3["LABEL"]  )
 
    ):
        buy(
            app,varsBc,varsLb,vars,params,
            "P",params.P_r3  ,debug_mode
        )

    #########################################################
    ####################       PUT F1     ###################
    #########################################################
    # elif ( 
    #     (params.P_f1["TIME"][0] <=timeNow  < params.P_f1["TIME"][1])
    #     and  (params.P_f1["D"][0] <= vars.dput   < params.P_f1["D"][1])
    #     and   (params.P_f1["DO"][0] <=vars.doput   < params.P_f1["DO"][1])
    #      and( (params.P_f1["DCALL"][0] <=vars.dcall   < params.P_f1["DCALL"][1])
    #      and (vars.askbid_call < params.max_askbid_compra_alt))
    #     # and (varsLb.label==params.P_f1["LABEL"]  )
 
    # ):
    #     buy(
    #         app,varsBc,varsLb,vars,params,
    #         "P",params.P_f1  ,debug_mode
    #     )
     
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
            vars.tipo = regla['REGLA']
            vars.call = True
            vars.regla = f"CALL - {regla['REGLA']}"
            vars.regla_ant = vars.regla
            vars.status = "CALL"
            vars.priceBuy=vars.cask
            vars.params_regla =regla
        elif tipo == "P":
            vars.tipo = regla['REGLA']
            vars.put = True
            vars.regla = f"PUT - {regla['REGLA']}"
            vars.regla_ant = vars.regla
            vars.status = "PUT"
            vars.priceBuy=vars.pask
            vars.params_regla =regla
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
            asyncio.run(send_buy(app, varsBc, params, tipo,regla['REGLA']))
        # LECTURA PREVIA
        readIBData_action(app, vars, tipo, regla['REGLA'])

        # ENVIO DE ORDEN DE COMPRA
        flag = buyOptionContract(app, params, vars, ask, tipo, contract, symbol)
        if flag == False:
            printStamp("-NO SE PUDO CONCRETAR LA COMPRA-")
            return False

        # ESPERA DE LA ORDEN DE COMPRA
        app.statusIB = False
        app.Error = False

        printStamp("-wait Status-")
        vars.regla = f"BUY"
        while app.statusIB == False:

            timeNow = datetime.now(params.zone).time()

            if (timeNow.minute % 10 == 0 or timeNow.minute % 10 == 5):
                if varsLb.flag_minuto_label:
                    generar_label(params, varsLb,app)
                    varsLb.flag_minuto_label=False
                    time.sleep(0.5)
            else:
                varsLb.flag_minuto_label=True

            # if int(timeNow.second) in params.frecuencia_accion:
            calculations(app, vars,varsBc, params) 
            # ESPERANDO Y REGISTRANDO
            vars.status = "BUYING"
            saveVars(vars, app, params, False)
            writeDayTrade(app, vars,varsLb, params)
            vars.regla = f""    
            if app.Error:
                break
            time.sleep(0.5)
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
            vars.tipo = regla['REGLA']
            vars.call = True
            vars.regla = f"CALL - {regla['REGLA']}"
            vars.regla_ant = vars.regla
            vars.status = "CALL"
            vars.params_regla =regla
        elif tipo == "P":
            vars.tipo = regla['REGLA']
            vars.put = True
            vars.regla = f"PUT - {regla['REGLA']}"
            vars.regla_ant = vars.regla
            vars.status = "PUT"
            vars.params_regla =regla
        else:
            return False
        read_buy(vars)
        return True

def calculos_call(vars, params):
    #---------------------------------------------------
    '''
    Calculos de call para bloquear o habilitar reglas 
    de compra.
    '''
    #---------------------------------------------------
    #########################################################
    ###################      CALCULOS      ##################
    #########################################################
   # RESET BASICO
    for variable,parametro in vars.parametros_reglas.items():
        if "red" in parametro:
            continue
        regla=parametro['REGLA']
        if regla in vars.flag_Call_reset and parametro["TIPO"]=="CALL":

            if vars.docall >= parametro["DO"][1]:
                vars.flag_Call_reset[regla] = False
            elif vars.docall < parametro["DO"][0]:
                vars.flag_Call_reset[regla] = True
            else:continue
 

    
 
def calculos_put(vars, params):
    #---------------------------------------------------
    '''
    Calculos de put para bloquear o habilitar reglas 
    de compra.
    '''
    #---------------------------------------------------
    #########################################################
    ###################      CALCULOS      ##################
    #########################################################
    
   
    # RESET BASICO
    for variable,parametro in vars.parametros_reglas.items():
        if "red" in parametro:
            continue
        regla=parametro['REGLA']
        if regla in vars.flag_Put_reset and parametro["TIPO"]=="PUT":
            if vars.doput >= parametro["DO"] [1]:
                vars.flag_Put_reset[regla] = False
            elif vars.doput < parametro["DO"] [0]:
                vars.flag_Put_reset[regla] = True
            else:continue



    # RESET ESCALONADO
 
    for variable,parametro in vars.parametros_reglas.items():
        if "red" in parametro:
            continue
        regla=parametro['REGLA']
        if regla in vars.flag_Put_reset_esc and parametro["TIPO"]=="PUT":

            if vars.doput  >= parametro["DO"] [1]:
                vars.flag_Put_reset_esc[regla] = False

            elif  vars.flag_Put_reset_esc[regla] == False and\
            vars.doput_ant  < vars.doput  and \
                ( parametro["DO"] [0] <= vars.doput  <= parametro["DO"] [1]):
                vars.flag_Put_reset_esc[regla] = True
                
            elif vars.doput  < parametro["DO"] [0]:
                vars.flag_Put_reset_esc[regla] = True
            else:
                pass
                

     

def calculos_previos(vars,varsLb, params,debug_mode):
    from datetime import time as dt_time

    if debug_mode:
        timeNow=vars.df["HORA"][vars.i]
    else:
        timeNow = datetime.now(params.zone).time()

 

    if  (( timeNow <= params.P_label_1 ["TIME"][1] ) and 
          ( varsLb.label!=vars.label_ant  and
            varsLb.label==params.P_label_1 ["LABEL"]and 
            vars.flag_cambio_R1_label==False)) :
        vars.flag_cambio_R1_label=True