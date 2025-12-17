import json


def clean_vars(vars,varsApp):
    vars.minutos = 0
    vars.compra = True
    vars.call=False
    vars.call=False
    vars.manifesto = False

    vars.ugs_n = 0
    vars.ugs_n_ant = 0
    vars.pico = 0
    vars.priceBuy = 0
 
    vars.flag_Call_R2 = False
    vars.flag_Put_R2 = False
    
    vars.flag_Call_reset_r2=False
    vars.flag_Call_reset_r1=False
    vars.flag_Call_reset_r1_e  =False
    vars.flag_Call_reset_r1_e2= False
    vars.flag_bloqueo_r1_e= False
    vars.flag_cambio_fast= False
    vars.flag_Put_reset_r3= False
    vars.flag_cambio_R1_label= False
    vars.flag_Put_reset_r1_label= False
    vars.flag_cambio_f= False
    vars.flag_Call_reset_r1_c=False

    vars.flag_Call_reset_r1_inv=False
    vars.flag_Call_F_1=False
    vars.flag_Call_F_2=False
    vars.flag_Put_reset_R2=False
    vars.flag_Put_reset_R2e=False
    vars.flag_Put_reset_r2_fast=False
    vars.flag_Put_reset_r1_fast=False
    vars.flag_Put_reset_r1_label_2=False
        



    vars.rule = True

    vars.accion_mensaje = 0
    vars.bloqueo = True
    vars.status = "ON"
    vars.venta_intentos=0
    vars.tipo=""
    vars.real_priceBuy =0
    varsApp.flag_bloqueo_tiempo=False


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

        with open(file_name, "w") as file:
            json.dump(datos, file, indent=4)