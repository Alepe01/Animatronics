import os
import random
import threading
import time
import pygame
from comunicacionMicro import ArduinoController

class CantanteManager:
    def __init__(self, music_folder="musica", arduino_controller=None):
        """
        Inicializar el manager del modo cantante
        """
        self.music_folder = music_folder
        self.arduino = arduino_controller
        self.playlist = []
        self.current_song = None
        self.is_playing = False
        self.play_thread = None
        
        # Inicializar pygame para audio
        pygame.mixer.init()
        
        self.load_music_files()
        print(f"🎵 Cantante Manager inicializado con {len(self.playlist)} canciones")
    
    def load_music_files(self):
        """Cargar archivos de música desde la carpeta"""
        try:
            if not os.path.exists(self.music_folder):
                os.makedirs(self.music_folder)
                print(f"📁 Carpeta {self.music_folder} creada")
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
                        'formato': os.path.splitext(filename)[1]
                    })
            
            print(f"🎵 Cargadas {len(self.playlist)} canciones:")
            for song in self.playlist:
                print(f"  - {song['nombre']}{song['formato']}")
        
        except Exception as e:
            print(f"❌ Error cargando música: {e}")
            self.playlist = []
    
    def _create_sample_playlist(self):
        """Crear archivo de ejemplo con lista de canciones sugeridas"""
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
            with open(os.path.join(self.music_folder, "LEEME.txt"), 'w', encoding='utf-8') as f:
                f.write(sample_info)
            print("📄 Archivo de instrucciones creado en carpeta música")
        except Exception as e:
            print(f"❌ Error creando archivo de instrucciones: {e}")
    
    def get_random_song(self):
        """Obtener canción aleatoria"""
        if not self.playlist:
            return None
        return random.choice(self.playlist)
    
    def get_song_by_name(self, song_name):
        """Buscar canción por nombre (búsqueda parcial)"""
        song_name_lower = song_name.lower()
        for song in self.playlist:
            if song_name_lower in song['nombre'].lower():
                return song
        return None
    
    def play_song(self, song=None):
        """Reproducir canción específica o aleatoria"""
        if self.is_playing:
            self.stop_song()
            time.sleep(0.5)
        
        if song is None:
            song = self.get_random_song()
        
        if not song:
            return "¡No tengo canciones para cantar! ¡Soy un payaso sin repertorio!"
        
        self.current_song = song
        self.is_playing = True
        
        # Iniciar thread de reproducción
        self.play_thread = threading.Thread(target=self._play_song_thread, args=(song,), daemon=True)
        self.play_thread.start()
        
        return f"🎵 Ahora cantando: {song['nombre']}"
    
    def _play_song_thread(self, song):
        """Thread para reproducir canción y manejar animaciones"""
        try:
            print(f"🎵 Iniciando reproducción: {song['nombre']}")
            
            # Iniciar animación de habla
            if self.arduino:
                self.arduino.start_talking()
            
            # Cargar y reproducir música
            pygame.mixer.music.load(song['archivo'])
            pygame.mixer.music.play()
            
            # Monitorear reproducción
            while pygame.mixer.music.get_busy() and self.is_playing:
                time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ Error reproduciendo {song['nombre']}: {e}")
        
        finally:
            # Detener animación
            if self.arduino:
                self.arduino.stop_talking()
            
            self.is_playing = False
            self.current_song = None
            print(f"🎵 Reproducción terminada: {song['nombre']}")
    
    def stop_song(self):
        """Detener canción actual"""
        if self.is_playing:
            self.is_playing = False
            pygame.mixer.music.stop()
            
            if self.arduino:
                self.arduino.stop_talking()
            
            if self.play_thread and self.play_thread.is_alive():
                self.play_thread.join(timeout=1)
            
            print("⏹️ Canción detenida")
            return "¡Canción detenida! ¡Espero que no haya sido por mi voz!"
        
        return "¡No estoy cantando nada!"
    
    def pause_song(self):
        """Pausar canción actual"""
        if self.is_playing and pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            if self.arduino:
                self.arduino.stop_talking()
            return "⏸️ Canción pausada"
        return "¡No hay nada que pausar!"
    
    def resume_song(self):
        """Reanudar canción pausada"""
        try:
            pygame.mixer.music.unpause()
            if self.arduino and self.is_playing:
                self.arduino.start_talking()
            return "▶️ Canción reanudada"
        except:
            return "¡No hay nada que reanudar!"
    
    def get_playlist_info(self):
        """Obtener información de la playlist"""
        if not self.playlist:
            return "¡Mi playlist está más vacía que mi alma de payaso!"
        
        info = f"🎵 Playlist de Poncho ({len(self.playlist)} canciones):\n"
        for i, song in enumerate(self.playlist, 1):
            marker = "🎵" if song != self.current_song else "▶️"
            info += f"{marker} {i}. {song['nombre']}\n"
        
        return info
    
    def get_current_song_info(self):
        """Información de la canción actual"""
        if self.current_song and self.is_playing:
            return f"🎵 Cantando: {self.current_song['nombre']}"
        return "🔇 No estoy cantando nada"
    
    def handle_song_request(self, comment):
        """Manejar peticiones de canciones desde comentarios"""
        comment_lower = comment.lower()
        
        # Palabras clave para peticiones
        request_keywords = [
            "canta", "canción", "cancion", "música", "musica", 
            "toca", "interpreta", "tema", "play", "reproduce"
        ]
        
        # Verificar si es una petición
        is_request = any(keyword in comment_lower for keyword in request_keywords)
        
        if not is_request:
            return None
        
        # Buscar canción específica en el comentario
        for song in self.playlist:
            song_words = song['nombre'].lower().split('_')
            if any(word in comment_lower for word in song_words if len(word) > 2):
                return self.play_song(song)
        
        # Si no encuentra canción específica, tocar aleatoria
        return self.play_song()
    
    def get_song_stats(self):
        """Obtener estadísticas de canciones"""
        if not self.playlist:
            return "📊 No hay canciones disponibles"
        
        formats = {}
        for song in self.playlist:
            fmt = song['formato']
            formats[fmt] = formats.get(fmt, 0) + 1
        
        stats = f"📊 Estadísticas de Música:\n"
        stats += f"Total: {len(self.playlist)} canciones\n"
        stats += f"Formatos:\n"
        
        for fmt, count in formats.items():
            stats += f"  - {fmt}: {count} archivos\n"
        
        return stats
    
    def reload_playlist(self):
        """Recargar playlist desde carpeta"""
        old_count = len(self.playlist)
        self.load_music_files()
        new_count = len(self.playlist)
        
        return f"🔄 Playlist recargada: {old_count} → {new_count} canciones"
    
    def cleanup(self):
        """Limpiar recursos"""
        self.stop_song()
        try:
            pygame.mixer.quit()
        except:
            pass

