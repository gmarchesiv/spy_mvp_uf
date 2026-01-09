# ====================
#  - Librerias -
# ====================
 
import json
import os

import requests
 

from config.vars.broadcasting import varsBroadcasting
from functions.logs import printStamp
import statistics

import aiohttp
import asyncio
# =======================
#  - Broadcasting -
# =======================


def broadcasting_Alinear(varsBc,vars):

    #---------------------------------------------------
    '''
    Alineamiento del Label.
    '''
    #---------------------------------------------------

    # Lectura del Archivo
    file_name = "/usr/src/app/data/broadcasting.json"

    if os.path.exists(file_name):

        with open(file_name, "r") as json_file:
            try:
                data = json.load(json_file)
            except Exception as e:
                print(type(e).__name__, ":", e)
                varsBc = varsBroadcasting()
                data = json.load(json_file)

            if "aliniar" in data:
                if data["aliniar"] == True:
                    varsBc.aliniar = False

                    vars.call_close = data["call_close"]
                    vars.put_close = data["put_close"]
                    vars.call_open = data["call_open"]
                    vars.put_open = data["put_open"]
                    vars.flag_Call_R2 = data["flag_Call_R2"]
                    vars.flag_Put_R2 = data["flag_Put_R2"]
                    data["aliniar"] = False
                    with open(file_name, "w") as file:
                        json.dump(data, file, indent=4)


def broadcasting_Alinear_label( varsLb,params):

    #---------------------------------------------------
    '''
    Alineamiento del Label.
    '''
    #---------------------------------------------------
    data = []
    for user in params.users:
        url = f"http://{user['ip']}/get-label"
        response = requests.get(url)
        if response.status_code == 200:
            data.append(response.json())  
      
    comparar_label(data,varsLb)

def comparar_label(data,varsLb):
    agrupados = {}
    agrupados_list = {}
    resultado_no_listas={}
    for d in data:
        for k, v in d.items():
            if not   isinstance(v, list):
                agrupados.setdefault(k, []).append(v)
            else:
                agrupados_list.setdefault(k, []).append(v)

    # print(agrupados)
    # print(agrupados_list)
    # Calcular la mediana por cada llave
    resultado_no_listas  = {k: statistics.median(v) for k, v in agrupados.items() if    isinstance(v, list) }
    # print(resultado_no_listas)
    resultado_listas = {}
    for k, listas in agrupados_list.items():
        print(k)
        sumas = [sum(lst) for lst in listas]
        print(sumas)
        mediana = statistics.median(sumas)

        # Buscar la lista cuya suma esté más cerca a la mediana
        dif_min = float("inf")
        lista_mediana = None
        for lst in listas:
            s = sum(lst)
            if abs(s - mediana) < dif_min:
                dif_min = abs(s - mediana)
                lista_mediana = lst

        resultado_listas[k] = lista_mediana
    # print(resultado_listas)
 
    varsLb.label=resultado_no_listas["label"]
    varsLb.retorno = int( resultado_no_listas["retorno"] )
    varsLb.signo  = int( resultado_no_listas["signo"])
    varsLb.varianza  = resultado_no_listas["varianza"]
    varsLb.pico_etf= resultado_no_listas["pico_etf"]
    varsLb.d_pico  = resultado_no_listas["d_pico"] 
    varsLb.rsi= resultado_no_listas["rsi"]
    varsLb.mu= resultado_no_listas["mu"]
    varsLb.mu_conteo= resultado_no_listas["mu_conteo"]

    varsLb.retorno_lista.clear()
    varsLb.ret_1H_back.clear()
    varsLb.ret_3H_back.clear()
    varsLb.ret_6H_back.clear()
    varsLb.ret_12H_back.clear()
    varsLb.ret_24H_back.clear()
    varsLb.ret_96H_back.clear()
    varsLb.etf_price_lista.clear()

    varsLb.retorno_lista.extend(resultado_listas["retorno_lista"])
    varsLb.ret_1H_back.extend(resultado_listas["ret_1H_back"])
    varsLb.ret_3H_back.extend(resultado_listas["ret_3H_back"])
    varsLb.ret_6H_back.extend(resultado_listas["ret_6H_back"])
    varsLb.ret_12H_back.extend(resultado_listas["ret_12H_back"])
    varsLb.ret_24H_back.extend(resultado_listas["ret_24H_back"])
    varsLb.ret_96H_back.extend(resultado_listas["ret_96H_back"])
    varsLb.etf_price_lista.extend(resultado_listas["etf_price_lista"])

