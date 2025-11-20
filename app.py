from flask import Flask
from flask_cors import CORS

from controllers.usuario_controller import usuario_bp
from controllers.reconocimiento_controller import reco_bp
from controllers.historial_controller import historial_bp
from controllers.mcp_controller import mcp_bp


app = Flask(__name__)
CORS(app, supports_credentials=True)

# 🔥 SOLO AFECTAMOS EL RECONOCIMIENTO
app.register_blueprint(usuario_bp)            # tus rutas siguen igual
app.register_blueprint(historial_bp)          # tus rutas siguen igual
app.register_blueprint(reco_bp, url_prefix="/api/reco")  # solo este cambia
app.register_blueprint(mcp_bp, url_prefix='/')

@app.route("/")
def index():
    return "API Reconocimiento Facial UP!"

if __name__ == "__main__":
    app.run(debug=True)

