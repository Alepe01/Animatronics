import threading
import time
import tempfile
import os
import asyncio
import pygame
import speech_recognition as sr
try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False
    print("⚠️ edge-tts no disponible - síntesis de voz deshabilitada")

class AudioManager:
    """Manager común para funcionalidades de audio"""
    
    def __init__(self, arduino_controller=None):
        self.arduino = arduino_controller
        self.is_playing = False
        self.current_thread = None
        self.temp_files = []
        self.voice = "es-MX-JorgeNeural"
        
        # Inicializar pygame
        try:
            pygame.mixer.init()
            print("🔊 Audio Manager inicializado")
        except Exception as e:
            print(f"❌ Error inicializando audio: {e}")
    
    def play_audio_file(self, audio_file, callback=None):
        """Reproducir archivo de audio con callback opcional"""
        if self.is_playing:
            self.stop_audio()
            time.sleep(0.2)
        
        self.is_playing = True
        self.current_thread = threading.Thread(
            target=self._play_file_thread, 
            args=(audio_file, callback), 
            daemon=True
        )
        self.current_thread.start()
    
    def _play_file_thread(self, audio_file, callback):
        """Thread de reproducción de archivo"""
        try:
            if callback:
                callback('start')
            
            if self.arduino:
                self.arduino.start_talking()
            
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy() and self.is_playing:
                time.sleep(0.1)
                
        except Exception as e:
            print(f"❌ Error reproduciendo audio: {e}")
        finally:
            self.is_playing = False
            if self.arduino:
                self.arduino.stop_talking()
            if callback:
                callback('stop')
    
    def speak_text(self, text):
        """Convertir texto a voz y reproducir"""
        if not HAS_EDGE_TTS:
            print(f"🗣️ [TEXTO]: {text}")
            return
        
        if self.is_playing:
            self.stop_audio()
            time.sleep(0.2)
        
        self.is_playing = True
        self.current_thread = threading.Thread(
            target=self._speak_thread,
            args=(text,),
            daemon=True
        )
        self.current_thread.start()
    
    def _speak_thread(self, text):
        """Thread de síntesis de voz"""
        try:
            if self.arduino:
                self.arduino.start_talking()
            
            # Crear audio con Edge TTS
            audio_file = self._create_audio_async(text)
            
            if audio_file:
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy() and self.is_playing:
                    time.sleep(0.1)
                
                self.temp_files.append(audio_file)
        
        except Exception as e:
            print(f"❌ Error en síntesis de voz: {e}")
        finally:
            self.is_playing = False
            if self.arduino:
                self.arduino.stop_talking()
            self._cleanup_old_files()
    
    def _create_audio_async(self, text):
        """Crear archivo de audio usando Edge TTS"""
        if not HAS_EDGE_TTS:
            return None
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            async def generate():
                communicate = edge_tts.Communicate(text, self.voice)
                await communicate.save(temp_file.name)
            
            loop.run_until_complete(generate())
            loop.close()
            
            return temp_file.name
            
        except Exception as e:
            print(f"❌ Error creando audio: {e}")
            return None
    
    def stop_audio(self):
        """Detener reproducción"""
        self.is_playing = False
        try:
            pygame.mixer.music.stop()
        except:
            pass
        
        if self.arduino:
            self.arduino.stop_talking()
        
        if self.current_thread and self.current_thread.is_alive():
            self.current_thread.join(timeout=1)
    
    def pause_audio(self):
        """Pausar audio"""
        try:
            pygame.mixer.music.pause()
            if self.arduino:
                self.arduino.stop_talking()
            return True
        except Exception as e:
            print(f"❌ Error pausando: {e}")
            return False
    
    def resume_audio(self):
        """Reanudar audio"""
        try:
            pygame.mixer.music.unpause()
            if self.arduino and self.is_playing:
                self.arduino.start_talking()
            return True
        except Exception as e:
            print(f"❌ Error reanudando: {e}")
            return False
    
    def set_voice(self, voice_name):
        """Cambiar voz para síntesis"""
        available_voices = [
            "es-MX-JorgeNeural",  # Jorge México (Masculina)
            "es-MX-DaliaNeural",  # Dalia México (Femenina)
            "es-ES-ElviraNeural", # Elvira España (Femenina)
            "es-ES-AlvaroNeural", # Álvaro España (Masculina)
        ]
        
        if voice_name in available_voices:
            self.voice = voice_name
            print(f"🗣️ Voz cambiada a: {voice_name}")
            return True
        else:
            print(f"❌ Voz no disponible: {voice_name}")
            return False
    
    def get_available_voices(self):
        """Obtener lista de voces disponibles"""
        return [
            "es-MX-JorgeNeural",
            "es-MX-DaliaNeural",
            "es-ES-ElviraNeural",
            "es-ES-AlvaroNeural",
        ]
    
    def is_audio_playing(self):
        """Verificar si se está reproduciendo audio"""
        return self.is_playing
    
    def _cleanup_old_files(self):
        """Limpiar archivos temporales antiguos"""
        for file_path in self.temp_files[:]:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
                self.temp_files.remove(file_path)
            except Exception:
                pass
    
    def cleanup(self):
        """Limpiar todos los recursos"""
        self.stop_audio()
        self._cleanup_old_files()
        try:
            pygame.mixer.quit()
        except:
            pass

