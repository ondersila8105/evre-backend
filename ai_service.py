import requests
from config import config

class AIService:
    """Yapay zeka çağrılarını yöneten servis katmanı."""

    def __init__(self):
        self.api_key = config.GROQ_API_KEY
        self.context = config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcının mesajına EVRE marka kişiliğiyle yanıt üretir."""
        if gecmis is None:
            gecmis = []

        # Groq API anahtarı girilmemişse veya demo modundaysa kibar bir yanıt döndürür
        if not self.api_key or self.api_key == "gsk_demo_key":
            return (
                "Merhaba! EVRE Sürdürülebilir Dönüşüm Asistanıyım. "
                "Şu an demo modundayım ama eski kıyafetlerinizi zanaatkar ellerle "
                "yeniden tasarlamak için buradayım! İletişim bilgilerinizi bırakırsanız size ulaşabiliriz."
            )

        # Groq / LLM API Formatı
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Sistem mesajı ve konuşma geçmişi
        messages = [{"role": "system", "content": self.context}]
        for g in gecmis:
            messages.append(g)
        messages.append({"role": "user", "content": mesaj})

        data = {
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "temperature": 0.7
        }

        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return "Şu an yanıt üretirken ufak bir bağlantı sorunu yaşıyorum, lütfen tekrar deneyin."
        except Exception as e:
            return f"Servis hatası oluştu: {str(e)}"

ai_service = AIService()