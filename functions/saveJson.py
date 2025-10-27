# ====================
#  - Librerias -
# ====================
from datetime import datetime
import json
import os
import pytz


# =======================
#  - GUARDAR VAIRBALES -
# =======================
def saveJson(vars, app,  params, estado):
    file_name = "/usr/src/app/data/vars.json"
    now = datetime.now(params.zone)
    if os.path.exists(file_name):
 
        with open(file_name, "r") as json_file:
            data = json.load(json_file)

            # vars.aliniar=data["aliniar"]
            if  vars.sell_broadcasting ==False:
                vars.sell_broadcasting=data["sell_broadcasting"]
                vars.sell_tipo_broadcasting=data["sell_tipo_broadcasting"]
                vars.sell_regla_broadcasting=data["sell_regla_broadcasting"]
                vars.user_broadcasting = data["user_broadcasting"]
            if  vars.buy_broadcasting ==False:
                vars.buy_broadcasting=data["buy_broadcasting"]
                vars.buy_tipo_broadcasting=data["buy_tipo_broadcasting"]
                vars.buy_regla_broadcasting=data["buy_regla_broadcasting"]
                vars.user_broadcasting = data["user_broadcasting"]
 
 

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
        "exp_2": vars.exp_2,
        "strike_p_2": vars.strike_p_2,
        "strike_c_2": vars.strike_c_2,
        "put_close": vars.put_close,
        "call_close": vars.call_close,
        "put_close_2": vars.put_close_2,
        "call_close_2": vars.call_close_2,
        "put_open_2": vars.put_open_2,
        "call_open_2": vars.call_open_2,
        "put_open": vars.put_open,
        "call_open": vars.call_open,
        "date": now.date().isoformat(),
        "time": now.time().isoformat(),
        "price": price,
        "wallet": app.wallet,
        "call_option": call_dic,
        "put_option": put_dic,
        "flag_bloqueo_tiempo":vars.flag_bloqueo_tiempo,
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
        "flag_Put_reset_r2_e": vars.flag_Put_reset_r2_e,
        "flag_Put_reset_r1_e": vars.flag_Put_reset_r1_e,
        "flag_Put_reset_r1 ": vars.flag_Put_reset_r1,
        "flag_Put_reset_r1_c":vars.flag_Put_reset_r1_c,
        "flag_Call_reset_r1_e":vars.flag_Call_reset_r1_e,
        "flag_Call_reset_r1_e2":vars.flag_Call_reset_r1_e2,
        "flag_Put_reset_r1_i":vars.flag_Put_reset_r1_i,
        "flag_Call_reset_r3":vars.flag_Call_reset_r3,
        "flag_Put_reset_r1_c":vars.flag_Put_reset_r1_c,
        ###############################################
        # VARIABLES DE RUTINA
        ###############################################
        # "min_extras": vars.min_extras,
        # "min_desicion": vars.min_desicion,
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
        "askbid_call": vars.askbid_call,
        "askbid_put": vars.askbid_put,

        "dcall_2": vars.dcall_2,
        "dput_2": vars.dput_2,
        "docall_2": vars.docall_2,
        "doput_2": vars.doput_2,
        "askbid_call_2": vars.askbid_call_2,
        "askbid_put_2": vars.askbid_put_2,

        
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
        ###############################################
        # BROADCASTING
        ###############################################
        "hora_inicio": vars.hora_inicio,
        "aliniar": vars.aliniar,
        "sell_broadcasting": vars.sell_broadcasting,
        "sell_tipo_broadcasting": vars.sell_tipo_broadcasting,
        "sell_regla_broadcasting": vars.sell_regla_broadcasting,
        "buy_broadcasting": vars.buy_broadcasting,
        "buy_tipo_broadcasting": vars.buy_tipo_broadcasting,
        "buy_regla_broadcasting": vars.buy_regla_broadcasting,
        "buy": vars.buy,
        "sell": vars.sell,
        "conexion": True,
        "venta_intentos":vars.venta_intentos,
        "user_broadcasting": vars.user_broadcasting,
        "regla_broadcasting":vars.regla_broadcasting,
        ###############################################
        # VARIABLES DE APP
        ###############################################
        "cash": app.cash,
        "statusIB": app.statusIB,
        "execution_details": app.execution_details,
        "commissions": app.commissions,
        "sendError": app.sendError,
        "Error": app.Error,
        "Error_buy": app.Error_buy,
        ###############################################
        # LABEL
        ###############################################
        "flag_minuto_label": vars.flag_minuto_label,
        "label": int(vars.label),
        "retorno_lista":[float(x) for x in vars.retorno_lista],
        "retorno": vars.retorno,
        "signo": vars.signo,
        "varianza": vars.varianza,
        "pico_etf": vars.pico_etf,
        "d_pico": vars.d_pico,
        "ret_1H_back":[float(x) for x in vars.ret_1H_back],
        "ret_3H_back": [float(x) for x in vars.ret_3H_back],
        "ret_6H_back": [float(x) for x in vars.ret_6H_back],
        "ret_12H_back":[float(x) for x in vars.ret_12H_back],
        "ret_24H_back": [float(x) for x in vars.ret_24H_back],
        "ret_96H_back": [float(x) for x in vars.ret_96H_back],
        "etf_price_lista":[float(x) for x in vars.etf_price_lista],
        "rsi": vars.rsi,
        "mu": vars.mu,
        "mu_conteo": vars.mu_conteo ,
        "promedio_call": vars.promedio_call,
        "promedio_put": vars.promedio_put 
    
    }

    with open(file_name, "w") as json_file:
        json.dump(datos, json_file, indent=4)
