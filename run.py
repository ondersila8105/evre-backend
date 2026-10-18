from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from database import init_db
from routes import api_bp

def create_app():
    """Uygulama fabrikası (Application Factory)."""
    app = Flask(__name__)
    app.config.from_object(config)

    # CORS İzinleri (Wix Studio frontend bağlantısı için)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Veritabanını başlat
    init_db()

    # Rotaları (Blueprint) kaydet
    app.register_blueprint(api_bp, url_prefix='/api')

    # Canlılık kontrolü (Healthcheck)
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"durum": "aktif", "mesaj": "EVRE Backend Servisi Çalışıyor"}), 200

    return app

app = create_app()

if __name__ == '__main__':
    print("🚀 EVRE Backend Sunucusu Başlatılıyor...")
    app.run(host='0.0.0.0', port=5000, debug=True)