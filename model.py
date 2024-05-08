from typing import List, Optional
from pydantic import BaseModel


class DetallePedido(BaseModel):
    idProducto: int
    nombreProducto: str
    cantidad: int
    precio: float
    subtotal: float
    costoEnvio: float
    subtotalEnvio: float


class Pago(BaseModel):
    idTarjeta: int
    noTarjeta: str
    fecha: str
    monto: float
    estatus: str


class Paqueteria(BaseModel):
    idPaqueteria: int
    nombre: str


class EnvioDetalle(BaseModel):
    idProducto: int
    nombreProducto: str
    cantidadEnviada: int
    cantidadRecibida: int
    comentario: str


class Envio(BaseModel):
    fechaSalida: str
    fechaEntPlan: str
    fechaRecepcion: str
    noGuia: str
    paqueteria: Paqueteria
    detalle: List[EnvioDetalle]


class Comprador(BaseModel):
    idComprador: int
    nombre: str


class Vendedor(BaseModel):
    idVendedor: int
    nombre: str


class PedidoDetalle(BaseModel):
    idPedido: int
    fechaRegistro: str
    fechaConfirmacion: Optional[str]
    fechaCierre: Optional[str]
    costosEnvio: float
    subtotal: float
    totalPagar: float
    estatus: str
    motivoCancelacion: Optional[str]
    valoracion: Optional[int]
    detalle: List[DetallePedido]
    pago: Pago
    comprador: Comprador
    vendedor: Vendedor
    envio: Envio


class ConsultarPedidosRespuesta(BaseModel):
    estatus: str
    mensaje: str
    pedidos: List[PedidoDetalle]