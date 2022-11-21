from flask import Flask, render_template, Blueprint;
from flask_cors import CORS;

index = Blueprint('index', __name__, url_prefix='/index', template_folder='Vistas')
# producto = Blueprint('producto', __name__, url_prefix='/producto', template_folder='Vistas')


def create_app():
    app = Flask(__name__)
    # configurar referencias cruzadas
    # cuando se hacen peticiones de otros dominios
    CORS(app)
    app.config.from_object('configuracion.DevConfig')
    # registrar blueprints
    app.register_blueprint(index)
    # app.register_blueprint(producto)
    # from .Productos import producto
    # app.register_blueprint(producto)
    return app


app = create_app()


# ruta principal
@app.route('/')
def index():
    return render_template('Index.html')\


@app.route('/productos')
def productos():
    return render_template('productos.html')\

@app.route('/historialCompras')
def historialCompras():
    return render_template('historialCompras.html')

@app.route('/producto')
def producto():
    return render_template('Producto.html')

@app.route('/comentarios')
def comentarios():
    return render_template('comentarios.html')

@app.route('/carritoUsuario')
def carrito():
    return render_template('carritoUsuario.html', EsParaFavoritos=False)

@app.route('/favorito')
def favorito():
    return render_template('carritoUsuario.html', EsParaFavoritos=True)

@app.route('/procesoCompra')
def procesoCompra():
    return render_template('procesoCompra.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')



if __name__ == '__main__':
    print(__name__)
    app.run()
