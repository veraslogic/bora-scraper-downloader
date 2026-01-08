# 🇦🇷 BORA Scraper Downloader
**High-Resilience Automated Extraction PDFs for the Boletín Oficial de la República Argentina (BORA)**

<p align="center">
  <strong>
    <a href="#-español">🇪🇸 Español</a>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="#-english">🇺🇸 English</a>
  </strong>
</p>

---

<div id="español"></div>

## 🇪🇸 Documentación en Español

### 📋 Descripción General
El **BORA Scraper Downloader** es un motor de extracción de alta fidelidad diseñado para automatizar la descarga de documentos PDF del Boletín Oficial de la República Argentina (BORA). A diferencia de los descargadores simples, esta herramienta implementa técnicas de **simulación de comportamiento humano** para garantizar la continuidad del servicio frente a las medidas de seguridad del servidor oficial.

### 🛠️ Detalles Técnicos (Deep Dive)

Para garantizar la efectividad, el script opera bajo tres pilares de ingeniería:

#### 1. Session Priming (Inicialización de Contexto)
El servidor del BORA no permite descargas directas mediante URLs estáticas. El script replica el flujo de un navegador real:
1.  **Fase de Cebado**: Realiza una petición `GET` a la página de visualización del día para establecer las cookies de sesión y el estado del lado del servidor.
2.  **Petición de Carga**: Ejecuta una petición `POST` al endpoint de la API (`/pdf/download_section`) enviando exactamente los parámetros que espera el controlador JavaScript oficial.

#### 2. Resiliencia Anti-Bot
El sistema integra múltiples capas de protección para evitar bloqueos por IP o detección de actividad automatizada:
*   **Rotación de Identidad**: Utiliza un pool de `User-Agents` modernos, alternando la "huella digital" del navegador en cada sesión.
*   **Gestión de Pausas Heurísticas**: Implementa retardos aleatorios (`random.randint`) entre descargas, simulando el tiempo de lectura y navegación de un usuario humano.
*   **Refresco de Sesión**: El script destruye y recrea la sesión de red cada 5 días procesados, limpiando cookies acumuladas que podrían disparar alertas de seguridad.

#### 3. Integridad de Datos
*   **Verificación de Corrupción**: Detecta automáticamente si un archivo PDF se descargó de forma incompleta (archivos de <1KB) y permite reintentar la descarga de forma limpia.
*   **Estructura Jerárquica**: Organiza automáticamente las descargas por `/seccion/año/mes/`, facilitando la auditoría posterior.

### 🚀 Guía de Configuración

#### Requisitos
*   Python 3.8+ (Recomendado 3.10+)
*   Librería `requests` (`pip install requests`)

#### Configuración del Script
Edita la función `main()` en `descargador_bora.py` para definir tu objetivo:

```python
def main():
    # Rango de fechas: Desde el pasado hacia el presente
    fecha_inicio = datetime(2023, 1, 1) 
    fecha_fin = datetime(2024, 5, 31)
    
    # Seciones: 1 (Normativa), 2 (Sociedades), 3 (Contrataciones)
    descargar_dia_api(session, current_date, secciones=[2, 3])
```

---

<div id="english"></div>

## 🇺🇸 English Documentation

### 📋 Overview
The **BORA Scraper Downloader** is a high-fidelity extraction engine designed to automate the downloading of PDF documents from the Official Gazette of the Argentine Republic (BORA). Unlike basic downloaders, this tool implements **human behavior simulation** techniques to ensure service continuity against the official server's security measures.

### 🛠️ Technical Details (Deep Dive)

To ensure maximum effectiveness, the script is built on three engineering pillars:

#### 1. Session Priming (Context Initialization)
The BORA server does not allow direct downloads via static URLs. The script replicates the flow of a real browser:
1.  **Priming Phase**: It performs a `GET` request to the daily view page to set session cookies and server-side state.
2.  **Payload Dispatch**: It executes a `POST` request to the API endpoint (`/pdf/download_section`), sending the exact parameters expected by the official JavaScript controller.

#### 2. Anti-Bot Resilience
The system integrates multiple protection layers to avoid IP bans or automated activity detection:
*   **Identity Rotation**: Uses a pool of modern `User-Agents`, alternating the browser's "digital fingerprint" in each session.
*   **Heuristic Delay Management**: Implements randomized delays (`random.randint`) between downloads, simulating the reading and navigation time of a human user.
*   **Session Refreshing**: The script destroys and recreates the network session every 5 processed days, clearing accumulated cookies that could trigger security alerts.

#### 3. Data Integrity
*   **Corruption Detection**: Automatically detects if a PDF file was downloaded incompletely (files <1KB) and allows for a clean retry.
*   **Hierarchical Structure**: Automatically organizes downloads by `/section/year/month/`, facilitating future auditing.

### 🚀 Configuration Guide

#### Requirements
*   Python 3.8+ (Recommended 3.10+)
*   `requests` library (`pip install requests`)

#### Script Setup
Edit the `main()` function in `descargador_bora.py` to define your target:

```python
def main():
    # Date range: From past to present
    fecha_inicio = datetime(2023, 1, 1) 
    fecha_fin = datetime(2024, 5, 31)
    
    # Sections: 1 (Regulations), 2 (Corporations), 3 (Procurement)
    descargar_dia_api(session, current_date, secciones=[1, 2, 3])
```

---

## ⚠️ Disclaimer / Aviso Legal

**[ES]** Este software fue desarrollado exclusivamente para fines educativos y de investigación periodística. El uso responsable de los datos públicos y el respeto por los términos de servicio del sitio oficial es obligación del usuario.
**[EN]** This software is developed exclusively for educational and data journalism purposes. Responsible use of public data and respect for the official site's terms of service is the user's sole obligation.

---
**Developed by [VerasLogic](https://veraslogic.com)** 🦅
