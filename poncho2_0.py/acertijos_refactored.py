from base_manager import BaseManager
from response_handler import ResponseHandler, SarcasticResponder
import random
from difflib import SequenceMatcher

class AcertijoManager(BaseManager):
    """Manager de acertijos refactorizado usando BaseManager"""
    
    def __init__(self, acertijos_file="acertijos.json"):
        super().__init__(acertijos_file)
        self.acertijo_actual = None
        self.intentos_fallidos = {}
        print(f"🧩 Acertijo Manager inicializado con {len(self.data.get('acertijos', []))} acertijos")
    
    def _create_default_data(self):
        """Crear acertijos por defecto"""
        self.data = {
            "acertijos": [
                {
                    "pregunta": "Tengo agujas pero no coso, tengo números pero no soy matemático. ¿Qué soy?",
                    "respuestas": ["reloj", "reloj de pared", "cronometro", "cronómetro"],
                    "pistas": ["Mido el tiempo", "Estoy en la pared", "Hago tic-tac"],
                    "dificultad": "fácil",
                    "categoria": "objetos"
                },
                {
                    "pregunta": "Blanco por dentro, verde por fuera. Si quieres que te lo diga, espera.",
                    "respuestas": ["pera", "la pera"],
                    "pistas": ["Es una fruta", "Tiene forma de gota", "Rima con espera"],
                    "dificultad": "fácil",
                    "categoria": "frutas"
                },
                {
                    "pregunta": "Vuelo sin alas, lloro sin ojos. Donde quiera que voy, la oscuridad me sigue. ¿Qué soy?",
                    "respuestas": ["nube", "las nubes", "una nube"],
                    "pistas": ["Estoy en el cielo", "Traigo lluvia", "Bloqueo el sol"],
                    "dificultad": "medio",
                    "categoria": "naturaleza"
                },
                {
                    "pregunta": "Tengo ciudades, pero no casas. Tengo montañas, pero no árboles. Tengo agua, pero no peces. ¿Qué soy?",
                    "respuestas": ["mapa", "un mapa", "el mapa"],
                    "pistas": ["Me usan para ubicarse", "Soy de papel", "Muestro lugares"],
                    "dificultad": "medio",
                    "categoria": "objetos"
                },
                {
                    "pregunta": "Cuanto más seco, más mojado. ¿Qué soy?",
                    "respuestas": ["toalla", "la toalla", "una toalla"],
                    "pistas": ["Me usan después del baño", "Absorbo agua", "Cuelgo en el baño"],
                    "dificultad": "fácil",
                    "categoria": "objetos"
                },
                {
                    "pregunta": "Si me nombras, desaparezco. ¿Qué soy?",
                    "respuestas": ["silencio", "el silencio"],
                    "pistas": ["Soy la ausencia de algo", "Existo cuando no hay ruido", "Los bibliotecarios me aman"],
                    "dificultad": "difícil",
                    "categoria": "conceptos"
                },
                {
                    "pregunta": "Cuanto más le quitas, más grande se hace. ¿Qué es?",
                    "respuestas": ["hoyo", "el hoyo", "agujero", "el agujero", "hueco"],
                    "pistas": ["Se hace cavando", "Puede ser profundo", "Los mineros me hacen"],
                    "dificultad": "medio",
                    "categoria": "conceptos"
                }
            ],
            "ganadores": {},
            "categorias": ["objetos", "frutas", "naturaleza", "conceptos"],
            "dificultades": ["fácil", "medio", "difícil"],
            "estadisticas": {
                "acertijos_planteados": 0,
                "acertijos_resueltos": 0,
                "intentos_totales": 0
            },
            "version": "2.0"
        }
    
    def get_acertijo_aleatorio(self):
        """Obtener acertijo aleatorio usando método heredado"""
        acertijo = self.get_random_choice("acertijos")
        if not acertijo:
            return "¡No tengo acertijos! ¡Mi cerebro está más vacío que mi corazón!"
        
        self.acertijo_actual = acertijo
        self.intentos_fallidos = {}
        
        # Incrementar estadística
        self.increment_counter("estadisticas", "acertijos_planteados")
        
        # Emoji de dificultad
        difficulty_emoji = {
            "fácil": "🟢",
            "medio": "🟡", 
            "difícil": "🔴"
        }
        
        emoji = difficulty_emoji.get(acertijo["dificultad"], "❓")
        
        return f"🧩 ACERTIJO {emoji}:\n\n{acertijo['pregunta']}\n\n¡A ver si no eres tan tonto como pareces!"
    
    def verificar_respuesta(self, username, respuesta):
        """Verificar respuesta usando funciones comunes"""
        if not self.acertijo_actual:
            return "¡No hay acertijo activo, genio!"
        
        # Limpiar respuesta
        respuesta_limpia = self._limpiar_respuesta(ResponseHandler.clean_text(respuesta))
        respuestas_correctas = [self._limpiar_respuesta(r) for r in self.acertijo_actual["respuestas"]]
        
        # Incrementar intentos totales
        self.increment_counter("estadisticas", "intentos_totales")
        
        # Verificar respuesta exacta
        if respuesta_limpia in respuestas_correctas:
            return self._respuesta_correcta(username)
        
        # Verificar respuesta similar
        for respuesta_correcta in respuestas_correctas:
            similarity = ResponseHandler.get_similarity(respuesta_limpia, respuesta_correcta)
            if similarity > 0.8:
                return self._respuesta_correcta(username)
        
        return self._respuesta_incorrecta(username)
    
    def _limpiar_respuesta(self, respuesta):
        """Limpiar respuesta para comparación"""
        respuesta_limpia = respuesta.lower().strip()
        
        # Remover artículos y palabras comunes
        palabras_ignorar = ["el", "la", "los", "las", "un", "una", "es", "soy"]
        palabras = respuesta_limpia.split()
        palabras_filtradas = [p for p in palabras if p not in palabras_ignorar]
        
        return " ".join(palabras_filtradas) if palabras_filtradas else respuesta_limpia
    
    def _respuesta_correcta(self, username):
        """Manejar respuesta correcta"""
        # Actualizar puntuación usando método heredado
        self.increment_counter("ganadores", username)
        self.increment_counter("estadisticas", "acertijos_resueltos")
        
        # Limpiar intentos fallidos
        if username in self.intentos_fallidos:
            del self.intentos_fallidos[username]
        
        # Respuestas sarcásticas de felicitación
        felicitaciones = [
            f"¡Correcto, {username}! ¡Hasta un reloj descompuesto da la hora correcta dos veces al día!",
            f"¡Bien {username}! ¡Por fin usaste esa cosa que tienes entre las orejas!",
            f"¡Exacto, {username}! ¡Veo que no eres tan inútil como pensé!",
            f"¡Correcto, {username}! ¡Felicidades por tener más de dos neuronas funcionando!",
        ]
        
        respuesta = random.choice(felicitaciones)
        aciertos = self.get_counter("ganadores", username)
        respuesta += f"\n\n🏆 Llevas {aciertos} acertijos correctos."
        
        # Personalizar usando ResponseHandler
        respuesta = ResponseHandler.personalize_by_name(username, respuesta)
        
        # Limpiar acertijo actual
        self.acertijo_actual = None
        
        return respuesta
    
    def _respuesta_incorrecta(self, username):
        """Manejar respuesta incorrecta"""
        # Incrementar intentos fallidos
        if username not in self.intentos_fallidos:
            self.intentos_fallidos[username] = 0
        self.intentos_fallidos[username] += 1
        
        intentos = self.intentos_fallidos[username]
        
        # Respuestas escaladas usando SarcasticResponder
        if intentos == 1:
            burlas = [
                f"¡Incorrecto, {username}! ¡Pero no te preocupes, todos empezamos siendo tontos!",
                f"¡Fallaste, {username}! ¡Inténtalo de nuevo, a ver si la suerte te acompaña!",
                f"¡Nope, {username}! ¡Tu cerebro necesita más ejercicio!",
            ]
        elif intentos == 2:
            burlas = [
                f"¡Otra vez mal, {username}! ¡Tu récord de fracasos va creciendo!",
                f"¡Dos errores, {username}! ¡Impresionante consistencia en ser malo!",
                f"¡Fallaste de nuevo, {username}! ¡Al menos eres constante!",
            ]
        elif intentos == 3:
            burlas = [
                f"¡Tres errores, {username}! ¡Eres todo un profesional... del fracaso!",
                f"¡Triple falla, {username}! ¡Tu talento para errar es impresionante!",
                f"¡Tercera vez mal, {username}! ¡Deberías dedicarte a otra cosa!",
            ]
        else:
            burlas = [
                f"¡{intentos} errores, {username}! ¡Ya perdí la cuenta de tus fracasos!",
                f"¡Sigues fallando, {username}! ¡Al menos eres entretenido!",
                f"¡{intentos} intentos y nada, {username}! ¡Eres una obra de arte... del desastre!",
            ]
        
        respuesta = random.choice(burlas)
        
        # Dar pista después de varios intentos
        if intentos >= 2 and self.acertijo_actual:
            pistas = self.acertijo_actual.get("pistas", [])
            if pistas:
                pista_index = min(intentos - 2, len(pistas) - 1)
                respuesta += f"\n\n💡 Pista: {pistas[pista_index]}"
        
        # Revelar respuesta después de muchos intentos
        if intentos >= 5 and self.acertijo_actual:
            respuesta_correcta = self.acertijo_actual["respuestas"][0]
            respuesta += f"\n\n🤦 La respuesta era: {respuesta_correcta}"
            respuesta += f"\n¡Pero {username}, ¡ni regalada la adivinaste!"
            self.acertijo_actual = None
        
        return ResponseHandler.personalize_by_name(username, respuesta)
    
    def dar_pista(self):
        """Dar pista del acertijo actual"""
        if not self.acertijo_actual:
            return "¡No hay acertijo activo para dar pistas, genio!"
        
        pistas = self.acertijo_actual.get("pistas", [])
        if not pistas:
            return "¡Este acertijo no tiene pistas! ¡Arréglate como puedas!"
        
        pista = random.choice(pistas)
        return f"💡 Pista: {pista}\n\n¡Espero que eso ayude a tu cerebro de mosquito!"
    
    def get_acertijo_by_categoria(self, categoria):
        """Obtener acertijo de una categoría específica"""
        acertijos = self.data.get("acertijos", [])
        acertijos_categoria = [a for a in acertijos if a.get("categoria", "").lower() == categoria.lower()]
        
        if not acertijos_categoria:
            return f"No tengo acertijos de '{categoria}', ¡pero tengo muchos de lo inútil que eres!"
        
        self.acertijo_actual = random.choice(acertijos_categoria)
        self.intentos_fallidos = {}
        self.increment_counter("estadisticas", "acertijos_planteados")
        
        difficulty_emoji = {"fácil": "🟢", "medio": "🟡", "difícil": "🔴"}
        emoji = difficulty_emoji.get(self.acertijo_actual["dificultad"], "❓")
        
        return f"🧩 ACERTIJO DE {categoria.upper()} {emoji}:\n\n{self.acertijo_actual['pregunta']}\n\n¡A ver si sabes algo de {categoria}!"
    
    def get_ranking(self):
        """Obtener ranking de ganadores"""
        ganadores = self.data.get("ganadores", {})
        if not ganadores:
            return "¡No hay ganadores aún! ¡Todos son igual de inútiles!"
        
        ranking = sorted(ganadores.items(), key=lambda x: x[1], reverse=True)
        
        resultado = "🏆 RANKING DE ACERTIJOS:\n\n"
        for i, (username, aciertos) in enumerate(ranking[:10], 1):
            medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
            resultado += f"{medal} {username}: {aciertos} acertijos\n"
        
        return resultado
    
    def responder_comentario_modo_acertijo(self, username, comentario):
        """Responder comentarios en modo acertijo usando ResponseHandler"""
        comentario_lower = ResponseHandler.clean_text(comentario).lower()
        
        # Comandos especiales
        if ResponseHandler.detect_keywords(comentario_lower, ["pista", "ayuda", "hint"]):
            return self.dar_pista()
        
        if ResponseHandler.detect_keywords(comentario_lower, ["ranking", "puntuacion", "puntaje"]):
            return self.get_ranking()
        
        if ResponseHandler.detect_keywords(comentario_lower, ["nuevo", "otro", "siguiente"]):
            return self.get_acertijo_aleatorio()
        
        # Si hay acertijo activo, verificar respuesta
        if self.acertijo_actual:
            return self.verificar_respuesta(username, comentario)
        
        # Si no hay acertijo activo, dar uno nuevo
        return self.get_acertijo_aleatorio()
    
    def get_acertijo_stats(self):
        """Obtener estadísticas usando método heredado"""
        base_stats = self.get_stats()
        
        # Estadísticas específicas
        planteados = self.get_counter("estadisticas", "acertijos_planteados")
        resueltos = self.get_counter("estadisticas", "acertijos_resueltos")
        intentos = self.get_counter("estadisticas", "intentos_totales")
        
        # Análisis por categorías y dificultades
        categorias = {}
        dificultades = {}
        
        for acertijo in self.data.get("acertijos", []):
            cat = acertijo.get("categoria", "sin categoría")
            dif = acertijo.get("dificultad", "sin dificultad")
            categorias[cat] = categorias.get(cat, 0) + 1
            dificultades[dif] = dificultades.get(dif, 0) + 1
        
        stats = f"{base_stats}\n"
        stats += f"Acertijos planteados: {planteados}\n"
        stats += f"Acertijos resueltos: {resueltos}\n"
        stats += f"Intentos totales: {intentos}\n"
        
        if planteados > 0:
            tasa_exito = (resueltos / planteados) * 100
            stats += f"Tasa de éxito: {tasa_exito:.1f}%\n"
        
        stats += f"Jugadores: {len(self.data.get('ganadores', {}))}\n"
        
        stats += f"\nCategorías:\n"
        for cat, count in sorted(categorias.items()):
            stats += f"  - {cat}: {count}\n"
        
        stats += f"\nDificultades:\n"
        for dif, count in sorted(dificultades.items()):
            stats += f"  - {dif}: {count}\n"
        
        return stats
    
    def agregar_acertijo(self, pregunta, respuestas, pistas=None, dificultad="medio", categoria="personalizado"):
        """Agregar nuevo acertijo"""
        nuevo_acertijo = {
            "pregunta": pregunta,
            "respuestas": respuestas if isinstance(respuestas, list) else [respuestas],
            "pistas": pistas or [],
            "dificultad": dificultad,
            "categoria": categoria
        }
        
        self.add_item_to_list("acertijos", nuevo_acertijo)
        return f"✅ Acertijo agregado a categoría: {categoria}"
    
    def search_acertijos(self, keyword):
        """Buscar acertijos por palabra clave"""
        keyword_lower = keyword.lower()
        matching_riddles = []
        
        for acertijo in self.data.get("acertijos", []):
            if keyword_lower in acertijo["pregunta"].lower():
                matching_riddles.append(acertijo)
        
        if not matching_riddles:
            return f"No encontré acertijos sobre '{keyword}'. ¡Pero encontré uno sobre lo tonto que eres!"
        
        return f"🔍 Encontré {len(matching_riddles)} acertijos sobre '{keyword}'"
    
    def get_categorias(self):
        """Obtener categorías disponibles usando método heredado"""
        return self.data.get("categorias", [])
    
    def reset_game(self):
        """Resetear juego actual"""
        self.acertijo_actual = None
        self.intentos_fallidos = {}
        return "🔄 Juego reseteado. ¡Listo para un nuevo acertijo!"
    
    def get_current_riddle_info(self):
        """Obtener información del acertijo actual"""
        if not self.acertijo_actual:
            return "No hay acertijo activo actualmente."
        
        info = f"🧩 Acertijo actual:\n"
        info += f"Pregunta: {self.acertijo_actual['pregunta']}\n"
        info += f"Categoría: {self.acertijo_actual.get('categoria', 'N/A')}\n"
        info += f"Dificultad: {self.acertijo_actual.get('dificultad', 'N/A')}\n"
        info += f"Intentos fallidos: {dict(self.intentos_fallidos)}\n"
        
        return info

# Ejemplo de uso
if __name__ == "__main__":
    manager = AcertijoManager()
    
    print(f"🧩 Total de acertijos: {len(manager.data.get('acertijos', []))}")
    print(f"📂 Categorías: {manager.get_categorias()}")
    
    print("\n🧩 ACERTIJO ALEATORIO:")
    acertijo = manager.get_acertijo_aleatorio()
    print(acertijo)
    
    print(f"\n📈 ESTADÍSTICAS:")
    print(manager.get_acertijo_stats())