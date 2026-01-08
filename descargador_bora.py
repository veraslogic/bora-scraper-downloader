import os
import requests
import time
import hashlib
import logging
import base64
import random
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
BASE_DIR = "descargas_bora"

# Configurar Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("BoraDownloader")

# --- UTILIDADES ---

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def calculate_content_hash(content_bytes):
    """Calcula SHA-256 debytes en memoria."""
    return hashlib.sha256(content_bytes).hexdigest()

def get_seccion_slug(seccion_id):
    slugs = {1: "primera", 2: "segunda", 3: "tercera", 4: "cuarta"}
    return slugs.get(seccion_id)


def get_robust_session():
    """Crea una sesión nueva con User-Agent rotativo para maximizar compatibilidad."""
    session = requests.Session()
    # Lista de UAs modernos para compatibilidad
    uas = [
        f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/{random.randint(115, 122)}.0.0.0 Safari/537.36"
    ]
    ua = random.choice(uas)
    
    session.headers.update({
        "User-Agent": ua,
        "Referer": "https://www.boletinoficial.gob.ar/",
        "Origin": "https://www.boletinoficial.gob.ar",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    })
    # Warmup
    try:
        session.get("https://www.boletinoficial.gob.ar/", timeout=10)
    except: pass
    return session

def get_page_url(seccion_id, fecha_clean):
    """URL de la página de la sección (HTML)."""
    slug = get_seccion_slug(seccion_id)
    return f"https://www.boletinoficial.gob.ar/seccion/{slug}/{fecha_clean}"

def descargar_dia_api(session, fecha_obj, secciones=[2, 3]):
    """
    Descarga usando POST API con Session Priming.
    1. GET /seccion/{slug}/{yyyymmdd} -> Inicializa cookies de sesión.
    2. POST /pdf/download_section {nombreSeccion: ...} -> Solicita el PDF.
    """
    fecha_clean = fecha_obj.strftime("%Y%m%d")
    fecha_iso = fecha_obj.strftime("%Y-%m-%d")
    year = fecha_obj.strftime("%Y")
    month = fecha_obj.strftime("%m")
    
    api_url = "https://www.boletinoficial.gob.ar/pdf/download_section"
    
    for sec_id in secciones:
        slug = get_seccion_slug(sec_id)
        if not slug: continue
        
        save_dir = os.path.join(BASE_DIR, f"seccion_{sec_id}", year, month)
        ensure_dir(save_dir)
        filename = f"BORA_SEC{sec_id}_{fecha_clean}.pdf"
        filepath = os.path.join(save_dir, filename)
        
        # Check local simple
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            logger.info(f"⏭️ Cache Local (Skip): {filename}")
            continue
            
        # 1. PRIME SESSION (Visitar la página del día)
        page_url = get_page_url(sec_id, fecha_clean)
        # logger.info(f"🌍 Priming Session: {page_url}")
        try:
            session.get(page_url, timeout=30)
            time.sleep(random.randint(2, 5)) # Pausa de cortesía
        except Exception as e:
            logger.warning(f"⚠️ Error priming session: {e}")
            continue

        logger.info(f"⬇️ API POST Sección {sec_id} ({slug}) para {fecha_iso}...")
        
        # El JS oficial NO manda fecha, solo sección. Confía en el estado de la sesión.
        payload = {
            "nombreSeccion": slug
        }
        
        try:
            r = session.post(api_url, data=payload, timeout=90)
            
            if r.status_code == 200:
                try:
                    data = r.json()
                    pdf_b64 = data.get("pdfBase64")
                    
                    if pdf_b64:
                        pdf_bytes = base64.b64decode(pdf_b64)
                        
                        file_size_kb = len(pdf_bytes) // 1024
                        logger.info(f"✅ Descargado: {filename} ({file_size_kb} KB)")
                        
                        with open(filepath, "wb") as f:
                            f.write(pdf_bytes)
                            
                        logger.info(f"💾 Guardado localmente: {os.path.basename(filepath)}")
                        
                        # Pausa Respectful
                        sleep_time = random.randint(15, 30)
                        logger.info(f"💤 Pausa de cortesía {sleep_time}s...")
                        time.sleep(sleep_time)

                    else:
                        logger.warning(f"⚠️ {fecha_iso}: JSON sin PDF (¿Feriado?)")
                except:
                     logger.warning(f"⚠️ {fecha_iso}: Error parseando JSON")
            else:
                logger.warning(f"⚠️ {fecha_iso}: HTTP {r.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error red: {e}")
            time.sleep(10)
            
    return True

def clean_corrupted_files():
    """Elimina archivos pequeños (< 2KB) que suelen ser errores HTML."""
    count = 0
    for root, _, files in os.walk(BASE_DIR):
        for f in files:
            path = os.path.join(root, f)
            if os.path.getsize(path) < 2048: # 2KB
                os.remove(path)
                count += 1
    if count: logger.info(f"🧹 Se eliminaron {count} archivos corruptos/HTML.")

def main():
    # Configuración: Sección 2, desde Mayo 2024 hasta Enero 2023
    fecha_inicio = datetime(2023, 1, 1)
    fecha_fin = datetime(2024, 5, 31)
    
    logger.info(f"🚀 Iniciando Downloader SECCIÓN 2: {fecha_inicio.date()} → {fecha_fin.date()}")
    clean_corrupted_files()
    
    session = get_robust_session()
    
    requests_count = 0
    current_date = fecha_fin
    
    while current_date >= fecha_inicio:
        # Skip domingos Y sábados (a veces no hay)
        if current_date.weekday() >= 5: 
            current_date -= timedelta(days=1)
            continue
            
        descargar_dia_api(session, current_date, secciones=[2])
        
        current_date -= timedelta(days=1)
        requests_count += 1
        
        # Rotar sesión cada 5 días procesados
        if requests_count % 5 == 0:
            logger.info("🔄 Gestionando nueva sesión...")
            session = get_robust_session()
            time.sleep(random.randint(10, 20))

if __name__ == "__main__":
    ensure_dir(BASE_DIR)
    main()
