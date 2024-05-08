from pymongo import MongoClient

class ConexionMongoDB:
    def __init__(self):
        self.cliente = MongoClient()
        self.bd = self.cliente.ShopiteszREST
        self.envios = self.bd.envios
        self.paqueterias = self.bd.paqueterias
        self.pedidos = self.bd.pedidos
        self.usuarios = self.bd.usuarios
        self.productos = self.bd.productos
        self.categorias = self.bd.categorias

    def cerrar(self):
        self.cliente.close()