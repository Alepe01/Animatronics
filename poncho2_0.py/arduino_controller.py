import serial
import time
import threading

class ArduinoController:
    """Controlador Arduino integrado con el sistema dual robot"""
    
    def __init__(self, port="COM16", baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.connected = False
        self.command_queue = []
        self.queue_lock = threading.Lock()
        
        self.connect()
    
    def connect(self):
        """Establecer conexión con Arduino"""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Esperar a que se establezca la conexión
            self.connected = True
            print(f"✅ Arduino conectado en {self.port}")
            
            # Enviar comando de test para verificar conexión
            self.send_command("RESET")
            
        except Exception as e:
            print(f"❌ Error conectando Arduino: {e}")
            self.ser = None
            self.connected = False
    
    def send_command(self, command):
        """Enviar comando al Arduino de forma segura"""
        if not self.connected or not self.ser:
            print("❌ Arduino no conectado")
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
    
    # === COMANDOS PARA PONCHO ===
    def start_talking(self):
        """Poncho inicia animación de habla"""
        return self.send_command("TALK")
    
    def stop_talking(self):
        """Poncho detiene animación de habla"""
        return self.send_command("STOP")
    
    def happy_animation(self):
        """Poncho animación de felicidad"""
        return self.send_command("HAPPY")
    
    def sad_animation(self):
        """Poncho animación de tristeza"""
        return self.send_command("SAD")
    
    def angry_animation(self):
        """Poncho animación de enojo"""
        return self.send_command("ANGRY")
    
    def blink_animation(self):
        """Poncho parpadeo"""
        return self.send_command("BLINK")
    
    # === COMANDOS PARA ROBOT DE REGALOS ===
    def gift_animation(self):
        """Robot de regalos: animación básica"""
        return self.send_command("GIFT")
    
    def gift_combo_animation(self):
        """Robot de regalos: animación de combo"""
        return self.send_command("GIFT_COMBO")
    
    def gift_celebration_animation(self):
        """Robot de regalos: animación de celebración"""
        return self.send_command("GIFT_CELEBRATION")
    
    def gift_stop_animation(self):
        """Robot de regalos: detener animación"""
        return self.send_command("GIFT_STOP")
    
    # === COMANDOS GENERALES ===
    def reset_position(self):
        """Resetear ambos robots a posición inicial"""
        return self.send_command("RESET")
    
    def test_poncho(self):
        """Probar solo Poncho"""
        return self.send_command("TEST")
    
    def test_dual_system(self):
        """Probar ambos robots"""
        return self.send_command("TEST_DUAL")
    
    def custom_command(self, command):
        """Enviar comando personalizado"""
        return self.send_command(command)
    
    # === FUNCIONES DE UTILIDAD ===
    def is_connected(self):
        """Verificar si está conectado"""
        return self.connected and self.ser is not None
    
    def reconnect(self):
        """Intentar reconectar"""
        if self.ser:
            try:
                self.ser.close()
            except:
                pass
        
        self.connect()
        return self.connected
    
    def close(self):
        """Cerrar conexión"""
        if self.ser:
            try:
                self.ser.close()
                print("🔌 Conexión Arduino cerrada")
            except:
                pass
        self.connected = False
        self.ser = None
    
    def test_connection(self):
        """Probar la conexión"""
        if self.send_command("TEST_DUAL"):
            print("✅ Test de conexión dual exitoso")
            return True
        else:
            print("❌ Test de conexión fallido")
            return False

# === FUNCIONES DE UTILIDAD ===
def get_available_ports():
    """Obtener puertos COM disponibles"""
    try:
        import serial.tools.list_ports
    except ImportError:
        print("❌ pyserial no instalado. Instala con: pip install pyserial")
        return []
    
    ports = serial.tools.list_ports.comports()
    available_ports = []
    
    for port in ports:
        available_ports.append({
            'device': port.device,
            'description': port.description,
            'hwid': port.hwid
        })
    
    return available_ports

def find_arduino_port():
    """Buscar automáticamente el puerto del Arduino"""
    ports = get_available_ports()
    
    # Buscar puertos que puedan ser Arduino
    arduino_keywords = ['arduino', 'ch340', 'cp2102', 'ftdi', 'usb serial', 'serial port']
    
    for port in ports:
        description = port['description'].lower()
        for keyword in arduino_keywords:
            if keyword in description:
                return port['device']
    
    # Si no encuentra ninguno, devolver el primer puerto disponible
    if ports:
        return ports[0]['device']
    
    return None

# === INTEGRACIÓN CON AUDIO MANAGER ===
class ArduinoAudioManager:
    """Versión del AudioManager que incluye control de Arduino"""
    
    def __init__(self, arduino_controller=None):
        self.arduino = arduino_controller
        # Aquí incluirías la lógica de AudioManager original
        # pero con integración de Arduino
    
    def speak_text(self, text):
        """Hablar texto y animar Arduino"""
        if self.arduino:
            self.arduino.start_talking()
        
        # Aquí iría la lógica de síntesis de voz
        # Al terminar:
        time.sleep(2)  # Simular duración del audio
        
        if self.arduino:
            self.arduino.stop_talking()
    
    def is_audio_playing(self):
        """Verificar si está reproduciendo audio"""
        # Implementar lógica real
        return False

# === WRAPPER PARA EASY INTEGRATION ===
class DualRobotArduino:
    """Wrapper simplificado para control dual del Arduino"""
    
    def __init__(self, port="COM16"):
        self.arduino = ArduinoController(port)
        print(f"🤖 Dual Robot Arduino inicializado en {port}")
    
    def poncho_talk(self):
        """Poncho empieza a hablar"""
        return self.arduino.start_talking()
    
    def poncho_stop(self):
        """Poncho para de hablar"""
        return self.arduino.stop_talking()
    
    def poncho_emotion(self, emotion):
        """Poncho muestra emoción"""
        emotions = {
            "happy": self.arduino.happy_animation,
            "sad": self.arduino.sad_animation,
            "angry": self.arduino.angry_animation,
            "blink": self.arduino.blink_animation
        }
        
        if emotion.lower() in emotions:
            return emotions[emotion.lower()]()
        else:
            print(f"❌ Emoción '{emotion}' no reconocida")
            return False
    
    def regalo_basic(self):
        """Regalo básico"""
        return self.arduino.gift_animation()
    
    def regalo_combo(self):
        """Combo de regalos"""
        return self.arduino.gift_combo_animation()
    
    def regalo_celebration(self):
        """Celebración de racha"""
        return self.arduino.gift_celebration_animation()
    
    def reset_all(self):
        """Resetear todo el sistema"""
        return self.arduino.reset_position()
    
    def test_system(self):
        """Probar todo el sistema"""
        return self.arduino.test_dual_system()
    
    def is_connected(self):
        """Verificar conexión"""
        return self.arduino.is_connected()
    
    def cleanup(self):
        """Limpiar recursos"""
        self.arduino.close()

# === EJEMPLO DE USO ===
if __name__ == "__main__":
    print("🤖 Probando comunicación Arduino Dual Robot...")
    
    # Buscar puerto automáticamente
    auto_port = find_arduino_port()
    if auto_port:
        print(f"🔍 Puerto detectado: {auto_port}")
    
    # Mostrar puertos disponibles
    print("\n📋 Puertos disponibles:")
    for port in get_available_ports():
        print(f"  - {port['device']}: {port['description']}")
    
    # Crear controlador dual
    dual_robot = DualRobotArduino(auto_port or "COM16")
    
    if dual_robot.is_connected():
        print("\n🧪 Probando sistema dual...")
        
        # Probar Poncho
        print("\n🎭 Probando Poncho...")
        dual_robot.poncho_talk()
        time.sleep(2)
        dual_robot.poncho_emotion("happy")
        time.sleep(2)
        dual_robot.poncho_stop()
        
        # Probar Robot de Regalos
        print("\n🎁 Probando Robot de Regalos...")
        dual_robot.regalo_basic()
        time.sleep(3)
        dual_robot.regalo_combo()
        time.sleep(3)
        dual_robot.regalo_celebration()
        time.sleep(5)
        
        # Reset
        print("\n🔄 Reseteando sistema...")
        dual_robot.reset_all()
        
        print("\n✅ Pruebas completadas")
    else:
        print("\n❌ No se pudo conectar con Arduino")
    
    dual_robot.cleanup()