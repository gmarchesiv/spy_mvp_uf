# ====================
#  - Librerias -
# ====================
from datetime import datetime
import json
import os
import pytz
import asyncio

# =======================
#  - GUARDAR VAIRBALES -
# =======================
def saveVars(vars, app,  params, estado):
    #---------------------------------------------------
    '''
    Guardado de los datos en json.
    '''
    #---------------------------------------------------
    file_name = "/usr/src/app/data/vars.json"
    now = datetime.now(params.zone)
  
    if estado:

        call_dic = {
            "ask": 0,
            "bid": 0,
            "askSize": 0,
            "bidSize": 0,
            "symbol": "",
            "strike": "",
        }
        put_dic = {
            "ask": 0,
            "bid": 0,
            "askSize": 0,
            "bidSize": 0,
            "symbol": "",
            "strike": "",
        }
        price = 0
    else:

        call_dic = {
            "ask": vars.cask,
            "bid": vars.cbid,
            "askSize": app.options[1]["ASK_SIZE"],
            "bidSize": app.options[1]["BID_SIZE"],
            "symbol": app.options[1]["symbol"],
            "strike": app.options[1]["strike"],
        }
        put_dic = {
            "ask": vars.pask,
            "bid": vars.pbid,
            "askSize": app.options[2]["ASK_SIZE"],
            "bidSize": app.options[2]["BID_SIZE"],
            "symbol": app.options[2]["symbol"],
            "strike": app.options[2]["strike"],
        }

        price = app.etfs[5]["price"]

    datos = {
        "name": params.name,
        "exchange": vars.exchange,
        "exp": vars.exp,
        "strike_p": vars.strike_p,
        "strike_c": vars.strike_c,
        "put_close": vars.put_close,
        "call_close": vars.call_close,
        "put_open": vars.put_open,
        "call_open": vars.call_open,
        "date": now.date().isoformat(),
        "time": now.time().isoformat(),
        "price": price,
        "wallet": app.wallet,
        "call_option": call_dic,
        "put_option": put_dic,
 
        ###############################################
        # VARIABLES DE TIEMPO
        ###############################################
        "minutos": vars.minutos,
        "n_minutos": vars.n_minutos,
        "minutos_trade": vars.minutos_trade,
        ###############################################
        # VARIABLES DE FLAGS
        ###############################################
        "call": vars.call,
        "put": vars.put,
        "compra": vars.compra,
        "manifesto": vars.manifesto,
        "flag_Call_R2": vars.flag_Call_R2,
        "flag_Put_R2": vars.flag_Put_R2,

        "flag_Call_reset_r1":vars.flag_Call_reset_r1,
        "flag_Call_reset_r3":vars.flag_Call_reset_r3,
        "flag_Call_reset_r1_e":vars.flag_Call_reset_r1_e,
        "flag_Call_reset_r1_e2":vars.flag_Call_reset_r1_e2,

        "flag_Put_reset_r2_e": vars.flag_Put_reset_r2_e,
        "flag_Put_reset_r1 ": vars.flag_Put_reset_r1,
        "flag_Put_reset_r1_c":vars.flag_Put_reset_r1_c,
        "flag_Put_reset_r1_c2":vars.flag_Put_reset_r1_c2,
        "flag_Put_reset_r1_fast":vars.flag_Put_reset_r1_fast,
        "flag_Put_reset_r1_i":vars.flag_Put_reset_r1_i,
        "flag_Put_reset_f2":vars.flag_Put_reset_f2,
        "flag_Put_reset_r3":vars.flag_Put_reset_r3,

        "flag_Call_reset_r3_2":vars.flag_Call_reset_r3_2,
        "flag_Put_reset_r1_label":vars.flag_Put_reset_r1_label,
        "flag_cambio_R1_label":vars.flag_cambio_R1_label,

        "flag_Call_reset_r2":vars.flag_Call_reset_r2,
        "flag_Call_reset_r2_2":vars.flag_Call_reset_r2_2,
        "flag_Call_reset_r1_i_2":vars.flag_Call_reset_r1_i_2,
        "flag_Call_reset_r1_c":vars.flag_Call_reset_r1_c,
        "flag_Call_reset_r1_f":vars.flag_Call_reset_r1_f,
        "flag_Call_reset_r1_f2":vars.flag_Call_reset_r1_f2,
        "flag_Put_reset_r2": vars.flag_Put_reset_r2,

        
        ###############################################
        # VARIABLES DE RUTINA
        ###############################################
      
        "ugs_n": vars.ugs_n,
        "ugs_n_ant": vars.ugs_n_ant,
        "pico": vars.pico,
        "tipo": vars.tipo,
        ###############################################
        # VARIABLES DE TRADING
        ###############################################
        "vix": vars.vix,
        "dcall": vars.dcall,
        "dput": vars.dput,
        "docall": vars.docall,
        "doput": vars.doput,
        "doput_ant": vars.doput_ant,
        "askbid_call": vars.askbid_call,
        "askbid_put": vars.askbid_put,
        "askbid_call_prom": [float(x) for x in vars.askbid_call_prom],
        "askbid_put_prom":  [float(x) for x in vars.askbid_put_prom],
        "quantity": vars.quantity,
        "rentabilidad": vars.rentabilidad,
        "rentabilidad_ant": vars.rentabilidad_ant,
        "priceBuy": vars.priceBuy,
        "real_priceBuy":vars.real_priceBuy,
        "caida": vars.caida,
        "regla": vars.regla,
        "trades": vars.trades,
        "fecha": vars.fecha,
        "dif_exp": vars.dif_exp,
        "strikes": vars.strikes,
        # "dic_strike": vars.dic_strike,
        # "dic_exp_strike": vars.dic_exp_strike,
        "rule": vars.rule,
        "accion_mensaje": vars.accion_mensaje,
        "bloqueo": vars.bloqueo,
        "status": vars.status,
        "hora_inicio": vars.hora_inicio,
     
        "promedio_call": vars.promedio_call,
        "promedio_put": vars.promedio_put 
    
    }

    with open(file_name, "w") as json_file:
        json.dump(datos, json_file, indent=4)


