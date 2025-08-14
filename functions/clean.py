import json


def clean_vars(vars):
    vars.compra = True

    vars.flag_desicion = True
    vars.flag_pos = False
    vars.flag_neg = False
    vars.manifesto = False

    vars.ugs_n = 0
    vars.ugs_n_ant = 0
    vars.pico = 0
 
    vars.priceBuy = 0
    
    vars.flag_Call_R2 = False
    vars.flag_Put_R2 = False
    vars.flag_Put_reset_r2_e = False
    vars.flag_Put_reset_r1_e = False
    vars.flag_Put_reset_r1 = False
    vars.flag_Put_reset_r1_c = False
    vars.flag_Call_reset_r1_e=False


    vars.rule = True

    vars.accion_mensaje = 0
    vars.bloqueo = True
    vars.status = "ON"
    vars.tipo=""
    vars.venta_intentos=0
    vars.flag_bloqueo_tiempo=False



def clean_broadcasting(vars):
    # LIMPIEZA DE LAS VARIBALES BROADCASTING
    vars.aliniar = False
    vars.sell_broadcasting = False
    vars.sell_tipo_broadcasting = ""
    vars.sell_regla_broadcasting = ""
    vars.buy_broadcasting = False
    vars.buy_tipo_broadcasting = ""
    vars.buy_regla_broadcasting = ""
    vars.buy = False
    vars.sell = False
    vars.regla_broadcasting = ""
    vars.user_broadcasting = ""

    file_name = "/usr/src/app/data/vars.json"
    with open(file_name, "r") as file:
        datos = json.load(file)

        datos["aliniar"] = False
        datos["sell_broadcasting"] = False
        datos["sell_tipo_broadcasting"] = ""
        datos["sell_regla_broadcasting"] = ""
        datos["buy_broadcasting"] = False
        datos["buy_tipo_broadcasting"] = ""
        datos["buy_regla_broadcasting"] = ""
        datos["buy"] = False
        datos["sell"] = False
        datos["regla_broadcasting"] = ""
        datos["user_broadcasting"] = ""

        with open(file_name, "w") as file:
            json.dump(datos, file, indent=4)