# --- FUNCIONES DE UTILIDAD ---
def crear_playlist_ejemplo():
    """Crear playlist de ejemplo para testing"""
    music_folder = "musica_ejemplo"
    if not os.path.exists(music_folder):
        os.makedirs(music_folder)
    
    # Crear archivo de lista de canciones sugeridas
    songs_list = """
# LISTA DE CANCIONES SUGERIDAS PARA PONCHO #

Canciones de Cumpleaños:
- Las Mañanitas.mp3
- Happy Birthday.mp3
- Cumpleaños Feliz.mp3

Música de Circo/Payasos:
- Entrada de Gladiadores.mp3
- El Payaso Loco.mp3
- Música de Circo.mp3

Canciones Populares:
- Cielito Lindo.mp3
- La Cucaracha.mp3
- Pin Pon.mp3

Música Divertida:
- El Twist del Payaso.mp3
- Canción del Circo.mp3
- Melodía Alegre.mp3
"""
    
    with open(os.path.join(music_folder, "canciones_sugeridas.txt"), 'w', encoding='utf-8') as f:
        f.write(songs_list)
    
    print(f"📁 Carpeta de ejemplo creada: {music_folder}")

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    print("🎵 Probando modo cantante...")
    
    # Crear ejemplo si no existe música
    crear_playlist_ejemplo()
    
    # Crear manager
    arduino = None  # Puedes pasar ArduinoController() aquí
    cantante = CantanteManager(arduino_controller=arduino)
    
    if cantante.playlist:
        # Mostrar playlist
        print("\n" + cantante.get_playlist_info())
        
        # Mostrar estadísticas
        print("\n" + cantante.get_song_stats())
        
        # Probar reproducción (descomenta si tienes archivos de música)
        # print("\n🧪 Probando reproducción...")
        # resultado = cantante.play_song()
        # print(resultado)
        # time.sleep(5)
        # cantante.stop_song()
        
        # Probar manejo de peticiones
        print("\n🧪 Probando manejo de peticiones...")
        test_comments = [
            "canta las mañanitas",
            "pon música alegre", 
            "no me gusta esto",
            "toca cumpleaños feliz"
        ]
        
        for comment in test_comments:
            resultado = cantante.handle_song_request(comment)
            if resultado:
                print(f"'{comment}' → {resultado}")
            else:
                print(f"'{comment}' → No es petición musical")
    
    else:
        print("❌ No hay canciones disponibles")
        print("💡 Agrega archivos MP3/WAV/OGG a la carpeta 'musica' para probar")
    
    cantante.cleanup()
    print("\n✅ Pruebas de cantante completadas")