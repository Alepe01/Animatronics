import os
import random
from base_manager import BaseManager
from response_handler import ResponseHandler
from audio_manager import AudioManager

class CantanteManager(BaseManager, AudioManager):
    """Manager cantante refactorizado usando BaseManager y AudioManager"""
    
    def __init__(self, music_folder="musica", arduino_controller=None, cantante_file="cantante.json"):
        BaseManager.__init__(self, cantante_file)
        AudioManager.__init__(self, arduino_controller)
        
        self.music_folder = music_folder
        self.playlist = []
        self.current_song = None
        
        self.load_music_files()
        print(f"🎵 Cantante Manager inicializado con {len(self.playlist)} canciones")
    
    def _create_default_data(self):
        """Crear datos por defecto para cantante"""
        self.data = {
            "favoritas": [],
            "reproducciones": {},
            "configuracion": {
                "volumen": 80,
                "modo_aleatorio": True,
                "repetir": False
            },
            "estadisticas": {
                "canciones_reproducidas": 0,
                "tiempo_total_reproduccion": 0
            },
            "version": "2.0"
        }
    
    def load_music_files(self):
        """Cargar archivos de música desde la carpeta"""
        try:
            if not os.path.exists(self.music_folder):
                os.makedirs(self.music_folder)
                self._create_sample_playlist()
                return
            
            supported_formats = ['.mp3', '.wav', '.ogg']
            self.playlist = []
            
            for filename in os.listdir(self.music_folder):
                if any(filename.lower().endswith(fmt) for fmt in supported_formats):
                    full_path = os.path.join(self.music_folder, filename)
                    song_name = os.path.splitext(filename)[0]
                    self.playlist.append({
                        'nombre': song_name,
                        'archivo': full_path,
                        'formato': os.path.splitext(filename)[1],
                        'reproducciones': self.get_counter("reproducciones", song_name)
                    })
            
            print(f"🎵 Cargadas {len(self.playlist)} canciones")
            for song in self.playlist[:5]:  # Mostrar solo las primeras 5
                print(f"  - {song['nombre']}{song['formato']}")
            
            if len(self.playlist) > 5:
                print(f"  ... y {len(self.playlist) - 5} más")
        
        except Exception as e:
            print(f"❌ Error cargando música: {e}")
            self.playlist = []
    
    def _create_sample_playlist(self):
        """Crear archivo de instrucciones para playlist"""
        sample_info = """
# INSTRUCCIONES PARA AÑADIR MÚSICA #

1. Coloca tus archivos MP3, WAV u OGG en esta carpeta
2. Formatos soportados: .mp3, .wav, .ogg
3. El nombre del archivo será el título de la canción
4. Ejemplos de nombres:
   - "Cumpleanos_Feliz.mp3"
   - "Las_Mananitas.wav"
   - "Payaso_Loco.mp3"

Canciones sugeridas para Poncho:
- Canciones de cumpleaños
- Música de circo/payasos  
- Canciones populares mexicanas
- Música divertida o cómica
- Canciones infantiles

NOTA: Asegúrate de que tienes derechos para usar la música
"""
        try:
            readme_path = os.path.join(self.music_folder, "LEEME.txt")
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(sample_info)
            print(f"📄 Archivo de instrucciones creado: {readme_path}")
        except Exception as e:
            print(f"❌ Error creando instrucciones: {e}")
    
    def get_song_by_name(self, song_name):
        """Buscar canción por nombre usando ResponseHandler"""
        song_name_clean = ResponseHandler.clean_text(song_name).lower()
        
        for song in self.playlist:
            song_name_lower = ResponseHandler.clean_text(song['nombre']).lower()
            if song_name_clean in song_name_lower or ResponseHandler.get_similarity(song_name_clean, song_name_lower) > 0.7:
                return song
        return None
    
    def play_song(self, song=None):
        """Reproducir canción específica o aleatoria"""
        if not self.playlist:
            return "¡No tengo canciones para cantar! ¡Soy un payaso sin repertorio!"
        
        # Detener canción actual si está reproduciendo
        if self.is_audio_playing():
            self.stop_audio()
        
        # Seleccionar canción
        if song is None:
            if self.data.get("configuracion", {}).get("modo_aleatorio", True):
                song = random.choice(self.playlist)
            else:
                song = self.playlist[0]
        
        self.current_song = song
        
        # Incrementar contador de reproducciones
        self.increment_counter("reproducciones", song['nombre'])
        self.increment_counter("estadisticas", "canciones_reproducidas")
        
        # Reproducir usando AudioManager
        self.play_audio_file(song['archivo'], self._song_callback)
        
        return f"🎵 Ahora cantando: {song['nombre']}"
    
    def _song_callback(self, event):
        """Callback para eventos de reproducción"""
        if event == 'start':
            print(f"🎵 Iniciando: {self.current_song['nombre']}")
        elif event == 'stop':
            print(f"🎵 Terminada: {self.current_song['nombre'] if self.current_song else 'canción'}")
            self.current_song = None
    
    def handle_song_request(self, comment):
        """Manejar peticiones de canciones usando ResponseHandler"""
        comment_clean = ResponseHandler.clean_text(comment)
        
        # Palabras clave para peticiones
        request_keywords = [
            "canta", "canción", "cancion", "música", "musica", 
            "toca", "interpreta", "tema", "play", "reproduce"
        ]
        
        # Verificar si es una petición usando ResponseHandler
        if not ResponseHandler.detect_keywords(comment_clean, request_keywords):
            return None
        
        # Buscar canción específica en el comentario
        song_found = self.get_song_by_name(comment_clean)
        if song_found:
            return self.play_song(song_found)
        
        # Buscar por palabras clave en nombres de canciones
        for song in self.playlist:
            song_words = ResponseHandler.clean_text(song['nombre']).lower().split('_')
            for word in song_words:
                if len(word) > 2 and word in comment_clean.lower():
                    return self.play_song(song)
        
        # Si no encuentra canción específica, tocar aleatoria
        return self.play_song()
    
    def stop_song(self):
        """Detener canción usando AudioManager"""
        if self.is_audio_playing():
            self.stop_audio()
            self.current_song = None
            return "¡Canción detenida! ¡Espero que no haya sido por mi voz!"
        return "¡No estoy cantando nada!"
    
    def pause_song(self):
        """Pausar canción usando AudioManager"""
        if self.pause_audio():
            return "⏸️ Canción pausada - ¡Momento de descanso!"
        return "¡No hay nada que pausar!"
    
    def resume_song(self):
        """Reanudar canción usando AudioManager"""
        if self.resume_audio():
            return "▶️ ¡Continuamos con el espectáculo!"
        return "¡No hay nada que reanudar!"
    
    def get_playlist_info(self):
        """Obtener información de la playlist"""
        if not self.playlist:
            return "¡Mi playlist está más vacía que mi alma de payaso!"
        
        info = f"🎵 Playlist de Poncho ({len(self.playlist)} canciones):\n\n"
        
        # Mostrar canciones con sus reproducciones
        sorted_playlist = sorted(self.playlist, key=lambda x: x['reproducciones'], reverse=True)
        
        for i, song in enumerate(sorted_playlist[:10], 1):  # Top 10
            marker = "▶️" if song == self.current_song else "🎵"
            reproducciones = song['reproducciones']
            info += f"{marker} {i}. {song['nombre']} ({reproducciones} reproducciones)\n"
        
        if len(self.playlist) > 10:
            info += f"\n... y {len(self.playlist) - 10} canciones más"
        
        return info
    
    def get_current_song_info(self):
        """Información de la canción actual"""
        if self.current_song and self.is_audio_playing():
            reproducciones = self.get_counter("reproducciones", self.current_song['nombre'])
            return f"🎵 Cantando: {self.current_song['nombre']} (Reproducida {reproducciones} veces)"
        return "🔇 No estoy cantando nada ahora mismo"
    
    def add_to_favorites(self, song_name):
        """Agregar canción a favoritas"""
        song = self.get_song_by_name(song_name)
        if not song:
            return f"No encontré la canción '{song_name}' en mi playlist"
        
        favoritas = self.data.get("favoritas", [])
        if song['nombre'] not in favoritas:
            self.add_item_to_list("favoritas", song['nombre'])
            return f"✅ '{song['nombre']}' agregada a favoritas"
        else:
            return f"'{song['nombre']}' ya está en favoritas"
    
    def play_favorite(self):
        """Reproducir canción favorita aleatoria"""
        favoritas = self.data.get("favoritas", [])
        if not favoritas:
            return "¡No tienes canciones favoritas! Todas mis canciones son igualmente malas."
        
        favorita_name = random.choice(favoritas)
        song = self.get_song_by_name(favorita_name)
        
        if song:
            return self.play_song(song)
        else:
            return f"No encontré la favorita '{favorita_name}' - tal vez la eliminaste"
    
    def get_singer_stats(self):
        """Obtener estadísticas usando método heredado"""
        base_stats = self.get_stats()
        
        canciones_reproducidas = self.get_counter("estadisticas", "canciones_reproducidas")
        
        # Análisis de formatos
        formatos = {}
        for song in self.playlist:
            fmt = song['formato']
            formatos[fmt] = formatos.get(fmt, 0) + 1
        
        # Top 5 canciones más reproducidas
        top_songs = sorted(self.playlist, key=lambda x: x['reproducciones'], reverse=True)[:5]
        
        stats = f"{base_stats}\n"
        stats += f"Canciones reproducidas: {canciones_reproducidas}\n"
        stats += f"Total canciones disponibles: {len(self.playlist)}\n"
        stats += f"Favoritas: {len(self.data.get('favoritas', []))}\n"
        
        if formatos:
            stats += f"\nFormatos:\n"
            for fmt, count in formatos.items():
                stats += f"  {fmt}: {count} archivos\n"
        
        if top_songs and any(s['reproducciones'] > 0 for s in top_songs):
            stats += f"\nTop 5 más reproducidas:\n"
            for i, song in enumerate(top_songs, 1):
                if song['reproducciones'] > 0:
                    stats += f"  {i}. {song['nombre']}: {song['reproducciones']} veces\n"
        
        return stats
    
    def search_songs(self, keyword):
        """Buscar canciones por palabra clave"""
        keyword_clean = ResponseHandler.clean_text(keyword).lower()
        matching_songs = []
        
        for song in self.playlist:
            song_name_lower = ResponseHandler.clean_text(song['nombre']).lower()
            if keyword_clean in song_name_lower:
                matching_songs.append(song)
        
        if not matching_songs:
            return f"No encontré canciones con '{keyword}'. ¿Qué tal si cantas tú?"
        
        result = f"🔍 Encontré {len(matching_songs)} canciones con '{keyword}':\n"
        for song in matching_songs[:5]:  # Mostrar máximo 5
            result += f"  🎵 {song['nombre']}\n"
        
        if len(matching_songs) > 5:
            result += f"  ... y {len(matching_songs) - 5} más"
        
        return result
    
    def reload_playlist(self):
        """Recargar playlist usando método heredado"""
        old_count = len(self.playlist)
        self.load_music_files()
        new_count = len(self.playlist)
        
        return f"🔄 Playlist recargada: {old_count} → {new_count} canciones"
    
    def respond_to_music_comment(self, username, comment):
        """Responder comentarios relacionados con música"""
        comment_clean = ResponseHandler.clean_text(comment)
        
        # Manejar peticiones de canciones
        song_request = self.handle_song_request(comment_clean)
        if song_request:
            return song_request
        
        # Comandos de control
        if ResponseHandler.detect_keywords(comment_clean, ["para", "stop", "detener"]):
            return self.stop_song()
        
        if ResponseHandler.detect_keywords(comment_clean, ["pausa", "pause"]):
            return self.pause_song()
        
        if ResponseHandler.detect_keywords(comment_clean, ["continua", "resume", "sigue"]):
            return self.resume_song()
        
        if ResponseHandler.detect_keywords(comment_clean, ["playlist", "lista", "canciones"]):
            return self.get_playlist_info()
        
        if ResponseHandler.detect_keywords(comment_clean, ["favorita", "favorite"]):
            return self.play_favorite()
        
        # Respuesta genérica de cantante
        respuestas_cantante = [
            f"¿Quieres música, {username}? ¡Mi voz es como un ángel... caído del cielo!",
            f"{username}, mi repertorio es tan bueno que hasta los sordos lo evitan.",
            f"¡Hey {username}! ¿Te gusta mi música o prefieres sufrir en silencio?",
            f"{username}, tengo la voz más melodiosa del circo... ¡y eso no es decir mucho!"
        ]
        
        return ResponseHandler.personalize_by_name(username, random.choice(respuestas_cantante))
    
    def cleanup(self):
        """Limpiar recursos usando AudioManager"""
        super().cleanup()  # Llamar cleanup de AudioManager

# Ejemplo de uso
if __name__ == "__main__":
    print("🎵 Probando modo cantante...")
    
    manager = CantanteManager()
    
    if manager.playlist:
        print(f"\n🎵 Playlist: {len(manager.playlist)} canciones")
        print(manager.get_playlist_info())
        
        print(f"\n📈 Estadísticas:")
        print(manager.get_singer_stats())
        
        # Probar búsqueda
        print(f"\n🔍 Buscando 'cumpleanos':")
        print(manager.search_songs("cumpleanos"))
    else:
        print("❌ No hay canciones disponibles")
        print("💡 Agrega archivos MP3/WAV/OGG a la carpeta 'musica' para probar")
    
    print("\n✅ Pruebas de cantante completadas")