from ..config.mysqlconnection import connectToMySQL

class Producto:
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.precio = data['precio']
        self.descuento = data['descuento']
        self.imagen = data['imagen']
        self.stock_ideal = data['stock_ideal']
        self.stock_disponible = data['stock_disponible']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.marca_id = data['marca_id']
        self.categoria_id = data['categoria_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM productos WHERE stock_disponible > 0;"
        mysql = connectToMySQL('proyecto_grupal_bd')
        results = mysql.query_db(query)
        productos = []
        for row in results:
            productos.append(cls(row))
        return productos
    
    @classmethod
    def get_carrito(cls, ids):
        productos = []
        for id in ids:
            query = f"SELECT * FROM productos WHERE id = {id};"
            mysql = connectToMySQL('proyecto_grupal_bd')
            result = mysql.query_db(query)
            productos.append(cls(result[0]))
        return productos

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM productos WHERE id = %(id)s;"
        data = {
            "id" : id
        }
        mysql = connectToMySQL('proyecto_grupal_bd')
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return result[0]
        else:
            return None

    @classmethod
    def get_stock(cls, id):
        query = "SELECT stock_disponible FROM productos WHERE id = %(id)s;"
        data = {
            "id" : id
        }
        mysql = connectToMySQL('proyecto_grupal_bd')
        result = mysql.query_db(query,data)
        if len(result) > 0:
            return result[0]['stock_disponible']
        else:
            return None
        
    
    
    @classmethod
    def save(cls,data):
        query = """INSERT INTO productos (nombre, descripcion, precio, descuento, imagen, stock_ideal, stock_disponible, created_at, 
        updated_at, marca_id, categoria_id) VALUES (%(nombre)s, %(descripcion)s, %(precio)s, 0, %(imagen)s, 
        %(stock_ideal)s, %(stock_disponible)s, NOW(), NOW(), %(marca_id)s, %(categoria_id)s);"""
        return connectToMySQL('proyecto_grupal_bd').query_db(query,data)
    
    @classmethod
    def update_producto(cls, data):
        query = """UPDATE productos SET nombre = %(nombre)s, descripcion = %(descripcion)s, precio = %(precio)s, 
        stock_ideal = %(stock_ideal)s, stock_disponible = %(stock_disponible)s, updated_at = NOW(),
        marca_id = %(marca_id)s, descuento= %(descuento)s, categoria_id = %(categoria_id)s WHERE id = %(id)s"""
        return connectToMySQL('proyecto_grupal_bd').query_db(query, data)

    @classmethod
    def update_stock(cls, id):
        query = "UPDATE productos SET stock_disponible = stock_ideal WHERE id = %(id)s"
        data = {
            "id" : id
        }
        return connectToMySQL('proyecto_grupal_bd').query_db(query, data)
    
    @classmethod
    def update_venta(cls, data):
        query = "UPDATE productos SET stock_disponible = stock_disponible - %(cantidad)s WHERE id = %(id)s"
        return connectToMySQL('proyecto_grupal_bd').query_db(query, data)
    
    @staticmethod
    def obtener_id_siguiente():
        query = "SELECT MAX(id) as siguiente FROM productos;"
        mysql = connectToMySQL('proyecto_grupal_bd')
        result = mysql.query_db(query)
        if result[0]["siguiente"] != None:
            return result[0]['siguiente'] + 1
        else:
            return 1
        
    @staticmethod
    def obtener_precio(id):
        query = "SELECT precio, descuento FROM productos WHERE id = %(id)s;"
        data = {
            "id" : id
        }
        mysql = connectToMySQL('proyecto_grupal_bd')
        result = mysql.query_db(query,data)
        if result[0]["descuento"] == 0:
            return result[0]['precio']
        else:
            precio = result[0]['precio'] -  result[0]['precio'] * result[0]['descuento'] / 100
            return int(precio)



