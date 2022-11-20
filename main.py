from flask import Flask, render_template, Blueprint;
from flask_cors import CORS;

index = Blueprint('index', __name__, url_prefix='/index', template_folder='Vistas')


def create_app():
    app = Flask(__name__)
    # configurar referencias cruzadas
    # cuando se hacen peticiones de otros dominios
    CORS(app)
    app.config.from_object('configuracion.DevConfig')
    # registrar blueprints
    app.register_blueprint(index)
    # from .Productos import producto
    # app.register_blueprint(producto)
    return app


app = create_app()


# ruta principal
@app.route('/')
def index():
    return render_template('Index.html')


if __name__ == '__main__':
    print(__name__)
    app.run()
