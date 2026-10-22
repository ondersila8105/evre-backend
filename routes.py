from flask import Blueprint, request, jsonify
from ai_service import ai_service
from database import lead_ekle, tum_leadler

# API Rotaları için Blueprint oluşturuyoruz
api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Sağlık kontrolü uç noktası"""
    return jsonify({"status": "healthy", "message": "EVRE Backend çalışıyor!"}), 200

@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    """Wix üzerinden gelen kullanıcı mesajını alır ve AI yanıtı döndürür."""
    data = request.get_json() or {}
    mesaj = data.get('mesaj', '')
    gecmis = data.get('gecmis', [])

    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj alanı boş olamaz"}), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({"basari": True, "cevap": cevap}), 200
    except Exception as e:
        return jsonify({"basari": False, "hata": f"AI Servis Hatası: {str(e)}"}), 503

@api_bp.route('/leads', methods=['POST'])
def yeni_lead():
    """Wix formundan gelen yeni iletişim bilgilerini veritabanına kaydeder."""
    data = request.get_json() or {}
    isim = data.get('isim')
    telefon = data.get('telefon')
    email = data.get('email', '')  # <-- 1. YENİ: Wix'ten gelen email verisini çekiyoruz
    mesaj = data.get('mesaj', '')

    if not isim or not telefon:
        return jsonify({"basari": False, "hata": "İsim ve telefon alanları zorunludur"}), 400

    try:
        lead_ekle(isim, telefon, email, mesaj)  # <-- 2. YENİ: email parametresini ekledik
        return jsonify({"basari": True, "mesaj": "Müşteri adayı başarıyla kaydedildi"}), 201
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Veritabanı Hatası: {str(e)}"}), 500

@api_bp.route('/leads', methods=['GET'])
def lead_listele():
    """Yönetim paneli için tüm kayıtlı müşteri adaylarını getirir."""
    try:
        kayitlar = tum_leadler()
        return jsonify({"basari": True, "data": kayitlar}), 200
    except Exception as e:
        return jsonify({"basari": False, "hata": str(e)}), 500
