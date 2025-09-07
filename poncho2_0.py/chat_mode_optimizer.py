from base_manager import BaseManager
from response_handler import ResponseHandler
import hashlib
import time
import random
import threading
from collections import defaultdict, deque

class ChatModeOptimizer(BaseManager):
    """Optimizador para el Modo 1 Chat que resuelve problemas de variabilidad y rendimiento"""
    
    def __init__(self, openai_client=None, optimizer_file="chat_optimizer.json"):
        super().__init__(optimizer_file)
        self.openai_client = openai_client
        self.response_cache = {}  # Cache de respuestas
        self.user_patterns = defaultdict(list)  # Patrones por usuario
        self.repeated_questions = defaultdict(int)  # Contador de preguntas repetidas
        self.batch_processing = True
        self.max_batch_size = 15  # Máximo de comentarios por lote
        self.processing_timeout = 8  # Timeout para generar respuesta
        print("🧠 Chat Mode Optimizer inicializado")
    
    def _create_default_data(self):
        """Crear datos por defecto para el optimizador"""
        self.data = {
            "response_variations": {
                # Variaciones para preguntas repetidas comunes
                "como_estas": [
                    "¿Cómo estoy? Como un payaso en una funeral: fuera de lugar pero entreteniendo.",
                    "Estoy como siempre: fingiendo que todo está bien mientras por dentro grito.",
                    "Mi estado emocional es como mi maquillaje: una máscara colorida sobre el vacío.",
                    "¿Yo? Estoy viviendo el sueño... de otra persona, porque el mío se volvió pesadilla.",
                    "Como un globo desinflado: aún floto, pero ya no tengo la misma gracia."
                ],
                "que_haces": [
                    "¿Qué hago? Fingir que soy gracioso mientras mi vida se desmorona lentamente.",
                    "Lo mismo de siempre: hacer reír a otros mientras lloro por dentro.",
                    "Actualmente estoy cuestionando mis decisiones de vida... todas fueron malas.",
                    "Trabajo en mi nueva comedia: 'Cómo arruinar tu vida en 10 pasos fáciles'.",
                    "Practico mi sonrisa falsa. Ya llevo 47 años y aún no la perfecciono."
                ],
                "eres_gracioso": [
                    "¿Gracioso? Soy tan gracioso como un accidente de tráfico... la gente se queda viendo pero nadie disfruta.",
                    "Mi humor es como el vino barato: parece buena idea hasta que lo pruebas.",
                    "Gracioso es una palabra muy generosa. Prefiero 'tragicómico'.",
                    "Si soy gracioso, entonces mi vida es una comedia... pero del tipo que te hace llorar.",
                    "Mi humor es tan negro que absorbe la luz de las sonrisas ajenas."
                ],
                "eres_malo": [
                    "¿Malo? Nah, soy pésimo. Hay una diferencia: lo malo tiene potencial de mejorar.",
                    "No soy malo, soy un artista incomprendido... muy, muy incomprendido.",
                    "Malo es quedarse corto. Soy un desastre con patas y maquillaje.",
                    "Al menos reconoces mi talento para la mediocridad. Eso ya es algo.",
                    "Malo implica que hay algo bueno con qué comparar. En mi caso, no existe tal punto de referencia."
                ],
                "saludo": [
                    "Hola... otra víctima se acerca a mi espectáculo de horror.",
                    "¡Saludos! Bienvenido a mi crisis existencial en tiempo real.",
                    "Hola, espero que tengas mejores planes de vida que yo.",
                    "¡Hey! Otro espectador para mi tragedia personal.",
                    "Saludos, querida audiencia de mi descenso a la locura."
                ]
            },
            "batch_templates": {
                # Templates para diferentes tamaños de lote
                "small_batch": "Responde a estos {count} comentarios con sarcasmo:",
                "medium_batch": "El chat está activo con {count} mensajes. Responde como Poncho:",
                "large_batch": "Muchos comentarios ({count}). Haz una respuesta general sarcástica que cubra el ambiente:"
            },
            "fallback_responses": [
                "Mi cerebro de payaso se sobrecargó con tantos comentarios brillantes.",
                "Wow, tanta sabiduría junta que no sé por dónde empezar a burlarme.",
                "El chat está más activo que mi carrera... y eso no es decir mucho.",
                "Tantos mensajes, tan poco tiempo para insultarlos a todos individualmente.",
                "Mi sarcasmo no da abasto para tanta 'profundidad' intelectual."
            ],
            "anti_spam_responses": [
                "¿En serio vas a repetir lo mismo? Mi creatividad para insultarte también tiene límites.",
                "Ya preguntaste eso. ¿Tu memoria es tan mala como tu sentido del humor?",
                "Repetir la misma pregunta no va a cambiar que sigues siendo aburrido.",
                "¿Esta es tu estrategia? ¿Aburrir al payaso hasta la muerte? Está funcionando.",
                "Si vas a ser molesto, al menos sé original en tu molestia."
            ],
            "configuracion": {
                "max_repetitions_before_variation": 3,
                "cache_expiry_minutes": 30,
                "batch_size_small": 5,
                "batch_size_medium": 10,
                "response_timeout_seconds": 8
            },
            "estadisticas": {
                "respuestas_generadas": 0,
                "respuestas_desde_cache": 0,
                "preguntas_repetidas_detectadas": 0,
                "timeouts": 0
            },
            "version": "2.0"
        }
    
    def process_comments_optimized(self, comments_batch):
        """Procesar comentarios con optimizaciones"""
        if not comments_batch:
            return None
        
        start_time = time.time()
        batch_size = len(comments_batch)
        
        # Estrategia según tamaño del lote
        if batch_size <= 5:
            return self._process_small_batch(comments_batch)
        elif batch_size <= 15:
            return self._process_medium_batch(comments_batch)
        else:
            return self._process_large_batch(comments_batch)
    
    def _process_small_batch(self, comments_batch):
        """Procesar lote pequeño (1-5 comentarios) - Respuestas individuales"""
        responses = []
        
        for username, comment, msg_type in comments_batch:
            # Verificar si es pregunta repetida
            question_hash = self._get_question_hash(comment)
            repetition_count = self.repeated_questions[question_hash]
            
            if repetition_count >= 3:
                response = self._get_anti_spam_response(username, comment)
                responses.append(f"{username}: {response}")
                continue
            
            # Intentar respuesta variada para preguntas comunes
            varied_response = self._get_varied_response(username, comment, repetition_count)
            if varied_response:
                responses.append(f"{username}: {varied_response}")
                self.repeated_questions[question_hash] += 1
                continue
            
            # Si no es pregunta repetida común, usar OpenAI con timeout
            ai_response = self._get_ai_response_with_timeout(username, comment)
            if ai_response:
                responses.append(f"{username}: {ai_response}")
            else:
                # Fallback si OpenAI falla
                fallback = self._get_fallback_response(username)
                responses.append(f"{username}: {fallback}")
        
        self.increment_counter("estadisticas", "respuestas_generadas")
        return "\n\n".join(responses)
    
    def _process_medium_batch(self, comments_batch):
        """Procesar lote mediano (6-15 comentarios) - Respuesta grupal"""
        # Agrupar por tipo de interacción
        questions = []
        compliments = []
        insults = []
        greetings = []
        others = []
        
        for username, comment, msg_type in comments_batch:
            comment_lower = comment.lower()
            
            if self._is_question(comment):
                questions.append((username, comment))
            elif ResponseHandler.detect_keywords(comment_lower, ["gracioso", "genial", "me gusta"]):
                compliments.append((username, comment))
            elif ResponseHandler.detect_keywords(comment_lower, ["malo", "aburrido", "no me gusta"]):
                insults.append((username, comment))
            elif ResponseHandler.detect_keywords(comment_lower, ["hola", "hi", "saludos"]):
                greetings.append((username, comment))
            else:
                others.append((username, comment))
        
        # Generar respuesta grupal inteligente
        return self._generate_group_response(questions, compliments, insults, greetings, others)
    
    def _process_large_batch(self, comments_batch):
        """Procesar lote grande (15+ comentarios) - Respuesta general"""
        batch_size = len(comments_batch)
        
        # Respuestas para lotes muy grandes
        large_batch_responses = [
            f"¡{batch_size} comentarios! ¿Esto es un chat o una invasión? Mi sarcasmo no da para tantos.",
            f"Wow, {batch_size} mensajes. El chat está más activo que mi vida amorosa... y eso es decir mucho.",
            f"¡{batch_size} comentarios! Si pusieran esa energía en algo útil... nah, mejor sigan aquí.",
            f"Tantos mensajes que mi cerebro de payaso se sobrecargó. Dejen de ser tan 'brillantes' todos a la vez.",
            f"¡{batch_size} comentarios! ¿Es mi cumpleaños o qué? Porque esto se siente como un castigo."
        ]
        
        # Mencionar algunos usuarios específicos
        mentioned_users = random.sample([c[0] for c in comments_batch], min(3, len(comments_batch)))
        user_mentions = ", ".join(mentioned_users)
        
        base_response = random.choice(large_batch_responses)
        return f"{base_response}\n\nSaludos especiales a {user_mentions} por contribuir al caos."
    
    def _get_varied_response(self, username, comment, repetition_count):
        """Obtener respuesta variada para preguntas comunes"""
        comment_lower = ResponseHandler.clean_text(comment).lower()
        
        # Detectar tipo de pregunta común
        variation_key = None
        
        if ResponseHandler.detect_keywords(comment_lower, ["como estas", "que tal", "how are you"]):
            variation_key = "como_estas"
        elif ResponseHandler.detect_keywords(comment_lower, ["que haces", "what are you doing"]):
            variation_key = "que_haces"
        elif ResponseHandler.detect_keywords(comment_lower, ["gracioso", "funny", "divertido"]):
            variation_key = "eres_gracioso"
        elif ResponseHandler.detect_keywords(comment_lower, ["malo", "bad", "terrible"]):
            variation_key = "eres_malo"
        elif ResponseHandler.detect_keywords(comment_lower, ["hola", "hi", "hey", "saludos"]):
            variation_key = "saludo"
        
        if variation_key:
            variations = self.data.get("response_variations", {}).get(variation_key, [])
            if variations:
                # Seleccionar variación basada en el número de repetición
                variation_index = repetition_count % len(variations)
                response = variations[variation_index]
                return ResponseHandler.personalize_by_name(username, response)
        
        return None
    
    def _get_anti_spam_response(self, username, comment):
        """Respuesta para usuarios que repiten mucho"""
        anti_spam = self.data.get("anti_spam_responses", [])
        response = random.choice(anti_spam) if anti_spam else "Ya preguntaste eso."
        
        self.increment_counter("estadisticas", "preguntas_repetidas_detectadas")
        return ResponseHandler.personalize_by_name(username, response)
    
    def _get_ai_response_with_timeout(self, username, comment):
        """Obtener respuesta de OpenAI con timeout"""
        if not self.openai_client:
            return None
        
        # Usar threading para timeout
        response_container = [None]
        
        def get_response():
            try:
                prompt = f"Responde como Poncho el payaso sarcástico a {username}: '{comment}'"
                
                completion = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres Poncho el payaso sarcástico. Respuestas cortas y mordaces."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=100,
                    timeout=self.processing_timeout
                )
                
                response_container[0] = completion.choices[0].message.content.strip()
            except Exception as e:
                print(f"Error OpenAI: {e}")
                response_container[0] = None
        
        # Ejecutar con timeout
        thread = threading.Thread(target=get_response)
        thread.start()
        thread.join(timeout=self.processing_timeout)
        
        if thread.is_alive():
            self.increment_counter("estadisticas", "timeouts")
            print("⏰ Timeout en respuesta OpenAI")
            return None
        
        return response_container[0]
    
    def _get_fallback_response(self, username):
        """Respuesta de respaldo cuando OpenAI falla"""
        fallbacks = self.data.get("fallback_responses", [])
        response = random.choice(fallbacks) if fallbacks else "Mi cerebro se descompuso."
        return ResponseHandler.personalize_by_name(username, response)
    
    def _generate_group_response(self, questions, compliments, insults, greetings, others):
        """Generar respuesta grupal inteligente"""
        parts = []
        
        # Saludar si hay saludos
        if greetings:
            names = [name for name, _ in greetings[:3]]
            parts.append(f"¡Hola {', '.join(names)}! Más víctimas para mi espectáculo.")
        
        # Responder a cumplidos
        if compliments:
            count = len(compliments)
            parts.append(f"{count} personas me halagan... claramente tienen mal gusto.")
        
        # Responder a insultos
        if insults:
            count = len(insults)
            parts.append(f"{count} personas me critican... al fin alguien con criterio.")
        
        # Responder a preguntas
        if questions:
            count = len(questions)
            if count == 1:
                username, question = questions[0]
                ai_response = self._get_ai_response_with_timeout(username, question)
                if ai_response:
                    parts.append(f"{username} pregunta: {ai_response}")
                else:
                    parts.append(f"{username}, tu pregunta es tan profunda que necesito tiempo para procesarla.")
            else:
                parts.append(f"{count} preguntas... ¿esto es un interrogatorio? Mi abogado dice que no responda.")
        
        # Comentarios generales
        if others:
            parts.append("El resto de comentarios son tan profundos que los haré marco para mi pared.")
        
        return " ".join(parts) if parts else "El chat está tan activo que no sé si reír o llorar... mejor ambos."
    
    def _is_question(self, text):
        """Determinar si es una pregunta"""
        indicators = ["?", "qué", "cómo", "cuál", "cuándo", "dónde", "por qué", "quién"]
        return any(indicator in text.lower() for indicator in indicators)
    
    def _get_question_hash(self, question):
        """Generar hash para detectar preguntas repetidas"""
        clean_question = ResponseHandler.clean_text(question).lower()
        # Remover palabras comunes para mejor detección
        words = clean_question.split()
        content_words = [w for w in words if w not in ["el", "la", "de", "que", "es", "por", "como"]]
        normalized = " ".join(sorted(content_words))
        return hashlib.md5(normalized.encode()).hexdigest()[:8]
    
    def get_optimizer_stats(self):
        """Obtener estadísticas del optimizador"""
        base_stats = self.get_stats()
        
        respuestas_generadas = self.get_counter("estadisticas", "respuestas_generadas")
        respuestas_cache = self.get_counter("estadisticas", "respuestas_desde_cache")
        preguntas_repetidas = self.get_counter("estadisticas", "preguntas_repetidas_detectadas")
        timeouts = self.get_counter("estadisticas", "timeouts")
        
        stats = f"{base_stats}\n"
        stats += f"Respuestas generadas: {respuestas_generadas}\n"
        stats += f"Respuestas desde cache: {respuestas_cache}\n"
        stats += f"Preguntas repetidas detectadas: {preguntas_repetidas}\n"
        stats += f"Timeouts de OpenAI: {timeouts}\n"
        
        if respuestas_generadas > 0:
            eficiencia = ((respuestas_generadas - timeouts) / respuestas_generadas) * 100
            stats += f"Eficiencia de respuesta: {eficiencia:.1f}%\n"
        
        stats += f"Preguntas únicas trackeadas: {len(self.repeated_questions)}\n"
        
        # Top preguntas más repetidas
        if self.repeated_questions:
            top_repeated = sorted(self.repeated_questions.items(), key=lambda x: x[1], reverse=True)[:5]
            stats += f"\nTop preguntas más repetidas:\n"
            for hash_q, count in top_repeated:
                stats += f"  Hash {hash_q}: {count} veces\n"
        
        return stats
    
    def clear_repeated_questions(self):
        """Limpiar historial de preguntas repetidas"""
        count = len(self.repeated_questions)
        self.repeated_questions.clear()
        return f"🧹 {count} patrones de preguntas repetidas limpiados."
    
    def add_custom_variation(self, trigger_words, responses):
        """Agregar variación personalizada"""
        key = "_".join(trigger_words)
        if "response_variations" not in self.data:
            self.data["response_variations"] = {}
        
        self.data["response_variations"][key] = responses
        self.save_data()
        return f"✅ Variación personalizada agregada para: {trigger_words}"

