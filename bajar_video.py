import yt_dlp

def descargar_video(url):
    # 1. Configuración de la descarga
    opciones = {
        'format': 'best',  # Descargar la mejor calidad disponible
        'outtmpl': '%(title)s.%(ext)s',  # Nombre del archivo final (Titulo.extensión)
    }

    # 2. El Bloque de "Intento" (Manejo de Errores)
    try:
        print(f"🦅 Iniciando descarga de: {url}...")
        
        # 3. Llamar al motor de descarga con nuestras opciones
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
            
        print("✅ ¡Misión Cumplida! Video descargado exitosamente.")

    except Exception as e:
        print(f"❌ Error en la misión: {e}")

# 4. Zona de Ejecución
if __name__ == "__main__":
    link = input("Pegue el link del video aquí, Comandante: ")
    descargar_video(link)