class ArduinoAudioManager(AudioManager):
    """AudioManager con integración sincronizada de Arduino"""
    
    def __init__(self, arduino_controller=None, voice="es-MX-JorgeNeural"):
        super().__init__(arduino_controller)
        self.arduino = arduino_controller
        self.is_currently_speaking = False
        self._stop_requested = False  # Nueva bandera para controlar paradas
        self._arduino_state = "STOP"  # Tracking del estado del Arduino: STOP, THINKING, TALK
        self._lock = threading.Lock()  # Lock para thread safety
        
        # Configurar voz específica para este manager
        self.voice = voice
        print(f"🗣️ ArduinoAudioManager inicializado con voz: {voice}")
    
    def _send_arduino_talk(self):
        """Enviar comando TALK al Arduino con protección"""
        with self._lock:
            if self.arduino and self.arduino.is_connected() and self._arduino_state != "TALK":
                self.arduino.start_talking()
                self._arduino_state = "TALK"
                print("🤖 Arduino: TALK enviado (protegido)")
            elif self._arduino_state == "TALK":
                print("🤖 Arduino: TALK ignorado (ya en TALK)")
    
    def _send_arduino_thinking(self):
        """Enviar comando THINKING al Arduino con protección"""
        with self._lock:
            if self.arduino and self.arduino.is_connected() and self._arduino_state != "THINKING":
                self.arduino.send_command("THINKING")
                self._arduino_state = "THINKING"
                print("🤖 Arduino: THINKING enviado (procesando respuesta)")
            elif self._arduino_state == "THINKING":
                print("🤖 Arduino: THINKING ignorado (ya en THINKING)")
    
    def _send_arduino_stop(self):
        """Enviar comando STOP al Arduino con protección"""
        with self._lock:
            if self.arduino and self.arduino.is_connected() and self._arduino_state != "STOP":
                self.arduino.stop_talking()
                self._arduino_state = "STOP"
                print("🤖 Arduino: STOP enviado (protegido)")
            elif self._arduino_state == "STOP":
                print("🤖 Arduino: STOP ignorado (ya en STOP)")
    
    def speak_text(self, text):
        """Hablar en thread separado pero con sincronización correcta"""
        if not text:
            return
        
        # Detener audio anterior si existe - SIN enviar STOP al Arduino
        if self.is_currently_speaking:
            self._stop_requested = True  # Marcar que se solicitó parada
            self._stop_audio_silent()  # Parada silenciosa sin STOP al Arduino
            time.sleep(0.2)
        
        # Resetear banderas
        self._stop_requested = False
        self.is_currently_speaking = True
        self.is_playing = True
        
        print("🔊 Iniciando nueva reproducción de audio...")
        
        # Iniciar animación de forma protegida
        self._send_arduino_talk()
        
        # Crear thread para el audio
        self.current_thread = threading.Thread(
            target=self._speak_thread_sync,
            args=(text,),
            daemon=True
        )
        self.current_thread.start()
    
    def _speak_thread_sync(self, text):
        """Thread que maneja el audio con sincronización perfecta"""
        audio_completed_naturally = False
        
        try:
            from response_handler import ResponseHandler
            clean_text = ResponseHandler.clean_text(text)
            
            if HAS_EDGE_TTS:
                # Crear y reproducir audio
                audio_file = self._create_audio_sync(clean_text)
                
                if audio_file and not self._stop_requested:
                    pygame.mixer.music.load(audio_file)
                    pygame.mixer.music.play()
                    
                    print("🔊 Audio iniciado, esperando a que termine...")
                    
                    # Esperar hasta que termine completamente O se solicite parada
                    while pygame.mixer.music.get_busy() and self.is_playing and not self._stop_requested:
                        time.sleep(0.1)
                    
                    # Verificar si terminó naturalmente
                    if not self._stop_requested and not pygame.mixer.music.get_busy():
                        audio_completed_naturally = True
                        print("🔊 Audio terminó naturalmente")
                    elif self._stop_requested:
                        print("🔊 Audio detenido por solicitud externa")
                    
                    # Limpiar archivo
                    try:
                        os.unlink(audio_file)
                    except:
                        pass
                else:
                    if self._stop_requested:
                        print("🔊 Creación de audio cancelada por stop request")
                        return
                    # Fallback - Simular duración con thinking
                    duration = len(clean_text) * 0.1
                    print(f"🔊 Simulando audio por {duration:.1f} segundos...")
                    
                    # Simular duración pero verificar stop_requested
                    start_time = time.time()
                    while (time.time() - start_time) < duration and not self._stop_requested:
                        time.sleep(0.1)
                    
                    if not self._stop_requested:
                        audio_completed_naturally = True
            else:
                # Sin TTS, simular duración
                duration = len(clean_text) * 0.08
                print(f"🗣️ [TEXTO]: {clean_text}")
                print(f"🔊 Simulando habla por {duration:.1f} segundos...")
                
                start_time = time.time()
                while (time.time() - start_time) < duration and not self._stop_requested:
                    time.sleep(0.1)
                
                if not self._stop_requested:
                    audio_completed_naturally = True
        
        except Exception as e:
            print(f"❌ Error en thread de audio: {e}")
        
        finally:
            # SOLO enviar STOP si el audio terminó naturalmente
            # NO enviar si fue interrumpido por stop_audio()
            if audio_completed_naturally and not self._stop_requested:
                print("🔊 Finalizando audio (terminación natural)...")
                self._send_arduino_stop()
            elif self._stop_requested:
                print("🔊 Audio interrumpido - STOP ya enviado por stop_audio()")
            
            self.is_currently_speaking = False
            self.is_playing = False
            self._stop_requested = False
            print("✅ Audio finalizado completamente")
    
    def start_thinking_mode(self):
        """Activar modo THINKING para cuando se esté procesando una respuesta"""
        self._send_arduino_thinking()
        print("🤔 Modo THINKING activado - procesando respuesta...")
    
    def process_and_speak(self, process_function, *args, **kwargs):
        """Procesar respuesta con thinking mode, luego hablar"""
        try:
            # 1. Activar thinking mode
            self.start_thinking_mode()
            
            # 2. Procesar respuesta (función personalizada)
            response = process_function(*args, **kwargs)
            
            # 3. Hablar la respuesta (cambia automáticamente a TALK)
            if response:
                self.speak_text(response)
            
            return response
            
        except Exception as e:
            print(f"❌ Error en process_and_speak: {e}")
            self._send_arduino_stop()
            return f"Error procesando respuesta: {e}"
    
    def _create_audio_sync(self, text):
        """Crear archivo de audio de forma sincronizada"""
        if not HAS_EDGE_TTS:
            return None
        
        try:
            import tempfile
            import asyncio
            import edge_tts
            
            # Crear archivo temporal
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            # Función async para generar audio
            async def generate_audio():
                communicate = edge_tts.Communicate(text, self.voice)
                await communicate.save(temp_file.name)
            
            # Ejecutar de forma sincronizada
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(generate_audio())
            loop.close()
            
            return temp_file.name
            
        except Exception as e:
            print(f"❌ Error creando audio: {e}")
            return None
    
    def _stop_audio_silent(self):
        """Detener audio SIN enviar comando STOP al Arduino"""
        print("🔇 _stop_audio_silent() llamado - sin comando Arduino")
        
        # Marcar que se solicitó parada
        self._stop_requested = True
        self.is_playing = False
        self.is_currently_speaking = False
        
        try:
            pygame.mixer.music.stop()
            print("🔊 pygame.mixer.music.stop() ejecutado (silencioso)")
        except:
            pass
        
        # NO enviar comando al Arduino aquí - la nueva reproducción enviará START
    
    def stop_audio(self):
        """Detener audio y animación inmediatamente"""
        print("🛑 stop_audio() llamado")
        
        # Marcar que se solicitó parada
        self._stop_requested = True
        self.is_playing = False
        self.is_currently_speaking = False
        
        try:
            pygame.mixer.music.stop()
            print("🔊 pygame.mixer.music.stop() ejecutado")
        except:
            pass
        
        # Detener animación de Arduino de forma protegida
        self._send_arduino_stop()
    
    def pause_audio(self):
        """Pausar audio y animación"""
        try:
            pygame.mixer.music.pause()
            # Pausar también la animación de Arduino
            self._send_arduino_stop()
            return True
        except Exception as e:
            print(f"❌ Error pausando: {e}")
            return False
    
    def resume_audio(self):
        """Reanudar audio y animación"""
        try:
            pygame.mixer.music.unpause()
            # Reanudar animación si estaba hablando
            if self.is_currently_speaking:
                self._send_arduino_talk()
            return True
        except Exception as e:
            print(f"❌ Error reanudando: {e}")
            return False
    
    def is_audio_playing(self):
        """Verificar si está reproduciendo audio"""
        return self.is_currently_speaking or super().is_audio_playing()