# Integración con ModeController
def integrate_chat_optimizer(mode_controller, openai_client):
    """Integrar el optimizador con el ModeController existente"""
    
    # Crear optimizador
    optimizer = ChatModeOptimizer(openai_client)
    
    # Reemplazar el método _handle_chat_mode original
    original_handle_chat = mode_controller._handle_chat_mode
    
    def optimized_handle_chat(comments_batch):
        """Versión optimizada del manejo de chat"""
        try:
            # Usar el optimizador
            response = optimizer.process_comments_optimized(comments_batch)
            if response:
                return response
            
            # Fallback al método original si el optimizador falla
            return original_handle_chat(comments_batch)
        
        except Exception as e:
            print(f"❌ Error en chat optimizado: {e}")
            return original_handle_chat(comments_batch)
    
    # Reemplazar el método
    mode_controller._handle_chat_mode = optimized_handle_chat
    mode_controller.chat_optimizer = optimizer
    
    print("🧠 Chat Optimizer integrado exitosamente")
    return optimizer

# Ejemplo de uso
if __name__ == "__main__":
    print("🧠 Probando Chat Optimizer...")
    
    # Crear optimizador
    optimizer = ChatModeOptimizer()
    
    # Simular diferentes tamaños de lote
    print("\n📝 LOTE PEQUEÑO (3 comentarios):")
    small_batch = [
        ("Juan", "¿Cómo estás?", "comment"),
        ("Ana", "Eres muy gracioso", "comment"),
        ("Pedro", "¿Cómo estás?", "comment")  # Repetida
    ]
    
    response = optimizer.process_comments_optimized(small_batch)
    print(response)
    
    print("\n📝 LOTE MEDIANO (8 comentarios):")
    medium_batch = [
        ("User1", "Hola", "comment"),
        ("User2", "¿Qué haces?", "comment"),
        ("User3", "Eres malo", "comment"),
        ("User4", "Me gusta tu show", "comment"),
        ("User5", "¿Cómo estás?", "comment"),
        ("User6", "Aburrido", "comment"),
        ("User7", "¿Tienes familia?", "comment"),
        ("User8", "Genial", "comment")
    ]
    
    response = optimizer.process_comments_optimized(medium_batch)
    print(response)
    
    print("\n📝 LOTE GRANDE (20+ comentarios):")
    large_batch = [(f"User{i}", f"Mensaje {i}", "comment") for i in range(25)]
    
    response = optimizer.process_comments_optimized(large_batch)
    print(response)
    
    # Estadísticas
    print(f"\n📊 ESTADÍSTICAS:")
    print(optimizer.get_optimizer_stats())
    
    print("\n✅ Pruebas del optimizador completadas")