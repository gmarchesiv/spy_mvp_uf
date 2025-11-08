from flask import Flask, jsonify, request, abort
import json
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta

from datetime import time as dt_time
import subprocess
import os

import pytz

# Modificar el PATH para incluir el directorio donde está el binario de Docker
os.environ["PATH"] += os.pathsep + "/usr/bin/docker"


app = Flask(__name__)
origin = {"origins": "http://localhost:3001"}
CORS(
    app,
    resources={
        r"/get-data": origin,
        r"/transactions": origin,
        r"/daytrade": origin,
        r"/reset": origin,
        r"/hard_reset": origin,
        r"/conection-status": origin,
        r"/daytrade_all": origin,
        r"/broadCasting-aliniar": origin,
        r"/broadCasting-strike": origin,
        r"/broadCasting-sell": origin,
        r"/broadCasting-sell-auto": origin,
        r"/broadCasting-buy": origin,
        r"/get-price": origin,
        r"/get-regla": origin,
    },
)


def get_db_connection():
    conn = sqlite3.connect("/usr/src/dataBase.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/get-data", methods=["GET"])
def get_json():
    
    try:
        file_name = "/usr/src/vars.json"
        with open(file_name, "r") as f:
            data_vars = json.load(f)
        file_name = "/usr/src/app.json"
        with open(file_name, "r") as f:
            data_app = json.load(f)
        file_name = "/usr/src/label.json"
        with open(file_name, "r") as f:
            data_label = json.load(f)

        data = {**data_vars, **data_app,**data_label}
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = get_db_connection()

    daytrade_data = conn.execute(
        """
        SELECT * FROM transactions ;
    """
    ).fetchall()
    conn.close()

    # Convertir los resultados a una lista de diccionarios
    daytrade_dicts = {}
    for row in daytrade_data:
        for column_index, column_name in enumerate(row.keys()):
            if column_name not in daytrade_dicts:
                daytrade_dicts[column_name] = []
            daytrade_dicts[column_name].append(row[column_index])

    return jsonify(daytrade_dicts)


@app.route("/daytrade", methods=["GET"])
def get_daytrade():
    conn = get_db_connection()
    today = datetime.today().strftime("%Y-%m-%d")

    daytrade_data = conn.execute(
        f"""
       SELECT *
FROM daytrade
WHERE DATE(date) = '{today}'
    """
    ).fetchall()
    conn.close()

    # Convertir los resultados a una lista de diccionarios
    daytrade_dicts = {}
    for row in daytrade_data:
        for column_index, column_name in enumerate(row.keys()):
            if column_name not in daytrade_dicts:
                daytrade_dicts[column_name] = []
            daytrade_dicts[column_name].append(row[column_index])

    return jsonify(daytrade_dicts)


@app.route("/daytrade_all", methods=["GET"])
def get_daytrade_all():
    conn = get_db_connection()
    today = datetime.today().strftime("%Y-%m-%d")

    daytrade_data = conn.execute(
        f"""
       SELECT *
FROM daytrade
 
    """
    ).fetchall()
    conn.close()

    # Convertir los resultados a una lista de diccionarios
    daytrade_dicts = {}
    for row in daytrade_data:
        for column_index, column_name in enumerate(row.keys()):
            if column_name not in daytrade_dicts:
                daytrade_dicts[column_name] = []
            daytrade_dicts[column_name].append(row[column_index])

    return jsonify(daytrade_dicts)


@app.route("/reset", methods=["GET"])
def get_reset():

    # Ejecutar el comando para reiniciar el contenedor
    try:
        subprocess.run(["docker", "restart", "portainer_agent"], check=True)
        subprocess.run(["docker", "restart", "ibkr_config-ibkr-1"], check=True)
        timeNow = datetime.now(pytz.timezone("America/New_York")).time()
        if timeNow < dt_time(9, 0) or timeNow >= dt_time(16, 0):

            subprocess.run(
                ["docker", "restart", "spy_mvp_uf-python_script-1"], check=True
            )

        return {"status": "success", "message": "Container restarted successfully"}, 200
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}, 500


@app.route("/hard_reset", methods=["GET"])
def get_hard_reset():

    # Ejecutar el comando para reiniciar el contenedor
    try:
        subprocess.run(["docker", "restart", "portainer_agent"], check=True)
        subprocess.run(["docker", "restart", "ibkr_config-ibkr-1"], check=True)
        subprocess.run(
                ["docker", "restart", "spy_mvp_uf-python_script-1"], check=True
            )
        subprocess.run(
                ["docker", "restart", "spy_mvp_uf-python_app-1"], check=True
            )

        return {"status": "success", "message": "Container restarted successfully"}, 200
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}, 500

@app.route("/conection-status", methods=["GET"])
def get_conection():

    # Ejecutar el comando para reiniciar el contenedor
    try:
        file_name = "/usr/src/vars.json"

        # Leer los datos existentes en el archivo JSON
        with open(file_name, "r") as f:
            data = json.load(f)

            if data["conexion"] :
                try:
                    fecha_data = datetime.strptime(data["date"], "%Y-%m-%d").date()  # Ajusta el formato si es necesario
                    hoy = datetime.today().date()
                    ayer = hoy - timedelta(days=1)
        
                    # Si la fecha no es hoy ni ayer, cambiar "conexion" a False
                    if fecha_data not in {hoy, ayer}:
                        data["conexion"] = False
                        
                        # Guardar los cambios en el archivo
                        with open(file_name, "w") as f:
                            json.dump(data, f, indent=4)
                except ValueError:
                    print("Error: El formato de la fecha en el archivo no es válido.")
 
            respuesta={
                "is_online": data["conexion"],
                "date": data["date"],
                "time": data["time"]
            }
        return respuesta, 200
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}, 500


