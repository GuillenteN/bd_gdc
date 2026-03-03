# PR0304: API de YouTube

```python
import requests
import pandas as pd
import math
import re

# CONFIGURACIÓN
API_KEY = 'AIzaSyCwnOZYfCeChUgu188Raxb44K18hwBNrRo'
CHANNEL_ID = 'UCvnNkJsbONVhdXuHY_LpsdA' 
BASE_URL = 'https://www.googleapis.com/youtube/v3'


# FUNCIONES DE INGESTA
# --------------------
def get_uploads_playlist_id(channel_id):
    """Paso 1: Obtener el ID de la lista de reproducción 'Uploads' del canal"""
    url = f"{BASE_URL}/channels?part=contentDetails&id={channel_id}&key={API_KEY}"
    response = requests.get(url).json()
    
    try:
        # TODO: Extrae el id del playlist (está en la clave uploads)
        playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        return playlist_id
    except KeyError:
        print("Error al obtener la playlist. Revisa el ID del canal y tu API Key.")
        return None

def get_all_video_ids(playlist_id):
    """Paso 2: Obtener todos los IDs de los videos de la playlist"""
    video_ids = []
    next_page_token = None
    
    print("Extrayendo IDs de videos...")
    
    while True:
        url = f"{BASE_URL}/playlistItems?part=contentDetails&maxResults=50&playlistId={playlist_id}&key={API_KEY}"
        
        # TODO: Si existe un next_page_token, añádelo a la URL (&pageToken=...)
        if next_page_token:
            url += f"&pageToken={next_page_token}"
            
        response = requests.get(url).json()
        
        for item in response.get('items', []):
            video_ids.append(item['contentDetails']['videoId'])
            
        # TODO: Lógica de paginación. 
        # Busca 'nextPageToken' en la respuesta. Si existe, actualiza la variable. Si no, rompe el bucle.
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
        
    print(f"Total de videos encontrados: {len(video_ids)}")
    return video_ids


def get_video_details(video_ids):
    """Paso 3: Obtener estadísticas de los videos en lotes de 50"""
    all_video_data = []
    
    # TODO: Agrupa la lista video_ids en sub-listas de máximo 50 elementos.
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        
        ids_string = ','.join(chunk)
        url = f"{BASE_URL}/videos?part=snippet,statistics,contentDetails&id={ids_string}&key={API_KEY}"
        
        response = requests.get(url).json()
        
        for video in response.get('items', []):
            
            video_data = {
                "video_id": video.get("id"),
                "title": video.get("snippet", {}).get("title"),
                "published_at": video.get("snippet", {}).get("publishedAt"),
                "views": int(video.get("statistics", {}).get("viewCount", 0)),
                "likes": int(video.get("statistics", {}).get("likeCount", 0)),
                "comments": int(video.get("statistics", {}).get("commentCount", 0)),
                "duration": video.get("contentDetails", {}).get("duration")
            }
            
            all_video_data.append(video_data)
            
    return all_video_data

def parse_duration(iso_duration):
    """Paso 4: Transformar la duración ISO 8601 (ej: PT1H2M10S) a segundos totales"""
    # TODO: Convierte la duración de ISO8601 a segundos
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, iso_duration)
    
    if not match:
        return 0  # Si no coincide, devolvemos 0 segundos
    
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    
    total_seconds = hours * 3600 + minutes * 60 + seconds
    
    return total_seconds


# EJECUCIÓN PRINCIPAL (PIPELINE)
# ------------------------------
if __name__ == "__main__":
    print("Iniciando pipeline de ingesta...")
    
    uploads_id = get_uploads_playlist_id(CHANNEL_ID)
    
    if uploads_id:
        lista_ids = get_all_video_ids(uploads_id)
        datos_completos = get_video_details(lista_ids)
        
        df = pd.DataFrame(datos_completos)
        
        # Limpieza básica
        df['published_at'] = pd.to_datetime(df['published_at'])  # Aseguramos que sea datetime
        df['duration_seconds'] = df['duration'].apply(parse_duration)  # Convertimos duración
        
        print("\nMuestra de los datos extraídos:")
        print(df.head())
        
        # 5. Guardar en un formato analítico
        df.to_parquet('dataset_canal_youtube.parquet', index=False)
        
        print("\nPipeline finalizado. Revisa tus archivos locales.")
```