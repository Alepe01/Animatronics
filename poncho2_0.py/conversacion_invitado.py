from base_manager import BaseManager
from response_handler import ResponseHandler
from audio_manager import AudioListener
import random
import time
import threading

class ConversacionInvitadoManager(BaseManager):
    """Manager para conversación con invitado usando audio de bocinas"""
    
    def __init__(self, conversacion_file="conversacion_invitado.json", audio_manager=None):
        super().__init__(conversacion_file)
        self.audio_manager = audio_manager
        self.audio_listener = None
        self.conversacion_activa = False
        self.invitado_actual = None
        self.historial_conversacion = []
        self.escuchando_invitado = False
        print("🎙️ Conversación Invitado Manager inicializado")
    
    def _create_default_data(self):
        """Crear datos por defecto para conversación con invitado"""
        self.data = {
            "tipos_entrevista": [
                {
                    "nombre": "Entrevista Casual",
                    "descripcion": "Conversación relajada y divertida",
                    "preguntas_sugeridas": [
                        "¿Cómo estás hoy?",
                        "¿Qué tal tu experiencia aquí?",
                        "¿Tienes alguna historia graciosa que contar?"
                    ]
                },
                {
                    "nombre": "Entrevista Personal",
                    "descripcion": "Preguntas sobre la vida del invitado",
                    "preguntas_sugeridas": [
                        "Háblanos un poco sobre ti",
                        "¿Cuál es tu mayor pasión?",
                        "¿Qué consejo darías a los viewers?"
                    ]
                },
                {
                    "nombre": "Entrevista Cómica",
                    "descripcion": "Enfoque en humor y entretenimiento",
                    "preguntas_sugeridas": [
                        "¿Cuál es tu chiste favorito?",
                        "¿Qué piensas de los payasos?",
                        "¿Has tenido alguna experiencia embarazosa?"
                    ]
                }
            ],
            "respuestas_automaticas": {
                "bienvenida": [
                    "¡Bienvenido a mi show! Espero que estés preparado para una conversación llena de sarcasmo y preguntas incómodas.",
                    "¡Hola! Te advierto que soy un payaso, así que esta entrevista puede ser un desastre... pero divertido.",
                    "¡Perfecto! Otro valiente se atreve a conversar conmigo. Esto va a estar interesante."
                ],
                "despedida": [
                    "¡Gracias por venir! Ha sido... bueno, ha sido algo.",
                    "¡Excelente conversación! Espero que sobrevivas a la experiencia.",
                    "¡Hasta la próxima! Gracias por aguantar mis preguntas raras."
                ],
                "no_escucho": [
                    "¿Hola? ¿Sigues ahí? Mi micrófono está funcionando, pero tal vez tu voz no.",
                    "Creo que perdí la conexión contigo... o tal vez solo decidiste que es mejor estar callado.",
                    "El silencio es oro, pero prefiero el ruido de una buena conversación."
                ]
            },
            "configuracion_audio": {
                "tiempo_escucha": 10,  # segundos máximo de escucha
                "volumen_minimo": 0.3,  # nivel mínimo para detectar voz
                "pausas_entre_respuestas": 2  # segundos de pausa
            },
            "estadisticas": {
                "entrevistas_realizadas": 0,
                "tiempo_total_conversacion": 0,
                "frases_detectadas": 0,
                "invitados_unicos": 0
            },
            "version": "2.0"
        }
    
    def iniciar_conversacion_invitado(self, nombre_invitado, tipo_entrevista=None):
        """Iniciar conversación con un invitado"""
        if self.conversacion_activa:
            return "Ya hay una conversación activa. Finaliza la actual primero."
        
        # Seleccionar tipo de entrevista
        tipos = self.data.get("tipos_entrevista", [])
        if tipo_entrevista:
            tipo_encontrado = None
            for t in tipos:
                if tipo_entrevista.lower() in t["nombre"].lower():
                    tipo_encontrado = t
                    break
            
            if not tipo_encontrado:
                return f"Tipo de entrevista '{tipo_entrevista}' no encontrado. Tipos disponibles: {', '.join([t['nombre'] for t in tipos])}"
        else:
            tipo_encontrado = self.get_random_choice("tipos_entrevista")
        
        if not tipo_encontrado:
            return "No hay tipos de entrevista disponibles."
        
        # Configurar conversación
        self.invitado_actual = {
            "nombre": nombre_invitado,
            "tipo_entrevista": tipo_encontrado,
            "inicio": time.time()
        }
        
        self.conversacion_activa = True
        self.historial_conversacion = []
        
        # Incrementar estadísticas
        self.increment_counter("estadisticas", "entrevistas_realizadas")
        if nombre_invitado not in self.data.get("invitados_historicos", {}):
            self.increment_counter("estadisticas", "invitados_unicos")
        
        # Configurar audio listener
        self.configurar_audio_listener()
        
        # Mensaje de bienvenida
        bienvenida = self.get_random_choice("respuestas_automaticas") or "¡Bienvenido!"
        
        mensaje = f"{bienvenida}\n\n"
        mensaje += f"🎙️ CONVERSACIÓN CON: {nombre_invitado}\n"
        mensaje += f"📋 Tipo: {tipo_encontrado['nombre']}\n"
        mensaje += f"📝 {tipo_encontrado['descripcion']}\n\n"
        mensaje += "🔊 Activando micrófono... ¡Habla cuando quieras!"
        
        return mensaje
    
    def configurar_audio_listener(self):
        """Configurar listener de audio para el invitado"""
        if not self.audio_manager:
            return
        
        try:
            # Crear listener específico para invitado
            self.audio_listener = AudioListener(self.procesar_audio_invitado)
            
            # Buscar dispositivo de audio interno (bocinas/altavoces)
            self.audio_listener.find_stereo_mix()
            
            print("🎧 Audio listener configurado para conversación con invitado")
        
        except Exception as e:
            print(f"❌ Error configurando audio listener: {e}")
            self.audio_listener = None
    
    def iniciar_escucha(self):
        """Iniciar escucha del invitado"""
        if not self.conversacion_activa:
            return "No hay conversación activa."
        
        if not self.audio_listener:
            return "Audio listener no configurado. Verifica la configuración de audio."
        
        if self.escuchando_invitado:
            return "Ya estoy escuchando al invitado."
        
        # Iniciar escucha
        self.escuchando_invitado = True
        self.audio_listener.start_listening()
        
        return f"🎧 Escuchando a {self.invitado_actual['nombre']}... ¡Habla!"
    
    def detener_escucha(self):
        """Detener escucha del invitado"""
        if not self.escuchando_invitado:
            return "No estoy escuchando."
        
        self.escuchando_invitado = False
        if self.audio_listener:
            self.audio_listener.stop_listening()
        
        return "🔇 Escucha detenida."
    
    def procesar_audio_invitado(self, texto_detectado):
        """Procesar audio convertido a texto del invitado"""
        if not self.conversacion_activa or not self.escuchando_invitado:
            return
        
        # Limpiar texto
        texto_limpio = ResponseHandler.clean_text(texto_detectado)
        
        if not texto_limpio or len(texto_limpio) < 3:
            return
        
        # Registrar en historial
        entrada_historial = {
            "timestamp": time.time(),
            "tipo": "invitado",
            "usuario": self.invitado_actual["nombre"],
            "contenido": texto_limpio
        }
        
        self.historial_conversacion.append(entrada_historial)
        self.increment_counter("estadisticas", "frases_detectadas")
        
        print(f"🎤 {self.invitado_actual['nombre']}: {texto_limpio}")
        
        # Generar respuesta
        respuesta = self._generar_respuesta_conversacion(texto_limpio)
        
        # Agregar respuesta al historial
        respuesta_historial = {
            "timestamp": time.time(),
            "tipo": "poncho",
            "usuario": "Poncho",
            "contenido": respuesta
        }
        
        self.historial_conversacion.append(respuesta_historial)
        
        # Reproducir respuesta usando audio manager
        if self.audio_manager:
            self.audio_manager.speak_text(respuesta)
        
        return respuesta
    
    def _generar_respuesta_conversacion(self, texto_invitado):
        """Generar respuesta basada en lo que dijo el invitado"""
        texto_lower = texto_invitado.lower()
        nombre_invitado = self.invitado_actual["nombre"]
        tipo_entrevista = self.invitado_actual["tipo_entrevista"]["nombre"].lower()
        
        # Respuestas según el contexto y tipo de entrevista
        if "casual" in tipo_entrevista:
            return self._respuesta_casual(nombre_invitado, texto_lower, texto_invitado)
        elif "personal" in tipo_entrevista:
            return self._respuesta_personal(nombre_invitado, texto_lower, texto_invitado)
        elif "cómica" in tipo_entrevista or "comica" in tipo_entrevista:
            return self._respuesta_comica(nombre_invitado, texto_lower, texto_invitado)
        else:
            return self._respuesta_generica(nombre_invitado, texto_invitado)
    
    def _respuesta_casual(self, nombre, texto_lower, texto_original):
        """Respuestas para entrevista casual"""
        # Detectar saludos
        if ResponseHandler.detect_keywords(texto_lower, ["hola", "buenas", "hi", "hey"]):
            respuestas = [
                f"¡Hola {nombre}! Bienvenido a mi show, donde la lógica viene a morir.",
                f"¡Hey {nombre}! Espero que estés listo para una conversación interesante.",
                f"Saludos {nombre}, prepárate para preguntas que no sabías que existían."
            ]
            return random.choice(respuestas)
        
        # Detectar estado de ánimo
        if ResponseHandler.detect_keywords(texto_lower, ["bien", "genial", "perfecto", "excelente"]):
            respuestas = [
                f"¡Perfecto {nombre}! Me alegra que estés bien, porque yo voy a arruinar tu día.",
                f"Qué bueno {nombre}, necesito que estés en tu mejor estado para soportar mis preguntas.",
                f"Excelente {nombre}, así me gusta, con energía para esta aventura."
            ]
            return random.choice(respuestas)
        
        if ResponseHandler.detect_keywords(texto_lower, ["mal", "cansado", "terrible", "horrible"]):
            respuestas = [
                f"¿Mal día {nombre}? ¡Perfecto! Así encajas con la temática de mi vida.",
                f"No te preocupes {nombre}, después de hablar conmigo te sentirás peor.",
                f"Tranquilo {nombre}, todos tenemos días malos... yo los tengo todos."
            ]
            return random.choice(respuestas)
        
        # Respuesta general casual
        respuestas_generales = [
            f"Interesante {nombre}, cuéntame más sobre eso.",
            f"Ya veo {nombre}, ¿y cómo te sientes al respecto?",
            f"Mm-hmm {nombre}, eso suena... como algo que diría alguien.",
            f"Fascinante {nombre}, aunque no estoy seguro de qué significa."
        ]
        
        return random.choice(respuestas_generales)
    
    def _respuesta_personal(self, nombre, texto_lower, texto_original):
        """Respuestas para entrevista personal"""
        if ResponseHandler.detect_keywords(texto_lower, ["familia", "padre", "madre", "hermano", "hijo"]):
            respuestas = [
                f"La familia es importante {nombre}, aunque la mía me abandonó cuando se enteraron de mi carrera.",
                f"¡Qué bonito {nombre}! Mi familia también es especial... especialmente disfuncional.",
                f"Familia... {nombre}, esa palabra me trae recuerdos dolorosos y cómicos."
            ]
            return random.choice(respuestas)
        
        if ResponseHandler.detect_keywords(texto_lower, ["trabajo", "carrera", "profesion", "empleo"]):
            respuestas = [
                f"El trabajo es esencial {nombre}, aunque el mío consiste en hacer reír a gente que no ríe.",
                f"Interesante carrera {nombre}, yo elegí ser payaso... claramente no soy bueno tomando decisiones.",
                f"Tu trabajo suena mejor que el mío {nombre}, yo hago reír por dinero y fracaso en ambas."
            ]
            return random.choice(respuestas)
        
        if ResponseHandler.detect_keywords(texto_lower, ["sueño", "meta", "objetivo", "ambición"]):
            respuestas = [
                f"Los sueños son importantes {nombre}, aunque los míos se convirtieron en pesadillas.",
                f"¡Qué ambicioso {nombre}! Yo también tuve sueños... luego me desperté.",
                f"Me gusta tu actitud {nombre}, sigue soñando mientras puedas."
            ]
            return random.choice(respuestas)
        
        # Respuesta personal general
        respuestas_generales = [
            f"Eso es muy personal {nombre}, gracias por compartirlo conmigo.",
            f"Me parece fascinante {nombre}, ¿hay algo más que quieras contar?",
            f"Aprecio tu honestidad {nombre}, no todos son tan abiertos.",
            f"Qué interesante perspectiva {nombre}, nunca lo había visto así."
        ]
        
        return random.choice(respuestas_generales)
    
    def _respuesta_comica(self, nombre, texto_lower, texto_original):
        """Respuestas para entrevista cómica"""
        if ResponseHandler.detect_keywords(texto_lower, ["chiste", "gracioso", "divertido", "humor"]):
            respuestas = [
                f"¡Humor {nombre}! Mi especialidad, aunque no soy muy bueno en ella.",
                f"Los chistes son geniales {nombre}, tengo miles... todos malos.",
                f"¿Te gusta el humor {nombre}? ¡Perfecto! Porque mi vida es una comedia trágica.",
                f"El humor es subjetivo {nombre}, pero el mío es objetivamente malo."
            ]
            return random.choice(respuestas)
        
        if ResponseHandler.detect_keywords(texto_lower, ["payaso", "circo", "espectáculo"]):
            respuestas = [
                f"¡Ah, hablando de payasos {nombre}! Soy un experto en la materia... lamentablemente.",
                f"El circo {nombre}, mi hogar dulce hogar... bueno, más bien amargo hogar.",
                f"Los payasos {nombre}, somos una especie en extinción... por buenas razones.",
                f"El mundo del espectáculo {nombre}, donde los sueños van a morir lentamente."
            ]
            return random.choice(respuestas)
        
        if ResponseHandler.detect_keywords(texto_lower, ["reir", "risa", "carcajada"]):
            respuestas = [
                f"¡La risa {nombre}! Mi trabajo es provocarla, aunque más bien provoco lágrimas.",
                f"Reír es saludable {nombre}, aunque mi humor puede ser tóxico.",
                f"La risa es contagiosa {nombre}, pero la mía causa inmunidad.",
                f"Me alegra que rías {nombre}, porque yo no he reído en años."
            ]
            return random.choice(respuestas)
        
        # Respuesta cómica general
        respuestas_generales = [
            f"Ja, ja, ja... {nombre}, fingir que es gracioso es parte de mi trabajo.",
            f"Qué cómico {nombre}, casi tan gracioso como mi situación laboral.",
            f"Interesante {nombre}, ¿tienes más material como ese?",
            f"No está mal {nombre}, aunque mi abuela cuenta mejores chistes... y está muerta."
        ]
        
        return random.choice(respuestas)
    
    def _respuesta_generica(self, nombre, texto_original):
        """Respuesta genérica cuando no se identifica el contexto"""
        respuestas = [
            f"Ya veo {nombre}, esa es una perspectiva... única.",
            f"Mm-hmm {nombre}, sigue hablando que esto se está poniendo interesante.",
            f"Entiendo {nombre}, o al menos finjo que entiendo.",
            f"Fascinante {nombre}, cuéntame más sobre eso.",
            f"Interesante punto de vista {nombre}, ¿cómo llegaste a esa conclusión?",
            f"Okay {nombre}, eso no me lo esperaba.",
            f"Ya veo {nombre}, ¿y qué opinas tú al respecto?"
        ]
        
        return ResponseHandler.personalize_by_name(nombre, random.choice(respuestas))
    
    def hacer_pregunta_invitado(self):
        """Hacer una pregunta al invitado"""
        if not self.conversacion_activa:
            return "No hay conversación activa."
        
        tipo_entrevista = self.invitado_actual["tipo_entrevista"]
        preguntas_sugeridas = tipo_entrevista.get("preguntas_sugeridas", [])
        
        if not preguntas_sugeridas:
            preguntas_generales = [
                "¿Qué tal tu día?",
                "¿Tienes alguna historia que contar?",
                "¿Qué opinas sobre esto?",
                "¿Hay algo que quieras compartir?"
            ]
            pregunta = random.choice(preguntas_generales)
        else:
            pregunta = random.choice(preguntas_sugeridas)
        
        nombre = self.invitado_actual["nombre"]
        pregunta_personalizada = f"{nombre}, {pregunta}"
        
        # Agregar al historial
        entrada_pregunta = {
            "timestamp": time.time(),
            "tipo": "poncho_pregunta",
            "usuario": "Poncho",
            "contenido": pregunta_personalizada
        }
        
        self.historial_conversacion.append(entrada_pregunta)
        
        # Reproducir pregunta
        if self.audio_manager:
            self.audio_manager.speak_text(pregunta_personalizada)
        
        return f"❓ {pregunta_personalizada}\n\n🎧 Escuchando respuesta..."
    
    def finalizar_conversacion_invitado(self):
        """Finalizar conversación con invitado"""
        if not self.conversacion_activa:
            return "No hay conversación activa que finalizar."
        
        # Detener escucha
        self.detener_escucha()
        
        # Calcular estadísticas de la sesión
        inicio = self.invitado_actual["inicio"]
        duracion = time.time() - inicio
        
        nombre = self.invitado_actual["nombre"]
        tipo = self.invitado_actual["tipo_entrevista"]["nombre"]
        
        # Actualizar estadísticas
        tiempo_actual = self.get_counter("estadisticas", "tiempo_total_conversacion")
        self.data["estadisticas"]["tiempo_total_conversacion"] = tiempo_actual + duracion
        
        # Guardar historial del invitado
        if "invitados_historicos" not in self.data:
            self.data["invitados_historicos"] = {}
        
        self.data["invitados_historicos"][nombre] = {
            "ultima_visita": time.time(),
            "tipo_entrevista": tipo,
            "duracion": duracion,
            "interacciones": len(self.historial_conversacion)
        }
        
        self.save_data()
        
        # Mensaje de despedida
        despedida = self.get_random_choice("respuestas_automaticas") or "¡Gracias por venir!"
        
        resultado = f"{despedida}\n\n"
        resultado += f"🎙️ RESUMEN DE LA CONVERSACIÓN:\n"
        resultado += f"Invitado: {nombre}\n"
        resultado += f"Tipo: {tipo}\n"
        resultado += f"Duración: {duracion/60:.1f} minutos\n"
        resultado += f"Interacciones: {len(self.historial_conversacion)}\n\n"
        resultado += f"¡Ha sido un placer conversar contigo, {nombre}!"
        
        # Limpiar estado
        self._limpiar_estado()
        
        return resultado
    
    def _limpiar_estado(self):
        """Limpiar estado de conversación"""
        if self.audio_listener:
            self.audio_listener.stop_listening()
            self.audio_listener = None
        
        self.conversacion_activa = False
        self.invitado_actual = None
        self.historial_conversacion = []
        self.escuchando_invitado = False
    
    def get_historial_conversacion(self, ultimas=10):
        """Obtener historial de la conversación actual"""
        if not self.historial_conversacion:
            return "No hay historial de conversación."
        
        historial = "📝 HISTORIAL DE CONVERSACIÓN:\n\n"
        
        for entrada in self.historial_conversacion[-ultimas:]:
            timestamp = time.strftime("%H:%M:%S", time.localtime(entrada["timestamp"]))
            usuario = entrada["usuario"]
            contenido = entrada["contenido"]
            tipo_icono = "🎤" if entrada["tipo"] == "invitado" else "🗣️"
            
            historial += f"[{timestamp}] {tipo_icono} {usuario}: {contenido}\n\n"
        
        return historial
    
    def get_tipos_entrevista(self):
        """Obtener tipos de entrevista disponibles"""
        tipos = self.data.get("tipos_entrevista", [])
        if not tipos:
            return "No hay tipos de entrevista disponibles."
        
        lista = "🎭 TIPOS DE ENTREVISTA DISPONIBLES:\n\n"
        for i, tipo in enumerate(tipos, 1):
            lista += f"{i}. {tipo['nombre']}\n   {tipo['descripcion']}\n"
            lista += f"   Preguntas ejemplo: {len(tipo.get('preguntas_sugeridas', []))}\n\n"
        
        return lista
    
    def get_estado_conversacion_invitado(self):
        """Obtener estado actual de la conversación con invitado"""
        if not self.conversacion_activa:
            return "No hay conversación activa con invitado."
        
        nombre = self.invitado_actual["nombre"]
        tipo = self.invitado_actual["tipo_entrevista"]["nombre"]
        inicio = self.invitado_actual["inicio"]
        duracion = time.time() - inicio
        
        estado = f"🎙️ CONVERSACIÓN ACTIVA CON: {nombre}\n"
        estado += f"Tipo: {tipo}\n"
        estado += f"Duración: {duracion/60:.1f} minutos\n"
        estado += f"Interacciones: {len(self.historial_conversacion)}\n"
        estado += f"Escuchando: {'Sí' if self.escuchando_invitado else 'No'}\n"
        
        return estado
    
    def get_invitado_stats(self):
        """Obtener estadísticas usando método heredado"""
        base_stats = self.get_stats()
        
        entrevistas = self.get_counter("estadisticas", "entrevistas_realizadas")
        tiempo_total = self.get_counter("estadisticas", "tiempo_total_conversacion")
        frases = self.get_counter("estadisticas", "frases_detectadas")
        invitados_unicos = self.get_counter("estadisticas", "invitados_unicos")
        
        stats = f"{base_stats}\n"
        stats += f"Entrevistas realizadas: {entrevistas}\n"
        stats += f"Tiempo total de conversación: {tiempo_total/3600:.1f} horas\n"
        stats += f"Frases detectadas: {frases}\n"
        stats += f"Invitados únicos: {invitados_unicos}\n"
        
        if entrevistas > 0:
            promedio_duracion = tiempo_total / entrevistas / 60
            promedio_frases = frases / entrevistas if entrevistas > 0 else 0
            stats += f"Duración promedio: {promedio_duracion:.1f} minutos\n"
            stats += f"Frases promedio por entrevista: {promedio_frases:.1f}\n"
        
        # Estado actual
        if self.conversacion_activa:
            stats += f"\nEstado: Conversación activa con {self.invitado_actual['nombre']}\n"
        else:
            stats += f"\nEstado: Sin conversación activa\n"
        
        # Invitados históricos
        invitados_historicos = self.data.get("invitados_historicos", {})
        if invitados_historicos:
            stats += f"\nInvitados históricos: {len(invitados_historicos)}\n"
            ultimo_invitado = max(invitados_historicos.items(), 
                                key=lambda x: x[1]["ultima_visita"])
            stats += f"Último invitado: {ultimo_invitado[0]}\n"
        
        return stats
    
    def cleanup(self):
        """Limpiar recursos"""
        self._limpiar_estado()

