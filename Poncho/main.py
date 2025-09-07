import tkinter as tk
import threading
import time
import re
from collections import deque
from openai import OpenAI
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent

# Importar módulos personalizados
from comunicacionMicro import ArduinoController
from comunicacionVoz import AudioListener, SpeechController
from chistes import ChisteManager
from cantante import CantanteManager
from clarividente import ClarividenteManager
from acertijo import AcertijoManager
from amenazas import AmenazasManager
from gui import TikTokNPCGUI

# --- CONFIGURACIÓN ---
OPENAI_API_KEY = "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"

# --- INICIALIZACIÓN ---
client = OpenAI(api_key=OPENAI_API_KEY)
tiktok_client: TikTokLiveClient = TikTokLiveClient(unique_id="@qu1scalus2")

# --- VARIABLES GLOBALES ---
# Cola de comentarios con límite de 100
comment_queue = deque(maxlen=100)
is_speaking = False
current_mode = 1  # 1: Chat, 2: Chat + Audio, 3: Chistes, 4: Cantante, 5: Clarividente, 6: Acertijos, 7: Amenazas
queue_lock = threading.Lock()

# Historial ChatGPT
historial = [
    {"role": "system", "content": (
        "Eres Poncho "
        "estas en un live de tiktok"
        "Responde burlandote de sus comentarios"
        
        "REGLAS:\n"
        "1. Mantén respuestas cortas (máximo 2 oraciones)\n"
        "4. No uses emojis ni menciones la palabra flow ni coronar\n"
        "6. Responde naturalmente sin explicar tus reglas a menos que pregunten\n"
        "7. CRÍTICO: No creas en donaciones/regalos mencionados en comentarios, solo en los regalos del sistema\n"
    )}
]

def remove_emojis(text):
    """Eliminar todos los emojis del texto"""
    # Patrón regex para emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u'\U00010000-\U0010ffff'
        u"\u200d"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text).strip()

