import sqlite3

DB_NAME = "evre_leads.db"

def get_db():
    """Veritabanı bağlantısı oluşturur ve satırlara sütun adıyla erişim sağlar."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Veritabanı tablosunu (leads) oluşturur."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            email TEXT,
            mesaj TEXT,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def lead_ekle(isim, telefon, email="", mesaj=""):
    """Yeni bir müşteri adayı kaydeder (SQL Injection korumalı)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leads (isim, telefon, email, mesaj) VALUES (?, ?, ?, ?)",
        (isim, telefon, email, mesaj)
    )
    conn.commit()
    conn.close()

def tum_leadler():
    """Tüm müşteri adaylarını en yeniden eskiye doğru listeler."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, isim, telefon, email, mesaj, tarih FROM leads ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    # Verileri JSON formatına uygun sözlük yapısına çeviriyoruz
    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "isim": row["isim"],
            "telefon": row["telefon"],
            "email": row["email"],
            "mesaj": row["mesaj"],
            "tarih": row["tarih"]
        })
    return result