# Ejemplo de uso
if __name__ == "__main__":
    manager = ConversacionInvitadoManager()
    
    print("🎙️ PROBANDO MODO CONVERSACIÓN INVITADO...")
    
    # Mostrar tipos de entrevista
    print("\n" + manager.get_tipos_entrevista())
    
    # Iniciar conversación
    print("\n🎭 INICIANDO CONVERSACIÓN:")
    inicio = manager.iniciar_conversacion_invitado("Juan Pérez", "casual")
    print(inicio)
    
    # Simular conversación
    print("\n💬 SIMULANDO CONVERSACIÓN:")
    
    # Simular audio detectado
    frases_test = [
        "Hola, me da mucho gusto estar aquí",
        "Pues la verdad estoy un poco nervioso",
        "¿Qué tal si hacemos algunas preguntas?",
        "Me gusta mucho tu show"
    ]
    
    for frase in frases_test:
        print(f"\n🎤 Simulando audio: '{frase}'")
        respuesta = manager.procesar_audio_invitado(frase)
        if respuesta:
            print(f"🗣️ Poncho: {respuesta}")
        time.sleep(1)
    
    # Mostrar historial
    print("\n📝 HISTORIAL:")
    print(manager.get_historial_conversacion())
    
    # Finalizar conversación
    print("\n🏁 FINALIZANDO:")
    final = manager.finalizar_conversacion_invitado()
    print(final)
    
    print("\n✅ Pruebas completadas")