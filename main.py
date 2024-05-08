from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pymongo import MongoClient
from dao import ConexionMongoDB
from model import  ConsultarPedidosRespuesta


app = FastAPI()

conexion = ConexionMongoDB()

@app.get("/pedidos/comprador/{idComprador}", response_model=dict, name="Consultar Pedidos por ID de Comprador")
def consultar_pedidos_por_id_comprador(idComprador: int) -> dict:
    pedidos = list(conexion.pedidos.find({"idComprador": idComprador}))

    if not pedidos:
        raise HTTPException(status_code=404, detail="No se encontraron pedidos para el comprador especificado")

    detalles_pedidos = []

    for pedido in pedidos:
        vendedor = conexion.usuarios.find_one({"_id": pedido["idVendedor"]})

        comprador = conexion.usuarios.find_one({"_id": pedido["idComprador"]})

        detalles_pedido = {
            "idPedido": str(pedido["_id"]),
            "fechaRegistro": pedido["fechaRegistro"],
            "fechaConfirmacion": pedido.get("fechaConfirmacion"),
            "fechaCierre": pedido.get("fechaCierre"),
            "costosEnvio": pedido["costosEnvio"],
            "subtotal": pedido["subtotal"],
            "totalPagar": pedido["total"],
            "estatus": pedido["estatus"],
            "motivoCancelacion": pedido.get("motivoCancelacion"),
            "valoracion": pedido.get("valoracion"),
            "detalle": [],
            "pago": {
                "fecha": pedido["pago"]["fecha"],
                "monto": pedido["pago"]["monto"],
                "idTarjeta": pedido["pago"]["idTarjeta"],
                "estatus": pedido["pago"]["estatus"]
            },
            "envio": {
                "fechaSalida": pedido["envio"]["fechaSalida"],
                "fechaEntPlan": pedido["envio"]["fechaEntPlan"],
                "fechaRecepcion": pedido["envio"]["fechaRecepcion"],
                "noGuia": pedido["envio"]["noGuia"],
                "idPaqueteria": pedido["envio"]["idPaqueteria"],
                "detalle": pedido["envio"]["detalle"]
            },
            "vendedor": {
                "idVendedor": str(vendedor["_id"]),
                "nombre": vendedor["nombre"]
            },
            "comprador": {
                "idComprador": str(comprador["_id"]),
                "nombre": comprador["nombre"]
            }
        }

        for detalle_pedido in pedido["detalle"]:
            detalles_pedido["detalle"].append({
                "idProducto": str(detalle_pedido["idProducto"]),
                "cantidad": detalle_pedido["cantidad"],
                "precio": detalle_pedido["precio"],
                "subtotal": detalle_pedido["subtotal"],
                "costoEnvio": detalle_pedido["costoEnvio"],
                "subtotalEnvio": detalle_pedido["subtotalEnvio"]
            })

        detalles_pedidos.append(detalles_pedido)

    return {"estatus": pedido["estatus"], "mensaje": "Pedidos encontrados", "pedidos": detalles_pedidos}
