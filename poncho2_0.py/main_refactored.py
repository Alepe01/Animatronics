import tkinter as tk
import threading
import time
import serial
import serial.tools.list_ports
from openai import OpenAI
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent

# Importar módulos refactorizados
from base_manager import BaseManager
from response_handler import ResponseHandler
from audio_manager import ArduinoAudioManager, AudioListener
from mode_controller import ModeController
from chistes_refactored import ChisteManager
from acertijos_refactored import AcertijoManager
from amenazas_refactored import AmenazasManager
from clarividente_refactored import ClarividenteManager
from cantante_refactored import CantanteManager
from conversacion_publico import ConversacionPublicoManager
from conversacion_invitado import ConversacionInvitadoManager
from dual_robot_controller import DualRobotController
from gui_refactored import RefactoredGUI

# Configuración
OPENAI_API_KEY = "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"
TIKTOK_USERNAME = "@qu1scalus2"
ARDUINO_PORT = "COM16"  # Puerto del Arduino

class ArduinoController:
    """Controlador Arduino integrado"""
    
    def __init__(self, port="COM16", baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.connected = False
        self.connect()
    
    def connect(self):
        """Establecer conexión con Arduino"""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
            self.connected = True
            print(f"✅ Arduino conectado en {self.port}")
            self.send_command("RESET")
        except Exception as e:
            print(f"❌ Error conectando Arduino: {e}")
            self.ser = None
            self.connected = False
    
    def send_command(self, command):
        """Enviar comando al Arduino"""
        if not self.connected or not self.ser:
            return False
        
        try:
            command_bytes = f"{command}\n".encode()
            self.ser.write(command_bytes)
            time.sleep(0.1)
            print(f"📤 Arduino: {command}")
            return True
        except Exception as e:
            print(f"❌ Error enviando comando: {e}")
            return False
    
    # Comandos para Poncho
    def start_talking(self):
        return self.send_command("TALK")
    
    def start_thinking(self):
        return self.send_command("THINKING")
    
    def stop_talking(self):
        return self.send_command("STOP")
    
    def happy_animation(self):
        return self.send_command("HAPPY")
    
    def sad_animation(self):
        return self.send_command("SAD")
    
    def angry_animation(self):
        return self.send_command("ANGRY")
    
    def blink_animation(self):
        return self.send_command("BLINK")
    
    # Comandos para Robot de Regalos
    def gift_animation(self):
        return self.send_command("GIFT")
    
    def gift_combo_animation(self):
        return self.send_command("GIFT_COMBO")
    
    def gift_celebration_animation(self):
        return self.send_command("GIFT_CELEBRATION")
    
    def gift_stop_animation(self):
        return self.send_command("GIFT_STOP")
    
    # Comandos generales
    def reset_position(self):
        return self.send_command("RESET")
    
    def test_dual_system(self):
        return self.send_command("TEST_DUAL")
    
    def is_connected(self):
        return self.connected and self.ser is not None
    
    def close(self):
        if self.ser:
            try:
                self.ser.close()
                print("🔌 Conexión Arduino cerrada")
            except:
                pass
        self.connected = False
        self.ser = None

def find_arduino_port():
    """Buscar puerto del Arduino automáticamente"""
    try:
        ports = serial.tools.list_ports.comports()
        arduino_keywords = ['arduino', 'ch340', 'cp2102', 'ftdi', 'usb serial']
        
        for port in ports:
            description = port.description.lower()
            for keyword in arduino_keywords:
                if keyword in description:
                    return port.device
        
        # Si no encuentra, usar el puerto por defecto
        return ARDUINO_PORT
    except Exception:
        return ARDUINO_PORT

class RefactoredNPCApp:
    """Aplicación principal refactorizada con Arduino integrado y voces duales"""
    
    def __init__(self):
        print("🤖 Inicializando Poncho el Payaso - Versión con Arduino y Voces Duales")
        
        # Inicializar Arduino primero
        self.setup_arduino()
        
        # Inicializar componentes base
        self.setup_openai()
        self.setup_tiktok()
        
        # Inicializar managers usando clases refactorizadas
        self.managers = {
            'chistes': ChisteManager(),
            'acertijos': AcertijoManager(), 
            'amenazas': AmenazasManager(),
            'clarividente': ClarividenteManager(),
            'cantante': CantanteManager(),
            'conversacion_publico': ConversacionPublicoManager(),
            'conversacion_invitado': ConversacionInvitadoManager()
        }
        
        print("✅ Managers inicializados:")
        for name in self.managers.keys():
            print(f"  - {name}")
        
        # NO crear audio_manager aquí - dejar que cada robot cree el suyo
        self.audio_listener = AudioListener(self.handle_audio_input)
        
        # Inicializar controlador dual con Arduino - sin audio_manager
        self.dual_controller = DualRobotController(
            self.managers,
            audio_manager=None,  # Cada robot creará el suyo
            openai_client=self.openai_client,
            arduino_controller=self.arduino_controller  # Pasar arduino controller
        )
        
        # Para compatibilidad, usar el audio manager de Poncho como principal
        self.audio_manager = self.dual_controller.poncho_controller.audio_manager
        
        # Configurar callbacks
        self.dual_controller.register_poncho_callback(self.on_mode_change)
        self.dual_controller.register_regalo_callback(self.on_gift_received)
        
        # Crear referencia para ventana de pruebas
        self.dual_controller.parent_app = self
        
        # Inicializar GUI pasando el controlador dual
        self.root = tk.Tk()
        self.gui = RefactoredGUI(self.root, self.dual_controller)
        
        # Conectar GUI con aplicación principal para ventana de pruebas
        self.gui.parent_app = self
        
        print("✅ Sistema dual robot con Arduino inicializado completamente")
        print("🗣️ Poncho habla con voz de Jorge, Robot Regalos con voz de Álvaro")
    
    def setup_arduino(self):
        """Configurar conexión con Arduino"""
        try:
            # Buscar puerto automáticamente
            arduino_port = find_arduino_port()
            print(f"🔍 Intentando conectar Arduino en {arduino_port}")
            
            self.arduino_controller = ArduinoController(arduino_port)
            
            if self.arduino_controller.is_connected():
                print("✅ Arduino conectado correctamente")
                # Probar el sistema dual
                self.arduino_controller.test_dual_system()
            else:
                print("⚠️ Arduino no conectado - funcionará sin animaciones físicas")
                
        except Exception as e:
            print(f"❌ Error configurando Arduino: {e}")
            self.arduino_controller = None
    
    def setup_openai(self):
        """Configurar OpenAI"""
        try:
            if OPENAI_API_KEY and OPENAI_API_KEY != "tu-api-key-aqui":
                self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
                print("✅ OpenAI configurado")
            else:
                self.openai_client = None
                print("⚠️ OpenAI no configurado - usando respuestas automáticas")
        except Exception as e:
            print(f"❌ Error configurando OpenAI: {e}")
            self.openai_client = None
    
    def setup_tiktok(self):
        """Configurar cliente de TikTok"""
        try:
            if TIKTOK_USERNAME and TIKTOK_USERNAME != "@tu-usuario-aqui":
                self.tiktok_client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)
                self.setup_tiktok_events()
                print("✅ TikTok cliente configurado")
            else:
                self.tiktok_client = None
                print("⚠️ TikTok no configurado - modo offline")
        except Exception as e:
            print(f"❌ Error configurando TikTok: {e}")
            self.tiktok_client = None
    
    def setup_tiktok_events(self):
        """Configurar eventos de TikTok usando decoradores"""
        @self.tiktok_client.on(ConnectEvent)
        async def on_connect(event):
            message = f"Conectado a TikTok: {event.unique_id}"
            self.gui.add_system_message(message)
            print(f"🔗 {message}")
        
        @self.tiktok_client.on(CommentEvent)
        async def on_comment(event):
            username = ResponseHandler.clean_text(event.user.nickname)
            comment = ResponseHandler.clean_text(event.comment)
            
            if username and comment:
                self.handle_comment(username, comment, "comment")
        
        @self.tiktok_client.on(GiftEvent)
        async def on_gift(event):
            if (event.gift.streakable and not event.streaking) or not event.gift.streakable:
                username = ResponseHandler.clean_text(event.user.nickname)
                gift_info = f"{event.gift.name} x{event.repeat_count}"
                gift_info = ResponseHandler.clean_text(gift_info)
                
                if username and gift_info:
                    self.handle_comment(username, gift_info, "gift")
    
    def handle_comment(self, username, comment, msg_type):
        """Manejar comentario dirigiéndolo al robot apropiado con sistema de voces"""
        # El DualRobotController se encarga de dirigir automáticamente
        # Incluye THINKING mode automático para Poncho
        self.dual_controller.add_comment(username, comment, msg_type)
        
        # Solo agregar a GUI los comentarios normales (no regalos)
        if msg_type != "gift":
            self.root.after(0, lambda: self.gui.add_comment(username, comment, msg_type))
            print(f"💬 {msg_type.upper()}: {username} -> {comment}")
        # Los regalos se manejan en on_gift_received
    
    def handle_audio_input(self, text):
        """Manejar entrada de audio"""
        clean_text = ResponseHandler.clean_text(text)
        if clean_text:
            self.handle_comment("Audio", clean_text, "audio")
    
    def on_gift_received(self, event_type, username, gift_info, response):
        """Callback para cuando el robot de regalos procesa un regalo"""
        # Las animaciones de Arduino ya se manejan en DualRobotController
        
        # Actualizar GUI
        if event_type == "gift":
            self.root.after(0, lambda: self.gui.add_gift(username, gift_info, response))
            print(f"🎁 REGALO: {username} -> {gift_info}")
            print(f"🤖 Robot Regalos (Álvaro): {response[:50]}...")
            
        elif event_type == "combo":
            self.root.after(0, lambda: self.gui.add_gift_combo(username, gift_info, response))
            print(f"🎁 COMBO: {gift_info}")
            
        elif event_type == "celebration":
            self.root.after(0, lambda: self.gui.add_celebration(gift_info, response))
            print(f"🎉 CELEBRACIÓN: {gift_info}")
            
        elif event_type == "system":
            self.root.after(0, lambda: self.gui.add_system_message(f"🎁 {response}"))
    
    def on_mode_change(self, new_mode, old_mode):
        """Callback para cambio de modo con animaciones Arduino"""
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
        
        message = f"🤖 Poncho cambió: {mode_names.get(old_mode, 'Desconocido')} → {mode_names.get(new_mode, 'Desconocido')}"
        self.gui.add_system_message(message)
        self.gui.add_system_message("🎁 Robot de Regalos sigue activo independientemente")
        
        # Animaciones específicas según modo
        if self.arduino_controller and self.arduino_controller.is_connected():
            if new_mode == 2:  # Chistes
                self.arduino_controller.happy_animation()
            elif new_mode == 3:  # Clarividente
                self.arduino_controller.blink_animation()
            elif new_mode == 5:  # Terrorífico
                self.arduino_controller.angry_animation()
            elif new_mode == 6:  # Cantante
                self.arduino_controller.happy_animation()
        
        # Configurar funcionalidades específicas según modo
        if new_mode == 7:  # Conversación con Público
            self.gui.add_system_message("💬 Poncho: Modo conversación pública activado")
        elif new_mode == 8:  # Conversación con Invitado
            self.gui.add_system_message("🎙️ Poncho: Modo entrevista activado")
    
    def run_tiktok_client(self):
        """Ejecutar cliente de TikTok en thread separado"""
        if self.tiktok_client:
            try:
                self.tiktok_client.run()
            except Exception as e:
                error_msg = f"Error en TikTok client: {e}"
                print(f"❌ {error_msg}")
                self.root.after(0, lambda: self.gui.add_system_message(error_msg))
    
    def start_application(self):
        """Iniciar la aplicación completa"""
        # Configurar cleanup al cerrar
        def on_closing():
            self.cleanup()
            self.root.destroy()
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Iniciar thread de TikTok
        if self.tiktok_client:
            tiktok_thread = threading.Thread(target=self.run_tiktok_client, daemon=True)
            tiktok_thread.start()
        
        # Mostrar información inicial
        self.show_startup_info()
        
        # Iniciar GUI
        print("🚀 Iniciando interfaz gráfica...")
        self.root.mainloop()
    
    def show_startup_info(self):
        """Mostrar información de inicio del sistema con Arduino y voces duales"""
        arduino_status = "✅ Conectado" if (self.arduino_controller and self.arduino_controller.is_connected()) else "❌ Desconectado"
        
        info_messages = [
            "🤡 PONCHO EL PAYASO - SISTEMA DUAL ROBOT + ARDUINO + VOCES DUALES v2.4",
            "",
            "🆕 NUEVA CARACTERÍSTICA: SISTEMA DE VOCES DUALES",
            "  🤖 ROBOT PRINCIPAL (PONCHO): Voz de Jorge (México) + animaciones físicas",
            "  🎁 ROBOT DE REGALOS: Voz de Álvaro (España) + servo 360°",
            f"  🔌 ARDUINO: {arduino_status}",
            "  🧠 THINKING MODE: LEDs PWM suave durante procesamiento",
            "",
            "✅ Separación de funciones:",
            "  - Poncho: Sarcástico, maneja todos los modos + movimientos físicos (Jorge)", 
            "  - Robot Regalos: Súper energético + animaciones de regalo (Álvaro)",
            "  - Arduino: Controla servos y LEDs en tiempo real",
            "",
            f"🎮 Modos disponibles para Poncho: {len(self.managers)} + Chat = 8 modos",
            f"🎁 Robot Regalos: Especializado 100% en agradecer regalos",
            f"🎵 Canciones: {len(self.managers['cantante'].playlist)}",
            f"🧩 Acertijos: {len(self.managers['acertijos'].data.get('acertijos', []))}",
            f"😂 Chistes: {len(self.managers['chistes'].data.get('chistes', []))}",
            "",
            "⚡ VENTAJAS DEL SISTEMA DUAL + ARDUINO + VOCES:",
            "  - Regalos procesados instantáneamente con animaciones físicas",
            "  - Poncho habla con voz masculina mexicana (Jorge)", 
            "  - Robot Regalos con voz masculina española (Álvaro)",
            "  - THINKING mode con LEDs PWM suave durante procesamiento",
            "  - LEDs sincronizados con audio y emociones",
            "🔄 Procesamiento paralelo optimizado + hardware integrado + voces distintivas"
        ]
        
        for message in info_messages:
            if message:
                print(message)
                self.gui.add_system_message(message)
            time.sleep(0.1)
    
    def get_system_stats(self):
        """Obtener estadísticas del sistema dual con Arduino y voces"""
        base_stats = self.dual_controller.get_combined_stats()
        
        arduino_info = ""
        if self.arduino_controller:
            status = "Conectado" if self.arduino_controller.is_connected() else "Desconectado"
            arduino_info = f"\n🔌 ARDUINO:\n  Estado: {status}\n  Puerto: {self.arduino_controller.port}\n"
        
        voice_info = "\n🗣️ SISTEMA DE VOCES:\n"
        voice_info += "  Poncho (Principal): Jorge (es-MX-JorgeNeural) - México\n"
        voice_info += "  Robot Regalos: Álvaro (es-ES-AlvaroNeural) - España\n"
        
        return base_stats + arduino_info + voice_info
    
    def test_all_systems(self):
        """Probar todos los sistemas incluido Arduino y voces"""
        print("🧪 Probando todos los sistemas con Arduino y voces duales...")
        
        # Probar Arduino primero
        if self.arduino_controller and self.arduino_controller.is_connected():
            print("🔧 Probando Arduino...")
            self.arduino_controller.test_dual_system()
            time.sleep(3)
        
        # Probar sistema de voces
        print("🗣️ Probando sistema de voces duales...")
        self.dual_controller.test_voice_system()
        time.sleep(4)
        
        # Probar modos de Poncho
        test_username = "TestUser"
        test_comments = [
            ("Hola Poncho", "comment", 1),
            ("Cuenta un chiste", "comment", 2),
            ("¿Cuál es mi futuro?", "comment", 3), 
            ("Un acertijo por favor", "comment", 4),
            ("Me das miedo", "comment", 5),
            ("Canta algo", "comment", 6)
        ]
        
        for i, (comment, msg_type, mode) in enumerate(test_comments, 1):
            print(f"\n🧪 Prueba {i}: Modo {mode} - {comment}")
            self.dual_controller.change_mode(mode)
            self.handle_comment(test_username, comment, msg_type)
            time.sleep(4)
        
        # Probar regalos
        print("\n🎁 Probando regalos...")
        gift_tests = [
            ("TestUser1", "Rosa x1", "gift"),
            ("TestUser2", "Corazón x5", "gift"), 
            ("TestUser3", "León x1", "gift")
        ]
        
        for username, gift_info, msg_type in gift_tests:
            self.handle_comment(username, gift_info, msg_type)
            time.sleep(3)
        
        print("\n✅ Pruebas de todos los sistemas completadas")
    
    def cleanup(self):
        """Limpiar recursos del sistema dual + Arduino"""
        print("🧹 Limpiando recursos del sistema dual + Arduino...")
        
        try:
            # Cerrar Arduino
            if self.arduino_controller:
                self.arduino_controller.reset_position()
                self.arduino_controller.close()
            
            # Limpiar sistema dual
            self.dual_controller.cleanup()
            print("✅ Recursos limpiados correctamente")
            
        except Exception as e:
            print(f"❌ Error durante cleanup: {e}")

def main():
    """Función principal"""
    print("=" * 60)
    print("🤡 PONCHO EL PAYASO - VERSIÓN CON ARDUINO Y VOCES DUALES")
    print("=" * 60)
    
    try:
        # Crear aplicación
        app = RefactoredNPCApp()
        
        # Opción para probar sistemas (descomenta si quieres)
        # app.test_all_systems()
        
        # Iniciar aplicación
        app.start_application()
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
    
    print("👋 ¡Hasta la vista, baby!")

if __name__ == "__main__":
    main()