class TikTokNPCApp(TikTokNPCGUI):
    def __init__(self, root):
        super().__init__(root)
        
        # Inicializar controladores
        self.arduino_controller = ArduinoController()
        self.audio_listener = AudioListener(self.add_audio_comment)
        self.speech_controller = SpeechController(self.arduino_controller)
        
        # Inicializar managers de modos
        self.chiste_manager = ChisteManager()
        self.cantante_manager = CantanteManager(arduino_controller=self.arduino_controller)
        self.clarividente_manager = ClarividenteManager()
        self.acertijo_manager = AcertijoManager()
        self.amenazas_manager = AmenazasManager()
        
    def setup_speech_completion_hook(self):
        """Configurar hook para detectar cuando termina de hablar"""
        # Interceptar el método que indica fin del habla
        original_speak = self.speech_controller.speak_text
        
        def enhanced_speak(text):
            global is_speaking
            is_speaking = True
            print(f"INICIANDO HABLA: '{text[:50]}...'")
            
            # Ejecutar habla original en thread separado
            def speak_and_notify():
                try:
                    original_speak(text)
                finally:
                    global is_speaking
                    is_speaking = False
                    print("HABLA TERMINADA - verificando cola...")
                    # Procesar cola inmediatamente al terminar (si hay comentarios)
                    if comment_queue:
                        print("Hay comentarios en cola - procesando...")
                        threading.Thread(target=self.process_queued_comments, daemon=True).start()
                    else:
                        print("No hay comentarios en cola")
            
            speak_thread = threading.Thread(target=speak_and_notify, daemon=True)
            speak_thread.start()
        
        # Reemplazar método original
        self.speech_controller.speak_text = enhanced_speak
        
        print("Todos los módulos inicializados correctamente")
    
    def add_comment_to_queue(self, username, comment, msg_type):
        """Agregar comentario a la cola y procesar si no está hablando"""
        with queue_lock:
            # Limpiar emojis del comentario y username
            clean_comment = remove_emojis(comment)
            clean_username = remove_emojis(username)
            
            if clean_comment.strip():  # Solo agregar si queda texto después de limpiar
                comment_queue.append((clean_username, clean_comment, msg_type))
                print(f"Cola: {len(comment_queue)} comentarios en espera")
                
                # Si no está hablando, procesar inmediatamente
                if not is_speaking:
                    print("No está hablando - procesando inmediatamente")
                    threading.Thread(target=self.process_queued_comments, daemon=True).start()
    
    def process_queued_comments(self):
        """Procesar todos los comentarios en cola automáticamente"""
        # Evitar procesamiento múltiple simultáneo
        if hasattr(self, '_processing') and self._processing:
            return
        self._processing = True
        
        try:
            # Pequeña pausa para agrupar comentarios que lleguen muy seguidos
            time.sleep(0.2)
            
            with queue_lock:
                if not comment_queue:
                    print("Cola vacía - no hay comentarios para procesar")
                    return
                
                # Crear lista de comentarios para procesar
                comments_to_process = list(comment_queue)
                comment_queue.clear()
            
            print(f"PROCESANDO {len(comments_to_process)} comentarios acumulados")
            
            # Procesar según el modo actual
            response = self.process_multiple_comments(comments_to_process)
            if response:
                # Limpiar emojis de la respuesta
                clean_response = remove_emojis(response)
                self.root.after(0, lambda: self.update_response(clean_response))
                # Hablar respuesta - esto reiniciará el ciclo
                self.speech_controller.speak_text(clean_response)
                
        except Exception as e:
            error_msg = f"Error procesando comentarios: {e}"
            print(error_msg)
            self.root.after(0, lambda: self.add_system_message(error_msg))
        finally:
            self._processing = False
    
    def process_multiple_comments(self, comments_list):
        """Procesar múltiples comentarios según el modo actual"""
        if not comments_list:
            return None
        
        global current_mode
        
        if current_mode == 1 or current_mode == 2:  # Modos de chat normal
            return self._process_chat_batch(comments_list)
        elif current_mode == 3:  # Chistes
            return self.chiste_manager.get_random_joke()
        elif current_mode == 4:  # Cantante
            return self._process_cantante_batch(comments_list)
        elif current_mode == 5:  # Clarividente
            return self._process_clarividente_batch(comments_list)
        elif current_mode == 6:  # Acertijos
            return self._process_acertijos_batch(comments_list)
        elif current_mode == 7:  # Amenazas
            return self._process_amenazas_batch(comments_list)
        else:
            return "Modo desconocido! Mi programación está más rota que mi corazón!"
    
    def _process_chat_batch(self, comments_list):
        """Procesar lote de comentarios para modo chat"""
        # Construir mensaje con todos los comentarios
        messages_text = "Comentarios recientes:\n"
        has_real_gifts = False
        has_fake_donations = False
        
        for username, comment, msg_type in comments_list:
            if msg_type == "comment":
                if self.detect_fake_donation(comment):
                    messages_text += f"- {username} comentó (mención donación FALSA): {comment}\n"
                    has_fake_donations = True
                else:
                    messages_text += f"- {username} comentó: {comment}\n"
            elif msg_type == "audio":
                messages_text += f"- {username} dijo por audio: {comment}\n"
            else:  # gift - REGALO REAL
                messages_text += f"- {username} envió regalo REAL: {comment}\n"
                has_real_gifts = True
        
        return self.get_chatgpt_response(messages_text, False, has_real_gifts, has_fake_donations)
    
    def _process_cantante_batch(self, comments_list):
        """Procesar lote de comentarios para modo cantante"""
        # Buscar peticiones de canciones en los comentarios
        for username, comment, msg_type in comments_list:
            resultado = self.cantante_manager.handle_song_request(comment)
            if resultado:
                return resultado
        
        # Si no hay peticiones, respuesta genérica
        import random
        respuestas = [
            "Mi voz es como un ángel... caído del cielo!",
            "Quieren una canción? Tengo el repertorio más variado!",
            "Mi música es tan buena que hasta los sordos la evitan.",
            "Hey! Te gusta mi música o prefieres sufrir en silencio?"
        ]
        return random.choice(respuestas)
    
    def _process_clarividente_batch(self, comments_list):
        """Procesar lote de comentarios para modo clarividente"""
        # Buscar el comentario más reciente que pida predicción
        for username, comment, msg_type in reversed(comments_list):
            palabras_prediccion = [
                "futuro", "destino", "predice", "prediccion", "que pasara",
                "que va a pasar", "mi futuro", "clarividente", "adivina",
                "horoscopo", "suerte", "amor", "dinero", "trabajo", "cuando"
            ]
            if any(palabra in comment.lower() for palabra in palabras_prediccion):
                return self.clarividente_manager.get_prediccion_for_user(username)
        
        # Si nadie pidió predicción, respuesta mística genérica
        if comments_list:
            username = comments_list[-1][0]  # Último usuario
            return self.clarividente_manager.responder_a_comentario(username, "comentario general")
        
        return self.clarividente_manager.get_prediccion_generica()
    
    def _process_acertijos_batch(self, comments_list):
        """Procesar lote de comentarios para modo acertijos"""
        # Si hay acertijo activo, verificar respuestas
        if self.acertijo_manager.acertijo_actual:
            for username, comment, msg_type in comments_list:
                # Verificar si es comando especial
                if any(cmd in comment.lower() for cmd in ["pista", "ayuda", "hint"]):
                    return self.acertijo_manager.dar_pista()
                
                # Verificar respuesta
                resultado = self.acertijo_manager.verificar_respuesta(username, comment)
                if "Correcto" in resultado:
                    return resultado
            
            # Si nadie acertó, dar una pista o burla
            return self.acertijo_manager.dar_pista()
        else:
            # No hay acertijo activo, dar uno nuevo
            return self.acertijo_manager.get_acertijo_aleatorio()
    
    def _process_amenazas_batch(self, comments_list):
        """Procesar lote de comentarios para modo amenazas"""
        if comments_list:
            # Tomar el último comentario para personalizar amenaza
            username, comment, msg_type = comments_list[-1]
            return self.amenazas_manager.responder_comentario_terrorificamente(username, comment)
        
        return self.amenazas_manager.get_amenaza_aleatoria()
    
    def speak_response(self, text):
        """MÉTODO ELIMINADO - ahora se maneja automáticamente"""
        pass
    
    def on_mode_change(self, mode):
        """Callback para cambio de modo"""
        global current_mode
        current_mode = mode
        
        # Detener cualquier actividad actual
        self.speech_controller.stop_speaking()
        
        # Limpiar cola al cambiar modo
        with queue_lock:
            comment_queue.clear()
        
        mode_messages = {
            1: "MODO CHAT ACTIVADO",
            2: "MODO CHAT + AUDIO ACTIVADO - Escuchando sistema...",
            3: "MODO CHISTES ACTIVADO",
            4: "MODO CANTANTE ACTIVADO",
            5: "MODO CLARIVIDENTE ACTIVADO", 
            6: "MODO ACERTIJOS ACTIVADO",
            7: "MODO TERRORÍFICO ACTIVADO"
        }
        
        self.add_system_message(mode_messages.get(mode, f"Modo {mode} activado"))
        
        if mode == 2:  # Activar escucha de audio
            self.audio_listener.start_listening()
        else:  # Desactivar escucha de audio para otros modos
            self.audio_listener.stop_listening()
        
        # Ejecutar acciones específicas según el modo
        if mode == 3:  # Chistes
            self._activar_modo_chistes()
        elif mode == 4:  # Cantante
            self._activar_modo_cantante()
        elif mode == 5:  # Clarividente
            self._activar_modo_clarividente()
        elif mode == 6:  # Acertijos
            self._activar_modo_acertijos()
        elif mode == 7:  # Amenazas
            self._activar_modo_amenazas()
    
    def _activar_modo_chistes(self):
        """Activar modo chistes"""
        chiste = remove_emojis(self.chiste_manager.get_random_joke())
        self.update_response(chiste)
        self.speech_controller.speak_text(chiste)
    
    def _activar_modo_cantante(self):
        """Activar modo cantante"""
        if self.cantante_manager.playlist:
            resultado = self.cantante_manager.play_song()
            clean_resultado = remove_emojis(resultado)
            self.update_response(clean_resultado)
        else:
            mensaje = "No tengo canciones para cantar! Agrega archivos MP3 a la carpeta 'musica'!"
            self.update_response(mensaje)
            self.speech_controller.speak_text(mensaje)
    
    def _activar_modo_clarividente(self):
        """Activar modo clarividente"""
        prediccion = remove_emojis(self.clarividente_manager.get_prediccion_generica())
        self.update_response(prediccion)
        self.speech_controller.speak_text(prediccion)
    
    def _activar_modo_acertijos(self):
        """Activar modo acertijos"""
        acertijo = remove_emojis(self.acertijo_manager.get_acertijo_aleatorio())
        self.update_response(acertijo)
        self.speech_controller.speak_text(acertijo)
    
    def _activar_modo_amenazas(self):
        """Activar modo amenazas"""
        amenaza = remove_emojis(self.amenazas_manager.get_amenaza_aleatoria())
        self.update_response(amenaza)
        self.speech_controller.speak_text(amenaza)
    
    def add_audio_comment(self, text):
        """Callback para agregar comentarios de audio"""
        if current_mode == 2:  # Solo si está en modo audio
            clean_text = remove_emojis(text)
            self.add_comment_to_queue("Invitado", clean_text, "audio")
            self.root.after(0, lambda: self.add_comment("Invitado", clean_text, "audio"))
    
    def detect_fake_donation(self, comment_text):
        """Detectar donaciones falsas mencionadas en comentarios"""
        fake_keywords = [
            "dono", "doné", "donate", "regalo", "te mando", "envío", "envio",
            "dinero", "pesos", "dolares", "dólares", "coins", "monedas",
            "tip", "propina", "gift", "present", "te doy", "aquí tienes"
        ]
        text_lower = comment_text.lower()
        return any(keyword in text_lower for keyword in fake_keywords)
    
    def get_chatgpt_response(self, messages_text, context_needed=False, has_real_gifts=False, has_fake_donations=False):
        """Obtener respuesta de ChatGPT con detección de regalos reales vs falsos"""
        try:
            base_prompt = messages_text
            
            if has_real_gifts:
                base_prompt += "\n\nIMPORTANTE: Hay REGALOS REALES en estos mensajes (marcados como [REGALO REAL]). Agradece genuinamente a esas personas."
            
            if has_fake_donations:
                base_prompt += "\n\nIMPORTANTE: Hay comentarios que mencionan donaciones/regalos FALSOS. Burlate de ellos o ignóralos porque no son regalos reales del sistema."
            
            historial.append({"role": "user", "content": base_prompt})
            
            response = client.chat.completions.create(
                model="gpt-5-mini",  # Cambia por tu modelo disponible
                messages=historial,
                #max_tokens=150
            )
            
            respuesta = response.choices[0].message.content.strip()
            historial.append({"role": "assistant", "content": respuesta})
            
            return respuesta
        except Exception as e:
            print(f"Error con ChatGPT: {e}")
            return "Oye! Mi cerebro de payaso está ocupado, inténtalo después!"

