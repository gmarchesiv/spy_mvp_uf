# ====================
#  - Librerias -
# ====================
 
import json
import os

import requests
 

from functions.logs import printStamp


import aiohttp
import asyncio
# =======================
#  - Broadcasting -
# =======================


def broadcasting_Aliniar(vars):
    # Lectura del Archivo
    file_name = "/usr/src/app/data/vars.json"

    if os.path.exists(file_name):

        with open(file_name, "r") as json_file:
            data = json.load(json_file)

            if "aliniar" in data:
                if data["aliniar"] == True:
                    vars.aliniar = False

                    vars.call_close = data["call_close"]
                    vars.put_close = data["put_close"]
                    vars.call_open = data["call_open"]
                    vars.put_open = data["put_open"]
                    vars.flag_Call_R2 = data["flag_Call_R2"]
                    vars.flag_Put_R2 = data["flag_Put_R2"]

def broadcasting_sell(vars,params,app):
    from rules.sell import sell
    # Lectura del Archivo
    file_name = "/usr/src/app/data/vars.json"
 

    if os.path.exists(file_name):
 
        with open(file_name, "r") as json_file:
            data = json.load(json_file)
 
            if 'sell_broadcasting' in data:
                if data["sell_broadcasting"] == True or vars.sell_broadcasting == True:
                    vars.sell_broadcasting = True
                    vars.sell_regla_broadcasting =  data["sell_regla_broadcasting"]
         
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
                    printStamp(f"-VENTA BROADCASTING POR :{vars.user_broadcasting } - {vars.sell_regla_broadcasting}")
         
                    venta=sell(
                            app,
                            vars,
                            params,
                            tipo,
                            vars.sell_regla_broadcasting,
                            app.options[val]["contract"],
                            app.options[val]["symbol"],
                        )
                    if venta:
                        vars.sell_broadcasting =False
                        return
                  
                    return
def broadcasting_sell_auto(vars,params,app,bc):
    
    # Lectura del Archivo
    file_name = "/usr/src/app/data/broadcasting.json"
 

    if os.path.exists(file_name):
 
        with open(file_name, "r") as json_file:
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

                    venta=sell_forzada(
                            app,
                            vars,
                            params,
                            tipo,
                            "FORZADA",
                            app.options[val]["contract"],
                            app.options[val]["symbol"],
                        )
                    if venta:
                        bc.sell=False
                        data["sell"] =  False 

                        with open(file_name, "w") as file:
                            json.dump(data, file, indent=4)
                        return
                  
                    return



def broadcasting_buy(vars,params,app):
    from rules.buy import buy
    # Lectura del Archivo
    file_name = "/usr/src/app/data/vars.json"
 
    try:
        if os.path.exists(file_name):
    
            with open(file_name, "r") as json_file:
                data = json.load(json_file)
    
                if 'buy_broadcasting' in data:
                    if data["buy_broadcasting"] == True or vars.buy_broadcasting == True:
                        vars.buy_broadcasting = True
                
                        vars.buy_tipo_broadcasting = data["buy_tipo_broadcasting"]
                        vars.buy_regla_broadcasting = data["buy_regla_broadcasting"]
                        vars.user_broadcasting = data["user_broadcasting"]
                        if vars.buy_tipo_broadcasting == "C":
                            val = 1
                            if vars.askbid_call > params.max_askbid_compra_abs or vars.cask <= 0:
                                return False
                            precio=vars.cask
                        elif vars.buy_tipo_broadcasting == "P":
                            val = 2
                            if vars.askbid_put > params.max_askbid_compra_abs or vars.pask <= 0:
                                return False
                            precio=vars.pask
                        else:
                            printStamp("-ERROR COMPRA BROADCASTING-")
                            return False
                        printStamp(f"-COMPRA BROADCASTING POR :{vars.user_broadcasting } - {vars.buy_tipo_broadcasting} - {vars.buy_regla_broadcasting}")
                        flag_buy = buy(
                            params,
                            app,
                            vars,
                            vars.buy_tipo_broadcasting ,
                            vars.buy_regla_broadcasting,
                            precio,
                            app.options[val]["contract"],
                            app.options[val]["symbol"],
                        )

                        if flag_buy == False:
                            return
                        vars.buy_broadcasting=False
                        return
    except:pass             
async def send_request(session, url, data, user):
    try:
        async with session.post(url, json=data, timeout=2) as response:
            if response.status == 200:
                printStamp(f"Orden enviada a {user['user']} exitosamente")
                print(await response.json())
            else:
                printStamp(f"Error al enviar los datos a {user['user']}: {response.status}")
                print(await response.json())
    except Exception as e:
        printStamp(f"Error en la conexión con {user['user']}: {str(e)}")

async def send_buy(app, vars, params, tipo, regla):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for user in params.users:
            url = f"http://{user['ip']}/broadCasting-buy"
            data = {"buy_tipo_broadcasting": tipo, "buy_regla_broadcasting": regla,"user_broadcasting":params.name}
            tasks.append(send_request(session, url, data, user))
        await asyncio.gather(*tasks)
    
    vars.buy_tipo_broadcasting = tipo
    vars.buy_regla_broadcasting = regla

async def send_sell(app, vars, params, tipo, regla):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for user in params.users:
            url = f"http://{user['ip']}/broadCasting-sell"
            data = {"sell_tipo_broadcasting": tipo, "sell_regla_broadcasting": regla,"user_broadcasting":params.name}
            tasks.append(send_request(session, url, data, user))
        await asyncio.gather(*tasks)
    
    vars.sell_tipo_broadcasting = tipo
    vars.sell_regla_broadcasting = regla

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

async def comparar_precios(vars, params):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_price(session, f"http://{user['ip']}/get-price",user["user"]) for user in params.users if user["rama"] == False]
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