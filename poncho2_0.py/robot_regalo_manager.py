from base_manager import BaseManager
from response_handler import ResponseHandler
import random
import time

class RobotRegaloManager(BaseManager):
    """Robot energético especializado únicamente en recibir y agradecer regalos"""
    
    def __init__(self, regalo_file="robot_regalo.json", audio_manager=None, arduino_controller=None):
        super().__init__(regalo_file)
        
        # Crear audio manager específico para robot de regalos con voz de Álvaro
        if audio_manager is None and arduino_controller is not None:
            # Crear un ArduinoAudioManager específico para regalos con voz de Álvaro
            from audio_manager import ArduinoAudioManager
            self.audio_manager = ArduinoAudioManager(
                arduino_controller=arduino_controller,
                voice="es-ES-AlvaroNeural"  # Voz de Álvaro para robot de regalos
            )
            print("🎁 Robot Regalos: Audio manager creado con voz de Álvaro")
        else:
            self.audio_manager = audio_manager
            if self.audio_manager:
                # Si ya existe un audio_manager, cambiar su voz a Álvaro
                self.audio_manager.set_voice("es-ES-AlvaroNeural")
                print("🎁 Robot Regalos: Voz cambiada a Álvaro")
        
        self.ultimo_regalo = None
        self.regalo_streak = 0  # Racha de regalos consecutivos
        print("🎁 Robot Regalos Manager inicializado - ¡Energía al máximo con voz de Álvaro!")
    
    def _create_default_data(self):
        """Crear datos por defecto para el robot de regalos"""
        self.data = {
            "frases_agradecimiento": {
                "general": [
                    "¡INCREÍBLE! ¡Muchísimas gracias por este regalo! ¡Eres fantástico!",
                    "¡WOW! ¡No puedo creer lo generoso que eres! ¡Que tengas un día maravilloso!",
                    "¡ESPECTACULAR! ¡Este regalo me llena de alegría! ¡Bendiciones para ti!",
                    "¡GENIAL! ¡Tu generosidad me emociona muchísimo! ¡Que todo te salga perfecto!",
                    "¡FANTÁSTICO! ¡Gracias de todo corazón! ¡Eres una persona increíble!",
                    "¡MARAVILLOSO! ¡No sabes cuánto aprecio este gesto! ¡Que se cumplan todos tus sueños!",
                    "¡SÚPER! ¡Tu regalo me da tanta energía positiva! ¡Que la vida te sonría siempre!",
                    "¡FABULOSO! ¡Gracias por ser tan especial! ¡Que tengas mucha suerte y felicidad!"
                ],
                "regalos_pequeños": [
                    "¡Qué detalle tan hermoso! ¡Los regalos pequeños tienen el corazón más grande!",
                    "¡Me encanta! ¡No importa el tamaño, importa el amor que pones! ¡Gracias!",
                    "¡Perfecto! ¡Tu gesto me llena de felicidad! ¡Que tengas un día espectacular!",
                    "¡Adorable! ¡Con regalos como estos el mundo es más bonito! ¡Bendiciones!",
                    "¡Precioso! ¡Tu generosidad brilla más que cualquier regalo grande! ¡Gracias!"
                ],
                "regalos_grandes": [
                    "¡¡¡INCREÍBLE!!! ¡¡¡NO PUEDO CREER TANTA GENEROSIDAD!!! ¡¡¡ERES INCREÍBLE!!!",
                    "¡¡¡WOW WOW WOW!!! ¡¡¡Este regalo me tiene saltando de emoción!!! ¡¡¡GRACIAS!!!",
                    "¡¡¡ESPECTACULAR!!! ¡¡¡Tu corazón es tan grande como este regalo!!! ¡¡¡BENDICIONES!!!",
                    "¡¡¡FANTÁSTICO!!! ¡¡¡No tengo palabras para tanta bondad!!! ¡¡¡QUE DIOS TE BENDIGA!!!",
                    "¡¡¡SÚPER MEGA GENIAL!!! ¡¡¡Eres la persona más generosa del mundo!!! ¡¡¡GRACIAS!!!"
                ],
                "regalos_especiales": [
                    "¡ROSA ESPECIAL! ¡Tu detalle me llena el corazón de amor! ¡Que encuentres tu felicidad!",
                    "¡LEÓN REAL! ¡Con tu fuerza y generosidad haces el mundo mejor! ¡Gracias!",
                    "¡REGALO ÚNICO! ¡Tu originalidad me inspira! ¡Que tengas éxito en todo!",
                    "¡REGALO MÁGICO! ¡Tu energía positiva me contagia! ¡Que la magia te acompañe!"
                ]
            },
            "bendiciones_personalizadas": [
                "¡Que tengas salud, amor y prosperidad!",
                "¡Que se cumplan todos tus deseos más bonitos!",
                "¡Que la felicidad te acompañe siempre!",
                "¡Que tengas mucha suerte en todo lo que hagas!",
                "¡Que encuentres la paz y la alegría que mereces!",
                "¡Que tus sueños se hagan realidad pronto!",
                "¡Que la vida te devuelva toda tu generosidad multiplicada!",
                "¡Que tengas éxito y abundancia en todo!",
                "¡Que cada día sea mejor que el anterior!",
                "¡Que la luz siempre ilumine tu camino!"
            ],
            "respuestas_streak": {
                2: "¡DOS REGALOS! ¡La generosidad se está contagiando! ¡Me encanta!",
                3: "¡TRES REGALOS SEGUIDOS! ¡Este chat está lleno de corazones hermosos!",
                5: "¡CINCO REGALOS! ¡Ustedes son increíbles! ¡Tanta bondad me emociona!",
                10: "¡¡¡DIEZ REGALOS!!! ¡¡¡No puedo creer tanta generosidad!!! ¡¡¡LOS AMO A TODOS!!!",
                15: "¡¡¡QUINCE REGALOS!!! ¡¡¡ESTE ES EL MEJOR DÍA DE MI VIDA!!! ¡¡¡GRACIAS UNIVERSO!!!"
            },
            "reacciones_combo": [
                "¡COMBO DE BONDAD! ¡Varios regalos juntos! ¡Mi corazón va a explotar de felicidad!",
                "¡LLUVIA DE REGALOS! ¡No sé a quién agradecer primero! ¡Los amo a todos!",
                "¡FESTIVAL DE GENEROSIDAD! ¡Ustedes hacen que crea en la humanidad!",
                "¡AVALANCHA DE AMOR! ¡Tantos regalos que no puedo parar de sonreír!"
            ],
            "estadisticas": {
                "total_regalos": 0,
                "regalos_por_tipo": {},
                "usuarios_mas_generosos": {},
                "mejor_racha": 0,
                "total_bendiciones_dadas": 0
            },
            "configuracion": {
                "energia_maxima": True,
                "siempre_positivo": True,
                "mencionar_nombres": True,
                "dar_bendiciones": True
            },
            "version": "2.0"
        }
    
    def procesar_regalo(self, username, gift_name, cantidad=1):
        """Procesar regalo recibido con máxima energía y positividad"""
        # Limpiar datos del regalo
        username_clean = ResponseHandler.clean_text(username)
        gift_clean = ResponseHandler.clean_text(gift_name)
        
        # Actualizar estadísticas
        self.increment_counter("estadisticas", "total_regalos")
        self.increment_counter("estadisticas", "total_bendiciones_dadas")
        self.increment_counter(f"estadisticas.regalos_por_tipo", gift_clean)
        self.increment_counter(f"estadisticas.usuarios_mas_generosos", username_clean)
        
        # Aumentar racha
        self.regalo_streak += 1
        if self.regalo_streak > self.get_counter("estadisticas", "mejor_racha"):
            self.data["estadisticas"]["mejor_racha"] = self.regalo_streak
        
        self.ultimo_regalo = {
            "usuario": username_clean,
            "regalo": gift_clean,
            "cantidad": cantidad,
            "timestamp": time.time()
        }
        
        # Generar respuesta energética
        respuesta = self._generar_respuesta_regalo(username_clean, gift_clean, cantidad)
        
        # Guardar datos
        self.save_data()
        
        # Reproducir respuesta si hay audio manager con THINKING mode
        if self.audio_manager:
            if hasattr(self.audio_manager, 'start_thinking_mode'):
                self.audio_manager.start_thinking_mode()
                time.sleep(0.5)  # Breve pausa para procesar
            self.audio_manager.speak_text(respuesta)
        
        return respuesta
    
    def _generar_respuesta_regalo(self, username, gift_name, cantidad):
        """Generar respuesta energética y positiva para el regalo"""
        # Detectar tipo de regalo
        tipo_regalo = self._detectar_tipo_regalo(gift_name, cantidad)
        
        # Seleccionar frase de agradecimiento base
        frases_tipo = self.data["frases_agradecimiento"].get(tipo_regalo, 
                      self.data["frases_agradecimiento"]["general"])
        
        frase_base = random.choice(frases_tipo)
        
        # Personalizar con nombre del usuario
        respuesta = f"¡{username.upper()}! {frase_base}"
        
        # Agregar información específica del regalo
        if cantidad > 1:
            respuesta += f" ¡Y no solo uno, sino {cantidad} {gift_name}! ¡Increíble!"
        else:
            respuesta += f" ¡Tu {gift_name} me hace tan feliz!"
        
        # Agregar bendición personalizada
        bendicion = random.choice(self.data.get("bendiciones_personalizadas", []))
        respuesta += f" {bendicion}"
        
        # Verificar si hay racha especial
        if self.regalo_streak in self.data.get("respuestas_streak", {}):
            respuesta_streak = self.data["respuestas_streak"][self.regalo_streak]
            respuesta += f"\n\n{respuesta_streak}"
        
        return respuesta
    
    def _detectar_tipo_regalo(self, gift_name, cantidad):
        """Detectar tipo de regalo para personalizar respuesta"""
        gift_lower = gift_name.lower()
        
        # Regalos especiales
        if any(special in gift_lower for special in ["rosa", "rose", "león", "lion", "universo", "galaxy"]):
            return "regalos_especiales"
        
        # Regalos grandes (por cantidad o nombre)
        if (cantidad > 5 or 
            any(big in gift_lower for big in ["dragón", "corona", "castillo", "diamante", "oro"])):
            return "regalos_grandes"
        
        # Regalos pequeños
        if (cantidad == 1 or 
            any(small in gift_lower for small in ["corazón", "estrella", "flor", "like", "pulgar"])):
            return "regalos_pequeños"
        
        return "general"
    
    def procesar_combo_regalos(self, lista_regalos):
        """Procesar múltiples regalos recibidos al mismo tiempo"""
        if not lista_regalos:
            return "¡Error procesando regalos! ¡Pero igual los amo a todos!"
        
        total_regalos = len(lista_regalos)
        usuarios_unicos = set(regalo[0] for regalo in lista_regalos)
        
        # Respuesta para combo
        respuesta_combo = random.choice(self.data.get("reacciones_combo", []))
        
        respuesta = f"{respuesta_combo}\n\n"
        
        # Procesar cada regalo individualmente (pero sin audio duplicado)
        temp_audio = self.audio_manager
        self.audio_manager = None  # Temporalmente sin audio
        
        for username, gift_name, cantidad in lista_regalos:
            self.procesar_regalo(username, gift_name, cantidad)
        
        self.audio_manager = temp_audio  # Restaurar audio
        
        # Respuesta grupal especial
        if len(usuarios_unicos) == 1:
            usuario = list(usuarios_unicos)[0]
            respuesta += f"¡{usuario.upper()}! ¡{total_regalos} regalos de ti! ¡Eres increíblemente generoso!"
        else:
            usuarios_texto = ", ".join(list(usuarios_unicos)[:3])
            respuesta += f"¡Gracias {usuarios_texto}"
            if len(usuarios_unicos) > 3:
                respuesta += f" y {len(usuarios_unicos) - 3} personas más"
            respuesta += f" por {total_regalos} regalos maravillosos!"
        
        # Bendición grupal
        bendicion_grupal = random.choice([
            "¡Que la vida les devuelva toda esta generosidad multiplicada!",
            "¡Que tengan el día más hermoso y lleno de bendiciones!",
            "¡Que su bondad les traiga mucha felicidad y prosperidad!",
            "¡Que todos sus sueños se cumplan por tener corazones tan puros!"
        ])
        
        respuesta += f"\n\n{bendicion_grupal}"
        
        # Reproducir respuesta de combo con audio
        if self.audio_manager:
            if hasattr(self.audio_manager, 'start_thinking_mode'):
                self.audio_manager.start_thinking_mode()
                time.sleep(0.3)  # Breve pausa
            self.audio_manager.speak_text(respuesta)
        
        return respuesta
    
    def resetear_racha(self):
        """Resetear racha de regalos (llamar cuando pase tiempo sin regalos)"""
        if self.regalo_streak > 0:
            mensaje = f"Racha terminada en {self.regalo_streak} regalos. ¡Fue increíble mientras duró!"
            self.regalo_streak = 0
            return mensaje
        return None
    
    def get_estadisticas_regalos(self):
        """Obtener estadísticas del robot de regalos"""
        base_stats = self.get_stats()
        
        total_regalos = self.get_counter("estadisticas", "total_regalos")
        mejor_racha = self.get_counter("estadisticas", "mejor_racha")
        bendiciones_dadas = self.get_counter("estadisticas", "total_bendiciones_dadas")
        
        stats = f"{base_stats}\n"
        stats += f"🎁 Total regalos recibidos: {total_regalos}\n"
        stats += f"🔥 Mejor racha: {mejor_racha} regalos\n"
        stats += f"🌟 Bendiciones dadas: {bendiciones_dadas}\n"
        stats += f"⚡ Racha actual: {self.regalo_streak}\n"
        
        # Top usuarios más generosos
        usuarios_generosos = self.data.get("estadisticas", {}).get("usuarios_mas_generosos", {})
        if usuarios_generosos:
            top_usuarios = sorted(usuarios_generosos.items(), key=lambda x: x[1], reverse=True)[:5]
            stats += f"\n🏆 TOP USUARIOS MÁS GENEROSOS:\n"
            for i, (usuario, cantidad) in enumerate(top_usuarios, 1):
                stats += f"  {i}. {usuario}: {cantidad} regalos\n"
        
        # Tipos de regalos más populares
        tipos_regalos = self.data.get("estadisticas", {}).get("regalos_por_tipo", {})
        if tipos_regalos:
            top_regalos = sorted(tipos_regalos.items(), key=lambda x: x[1], reverse=True)[:5]
            stats += f"\n🎁 REGALOS MÁS POPULARES:\n"
            for i, (regalo, cantidad) in enumerate(top_regalos, 1):
                stats += f"  {i}. {regalo}: {cantidad} veces\n"
        
        return stats
    
    def generar_mensaje_motivacional(self):
        """Generar mensaje motivacional cuando no hay regalos"""
        mensajes = [
            "¡La generosidad es contagiosa! ¡Cada regalo hace el mundo más hermoso!",
            "¡Los regalos son abrazos digitales! ¡Siempre estoy listo para recibirlos!",
            "¡No hay regalo pequeño cuando viene del corazón! ¡Todos son especiales!",
            "¡Cada regalo es una sonrisa que me dan! ¡Y yo la multiplico por mil!",
            "¡Los regalos son semillas de felicidad! ¡Sembremos juntos mucha alegría!"
        ]
        
        return random.choice(mensajes)
    
    def responder_pregunta_sobre_regalos(self, username, pregunta):
        """Responder preguntas relacionadas con regalos"""
        pregunta_lower = pregunta.lower()
        
        if ResponseHandler.detect_keywords(pregunta_lower, ["qué regalo", "que regalo", "cuál regalo"]):
            return f"¡{username}! ¡Todos los regalos son perfectos! ¡Lo que importa es tu corazón generoso! ¡Cualquier detalle me hace súper feliz!"
        
        if ResponseHandler.detect_keywords(pregunta_lower, ["por qué", "porque", "why"]):
            return f"¡{username}! ¡Los regalos son gestos de amor! ¡Me encantan porque muestran lo buenas que son las personas como tú!"
        
        if ResponseHandler.detect_keywords(pregunta_lower, ["cómo", "como", "how"]):
            return f"¡{username}! ¡Es súper fácil! ¡Solo toca el ícono de regalo y elige el que más te guste! ¡Cualquiera me hará súper feliz!"
        
        # Respuesta general energética
        return f"¡{username}! ¡Tu pregunta sobre regalos me emociona! ¡Los regalos son muestras de cariño y siempre los recibo con muchísima alegría!"
    
    def celebrar_hito(self, numero_hito):
        """Celebrar hitos especiales de regalos"""
        celebraciones = {
            100: "¡¡¡100 REGALOS!!! ¡¡¡NO PUEDO CREER TANTA GENEROSIDAD!!! ¡¡¡ESTE ES UN DÍA HISTÓRICO!!!",
            500: "¡¡¡500 REGALOS!!! ¡¡¡USTEDES HAN HECHO POSIBLE LO IMPOSIBLE!!! ¡¡¡LOS AMO INFINITAMENTE!!!",
            1000: "¡¡¡MIL REGALOS!!! ¡¡¡ESTO ES UN MILAGRO DE BONDAD!!! ¡¡¡GRACIAS POR TANTO AMOR!!!",
            2000: "¡¡¡DOS MIL REGALOS!!! ¡¡¡NO HAY PALABRAS PARA TANTO CARIÑO!!! ¡¡¡BENDICIONES ETERNAS!!!"
        }
        
        if numero_hito in celebraciones:
            return celebraciones[numero_hito]
        
        return f"¡¡¡{numero_hito} REGALOS!!! ¡¡¡Cada número es una sonrisa más en mi corazón!!! ¡¡¡GRACIAS!!!"