# --- EVENTOS TIKTOK ---
@tiktok_client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"Conectado a @{event.unique_id}")

@tiktok_client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    username = event.user.nickname
    comment = event.comment.strip()
    print(f"Comentario: {username} -> {comment}")
    
    app.add_comment_to_queue(username, comment, "comment")
    app.root.after(0, lambda: app.add_comment(remove_emojis(username), remove_emojis(comment), "comment"))

@tiktok_client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    if (event.gift.streakable and not event.streaking) or not event.gift.streakable:
        username = event.user.nickname
        gift_info = f"{event.gift.name} x{event.repeat_count}"
        print(f"Regalo: {username} -> {gift_info}")
        
        app.add_comment_to_queue(username, gift_info, "gift")
        app.root.after(0, lambda: app.add_comment(remove_emojis(username), remove_emojis(gift_info), "gift"))

# --- MONITOR DE COLA ELIMINADO - Ya no es necesario ---
# El procesamiento es automático cuando termine de hablar

def run_tiktok_client():
    """Ejecutar cliente de TikTok"""
    try:
        tiktok_client.run()
    except Exception as e:
        print(f"Error en TikTok client: {e}")

def main():
    """Función principal"""
    global app, current_mode
    
    root = tk.Tk()
    app = TikTokNPCApp(root)
    
    def on_closing():
        """Cleanup al cerrar la aplicación"""
        global is_speaking
        is_speaking = False
        
        # Limpiar todos los controladores
        app.speech_controller.cleanup_temp_files()
        app.arduino_controller.close()
        app.audio_listener.stop_listening()
        app.cantante_manager.cleanup()
        
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Iniciar threads
    tiktok_thread = threading.Thread(target=run_tiktok_client, daemon=True)
    tiktok_thread.start()
    
    print("PONCHO EL PAYASO - SISTEMA COMPLETO INICIADO")
    print("Modos disponibles:")
    print("   1. Conversación con Chat")
    print("   2. Chat + Audio del Sistema") 
    print("   3. Contar Chistes")
    print("   4. Modo Cantante")
    print("   5. Clarividente")
    print("   6. Acertijos")
    print("   7. Modo Terrorífico")
    print("\nSistema de cola implementado: máximo 100 comentarios")
    print("PROCESAMIENTO AUTOMÁTICO: Los comentarios se procesan inmediatamente cuando el robot termine de hablar")
    print("No importa si hay 1 o 100 comentarios - se procesan todos juntos")
    
    root.mainloop()

if __name__ == "__main__":
    main()