async def saveApp(varsApp, app,  params  ):
    #---------------------------------------------------
    '''
    Guardado de los datos en json.
    '''
    #---------------------------------------------------
    file_name = "/usr/src/app/data/app.json"
    now = datetime.now(params.zone)
  
    
    datos = {
        "cash": app.cash,
        "statusIB": app.statusIB,
        "execution_details": app.execution_details,
        "commissions": app.commissions,
        "sendError": app.sendError,
        "Error": app.Error,
        "Error_buy": app.Error_buy,
        "flag_bloqueo_tiempo":varsApp.flag_bloqueo_tiempo
        
    }

    with open(file_name, "w") as json_file:
        json.dump(datos, json_file, indent=4)



async def saveLabel(varsLb):
    file_name = "/usr/src/app/data/label.json"
    datos_lb = {
        ###############################################
        # LABEL
        ###############################################
        "flag_minuto_label": varsLb.flag_minuto_label,
        "label": int(varsLb.label),
        "retorno": varsLb.retorno,
        "signo": varsLb.signo,
        "varianza": varsLb.varianza,
        "pico_etf": varsLb.pico_etf,
        "d_pico": varsLb.d_pico,
        "rsi": varsLb.rsi,
        "mu": varsLb.mu,
        "mu_conteo": varsLb.mu_conteo ,

        # Listas y Deques
        "retorno_lista":[float(x) for x in varsLb.retorno_lista],
        "ret_1H_back":[float(x) for x in varsLb.ret_1H_back],
        "ret_3H_back": [float(x) for x in varsLb.ret_3H_back],
        "ret_6H_back": [float(x) for x in varsLb.ret_6H_back],
        "ret_12H_back":[float(x) for x in varsLb.ret_12H_back],
        "ret_24H_back": [float(x) for x in varsLb.ret_24H_back],
        "ret_96H_back": [float(x) for x in varsLb.ret_96H_back],
        "etf_price_lista":[float(x) for x in varsLb.etf_price_lista]
    
    }
    with open(file_name, "w") as json_file:
        json.dump(datos_lb, json_file, indent=4)