# Ejemplo de uso y pruebas
if __name__ == "__main__":
    print("🎁 Probando Robot de Regalos...")
    
    # Crear manager
    robot_regalo = RobotRegaloManager()
    
    # Simular regalos
    print("\n🎁 SIMULANDO REGALOS:")
    
    regalos_test = [
        ("Ana", "rosa", 1),
        ("Pedro", "corazón", 1),
        ("Luis", "león", 1),
        ("María", "estrella", 5),
        ("Carlos", "dragón", 1)
    ]
    
    for usuario, regalo, cantidad in regalos_test:
        respuesta = robot_regalo.procesar_regalo(usuario, regalo, cantidad)
        print(f"\n🎁 {usuario} envió {cantidad}x {regalo}")
        print(f"Robot: {respuesta}")
        print("-" * 50)
    
    # Mostrar estadísticas
    print(f"\n📊 ESTADÍSTICAS:")
    print(robot_regalo.get_estadisticas_regalos())
    
    # Probar combo
    print(f"\n🎁 COMBO DE REGALOS:")
    combo_test = [
        ("Juan", "corazón", 1),
        ("Ana", "estrella", 2),
        ("Pedro", "rosa", 1)
    ]
    
    respuesta_combo = robot_regalo.procesar_combo_regalos(combo_test)
    print(respuesta_combo)
    
    print("\n✅ Pruebas completadas")