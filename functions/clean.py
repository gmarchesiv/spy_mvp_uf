import json


def clean_vars(vars,varsApp):

    #---------------------------------------------------
    '''
    Limpieza de las variables de rutina y aplicacion.
    '''
    #---------------------------------------------------
    
    ###############################################
    # VARIABLES DE RUTINA
    ###############################################
    vars.ugs_n = 0
    vars.ugs_n_ant = 0
    vars.pico = 0
    vars.priceBuy = 0
    vars.accion_mensaje = 0
    vars.status = "ON"
    vars.tipo=""
    vars.venta_intentos=0
    ###############################################
    # VARIABLES DE FLAGS
    ###############################################
    vars.compra = True
    vars.manifesto = False
    vars.flag_Call_R2 = False
    vars.flag_Put_R2 = False
    vars.flag_Put_reset_r2_e = False
    vars.flag_Put_reset_r1_e = False
    vars.flag_Put_reset_r1 = False
    vars.flag_Put_reset_r1_c = False
    vars.flag_Call_reset_r1_e=False
    vars.flag_Call_reset_r1_e2 = False
    vars.flag_Put_reset_r1_i=False
    vars.flag_Call_reset_r3=False
    vars.flag_Put_reset_r1_c=False


    vars.rule = True
    vars.bloqueo = True
    varsApp.flag_bloqueo_tiempo=False
    vars.flag_Call_reset_r3 = False



def clean_broadcasting(varsBc):
    # LIMPIEZA DE LAS VARIBALES BROADCASTING
    varsBc.aliniar = False
    varsBc.sell = False
    varsBc.sell_tipo_broadcasting = ""
    varsBc.sell_regla_broadcasting = ""
    varsBc.buy = False
    varsBc.buy_tipo_broadcasting = ""
    varsBc.buy_regla_broadcasting = ""
    varsBc.buy = False
    varsBc.sell = False
    varsBc.regla_broadcasting = ""
    varsBc.user_broadcasting = ""

    file_name = "/usr/src/app/data/broadcasting.json"
    with open(file_name, "r") as file:
        datos = json.load(file)

        datos["aliniar"] = False
        datos["sell"] = False
        datos["sell_tipo_broadcasting"] = ""
        datos["sell_regla_broadcasting"] = ""
        datos["buy"] = False
        datos["buy_tipo_broadcasting"] = ""
        datos["buy_regla_broadcasting"] = ""
        datos["buy"] = False
        datos["sell"] = False
        datos["regla_broadcasting"] = ""
        datos["user_broadcasting"] = ""

        with open(file_name, "w") as file:
            json.dump(datos, file, indent=4)