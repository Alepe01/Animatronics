import pyaudio
import speech_recognition as sr
import threading
import time
import tempfile
import os
import asyncio
import pygame
import edge_tts
from comunicacionMicro import ArduinoController

class AudioListener:
    def __init__(self, callback_function):
        """
        Inicializar el listener de audio del sistema
        callback_function: función que se llama cuando se detecta audio
        """
        self.callback = callback_function
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.listening = False
        self.listen_thread = None
        
        # Configuración del reconocidor
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        self.setup_microphone()
    
    def setup_microphone(self):
        """Configurar micrófono (o dispositivo de audio interno)"""
        try:
            # Listar todos los dispositivos disponibles
            print("🔍 Dispositivos de audio disponibles:")
            for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"  {i}: {mic_name}")
            
            # Buscar dispositivo de mezcla estéreo (audio interno)
            stereo_mix_index = None
            for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
                if any(keyword in mic_name.lower() for keyword in 
                      ['stereo mix', 'mezcla estéreo', 'what u hear', 'loopback', 'wave out mix']):
                    stereo_mix_index = i
                    print(f"✅ Encontrado dispositivo de audio interno: {mic_name}")
                    break
            
            # Configurar micrófono
            if stereo_mix_index is not None:
                self.microphone = sr.Microphone(device_index=stereo_mix_index)
                print("🔊 Usando audio interno del sistema")
            else:
                self.microphone = sr.Microphone()
                print("🎤 Usando micrófono por defecto (no se encontró audio interno)")
                print("💡 Para capturar audio de YouTube, habilita 'Mezcla estéreo' en Windows")
            
            # Calibrar para ruido ambiental
            with self.microphone as source:
                print("🎤 Calibrando dispositivo de audio...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("✅ Dispositivo de audio configurado correctamente")
        except Exception as e:
            print(f"❌ Error configurando micrófono: {e}")
            self.microphone = None
    
    def start_listening(self):
        """Iniciar escucha de audio"""
        if not self.microphone:
            print("❌ Micrófono no disponible")
            return
        
        if self.listening:
            print("🎤 Ya está escuchando...")
            return
        
        self.listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        print("🎤 Iniciando escucha de audio del sistema...")
    
    def stop_listening(self):
        """Detener escucha de audio"""
        self.listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=1)
        print("🔇 Escucha de audio detenida")
    
    def _listen_loop(self):
        """Loop principal de escucha"""
        while self.listening:
            try:
                # Escuchar audio
                with self.microphone as source:
                    print("🎧 Escuchando...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Reconocer texto
                try:
                    text = self.recognizer.recognize_google(audio, language='es-ES')
                    if text.strip():
                        print(f"🗣️ Audio detectado: {text}")
                        self.callback(text)
                
                except sr.UnknownValueError:
                    # No se pudo entender el audio
                    pass
                except sr.RequestError as e:
                    print(f"❌ Error en el servicio de reconocimiento: {e}")
                    time.sleep(1)
            
            except sr.WaitTimeoutError:
                # Timeout normal, continuar
                pass
            except Exception as e:
                print(f"❌ Error en escucha: {e}")
                time.sleep(1)
    
    def select_audio_device(self, device_index=None):
        """Seleccionar dispositivo de audio específico"""
        try:
            if device_index is not None:
                self.microphone = sr.Microphone(device_index=device_index)
                device_name = sr.Microphone.list_microphone_names()[device_index]
                print(f"🔄 Cambiado a dispositivo: {device_name}")
            else:
                self.microphone = sr.Microphone()
                print("🔄 Cambiado a dispositivo por defecto")
            
            # Recalibrar
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            return True
        except Exception as e:
            print(f"❌ Error cambiando dispositivo: {e}")
            return False
    
    def find_stereo_mix(self):
        """Buscar y seleccionar automáticamente Mezcla Estéreo"""
        devices = sr.Microphone.list_microphone_names()
        
        stereo_keywords = [
            'stereo mix', 'mezcla estéreo', 'what u hear', 
            'loopback', 'wave out mix', 'speakers', 'altavoces'
        ]
        
        for i, device_name in enumerate(devices):
            for keyword in stereo_keywords:
                if keyword in device_name.lower():
                    print(f"🔊 Encontrado audio interno: {device_name}")
                    return self.select_audio_device(i)
        
        print("❌ No se encontró dispositivo de audio interno")
        print("💡 Habilita 'Mezcla estéreo' en Configuración de sonido de Windows")
        return False
        """Probar el micrófono"""
        if not self.microphone:
            return False
        
        try:
            with self.microphone as source:
                print("🎤 Prueba de micrófono - Habla algo...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            text = self.recognizer.recognize_google(audio, language='es-ES')
            print(f"✅ Texto reconocido: {text}")
            return True
        
        except Exception as e:
            print(f"❌ Error en prueba de micrófono: {e}")
            return False
    
    def get_microphone_list(self):
        """Obtener lista de micrófonos disponibles"""
        return sr.Microphone.list_microphone_names()

class SpeechController:
    def __init__(self, arduino_controller=None):
        """
        Controlador de síntesis de voz
        """
        self.arduino = arduino_controller
        self.voice = "es-MX-JorgeNeural"  # Voz Jorge México
        self.is_speaking = False
        self.temp_files = []
        
        # Inicializar pygame para audio
        pygame.mixer.init()
        print("🗣️ Controlador de voz inicializado")
    
    def speak_text(self, text):
        """Convertir texto a voz y reproducir"""
        if self.is_speaking:
            print("🗣️ Ya está hablando...")
            return
        
        # Iniciar animación en Arduino
        if self.arduino:
            self.arduino.start_talking()
        
        self.is_speaking = True
        
        try:
            # Crear audio con Edge TTS
            audio_file = self._create_audio_async(text)
            
            if audio_file:
                # Reproducir audio
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                # Esperar a que termine
                while pygame.mixer.music.get_busy() and self.is_speaking:
                    time.sleep(0.1)
                
                # Agregar a lista de archivos temporales
                self.temp_files.append(audio_file)
        
        except Exception as e:
            print(f"❌ Error en síntesis de voz: {e}")
        
        finally:
            self.is_speaking = False
            
            # Detener animación en Arduino
            if self.arduino:
                self.arduino.stop_talking()
            
            # Limpiar archivos viejos
            self._cleanup_old_files()
    
    def _create_audio_async(self, text):
        """Crear archivo de audio usando Edge TTS"""
        try:
            # Crear evento loop para async
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Crear archivo temporal
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            # Generar audio
            async def generate():
                communicate = edge_tts.Communicate(text, self.voice)
                await communicate.save(temp_file.name)
            
            loop.run_until_complete(generate())
            loop.close()
            
            return temp_file.name
            
        except Exception as e:
            print(f"❌ Error creando audio: {e}")
            return None
    
    def stop_speaking(self):
        """Detener reproducción de voz"""
        self.is_speaking = False
        pygame.mixer.music.stop()
        
        if self.arduino:
            self.arduino.stop_talking()
    
    def change_voice(self, voice_name):
        """Cambiar voz"""
        available_voices = [
            "es-MX-JorgeNeural",  # Jorge México (Masculina)
            "es-MX-DaliaNeural",  # Dalia México (Femenina)
            "es-ES-ElviraNeural", # Elvira España (Femenina)
            "es-ES-AlvaroNeural", # Álvaro España (Masculina)
            "es-AR-ElenaNeural",  # Elena Argentina (Femenina)
            "es-AR-TomasNeural"   # Tomás Argentina (Masculina)
        ]
        
        if voice_name in available_voices:
            self.voice = voice_name
            print(f"🗣️ Voz cambiada a: {voice_name}")
        else:
            print(f"❌ Voz no disponible: {voice_name}")
            print("Voces disponibles:", available_voices)
    
    def set_speaking_speed(self, speed):
        """Ajustar velocidad de habla (no implementado en Edge TTS básico)"""
        # Edge TTS básico no permite cambio de velocidad fácilmente
        print(f"⚙️ Velocidad de habla: {speed} (funcionalidad limitada)")
    
    def _cleanup_old_files(self):
        """Limpiar archivos de audio temporales"""
        for file_path in self.temp_files[:]:  # Copia de la lista
            try:
                os.unlink(file_path)
                self.temp_files.remove(file_path)
            except Exception:
                pass
    
    def cleanup_temp_files(self):
        """Limpiar todos los archivos temporales"""
        self._cleanup_old_files()
    
    def test_speech(self, text="Hola, soy Poncho el payaso"):
        """Probar síntesis de voz"""
        print("🧪 Probando síntesis de voz...")
        self.speak_text(text)

# --- FUNCIONES DE UTILIDAD ---
def list_audio_devices():
    """Listar dispositivos de audio disponibles"""
    p = pyaudio.PyAudio()
    print("🔊 Dispositivos de audio disponibles:")
    
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"  {i}: {info['name']} - Canales: {info['maxInputChannels']}")
    
    p.terminate()

def test_speech_recognition():
    """Probar reconocimiento de voz básico"""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    try:
        with microphone as source:
            print("🎤 Calibrando...")
            recognizer.adjust_for_ambient_noise(source)
        
        print("🗣️ Habla algo...")
        with microphone as source:
            audio = recognizer.listen(source, timeout=5)
        
        text = recognizer.recognize_google(audio, language='es-ES')
        print(f"✅ Texto reconocido: {text}")
        return text
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    print("🎤 Probando sistema de audio...")
    
    # Listar dispositivos
    list_audio_devices()
    
    # Probar reconocimiento básico
    print("\n🧪 Prueba de reconocimiento de voz:")
    test_speech_recognition()
    
    # Probar síntesis de voz
    print("\n🗣️ Probando síntesis de voz...")
    arduino = ArduinoController()  # Puede ser None si no hay Arduino
    speech = SpeechController(arduino)
    
    speech.test_speech("Hola, soy Poncho el payaso animatrónico")
    
    time.sleep(3)
    
    # Probar listener de audio
    print("\n🎧 Probando listener de audio...")
    
    def audio_callback(text):
        print(f"📝 Callback recibido: {text}")
        speech.speak_text(f"Escuché que dijiste: {text}")
    
    listener = AudioListener(audio_callback)
    listener.start_listening()
    
    print("🎤 Habla algo durante los próximos 10 segundos...")
    time.sleep(10)
    
    listener.stop_listening()
    speech.cleanup_temp_files()
    arduino.close()
    
    print("✅ Pruebas completadas")