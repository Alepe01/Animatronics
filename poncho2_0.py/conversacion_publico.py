from base_manager import BaseManager
from response_handler import ResponseHandler, SarcasticResponder
import random
import time

class ConversacionPublicoManager(BaseManager):
    """Manager para conversación interactiva con el público"""
    
    def __init__(self, conversacion_file="conversacion_publico.json"):
        super().__init__(conversacion_file)
        self.conversacion_activa = False
        self.tema_actual = None
        self.participantes = {}  # username: participacion_count
        self.preguntas_publico = []
        print("🗣️ Conversación Público Manager inicializado")
    
    def _create_default_data(self):
        """Crear datos por defecto para conversación con público"""
        self.data = {
            "temas_conversacion": [
                {
                    "titulo": "Vida de Payaso",
                    "descripcion": "Hablemos sobre la vida en el circo",
                    "preguntas_iniciales": [
                        "¿Cómo es ser un payaso profesional?",
                        "¿Cuál es la parte más difícil de tu trabajo?",
                        "¿Siempre quisiste ser payaso?"
                    ]
                },
                {
                    "titulo": "Consejos de la Vida",
                    "descripcion": "Poncho da consejos sarcásticos sobre la vida",
                    "preguntas_iniciales": [
                        "¿Cuál es tu consejo para ser feliz?",
                        "¿Cómo superar los problemas?",
                        "¿Qué opinas sobre las redes sociales?"
                    ]
                },
                {
                    "titulo": "Experiencias del Circo",
                    "descripcion": "Anécdotas y historias del mundo circense",
                    "preguntas_iniciales": [
                        "¿Cuál fue tu peor actuación?",
                        "¿Tienes miedo a las alturas?",
                        "¿Has tenido accidentes graciosos?"
                    ]
                },
                {
                    "titulo": "Preguntas Personales",
                    "descripcion": "El público pregunta lo que quiera",
                    "preguntas_iniciales": [
                        "¿Cuál es tu comida favorita?",
                        "¿Tienes familia?",
                        "¿Qué haces en tu tiempo libre?"
                    ]
                }
            ],
            "respuestas_automaticas": {
                "saludo": [
                    "¡Hola a todos! Bienvenidos a mi charla, donde la sabiduría es opcional y el sarcasmo es garantizado.",
                    "¡Buenas! Espero que estén listos para una conversación llena de verdades dolorosas y chistes malos.",
                    "¡Saludos, querido público! Prepárense para escuchar opiniones que no pidieron."
                ],
                "despedida": [
                    "¡Hasta aquí la charla! Espero haber arruinado su día de manera entretenida.",
                    "¡Nos vemos! Recuerden: la vida es como mi maquillaje, se ve mejor de lejos.",
                    "¡Adiós! Que tengan un día tan bueno como mi humor... es decir, cuestionable."
                ],
                "sin_preguntas": [
                    "¿Nadie tiene preguntas? ¡Perfecto! Así me gusta, un público tan callado como inteligente.",
                    "El silencio es oro, pero sus preguntas serían... bueno, tal vez plata.",
                    "¿No hay curiosidad? ¡Excelente! Menos trabajo para mí."
                ]
            },
            "moderacion": {
                "palabras_prohibidas": ["spam", "publicidad", "enlace"],
                "respuestas_moderacion": [
                    "¡Oye! Este es un espacio de conversación, no de spam.",
                    "¿En serio? ¿Publicidad aquí? ¡Más respeto!",
                    "Nada de enlaces raros. Solo conversación civilizada... bueno, más o menos."
                ]
            },
            "estadisticas": {
                "conversaciones_iniciadas": 0,
                "preguntas_respondidas": 0,
                "participantes_unicos": 0
            },
            "version": "2.0"
        }
    
    def iniciar_conversacion(self, tema=None):
        """Iniciar conversación con el público"""
        if self.conversacion_activa:
            return "Ya hay una conversación activa. ¿Quieren cambiar de tema?"
        
        temas = self.data.get("temas_conversacion", [])
        if tema:
            # Buscar tema específico
            tema_encontrado = None
            for t in temas:
                if tema.lower() in t["titulo"].lower():
                    tema_encontrado = t
                    break
            
            if not tema_encontrado:
                return f"No encontré el tema '{tema}'. Temas disponibles: {', '.join([t['titulo'] for t in temas])}"
        else:
            # Tema aleatorio
            tema_encontrado = self.get_random_choice("temas_conversacion")
        
        if not tema_encontrado:
            return "No tengo temas de conversación disponibles."
        
        self.tema_actual = tema_encontrado
        self.conversacion_activa = True
        self.preguntas_publico = []
        
        # Incrementar estadísticas
        self.increment_counter("estadisticas", "conversaciones_iniciadas")
        
        # Mensaje de inicio
        saludo = self.get_random_choice("respuestas_automaticas")
        if saludo is None:
            saludo = "¡Hola a todos!"
        
        inicio = f"{saludo}\n\n🎭 CONVERSACIÓN ABIERTA: {tema_encontrado['titulo']}\n"
        inicio += f"📝 {tema_encontrado['descripcion']}\n\n"
        inicio += "¡Hagan sus preguntas! Prometo responder con toda la sinceridad de un payaso mentiroso."
        
        return inicio
    
    def procesar_comentario_publico(self, username, comentario):
        """Procesar comentario del público en conversación"""
        if not self.conversacion_activa:
            return "No hay conversación activa. Escribe 'iniciar conversación' para comenzar."
        
        # Limpiar comentario
        comentario_limpio = ResponseHandler.clean_text(comentario)
        
        # Verificar moderación
        if self._necesita_moderacion(comentario_limpio):
            return self._respuesta_moderacion()
        
        # Registrar participante
        if username not in self.participantes:
            self.participantes[username] = 0
            self.increment_counter("estadisticas", "participantes_unicos")
        
        self.participantes[username] += 1
        
        # Detectar si es pregunta
        if self._es_pregunta(comentario_limpio):
            return self._responder_pregunta(username, comentario_limpio)
        else:
            return self._responder_comentario_general(username, comentario_limpio)
    
    def _es_pregunta(self, texto):
        """Determinar si es una pregunta"""
        # Indicadores de pregunta
        indicadores_pregunta = [
            "?", "qué", "cómo", "cuál", "cuándo", "dónde", "por qué", "quién",
            "what", "how", "which", "when", "where", "why", "who"
        ]
        
        texto_lower = texto.lower()
        return any(indicador in texto_lower for indicador in indicadores_pregunta)
    
    def _responder_pregunta(self, username, pregunta):
        """Responder pregunta del público"""
        self.preguntas_publico.append({
            "usuario": username,
            "pregunta": pregunta,
            "timestamp": time.time()
        })
        
        self.increment_counter("estadisticas", "preguntas_respondidas")
        
        # Generar respuesta basada en el tema actual
        respuesta = self._generar_respuesta_tematica(username, pregunta)
        
        # Personalizar usando ResponseHandler
        respuesta_personalizada = ResponseHandler.personalize_by_name(username, respuesta)
        
        return f"🤔 Pregunta de {username}: {pregunta}\n\n💭 {respuesta_personalizada}"
    
    def _generar_respuesta_tematica(self, username, pregunta):
        """Generar respuesta según el tema actual"""
        if not self.tema_actual:
            return "Buena pregunta, pero mi cerebro de payaso está más confundido que de costumbre."
        
        tema_titulo = self.tema_actual["titulo"].lower()
        pregunta_lower = pregunta.lower()
        
        # Respuestas específicas por tema
        if "vida de payaso" in tema_titulo:
            if ResponseHandler.detect_keywords(pregunta_lower, ["difícil", "duro", "problema"]):
                respuestas = [
                    "Lo más difícil es fingir que disfruto haciendo reír a gente como tú.",
                    "El reto más grande es no llorar bajo el maquillaje... aunque a veces lo hago.",
                    "La parte difícil es explicarle a mi familia por qué elegí esta carrera."
                ]
            elif ResponseHandler.detect_keywords(pregunta_lower, ["siempre", "quisiste", "soñabas"]):
                respuestas = [
                    "Desde niño soñé con hacer reír a la gente. Luego crecí y me di cuenta que era mejor hacerlos llorar.",
                    "¿Querer ser payaso? Más bien la vida me convirtió en uno sin preguntarme.",
                    "Mi vocación llegó cuando descubrí que ya tenía la cara para ello."
                ]
            else:
                respuestas = [
                    "Ser payaso es como ser terapeuta, pero con peor sueldo y mejor maquillaje.",
                    "Mi trabajo es simple: hacer reír a otros mientras yo muero por dentro.",
                    "El circo es mi hogar, aunque más bien parece un manicomio ambulante."
                ]
        
        elif "consejos" in tema_titulo:
            if ResponseHandler.detect_keywords(pregunta_lower, ["feliz", "felicidad", "alegría"]):
                respuestas = [
                    "Para ser feliz: baja tus expectativas hasta el suelo, luego bájalas más.",
                    "La felicidad está sobrevalorada. Mejor confórmate con no estar completamente miserable.",
                    "Mi consejo: encuentra a alguien más infeliz que tú y siéntete mejor."
                ]
            elif ResponseHandler.detect_keywords(pregunta_lower, ["problemas", "superar", "difícil"]):
                respuestas = [
                    "Los problemas son como el maquillaje: siempre se ven peor de cerca.",
                    "Para superar problemas: ignóralos hasta que se vuelvan más grandes. Funciona genial.",
                    "Mi estrategia es simple: si no puedes resolver un problema, búrlate de él."
                ]
            else:
                respuestas = [
                    "Mi filosofía de vida: si vas a fracasar, al menos hazlo con estilo.",
                    "El mejor consejo que puedo dar es... bueno, no me hagas caso en nada.",
                    "La vida es como un chiste malo: no tiene sentido, pero alguien se ríe."
                ]
        
        elif "circo" in tema_titulo:
            respuestas = [
                "En el circo cada día es una aventura... generalmente desastrosa.",
                "Mis compañeros del circo son como una familia disfuncional que no puedo abandonar.",
                "Las historias del circo son tan increíbles que hasta yo dudo si son reales.",
                "El circo me ha enseñado que la vida es un espectáculo, y yo soy el acto de relleno."
            ]
        
        else:  # Preguntas personales u otras
            if ResponseHandler.detect_keywords(pregunta_lower, ["comida", "comer", "favorita"]):
                respuestas = [
                    "Mi comida favorita son las lágrimas de los niños... ¡Es broma! Prefiero pizza fría.",
                    "Como de todo, especialmente las críticas. Son muy nutritivas para el alma.",
                    "Mi dieta consiste principalmente en decepción y algodón de azúcar."
                ]
            elif ResponseHandler.detect_keywords(pregunta_lower, ["familia", "esposa", "hijos"]):
                respuestas = [
                    "Mi familia me abandonó cuando se dieron cuenta de que el maquillaje no se quitaba.",
                    "Tengo una familia, pero prefieren fingir que no me conocen en público.",
                    "Mis únicos familiares son los otros payasos, y eso ya dice mucho."
                ]
            else:
                respuestas = [
                    "Esa es una pregunta muy personal... casi tanto como preguntarme por qué sigo vivo.",
                    "Mi vida privada es tan emocionante como ver pintura secarse, pero con menos color.",
                    "Prefiero no hablar de mi vida personal, ya es suficientemente trágica siendo pública."
                ]
        
        return random.choice(respuestas)
    
    def _responder_comentario_general(self, username, comentario):
        """Responder comentario que no es pregunta"""
        # Detectar tipo de comentario
        comentario_lower = comentario.lower()
        
        if ResponseHandler.detect_keywords(comentario_lower, ["gracioso", "divertido", "me gusta"]):
            respuestas = [
                f"Gracias {username}, aunque no sé si creer en tu buen gusto.",
                f"Me alegra que te guste {username}, eres de los pocos con criterio... cuestionable.",
                f"{username}, tu aprobación significa mucho... bueno, no tanto, pero algo."
            ]
        
        elif ResponseHandler.detect_keywords(comentario_lower, ["aburrido", "malo", "no me gusta"]):
            respuestas = [
                f"¿Aburrido, {username}? ¡Perfecto! Así sé que estoy siendo auténtico.",
                f"Lo siento {username}, no todos pueden apreciar el arte de la mediocridad.",
                f"{username}, tu opinión es muy valiosa... para el basurero."
            ]
        
        elif ResponseHandler.detect_keywords(comentario_lower, ["hola", "saludos", "buenas"]):
            respuestas = [
                f"¡Hola {username}! Bienvenido a mi charla, donde la lógica viene a morir.",
                f"Saludos {username}, espero que estés preparado para la decepción.",
                f"¡{username}! Otro valiente se une a este espectáculo de horror."
            ]
        
        else:
            # Respuesta general
            respuestas = [
                f"Interesante comentario, {username}. Casi tan profundo como un charco.",
                f"{username}, tu aporte es... bueno, es un aporte.",
                f"Gracias por compartir eso, {username}. Realmente enriquece... algo."
            ]
        
        return random.choice(respuestas)
    
    def _necesita_moderacion(self, texto):
        """Verificar si el comentario necesita moderación"""
        palabras_prohibidas = self.data.get("moderacion", {}).get("palabras_prohibidas", [])
        return ResponseHandler.detect_keywords(texto.lower(), palabras_prohibidas)
    
    def _respuesta_moderacion(self):
        """Respuesta de moderación"""
        respuestas = self.data.get("moderacion", {}).get("respuestas_moderacion", [
            "¡Oye! Mantengamos la conversación civilizada... más o menos."
        ])
        return random.choice(respuestas)
    
    def finalizar_conversacion(self):
        """Finalizar conversación actual"""
        if not self.conversacion_activa:
            return "No hay conversación activa que finalizar."
        
        # Estadísticas de la sesión
        num_preguntas = len(self.preguntas_publico)
        num_participantes = len(self.participantes)
        
        despedida = self.get_random_choice("respuestas_automaticas") or "¡Hasta luego!"
        
        resultado = f"{despedida}\n\n"
        resultado += f"📊 RESUMEN DE LA CONVERSACIÓN:\n"
        resultado += f"Tema: {self.tema_actual['titulo']}\n"
        resultado += f"Preguntas respondidas: {num_preguntas}\n"
        resultado += f"Participantes: {num_participantes}\n\n"
        resultado += "¡Gracias por participar en este caos organizado!"
        
        # Limpiar estado
        self.conversacion_activa = False
        self.tema_actual = None
        self.participantes = {}
        self.preguntas_publico = []
        
        return resultado
    
    def get_temas_disponibles(self):
        """Obtener lista de temas disponibles"""
        temas = self.data.get("temas_conversacion", [])
        if not temas:
            return "No hay temas disponibles para conversar."
        
        lista = "🎭 TEMAS DE CONVERSACIÓN DISPONIBLES:\n\n"
        for i, tema in enumerate(temas, 1):
            lista += f"{i}. {tema['titulo']}\n   {tema['descripcion']}\n\n"
        
        lista += "Escribe 'iniciar conversación [tema]' para comenzar!"
        return lista
    
    def get_estado_conversacion(self):
        """Obtener estado actual de la conversación"""
        if not self.conversacion_activa:
            return "No hay conversación activa."
        
        estado = f"🎭 CONVERSACIÓN ACTIVA: {self.tema_actual['titulo']}\n"
        estado += f"Participantes: {len(self.participantes)}\n"
        estado += f"Preguntas: {len(self.preguntas_publico)}\n\n"
        
        if self.preguntas_publico:
            estado += "Últimas preguntas:\n"
            for pregunta in self.preguntas_publico[-3:]:
                estado += f"- {pregunta['usuario']}: {pregunta['pregunta'][:50]}...\n"
        
        return estado
    
    def get_conversacion_stats(self):
        """Obtener estadísticas usando método heredado"""
        base_stats = self.get_stats()
        
        conversaciones = self.get_counter("estadisticas", "conversaciones_iniciadas")
        preguntas = self.get_counter("estadisticas", "preguntas_respondidas")
        participantes = self.get_counter("estadisticas", "participantes_unicos")
        
        stats = f"{base_stats}\n"
        stats += f"Conversaciones iniciadas: {conversaciones}\n"
        stats += f"Preguntas respondidas: {preguntas}\n"
        stats += f"Participantes únicos: {participantes}\n"
        
        if conversaciones > 0:
            promedio_preguntas = preguntas / conversaciones
            stats += f"Promedio preguntas por conversación: {promedio_preguntas:.1f}\n"
        
        # Estado actual
        if self.conversacion_activa:
            stats += f"\nEstado: Conversación activa ({self.tema_actual['titulo']})\n"
            stats += f"Participantes actuales: {len(self.participantes)}\n"
        else:
            stats += f"\nEstado: Sin conversación activa\n"
        
        return stats

