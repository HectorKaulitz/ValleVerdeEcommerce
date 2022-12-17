from flask import make_response, render_template
from mercadopago import sdk

from MySqlConexion import MySQL
import mercadopago


class MercadoPagoMetodos:

    sdk = mercadopago.SDK("TEST-794122390765832-070210-e16cfe697e949af73e29dcc6981a9dd0-30600392")

    def CrearPreferencia(self, idVenta):
        obv = MySQL();

        if (obv.ExisteVenta(idVenta)):
            productosVenta = obv.ObtenerProductosVenta(idVenta);
            items = [];

            ind = 0
            for productoVenta in productosVenta:
                item = {
                    "title": productoVenta.nombre,
                    "quantity":  int(productoVenta.cantidadPedida),
                    "unit_price": float(productoVenta.precioCobrado),
                };
                items.append(item);
                ind = ind +1

            preference_data = {
                "items":items
            }

            preference_response = self.sdk.preference().create(preference_data)
            preference = preference_response["response"]

            obv.AsignarPreferenciaMercadoPago(idVenta, preference['id']);

            return preference;

        else:
            return None;

