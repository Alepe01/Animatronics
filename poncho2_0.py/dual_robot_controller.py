import threading
import time
from mode_controller import ModeController
from robot_regalo_manager import RobotRegaloManager
from response_handler import ResponseHandler

class DualRobotController:
    """Controlador para sistema de dos robots: Poncho (principal) y Robot de Regalos"""
    
    def __init__(self, poncho_managers, audio_manager=None, openai_client=None, arduino_controller=None):
        # Robot Principal (Poncho) - maneja todo excepto regalos con voz de Jorge
        if audio_manager is None and arduino_controller is not None:
            from audio_manager import ArduinoAudioManager
            poncho_audio = ArduinoAudioManager(
                arduino_controller=arduino_controller,
                voice="es-MX-JorgeNeural"  # Voz de Jorge para Poncho
            )
        else:
            poncho_audio = audio_manager
            if poncho_audio:
                poncho_audio.set_voice("es-MX-JorgeNeural")
        
        self.poncho_controller = ModeController(poncho_managers, poncho_audio, openai_client)
        
        # Robot de Regalos - con su propio audio manager y voz de Álvaro
        self.robot_regalo = RobotRegaloManager(
            audio_manager=None,  # Crear uno nuevo
            arduino_controller=arduino_controller
        )
        
        # Configuración
        self.callbacks = []
        self.regalo_callbacks = []
        
        # Estado
        self.gift_processing_active = True
        self.last_gift_time = 0
        self.gift_timeout = 10  # Segundos sin regalo para resetear racha
        
        print("🤖 Dual Robot Controller inicializado")
        print("  - Poncho: Comentarios y conversación (Voz Jorge)")  
        print("  - Robot Regalos: Exclusivamente regalos (Voz Álvaro)")
    
    def register_poncho_callback(self, callback):
        """Registrar callback para el robot principal"""
        self.poncho_controller.register_callback(callback)
    
    def register_regalo_callback(self, callback):
        """Registrar callback para el robot de regalos"""
        self.regalo_callbacks.append(callback)
    
    def add_comment(self, username, comment, msg_type="comment"):
        """Dirigir comentario al robot apropiado"""
        if msg_type == "gift":
            # Dirigir al robot de regalos
            self._handle_gift(username, comment)
        else:
            # Dirigir al robot principal (Poncho) con THINKING mode
            self._handle_poncho_comment(username, comment, msg_type)
    
    def _handle_poncho_comment(self, username, comment, msg_type):
        """Manejar comentario de Poncho con modo THINKING"""
        try:
            # Activar THINKING mode en Poncho si tiene audio manager
            poncho_audio = self.poncho_controller.audio_manager
            if poncho_audio and hasattr(poncho_audio, 'start_thinking_mode'):
                poncho_audio.start_thinking_mode()
            
            # Procesar con el controlador de Poncho
            self.poncho_controller.add_comment(username, comment, msg_type)
            
        except Exception as e:
            print(f"❌ Error procesando comentario de Poncho: {e}")
    
    def _handle_gift(self, username, gift_info):
        """Manejar regalo con el robot especializado"""
        if not self.gift_processing_active:
            return
        
        try:
            # Parsear información del regalo
            gift_name, cantidad = self._parse_gift_info(gift_info)
            
            # Procesar con robot de regalos (incluye THINKING mode automático)
            response = self.robot_regalo.procesar_regalo(username, gift_name, cantidad)
            
            # Activar animación de Arduino para regalos
            if self.robot_regalo.audio_manager and self.robot_regalo.audio_manager.arduino:
                arduino = self.robot_regalo.audio_manager.arduino
                if arduino.is_connected():
                    if cantidad > 3:
                        arduino.send_command("GIFT_COMBO")
                    else:
                        arduino.send_command("GIFT")
            
            # Actualizar tiempo del último regalo
            self.last_gift_time = time.time()
            
            # Notificar callbacks del robot de regalos
            for callback in self.regalo_callbacks:
                try:
                    callback("gift", username, gift_info, response)
                except Exception as e:
                    print(f"❌ Error en callback de regalo: {e}")
            
            # Verificar si hay racha especial
            if self.robot_regalo.regalo_streak > 0 and self.robot_regalo.regalo_streak % 5 == 0:
                self._celebrate_streak()
            
        except Exception as e:
            print(f"❌ Error procesando regalo: {e}")
            # Respuesta de fallback
            fallback_response = f"¡Gracias {username}! ¡Tu regalo me llena de alegría!"
            for callback in self.regalo_callbacks:
                try:
                    callback("gift", username, gift_info, fallback_response)
                except:
                    pass
    
    def _parse_gift_info(self, gift_info):
        """Parsear información del regalo para extraer nombre y cantidad"""
        try:
            # Formato típico: "Rosa x3" o "León x1" o solo "Corazón"
            if " x" in gift_info:
                parts = gift_info.split(" x")
                gift_name = parts[0].strip()
                cantidad = int(parts[1]) if parts[1].isdigit() else 1
            else:
                gift_name = gift_info.strip()
                cantidad = 1
                
            return gift_name, cantidad
            
        except Exception as e:
            print(f"❌ Error parseando regalo: {e}")
            return gift_info, 1
    
    def _celebrate_streak(self):
        """Celebrar racha especial de regalos"""
        streak = self.robot_regalo.regalo_streak
        celebration = f"¡¡¡RACHA DE {streak} REGALOS!!! ¡¡¡LA GENEROSIDAD ESTÁ IMPARABLE!!!"
        
        # Activar animación de celebración en Arduino
        if self.robot_regalo.audio_manager and self.robot_regalo.audio_manager.arduino:
            arduino = self.robot_regalo.audio_manager.arduino
            if arduino.is_connected():
                arduino.send_command("GIFT_CELEBRATION")
        
        # Notificar celebration
        for callback in self.regalo_callbacks:
            try:
                callback("celebration", "Sistema", f"Racha x{streak}", celebration)
            except:
                pass
    
    def change_mode(self, new_mode):
        """Cambiar modo del robot principal (no afecta al robot de regalos)"""
        self.poncho_controller.change_mode(new_mode)
    
    def get_current_mode(self):
        """Obtener modo actual del robot principal"""
        return self.poncho_controller.get_current_mode()
    
    def get_mode_name(self, mode_num=None):
        """Obtener nombre del modo actual"""
        return self.poncho_controller.get_mode_name(mode_num)
    
    def toggle_gift_processing(self):
        """Activar/desactivar procesamiento de regalos"""
        self.gift_processing_active = not self.gift_processing_active
        status = "activado" if self.gift_processing_active else "desactivado"
        return f"🎁 Procesamiento de regalos {status}"
    
    def check_gift_timeout(self):
        """Verificar timeout de regalos y resetear racha si es necesario"""
        if self.last_gift_time > 0:
            time_since_last = time.time() - self.last_gift_time
            if time_since_last > self.gift_timeout:
                reset_message = self.robot_regalo.resetear_racha()
                if reset_message:
                    # Notificar reset de racha
                    for callback in self.regalo_callbacks:
                        try:
                            callback("system", "Robot Regalos", "Reset Racha", reset_message)
                        except:
                            pass
                self.last_gift_time = 0
    
    def force_process_poncho_queue(self):
        """Forzar procesamiento de cola de Poncho"""
        return self.poncho_controller.force_process_queue()
    
    def clear_poncho_queue(self):
        """Limpiar cola de Poncho"""
        return self.poncho_controller.clear_queue()
    
    def get_system_status(self):
        """Obtener estado del sistema dual"""
        poncho_status = self.poncho_controller.get_queue_status()
        
        status = {
            "poncho": {
                "modo": self.get_mode_name(),
                "cola": poncho_status['size'],
                "procesando": poncho_status['processing'],
                "audio": poncho_status['audio_playing'],
                "voz": "Jorge (es-MX-JorgeNeural)"
            },
            "regalo": {
                "activo": self.gift_processing_active,
                "racha_actual": self.robot_regalo.regalo_streak,
                "mejor_racha": self.robot_regalo.get_counter("estadisticas", "mejor_racha"),
                "total_regalos": self.robot_regalo.get_counter("estadisticas", "total_regalos"),
                "voz": "Álvaro (es-ES-AlvaroNeural)"
            },
            "sistema": {
                "ultimo_regalo": f"{time.time() - self.last_gift_time:.1f}s" if self.last_gift_time > 0 else "N/A"
            }
        }
        
        return status
    
    def get_combined_stats(self):
        """Obtener estadísticas combinadas de ambos robots"""
        poncho_managers = self.poncho_controller.managers
        
        stats = "📊 ESTADÍSTICAS SISTEMA DUAL:\n"
        stats += "=" * 50 + "\n\n"
        
        # Estado general
        status = self.get_system_status()
        stats += f"🤖 ROBOT PRINCIPAL (PONCHO) - VOZ JORGE:\n"
        stats += f"  Modo: {status['poncho']['modo']}\n"
        stats += f"  Cola: {status['poncho']['cola']} comentarios\n"
        stats += f"  Estado: {'Procesando' if status['poncho']['procesando'] else 'Esperando'}\n"
        stats += f"  Voz: {status['poncho']['voz']}\n\n"
        
        stats += f"🎁 ROBOT DE REGALOS - VOZ ÁLVARO:\n"
        stats += f"  Estado: {'Activo' if status['regalo']['activo'] else 'Inactivo'}\n"
        stats += f"  Racha actual: {status['regalo']['racha_actual']}\n"
        stats += f"  Mejor racha: {status['regalo']['mejor_racha']}\n"
        stats += f"  Total regalos: {status['regalo']['total_regalos']}\n"
        stats += f"  Voz: {status['regalo']['voz']}\n\n"
        
        # Estadísticas detalladas del robot de regalos
        stats += self.robot_regalo.get_estadisticas_regalos()
        
        return stats
    
    def handle_gift_combo(self, gifts_list):
        """Manejar múltiples regalos simultáneos"""
        if not self.gift_processing_active or not gifts_list:
            return
        
        try:
            # Procesar combo con robot de regalos
            combo_response = self.robot_regalo.procesar_combo_regalos(gifts_list)
            
            # Activar animación de combo en Arduino
            if self.robot_regalo.audio_manager and self.robot_regalo.audio_manager.arduino:
                arduino = self.robot_regalo.audio_manager.arduino
                if arduino.is_connected():
                    arduino.send_command("GIFT_COMBO")
            
            # Actualizar tiempo
            self.last_gift_time = time.time()
            
            # Notificar combo
            total_gifts = len(gifts_list)
            for callback in self.regalo_callbacks:
                try:
                    callback("combo", "Múltiples usuarios", f"{total_gifts} regalos", combo_response)
                except Exception as e:
                    print(f"Error en callback combo: {e}")
                    
        except Exception as e:
            print(f"Error procesando combo: {e}")
    
    def get_gift_suggestions(self):
        """Obtener sugerencias motivacionales para regalos"""
        return self.robot_regalo.generar_mensaje_motivacional()
    
    def answer_gift_question(self, username, question):
        """Responder pregunta sobre regalos con el robot especializado"""
        return self.robot_regalo.responder_pregunta_sobre_regalos(username, question)
    
    def test_voice_system(self):
        """Probar sistema de voces duales"""
        print("🗣️ Probando sistema de voces duales...")
        
        # Probar Poncho (Jorge)
        if self.poncho_controller.audio_manager:
            print("🤖 Poncho hablando con voz de Jorge...")
            self.poncho_controller.audio_manager.speak_text("Hola, soy Poncho con voz de Jorge de México")
            time.sleep(3)
        
        # Probar Robot Regalos (Álvaro)
        if self.robot_regalo.audio_manager:
            print("🎁 Robot Regalos hablando con voz de Álvaro...")
            self.robot_regalo.audio_manager.speak_text("¡Hola! Soy el Robot de Regalos con voz de Álvaro de España")
            time.sleep(3)
        
        print("✅ Prueba de voces completada")
    
    def cleanup(self):
        """Limpiar recursos de ambos robots"""
        if hasattr(self.poncho_controller, 'audio_manager'):
            self.poncho_controller.audio_manager.cleanup()
        
        if hasattr(self.robot_regalo, 'audio_manager') and self.robot_regalo.audio_manager:
            self.robot_regalo.audio_manager.cleanup()
        
        for manager in self.poncho_controller.managers.values():
            if hasattr(manager, 'cleanup'):
                manager.cleanup()

