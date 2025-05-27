from datetime import datetime


def trade_counter(vars, params):

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


def wallet_config(app, params, vars):

    wallet_load(app, params)
    trade_counter(vars, params)
    money = wallet_cash(app, params)
    block_Trades(vars, money)


def wallet_load(app, params):

    # SELECCION DE
    app.num_cuenta = params.cuenta
    if app.num_cuenta == "-":
        unica_key = next(iter(app.cuentas))
        app.wallet = app.cuentas[unica_key]

    else:
        app.wallet = app.cuentas[app.num_cuenta]


def wallet_cash(app, params):
    if params.typeIB == "PAPER":
        money = float(app.wallet["TotalCashValue"])
    else:
        money = float(app.wallet["SettledCash"])
    return money


def block_Trades(vars, money):
    if len(vars.trades) < 3 or money >= 25000:
        vars.bloqueo = False
