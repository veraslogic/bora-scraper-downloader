# 🇦🇷 BORA Scraper Downloader

<p align="center">
  <strong>
    <a href="#-documentación-en-español">🇪🇸 Español</a>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="#-english-documentation">🇺🇸 English</a>
  </strong>
</p>

---

<div id="es"></div>

## 🇪🇸 Documentación en Español

**Descargador de alta resiliencia para el Boletín Oficial de la República Argentina (BORA).**

Este script permite descargar masivamente los documentos (PDFs) del Boletín Oficial, gestionando automáticamente las sesiones y asegurando la integridad de las descargas. Diseñado para investigadores, periodistas de datos y desarrolladores que necesitan construir bases de datos históricas.

### 🔥 Características Clave
- **🕵️‍♂️ Gestión Robusta de Sesiones**: Implementa rotación de Identidad Digital (`User-Agent`) para maximizar la compatibilidad con el servidor.
- **🔄 Session Priming**: Inicializa cookies de sesión válidas visitando la página como un navegador real antes de solicitar el archivo, garantizando la descarga correcta.
- **🛡️ Tolerancia a Fallos**: Sistema de reintentos automáticos para manejar intermitencias de la API oficial o micro-cortes de red.
- **⚡ 100% Python Puro**: Script independiente sin bases de datos ni dependencias externas complejas.

### 🚀 Guía de Uso Rápida

#### 1. Instalación
Solo necesitas Python 3 y la librería `requests`:

```bash
pip install requests
```

#### 2. Configuración
Abre el archivo `descargador_bora.py` y ve al final, a la función `main()`. Ahí defines qué rango de fechas y qué secciones descargar:

```python
def main():
    # Ejemplo: Descargar Enero 2024 completo
    fecha_inicio = datetime(2024, 1, 1) 
    fecha_fin = datetime(2024, 1, 31)
```

> **Importante:** Puedes elegir qué secciones descargar (Licitaciones, Sociedades, Normativa) modificando el parámetro `secciones=[2]` en el script.

#### 3. Ejecución
```bash
python descargador_bora.py
```
Los archivos se guardarán ordenados en: `descargas_bora/seccion_X/año/mes/`.

---

<div id="en"></div>

## 🇺🇸 English Documentation

**Robust high-availability downloader for the Official Gazette of the Argentine Republic (BORA).**

This script allows for bulk downloading of PDF documents from the Official Gazette, automatically managing sessions and ensuring download integrity. Designed for researchers, data journalists, and developers building historical datasets.

### 🔥 Key Features
- **🕵️‍♂️ Robust Session Management**: Implements Digital Identity rotation (`User-Agent`) to maximize server compatibility and avoid stalls.
- **🔄 Session Priming**: Initializes valid session cookies by visiting the target page like a real browser before requesting the file, ensuring successful delivery.
- **🛡️ Fault Tolerance**: Built-in automatic retries to handle official API intermittency or network hiccups gracefully.
- **⚡ Pure Python**: Standalone tool. No databases or complex external dependencies required.

### 🚀 Quick Start Guide

#### 1. Installation
You only need Python 3 and `requests`:

```bash
pip install requests
```

#### 2. Configuration
Open `descargador_bora.py` and find the `main()` function at the bottom. Set your desired date range and sections:

```python
def main():
    # Example: Download all January 2024
    fecha_inicio = datetime(2024, 1, 1) 
    fecha_fin = datetime(2024, 1, 31)
```

> **Important:** You can choose which sections to download (Procurement, Corporations, Regulations) by modifying the `secciones=[2]` parameter in the script.

#### 3. Execution
```bash
python descargador_bora.py
```
Files will be saved automatically in: `descargas_bora/seccion_X/year/month/`.

---

## ⚠️ Disclaimer/Aviso Legal

**[ES]** Este software fue desarrollado exclusivamente para fines educativos y de investigación periodística. El uso responsable de los datos públicos es obligación del usuario.
**[EN]** This software is developed exclusively for educational and data journalism purposes. Responsible use of public data is the user's sole obligation.