class AudioListener:
    """Listener de audio del sistema reutilizable"""
    
    def __init__(self, callback_function):
        self.callback = callback_function
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.listening = False
        self.listen_thread = None
        
        # Configuración del reconocedor
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        self.setup_microphone()
    
    def setup_microphone(self):
        """Configurar micrófono"""
        try:
            # Buscar dispositivo de mezcla estéreo
            stereo_mix_index = self._find_stereo_mix_device()
            
            if stereo_mix_index is not None:
                self.microphone = sr.Microphone(device_index=stereo_mix_index)
                print("🔊 Usando audio interno del sistema")
            else:
                self.microphone = sr.Microphone()
                print("🎤 Usando micrófono por defecto")
            
            # Calibrar
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("✅ Dispositivo de audio configurado")
            
        except Exception as e:
            print(f"❌ Error configurando micrófono: {e}")
            self.microphone = None
    
    def _find_stereo_mix_device(self):
        """Buscar dispositivo de mezcla estéreo"""
        try:
            devices = sr.Microphone.list_microphone_names()
            for i, device_name in enumerate(devices):
                if any(keyword in device_name.lower() for keyword in 
                      ['stereo mix', 'mezcla estéreo', 'what u hear', 'loopback']):
                    return i
        except:
            pass
        return None
    
    def start_listening(self):
        """Iniciar escucha"""
        if not self.microphone or self.listening:
            return
        
        self.listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        print("🎧 Escucha de audio iniciada")
    
    def stop_listening(self):
        """Detener escucha"""
        self.listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=1)
        print("🔇 Escucha detenida")
    
    def _listen_loop(self):
        """Loop principal de escucha"""
        while self.listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                try:
                    text = self.recognizer.recognize_google(audio, language='es-ES')
                    if text.strip():
                        self.callback(text)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"❌ Error reconocimiento: {e}")
                    time.sleep(1)
            
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                print(f"❌ Error escucha: {e}")
                time.sleep(1)
    
    def select_audio_device(self, device_index):
        """Seleccionar dispositivo específico"""
        try:
            self.microphone = sr.Microphone(device_index=device_index)
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            return True
        except Exception as e:
            print(f"❌ Error cambiando dispositivo: {e}")
            return False
    
    def get_microphone_list(self):
        """Obtener lista de micrófonos"""
        try:
            return sr.Microphone.list_microphone_names()
        except:
            return []
    
    def test_microphone(self):
        """Probar micrófono actual"""
        if not self.microphone:
            return False
        
        try:
            with self.microphone as source:
                print("🎤 Prueba de micrófono - Habla algo...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            text = self.recognizer.recognize_google(audio, language='es-ES')
            print(f"✅ Reconocido: {text}")
            return True
        except Exception as e:
            print(f"❌ Error prueba: {e}")
            return False