@app.route("/broadCasting-aliniar", methods=["POST"])
def post_broadCasting_aliniar():
    file_name = "/usr/src/broadcasting.json"
    try:
        # Obtener el body de la solicitud
        body = request.json

        # Leer los datos existentes en el archivo JSON
        with open(file_name, "r") as f:
            data = json.load(f)

        # Actualizar los datos con los valores del body

        data["call_close"] = body.get("call_close", data.get("call_close"))
        data["put_close"] = body.get("put_close", data.get("put_close"))

        data["call_open"] = body.get("call_open", data.get("call_open"))
        data["put_open"] = body.get("put_open", data.get("put_open"))
        data["flag_Call_R2"] = body.get("flag_Call_R2", data.get("flag_Call_R2"))
        data["flag_Put_R2"] = body.get("flag_Put_R2", data.get("flag_Put_R2"))

        data["aliniar"] = True

        # Guardar los datos actualizados de nuevo en el archivo
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

        # Devolver los datos actualizados como respuesta
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/broadCasting-strike", methods=["POST"])
def post_broadCasting_strike():
    file_name = "/usr/src/vars.json"
    try:
        # Obtener el body de la solicitud
        body = request.json

        # Leer los datos existentes en el archivo JSON
        with open(file_name, "r") as f:
            data = json.load(f)
        data["exp"] = body.get("exp", data.get("exp"))
        # Actualizar los datos con los valores del body
        data["strike_c"] = body.get("strike_c", data.get("strike_c"))
        data["strike_p"] = body.get("strike_p", data.get("strike_p"))

        data["call_close"] = body.get("call_close", data.get("call_close"))
        data["put_close"] = body.get("put_close", data.get("put_close"))

        # Guardar los datos actualizados de nuevo en el archivo
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

        # Devolver los datos actualizados como respuesta
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/broadCasting-sell", methods=["POST"])
def post_broadCasting_sell():
    file_name = "/usr/src/broadcasting.json"
    try:
        # Obtener el body de la solicitud
        body = request.json

        # Leer los datos existentes en el archivo JSON
        with open(file_name, "r") as f:
            data = json.load(f)

        # Actualizar los datos con los valores del body
        data["sell_tipo"] = body.get(
            "sell_tipo", data.get("sell_tipo")
        )
        data["sell_regla"] = body.get(
            "sell_regla", data.get("sell_regla")
        )
        data["sell"] = True

        # Guardar los datos actualizados de nuevo en el archivo
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

        # Devolver los datos actualizados como respuesta
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/broadCasting-sell-auto", methods=["POST"])
def post_broadCasting_sell_auto():
    file_name = "/usr/src/broadcasting.json"
    try:
        body = request.json
 
        # Leer los datos existentes en el archivo JSON
        with open(file_name, "r") as f:
            data = json.load(f)
 
 
        data["sell"] = True
        data["max_askbid_venta_abs"] = body.get(
            "max_askbid_venta_abs", data.get("max_askbid_venta_abs")
        )
 

        # Guardar los datos actualizados de nuevo en el archivo
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

        # Devolver los datos actualizados como respuesta
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/broadCasting-buy", methods=["POST"])
def post_broadCasting_buy():
    file_name = "/usr/src/broadcasting.json"
    try:
        # Obtener el body de la solicitud
        body = request.json

        # Leer los datos existentes en el archivo JSON
        with open(file_name, "r") as f:
            data = json.load(f)

        # Actualizar los datos con los valores del body
        data["buy_tipo"] = body.get(
            "buy_tipo", data.get("buy_tipo")
        )
        data["buy_regla"] = body.get(
            "buy_regla", data.get("buy_regla")
        )
        data["buy"] = True

        # Guardar los datos actualizados de nuevo en el archivo
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

        # Devolver los datos actualizados como respuesta
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-price", methods=["GET"])
def get_price():

    # Ejecutar el comando para reiniciar el contenedor
    try:
        file_name = "/usr/src/vars.json"

        # Leer los datos existentes en el archivo JSON
        with open(file_name, "r") as f:
            data = json.load(f)

            
 
            respuesta={
                "priceBuy": float(data["priceBuy"] )
       
            }
        return respuesta, 200
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}, 500

@app.route("/get-regla", methods=["GET"])
def get_regla():

    # Ejecutar el comando para reiniciar el contenedor
    try:
        file_name = "/usr/src/vars.json"

        # Leer los datos existentes en el archivo JSON
        with open(file_name, "r") as f:
            data = json.load(f)

            status = bool(data.get("call") or data.get("put"))
 
            respuesta={
                "sell_regla": data["sell_regla"],
                "rentabilidad": data["rentabilidad"],
                "status":status
       
            }
        return respuesta, 200
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
