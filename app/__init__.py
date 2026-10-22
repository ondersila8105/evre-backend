from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from app.database import init_db
from app.routes import api_bp

def create_app():
    """Uygulama fabrikası (Application Factory)."""
    app = Flask(__name__)
    app.config.from_object(config)

    # CORS İzinleri (Wix Studio frontend bağlantısı için)
    CORS(app)

    # Veritabanını başlat
    init_db()

    # Rotaları (Blueprint) kaydet
    app.register_blueprint(api_bp, url_prefix='/api')

    # Kök dizin canlılık kontrolü (Healthcheck)
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"durum": "aktif", "mesaj": "EVRE Backend Servisi Çalışıyor"}), 200

    return app