def broadcasting_sell(varsBc,varsLb,vars,params,app):

    #---------------------------------------------------
    '''
    Realiza una Venta por Broadcasting, va a revisar
    la informacion recibida y forzara la regla de venta.
    '''
    #---------------------------------------------------

    from rules.sell import sell
    # Lectura del Archivo
    file_name = "/usr/src/app/data/broadcasting.json"
 
    try:
        if os.path.exists(file_name):
            
            with open(file_name, "r") as json_file:
                try:
                    data = json.load(json_file)
                except Exception as e:
                    print(type(e).__name__, ":", e)
                    varsBc = varsBroadcasting()
                    data = json.load(json_file)
    
                if 'sell' in data:
                    if data["sell"] == True or varsBc.sell == True:
                        varsBc.sell = True
                        varsBc.sell_regla =  data["sell_regla"]
                        varsBc.user = data["user"]
                        if vars.call:
                        
                            tipo="C"
                            if vars.askbid_call > params.max_askbid_venta_abs or vars.cbid <= 0:
                                return False
                        elif vars.put:
                        
                            tipo="P"
                            if vars.askbid_put > params.max_askbid_venta_abs or vars.pbid <= 0:
                                return False
                        else:
                            printStamp("-ERROR VENTA BROADCASTING-")
                            return False
                        printStamp(f"-VENTA BROADCASTING POR :{varsBc.user } - {varsBc.sell_regla}")
            
                        venta=sell(app,varsBc,varsLb,vars,params,
                                tipo, varsBc.sell_regla, debug_mode=False
                            )
                        if venta:
                            varsBc.sell =False
                            return
                    
                        return
        
    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("-ERROR VENTA BROADCASTING EN TRY-")  

def broadcasting_sell_auto(varsBc,varsLb,vars,params,app):

    #---------------------------------------------------
    '''
    Realiza una Venta Broadcasting Forzada.
    '''
    #---------------------------------------------------
    # Lectura del Archivo
    file_name = "/usr/src/app/data/broadcasting.json"
 

    if os.path.exists(file_name):
 
        with open(file_name, "r") as json_file:
            try:
                data = json.load(json_file)
            except Exception as e:
                print(type(e).__name__, ":", e)
                varsBc = varsBroadcasting()
                data = json.load(json_file)
 
            if 'sell' in data:
                if data["sell"] == True  :
                    params.max_askbid_venta_abs=data["max_askbid_venta_abs"]
                    if vars.call:
                        val = 1
                        tipo="C"
                        if vars.askbid_call > params.max_askbid_venta_abs or vars.cbid <= 0:
                            return False
                    elif vars.put:
                        val = 2
                        tipo="P"
                        if vars.askbid_put > params.max_askbid_venta_abs or vars.pbid <= 0:
                            return False
                    else:
                        printStamp("-ERROR VENTA BROADCASTING-")
                        return False
                    printStamp(f"-VENTA BROADCASTING POR : ALPHALYTICS - FORZADA")
                    
                    from rules.sell import sell_forzada

                    venta=sell_forzada(app,
                               varsBc,
                               varsLb,  
                            vars ,
                            params,
                            tipo,
                            "FORZADA",
                            app.options[val]["contract"],
                            app.options[val]["symbol"],
                        )
                    if venta:
                        varsBc.sell=False
                        data["sell"] =  False 

                        with open(file_name, "w") as file:
                            json.dump(data, file, indent=4)
                        return
                  
                    return

