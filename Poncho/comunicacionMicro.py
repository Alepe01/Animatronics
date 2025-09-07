import serial
import time

class ArduinoController:
    def __init__(self, port="COM16", baudrate=9600):
        """
        Inicializar la comunicación con Arduino
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.connected = False
        
        self.connect()
    
    def connect(self):
        """Establecer conexión con Arduino"""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Esperar a que se establezca la conexión
            self.connected = True
            print(f"✅ Conexión Arduino establecida en {self.port}")
        except Exception as e:
            print(f"❌ Error conectando Arduino: {e}")
            self.ser = None
            self.connected = False
    
    def send_command(self, command):
        """
        Enviar comando al Arduino
        """
        if not self.connected or not self.ser:
            print("❌ Arduino no conectado")
            return False
        
        try:
            command_bytes = f"{command}\n".encode()
            self.ser.write(command_bytes)
            time.sleep(0.1)
            print(f"📤 Comando enviado: {command}")
            return True
        except Exception as e:
            print(f"❌ Error enviando comando: {e}")
            return False
    
    def start_talking(self):
        """Iniciar animación de habla"""
        return self.send_command("TALK")
    
    def stop_talking(self):
        """Detener animación de habla"""
        return self.send_command("STOP")
    
    def gift_animation(self):
        """Animación especial para regalos"""
        return self.send_command("GIFT")
    
    def happy_animation(self):
        """Animación de felicidad"""
        return self.send_command("HAPPY")
    
    def sad_animation(self):
        """Animación de tristeza"""
        return self.send_command("SAD")
    
    def angry_animation(self):
        """Animación de enojo"""
        return self.send_command("ANGRY")
    
    def blink(self):
        """Parpadear"""
        return self.send_command("BLINK")
    
    def reset_position(self):
        """Resetear a posición inicial"""
        return self.send_command("RESET")
    
    def custom_command(self, command):
        """Enviar comando personalizado"""
        return self.send_command(command)
    
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
        """Probar la conexión enviando comando de test"""
        if self.send_command("TEST"):
            print("✅ Test de conexión exitoso")
            return True
        else:
            print("❌ Test de conexión fallido")
            return False

# --- FUNCIONES DE UTILIDAD ---
def get_available_ports():
    """Obtener puertos COM disponibles"""
    import serial.tools.list_ports
    
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
    arduino_keywords = ['arduino', 'ch340', 'cp2102', 'ftdi', 'usb serial']
    
    for port in ports:
        description = port['description'].lower()
        for keyword in arduino_keywords:
            if keyword in description:
                return port['device']
    
    # Si no encuentra ninguno, devolver el primer puerto disponible
    if ports:
        return ports[0]['device']
    
    return None

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    print("🤖 Probando comunicación con Arduino...")
    
    # Buscar puerto automáticamente
    auto_port = find_arduino_port()
    if auto_port:
        print(f"🔍 Puerto detectado automáticamente: {auto_port}")
    
    # Mostrar puertos disponibles
    print("\n📋 Puertos disponibles:")
    for port in get_available_ports():
        print(f"  - {port['device']}: {port['description']}")
    
    # Crear controlador
    arduino = ArduinoController()
    
    if arduino.is_connected():
        print("\n🧪 Probando comandos...")
        
        # Probar diferentes comandos
        commands = [
            ("TALK", "Iniciar animación de habla"),
            ("BLINK", "Parpadear"),
            ("HAPPY", "Animación feliz"),
            ("STOP", "Detener animación"),
            ("GIFT", "Animación de regalo"),
            ("RESET", "Resetear posición")
        ]
        
        for command, description in commands:
            print(f"\n🔧 {description}...")
            arduino.send_command(command)
            time.sleep(2)
        
        print("\n✅ Pruebas completadas")
    else:
        print("\n❌ No se pudo conectar con Arduino")
    
    arduino.close()