# ====================
#  - Librerias -
# ====================

from datetime import datetime
import time
import holidays
from datetime import time as dt_time

from functions.logs import printStamp
from functions.notifications import sendDisconnection


# ====================
#  - Funciones -
# ====================
 


def es_fecha_especial(fecha):
    
    #---------------------------------------------------
    '''
    Analiza los feriados programados y devuelve si es 
    Trading de medio dia , feriado o dia normal.
    '''
    #---------------------------------------------------

    # Fechas específicas
    fechas_especiales = {
        "4 de julio": (7, 4),
        "Thanksgiving": "thanksgiving",
        "Navidad": (12, 25),
        "Año Nuevo": (1, 1),
        "24 de diciembre": (12, 24),
        "3 de julio": (7, 3),
        "Martin Luther King Day": "mlk_day" ,
        "Día de los Presidentes": "presidents_day"
    }

    # Desglose de mes y día de la fecha proporcionada
    mes, dia = fecha.month, fecha.day

    # Verificar 4 de julio, Navidad, Año Nuevo
    if (mes, dia) == fechas_especiales["4 de julio"]:
        return "4 de julio", False
    elif (mes, dia) == fechas_especiales["Navidad"]:
        return "Navidad", False
    elif (mes, dia) == fechas_especiales["Año Nuevo"]:
        return "Año Nuevo", False
    elif (mes, dia) == fechas_especiales["24 de diciembre"]:
        return "Visperas de Navidad", True
    elif (mes, dia) == fechas_especiales["3 de julio"]:
        return "3 de julio", True  # Nueva condición para 3 de julio

    if mes == 1:
        primer_dia_enero = datetime(fecha.year, 1, 1)
        dia_de_la_semana = primer_dia_enero.weekday()
        # Calcular el primer lunes de enero
        primer_lunes = 1 + (7 - dia_de_la_semana) % 7
        tercer_lunes = primer_lunes + 14
        if dia == tercer_lunes:
            return "Martin Luther King Day", False

    # Verificar Día de los Presidentes (tercer lunes de febrero)
    if mes == 2:
        primer_dia_febrero = datetime(fecha.year, 2, 1)
        dia_de_la_semana = primer_dia_febrero.weekday()
        primer_lunes = 1 + (7 - dia_de_la_semana) % 7
        tercer_lunes = primer_lunes + 14
        if dia == tercer_lunes:
            return "Día de los Presidentes", False
        
    # Verificar Día de Acción de Gracias (cuarto jueves de noviembre)
    if mes == 11:
        # Calcular el cuarto jueves de noviembre
        primer_dia_noviembre = datetime(fecha.year, 11, 1)
        dia_de_la_semana = primer_dia_noviembre.weekday()
        # Calcular el primer jueves de noviembre
        primer_jueves = 1 + (3 - dia_de_la_semana) % 7
        cuarto_jueves = primer_jueves + 21
        if dia == cuarto_jueves:
            return "Thanksgiving", False
        # Verificar día después de Thanksgiving
        elif dia == cuarto_jueves + 1:
            return "Post Thanksgiving", True

    # Si no coincide con ninguna fecha especial
    return None, None


def isTradingDay(params):

    # ====================
    #  - Feriados -
    # ====================

    #---------------------------------------------------
    '''
        Revisamos si es Feriado antes de comenzar 
        la rutina, si es el caso no continuara ,
        en caso sea trading day parcial va cambiar 
        el parametro de FD a medio dia.
    '''
    #---------------------------------------------------
    now = datetime.now(params.zone)

    # Llamar a la función con la fecha actual
    resultado, accion = es_fecha_especial(now)

    if resultado:
        if accion:
            printStamp(f"{resultado} - HALF TRADING - ")
            params.fd = dt_time(12, 00)
            params.fin_rutina = dt_time(12, 5)
            return False
        printStamp(f"{resultado} - FERIADO - ")
        return True
    else:
        printStamp(f" - NORMAL TRADING - ")
        return False


def countdown(zone,app,vars,params):

    #---------------------------------------------------
    '''
    Genera una cuenta regresiva (minutos)
    antes de entrar al Trading Day.
    '''
    #---------------------------------------------------
    # ====================
    # - Cuenta Regresiva -
    # ====================

    now = datetime.now(zone)
    start_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
    end_time = now.replace(hour=16, minute=0, second=0, microsecond=0)

    minuto_ante = 99

    # Bucle de cuenta regresiva

    while True:

        now = datetime.now(zone)

        if now >= start_time and now <= end_time:
            break

        time_diff = start_time - now
        minutes_left = time_diff.total_seconds() // 60

        if minuto_ante != now.minute:
            if (int(minutes_left + 1)) == 1:
                printStamp(f"Faltan {int(minutes_left+1)} minuto para comenzar.")
            else:
                printStamp(f"Faltan {int(minutes_left+1)} minutos para comenzar.")
            minuto_ante = now.minute



        if app.alerta==True and vars.flag_alerta==False:
            sendDisconnection(params )
            vars.flag_alerta=True
        if vars.flag_alerta and app.alerta==False :
            vars.flag_alerta=False


        time.sleep(1)
