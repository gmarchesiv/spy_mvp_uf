from datetime import datetime
 
def wallet_config(app, params, vars):

    #---------------------------------------------------
    '''
    -Realizamos los siguientes analisis y configuraciones:

        1) Guardamos el numero de cuenta por defecto o el
            configurado en el archivo .env .
        2) Realizamos un conteo de las transacciones. 
        3) Extraemos la informacion del cash del clientes,
            este puede ser cash paper o live.
        4) Se Bloquea el trading por la cantidad de cash o 
            por numero de transacciones hechas .

    '''
    #---------------------------------------------------

    wallet_load(app, params)
    trade_counter(vars, params)
    money = wallet_cash(app, params)
    block_Trades(vars, money)


def wallet_load(app, params):
    #---------------------------------------------------
    '''
    Extrae la informacion de las billeteras del cliente.
    '''
    #---------------------------------------------------

    # SELECCION DE
    app.num_cuenta = params.cuenta
    if app.num_cuenta == "-":
        unica_key = next(iter(app.cuentas))
        app.wallet = app.cuentas[unica_key]

    else:
        app.wallet = app.cuentas[app.num_cuenta]

def trade_counter(vars, params):
    #---------------------------------------------------
    '''
    Hace un conteo de Trades , y al cambio de dia va 
    eliminando un trade cada 5 dias.
    '''
    #---------------------------------------------------

    now = datetime.now(params.zone).strftime("%Y-%m-%d")

    # Verificar y actualizar la fecha
    if vars.fecha != now:
        vars.fecha = now
        # Actualizar la lista de compras
        for i in range(len(vars.trades)):
            if vars.trades[i] > 0:
                vars.trades[i] -= 1

    # Eliminar todos los elementos que sean 0
    vars.trades = [x for x in vars.trades if x != 0]

def wallet_cash(app, params):
    if params.typeIB == "PAPER":
        money = float(app.wallet["TotalCashValue"])
    else:
        money = float(app.wallet["SettledCash"])
    return money


def block_Trades(vars, money):
    #---------------------------------------------------
    '''
    Bloqueo por muchos Trades realizados o por cash
    insuficiente.
    '''
    #---------------------------------------------------
    if len(vars.trades) < 3 or money >= 25000:
        vars.bloqueo = False
