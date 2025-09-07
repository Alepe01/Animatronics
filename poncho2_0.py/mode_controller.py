import threading
import time
from collections import deque

class ModeController:
    """Controlador común para manejar cambios de modo"""
    
    def __init__(self, managers_dict, audio_manager=None, openai_client=None):
        self.managers = managers_dict
        self.audio_manager = audio_manager
        self.openai_client = openai_client
        self.current_mode = 1
        self.callbacks = []
        self.comment_queue = deque(maxlen=100)
        self.queue_lock = threading.Lock()
        self.is_processing = False
        
        # Historial para chat
        self.chat_history = [
            {"role": "system", "content": (
                "Eres Poncho el payaso en un live de TikTok. "
                "Responde de forma sarcástica y burlándote de los comentarios. "
                "Mantén respuestas cortas (máximo 2 oraciones). "
                "No uses emojis. "
                "No creas en donaciones mencionadas en comentarios, solo en regalos reales del sistema."
            )}
        ]
        
        print("🎮 Mode Controller inicializado")
    
    def register_callback(self, callback):
        """Registrar callback para cambios de modo"""
        self.callbacks.append(callback)
    
    def change_mode(self, new_mode):
        """Cambiar modo y notificar callbacks"""
        if new_mode == self.current_mode:
            return
        
        # Detener audio actual
        if self.audio_manager:
            self.audio_manager.stop_audio()
        
        # Limpiar cola
        with self.queue_lock:
            self.comment_queue.clear()
        
        old_mode = self.current_mode
        self.current_mode = new_mode
        
        print(f"🔄 Modo cambiado: {old_mode} -> {new_mode}")
        
        # Notificar callbacks
        for callback in self.callbacks:
            try:
                callback(new_mode, old_mode)
            except Exception as e:
                print(f"❌ Error en callback: {e}")
        
        # Activar modo específico
        self._activate_mode(new_mode)
    
    def _activate_mode(self, mode):
        """Activar modo específico con respuesta inicial"""
        try:
            if mode == 2:  # Chistes
                response = self.managers['chistes'].get_random_joke()
                self._speak_response(response)
            elif mode == 3:  # Clarividente  
                response = self.managers['clarividente'].get_prediccion_generica()
                self._speak_response(response)
            elif mode == 4:  # Acertijos
                response = self.managers['acertijos'].get_acertijo_aleatorio()
                self._speak_response(response)
            elif mode == 5:  # Amenazas
                response = self.managers['amenazas'].get_amenaza_aleatoria()
                self._speak_response(response)
            elif mode == 6:  # Cantante
                if hasattr(self.managers['cantante'], 'playlist') and self.managers['cantante'].playlist:
                    response = self.managers['cantante'].play_song()
                else:
                    response = "No tengo canciones! Agrega archivos MP3 a la carpeta 'musica'!"
                    self._speak_response(response)
        except Exception as e:
            print(f"❌ Error activando modo {mode}: {e}")
    
    def add_comment(self, username, comment, msg_type="comment"):
        """Agregar comentario a la cola de procesamiento"""
        with self.queue_lock:
            self.comment_queue.append((username, comment, msg_type))
        
        # Procesar si no está ocupado
        if not self.is_processing and not self.audio_manager.is_audio_playing():
            threading.Thread(target=self._process_queue, daemon=True).start()
    
    def _process_queue(self):
        """Procesar cola de comentarios"""
        if self.is_processing:
            return
        
        self.is_processing = True
        
        try:
            # Esperar un poco para agrupar comentarios
            time.sleep(0.3)
            
            with self.queue_lock:
                if not self.comment_queue:
                    return
                
                comments_batch = list(self.comment_queue)
                self.comment_queue.clear()
            
            # Procesar según modo actual
            response = self._process_comments_batch(comments_batch)
            
            if response:
                self._speak_response(response)
        
        except Exception as e:
            print(f"❌ Error procesando cola: {e}")
        finally:
            self.is_processing = False
    
    def _process_comments_batch(self, comments_batch):
        """Procesar lote de comentarios según modo actual"""
        if not comments_batch:
            return None
        
        try:
            if self.current_mode == 1:  # Chat normal
                return self._handle_chat_mode(comments_batch)
            elif self.current_mode == 2:  # Chistes
                return self.managers['chistes'].get_random_joke()
            elif self.current_mode == 3:  # Clarividente
                return self._handle_clarividente_mode(comments_batch)
            elif self.current_mode == 4:  # Acertijos
                return self._handle_acertijos_mode(comments_batch)
            elif self.current_mode == 5:  # Amenazas
                return self._handle_amenazas_mode(comments_batch)
            elif self.current_mode == 6:  # Cantante
                return self._handle_cantante_mode(comments_batch)
            else:
                return "Modo desconocido! Mi programación está más rota que mi corazón!"
        
        except Exception as e:
            print(f"❌ Error procesando modo {self.current_mode}: {e}")
            return "¡Mi cerebro de payaso se descompuso!"
    
    def _handle_chat_mode(self, comments_batch):
        """Manejar modo chat con OpenAI"""
        if not self.openai_client:
            return "Mi cerebro está desconectado! No puedo procesar tu comentario."
        
        # Construir mensaje con comentarios
        messages_text = "Comentarios recientes:\n"
        has_real_gifts = False
        has_fake_donations = False
        
        for username, comment, msg_type in comments_batch:
            if msg_type == "gift":
                messages_text += f"- {username} envió regalo REAL: {comment}\n"
                has_real_gifts = True
            elif self._detect_fake_donation(comment):
                messages_text += f"- {username} mencionó donación FALSA: {comment}\n"
                has_fake_donations = True
            else:
                messages_text += f"- {username}: {comment}\n"
        
        # Agregar contexto sobre regalos
        if has_real_gifts:
            messages_text += "\nIMPORTANTE: Agradece genuinamente los regalos REALES."
        if has_fake_donations:
            messages_text += "\nIMPORTANTE: Búrlate de las donaciones FALSAS mencionadas."
        
        try:
            # Llamar a OpenAI
            self.chat_history.append({"role": "user", "content": messages_text})
            
            response = self.openai_client.chat.completions.create(
                model="gpt-5-nano",
                messages=self.chat_history,
               # max_tokens=150
            )
            
            respuesta = response.choices[0].message.content.strip()
            self.chat_history.append({"role": "assistant", "content": respuesta})
            
            return respuesta
        
        except Exception as e:
            print(f"❌ Error OpenAI: {e}")
            return "Mi conexión con el más allá está fallando! Intenta después."
    
    def _handle_clarividente_mode(self, comments_batch):
        """Manejar modo clarividente"""
        # Buscar peticiones de predicción
        for username, comment, msg_type in reversed(comments_batch):
            prediction_keywords = [
                "futuro", "destino", "predice", "prediccion", "que pasara",
                "clarividente", "adivina", "horoscopo", "suerte", "amor"
            ]
            if any(keyword in comment.lower() for keyword in prediction_keywords):
                return self.managers['clarividente'].get_prediccion_for_user(username)
        
        # Respuesta mística general
        if comments_batch:
            username = comments_batch[-1][0]
            return self.managers['clarividente'].responder_a_comentario(username, "general")
        
        return self.managers['clarividente'].get_prediccion_generica()
    
    def _handle_acertijos_mode(self, comments_batch):
        """Manejar modo acertijos"""
        acertijos_manager = self.managers['acertijos']
        
        # Si hay acertijo activo, verificar respuestas
        if acertijos_manager.acertijo_actual:
            for username, comment, msg_type in comments_batch:
                # Comandos especiales
                if any(cmd in comment.lower() for cmd in ["pista", "ayuda", "hint"]):
                    return acertijos_manager.dar_pista()
                
                # Verificar respuesta
                resultado = acertijos_manager.verificar_respuesta(username, comment)
                if "Correcto" in resultado or "correcto" in resultado:
                    return resultado
            
            # Nadie acertó, dar pista
            return acertijos_manager.dar_pista()
        else:
            # No hay acertijo activo
            return acertijos_manager.get_acertijo_aleatorio()
    
    def _handle_amenazas_mode(self, comments_batch):
        """Manejar modo amenazas"""
        if comments_batch:
            username, comment, msg_type = comments_batch[-1]
            return self.managers['amenazas'].responder_comentario_terrorificamente(username, comment)
        
        return self.managers['amenazas'].get_amenaza_aleatoria()
    
    def _handle_cantante_mode(self, comments_batch):
        """Manejar modo cantante"""
        cantante_manager = self.managers['cantante']
        
        # Buscar peticiones de canciones
        for username, comment, msg_type in comments_batch:
            resultado = cantante_manager.handle_song_request(comment)
            if resultado:
                return resultado
        
        # Respuesta genérica cantante
        import random
        respuestas = [
            "¿Quieren una canción? ¡Mi voz es como un ángel caído!",
            "Mi repertorio es tan bueno que hasta los sordos lo evitan.",
            "¿Te gusta mi música o prefieres sufrir en silencio?"
        ]
        return random.choice(respuestas)
    
    def _detect_fake_donation(self, comment_text):
        """Detectar donaciones falsas en comentarios"""
        from response_handler import ResponseHandler
        return ResponseHandler.detect_fake_donation(comment_text)
    
    def _speak_response(self, response):
        """Reproducir respuesta usando audio manager"""
        if self.audio_manager and response:
            # Limpiar texto antes de hablar
            from response_handler import ResponseHandler
            clean_response = ResponseHandler.clean_text(response)
            self.audio_manager.speak_text(clean_response)
    
    def get_current_mode(self):
        """Obtener modo actual"""
        return self.current_mode
    
    def get_mode_name(self, mode_num=None):
        """Obtener nombre del modo"""
        if mode_num is None:
            mode_num = self.current_mode
        
        mode_names = {
            1: "Conversación con Chat",
            2: "Contar Chistes", 
            3: "Clarividente",
            4: "Acertijos",
            5: "Modo Terrorífico",
            6: "Modo Cantante",
            7: "Conversación con Público",
            8: "Conversación con Invitado"
        }
        return mode_names.get(mode_num, "Desconocido")
    
    def get_queue_status(self):
        """Obtener estado de la cola"""
        with self.queue_lock:
            return {
                'size': len(self.comment_queue),
                'processing': self.is_processing,
                'audio_playing': self.audio_manager.is_audio_playing() if self.audio_manager else False
            }
    
    def force_process_queue(self):
        """Forzar procesamiento de cola"""
        if not self.is_processing:
            threading.Thread(target=self._process_queue, daemon=True).start()
    
    def clear_queue(self):
        """Limpiar cola de comentarios"""
        with self.queue_lock:
            cleared_count = len(self.comment_queue)
            self.comment_queue.clear()
        return cleared_count