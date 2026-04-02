# Bu faylni ishga tushirish uchun quyidagi kutubxonalarni o'rnating:
# pip install fastapi uvicorn pydantic

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import base64
import hashlib
import random
import string

app = FastAPI(title="DevMaster Studio API", description="Dasturchilar uchun yordamchi API")

# Brauzerdan so'rovlarni qabul qilish uchun CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ma'lumotlarni qabul qilish uchun modellar
class JSONData(BaseModel):
    raw_data: str

class TextData(BaseModel):
    text: str

class PasswordConfig(BaseModel):
    length: int = 12

@app.get("/")
def read_root():
    return {"status": "success", "message": "DevMaster API ishlamoqda!"}

@app.post("/api/format-json")
def format_json(data: JSONData):
    """Xom matnni qabul qilib, uni chiroyli JSON formatiga o'tkazadi"""
    try:
        parsed = json.loads(data.raw_data)
        formatted = json.dumps(parsed, indent=4)
        return {"status": "success", "formatted_json": formatted}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Noto'g'ri JSON formati: {str(e)}")

@app.post("/api/encode-base64")
def encode_base64(data: TextData):
    """Matnni Base64 ga o'giradi"""
    encoded = base64.b64encode(data.text.encode('utf-8')).decode('utf-8')
    return {"status": "success", "base64": encoded}

@app.post("/api/hash")
def generate_hash(data: TextData):
    """Matndan turli xesh (hash) larni yaratadi"""
    text_bytes = data.text.encode('utf-8')
    return {
        "md5": hashlib.md5(text_bytes).hexdigest(),
        "sha1": hashlib.sha1(text_bytes).hexdigest(),
        "sha256": hashlib.sha256(text_bytes).hexdigest()
    }

@app.post("/api/text-stats")
def get_text_stats(data: TextData):
    """Matn haqida statistik ma'lumotlarni qaytaradi"""
    return {
        "length": len(data.text),
        "word_count": len(data.text.split()),
        "reversed": data.text[::-1],
        "uppercase": data.text.upper(),
        "lowercase": data.text.lower()
    }

@app.post("/api/generate-password")
def generate_password(config: PasswordConfig):
    """Xavfsiz tasodifiy parol yaratadi"""
    if config.length < 4 or config.length > 64:
        raise HTTPException(status_code=400, detail="Parol uzunligi 4 va 64 oralig'ida bo'lishi kerak")
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(config.length))
    return {"status": "success", "password": password}

# Dasturni ishga tushirish: uvicorn app:app --reload