def broadcasting_buy(varsBc,varsLb,vars,params,app):

    #---------------------------------------------------
    '''
    Realiza una compra por Broadcasting, va a revisar
    la informacion recibida y forzara la regla de venta.
    '''
    #---------------------------------------------------

    from rules.buy import buy
    # Lectura del Archivo
    file_name = "/usr/src/app/data/broadcasting.json"
 
    try:
        if os.path.exists(file_name):
    
            with open(file_name, "r") as json_file:
                data = json.load(json_file)
    
                if 'buy' in data:
                    if data["buy"] == True or varsBc.buy == True:
                        varsBc.buy = True
                
                        varsBc.buy_tipo = data["buy_tipo"]
                        varsBc.buy_regla = data["buy_regla"]
                        varsBc.user = data["user"]
                        if varsBc.buy_tipo == "C":
                          
                            if vars.askbid_call > params.max_askbid_compra_abs or vars.cask <= 0:
                                return False
                          
                        elif varsBc.buy_tipo == "P":
                           
                            if vars.askbid_put > params.max_askbid_compra_abs or vars.pask <= 0:
                                return False
                            
                        else:
                            printStamp("-ERROR COMPRA BROADCASTING-")
                            return False
                        printStamp(f"-COMPRA BROADCASTING POR :{varsBc.user } - {varsBc.buy_tipo} - {varsBc.buy_regla}")
                        flag_buy = buy (app,varsBc,varsLb,vars,params,
                           varsBc.buy_tipo , varsBc.buy_regla ,debug_mode=False)

                        if flag_buy == False:
                            
                            varsBc.buy=False

                            data["buy"] = False 
                            with open(file_name, "w") as file:
                                json.dump(data, file, indent=4)
                            return
                        return
    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("-ERROR COMPRA BROADCASTING EN TRY-")             


async def send_request(session, url, data, user):
    try:
        async with session.post(url, json=data, timeout=1) as response:
            if response.status == 200:
                printStamp(f"Orden enviada a {user['user']} exitosamente")
                print(await response.json())
            else:
                printStamp(f"Error al enviar los datos a {user['user']}: {response.status}")
                print(await response.json())
    except Exception as e:
        printStamp(f"Error en la conexión con {user['user']}: {str(e)}")

async def send_buy( app,varsBc, params, tipo, regla):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for user in params.users:
            url = f"http://{user['ip']}/broadCasting-buy"
            data = {"buy_tipo": tipo, "buy_regla": regla,"user":params.name}
            tasks.append(send_request(session, url, data, user))
        await asyncio.gather(*tasks)
    
    varsBc.buy_tipo = tipo
    varsBc.buy_regla = regla

async def send_sell(  varsBc, params, tipo, regla):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for user in params.users:
            url = f"http://{user['ip']}/broadCasting-sell"
            data = {"sell_tipo": tipo, "sell_regla": regla,"user":params.name}
            tasks.append(send_request(session, url, data, user))
        await asyncio.gather(*tasks)
    
    varsBc.sell_tipo_broadcasting = tipo
    varsBc.sell_regla = regla

async def fetch_price(session, url,user):
    try:
        async with session.get(url, timeout=2) as response:
            if response.status == 200:
                data = await response.json()
                price = data.get("priceBuy", 9999)
                printStamp(f"{user} : {price} $")
                return price if price > 0 else None
    except Exception as e:
        pass
        # printStamp(f"Error obteniendo datos de {url}: {str(e)}")
    return None

async def comparar_precios(vars , params):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_price(session, f"http://{user['ip']}/get-price",user["user"])for user in params.users if user["rama"] == False]
        prices = await asyncio.gather(*tasks)
    
    # Filtrar valores None
    valid_prices = [price for price in prices if price is not None]
    
    # Agregar el valor anterior de vars.priceBuy si existe
    if vars.priceBuy is not None:
        valid_prices.append(vars.priceBuy)
    
    # Obtener el precio más bajo
    vars.priceBuy = min(valid_prices) if valid_prices else vars.priceBuy
 
    printStamp(f"Mi Precio Real: {vars.real_priceBuy} $")
    printStamp(f"Mi Precio actualizado: {vars.priceBuy} $")
 
    print("===============================================")
    return vars.priceBuy

def verificar_regla(params):
    reglas = set()
    
    for user in params.users:
        url = f"http://{user['ip']}/get-regla"
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                data = response.json()
                regla = data.get("regla_broadcasting")
                status = data.get("status")
                rent = data.get("rentabilidad")
                if status:
                    if regla is not None and regla != "":  # Evita agregar valores None o vacíos
                        printStamp(f"{user['user']} salida con regla: {regla} RENT: {round(rent*100,2)}%")

                        reglas.add(regla)
                    else:
                        printStamp(f"{user['user']} salida con regla: - RENT: {round(rent*100,2)}%")

                        reglas.add("-")

            else:
                printStamp(f"Error al obtener la regla de {user['user']}: {response.status_code}")
        except Exception as e:
            printStamp(f"Error en la conexión con {user['user']}: {str(e)}")
    print("===============================================")
    if len(reglas) <1 or "-" in reglas :
        return False
    return True