# Ejemplo de uso
if __name__ == "__main__":
    manager = ConversacionPublicoManager()
    
    print("🗣️ PROBANDO MODO CONVERSACIÓN PÚBLICO...")
    
    # Mostrar temas disponibles
    print("\n" + manager.get_temas_disponibles())
    
    # Iniciar conversación
    print("\n🎭 INICIANDO CONVERSACIÓN:")
    inicio = manager.iniciar_conversacion("vida de payaso")
    print(inicio)
    
    # Simular preguntas del público
    print("\n💬 SIMULANDO PREGUNTAS:")
    preguntas_test = [
        ("Juan", "¿Cómo empezaste a ser payaso?"),
        ("Ana", "¿Cuál es la parte más difícil de tu trabajo?"),
        ("Pedro", "Me encantas, eres muy gracioso"),
        ("Luis", "¿Tienes familia?")
    ]
    
    for usuario, pregunta in preguntas_test:
        respuesta = manager.procesar_comentario_publico(usuario, pregunta)
        print(f"\n{usuario}: {pregunta}")
        print(f"Poncho: {respuesta}")
    
    # Finalizar conversación
    print("\n🏁 FINALIZANDO:")
    final = manager.finalizar_conversacion()
    print(final)
    
    print("\n✅ Pruebas completadas")