# Integración con el sistema principal
def integrate_dual_robots(managers_dict, audio_manager, openai_client, arduino_controller=None):
    """Integrar sistema de dos robots al sistema existente"""
    dual_controller = DualRobotController(
        managers_dict, 
        audio_manager, 
        openai_client,
        arduino_controller
    )
    
    print("🤖 Sistema Dual Robot integrado:")
    print("  - Poncho: Maneja comentarios, conversación y todos los modos (Voz Jorge)")
    print("  - Robot Regalos: Maneja exclusivamente regalos con energía máxima (Voz Álvaro)")
    print("  - Arduino: Controla ambos robots con animaciones específicas")
    
    return dual_controller

# Ejemplo de uso
if __name__ == "__main__":
    print("🤖 Probando Dual Robot Controller con voces duales...")
    
    # Simular managers (mock)
    mock_managers = {
        'chistes': type('MockManager', (), {'get_random_joke': lambda: "Chiste de prueba"})(),
        'conversacion_publico': type('MockManager', (), {})()
    }
    
    # Crear controlador dual
    dual_controller = DualRobotController(mock_managers)
    
    print("\n💬 Probando comentarios normales (van a Poncho con Jorge):")
    dual_controller.add_comment("Juan", "Hola Poncho", "comment")
    dual_controller.add_comment("Ana", "¿Cómo estás?", "comment")
    
    print("\n🎁 Probando regalos (van al Robot de Regalos con Álvaro):")
    dual_controller.add_comment("Pedro", "Rosa x1", "gift")
    dual_controller.add_comment("María", "León x1", "gift")
    dual_controller.add_comment("Carlos", "Corazón x5", "gift")
    
    print("\n🎁 Probando combo de regalos:")
    combo_gifts = [
        ("User1", "Estrella", 1),
        ("User2", "Corazón", 2),
        ("User3", "Rosa", 1)
    ]
    dual_controller.handle_gift_combo(combo_gifts)
    
    print("\n📊 Estado del sistema:")
    status = dual_controller.get_system_status()
    for robot, data in status.items():
        print(f"{robot}: {data}")
    
    print("\n🗣️ Probando sistema de voces:")
    dual_controller.test_voice_system()
    
    print("\n✅ Pruebas completadas")