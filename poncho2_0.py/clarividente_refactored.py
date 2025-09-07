from base_manager import BaseManager
from response_handler import ResponseHandler
import random

class ClarividenteManager(BaseManager):
    """Manager clarividente refactorizado usando BaseManager"""
    
    def __init__(self, predicciones_file="predicciones.json"):
        super().__init__(predicciones_file)
        print(f"🔮 Clarividente Manager inicializado")
    
    def _create_default_data(self):
        """Crear predicciones por defecto"""
        self.data = {
            "frases_mysticas": [
                "Las cartas me susurran...",
                "Mi bola de cristal se nubla...",
                "Los espíritus del circo me dicen...",
                "Las estrellas revelan...",
                "El cosmos payaso me muestra...",
                "Mi tercer ojo de payaso ve...",
                "Los antepasados del circo confirman...",
                "La energía universal indica...",
                "Las fuerzas místicas revelan...",
                "Mi sabiduría ancestral dice...",
                "Los vientos del destino murmuran...",
                "La magia antigua predice..."
            ],
            "predicciones_genericas": [
                {
                    "tipo": "amor",
                    "prediccion": "Veo romance en tu futuro... pero también veo que hueles raro!",
                    "probabilidad": "73%"
                },
                {
                    "tipo": "dinero", 
                    "prediccion": "El dinero llegará a ti... cuando dejes de ser tan tacaño conmigo",
                    "probabilidad": "42%"
                },
                {
                    "tipo": "salud",
                    "prediccion": "Tu salud mejorará... si dejas de comer tanto y haces ejercicio",
                    "probabilidad": "67%"
                },
                {
                    "tipo": "trabajo",
                    "prediccion": "Un cambio laboral se aproxima... espero que sea para mejor",
                    "probabilidad": "55%"
                },
                {
                    "tipo": "viaje",
                    "prediccion": "Viajarás pronto... aunque sea solo al supermercado",
                    "probabilidad": "89%"
                },
                {
                    "tipo": "familia",
                    "prediccion": "Tu familia tendrá noticias... probablemente de que estás loco hablando conmigo",
                    "probabilidad": "91%"
                },
                {
                    "tipo": "secreto",
                    "prediccion": "Alguien te oculta algo... probablemente que piensa que estás loco",
                    "probabilidad": "85%"
                },
                {
                    "tipo": "sorpresa",
                    "prediccion": "Una sorpresa te espera... y no será agradable",
                    "probabilidad": "74%"
                }
            ],
            "predicciones_personales": {},
            "estadisticas": {
                "predicciones_dadas": 0,
                "usuarios_consultados": 0
            },
            "version": "2.0"
        }
    
    def get_prediccion_for_user(self, username):
        """Obtener predicción específica para un usuario"""
        predicciones_personales = self.data.get("predicciones_personales", {})
        username_lower = username.lower()
        
        # Si ya tiene predicción guardada, devolverla
        if username_lower in predicciones_personales:
            stored = predicciones_personales[username_lower]
            frase_mistica = self.get_random_choice("frases_mysticas")
            return f"🔮 {frase_mistica} {stored['prediccion']} (Probabilidad: {stored['probabilidad']})"
        
        # Crear nueva predicción
        prediccion_base = self.get_random_choice("predicciones_genericas")
        if not prediccion_base:
            return "Mi bola de cristal está rota! No puedo ver tu futuro."
        
        # Personalizar usando ResponseHandler
        prediccion_personalizada = self._personalizar_prediccion(username, prediccion_base.copy())
        
        # Guardar para futuras consultas
        predicciones_personales[username_lower] = {
            "prediccion": prediccion_personalizada["prediccion"],
            "tipo": prediccion_personalizada["tipo"],
            "probabilidad": prediccion_personalizada["probabilidad"]
        }
        self.data["predicciones_personales"] = predicciones_personales
        
        # Incrementar estadísticas
        self.increment_counter("estadisticas", "predicciones_dadas")
        if username_lower not in predicciones_personales:
            self.increment_counter("estadisticas", "usuarios_consultados")
        
        self.save_data()
        
        frase_mistica = self.get_random_choice("frases_mysticas")
        return f"🔮 {frase_mistica} {prediccion_personalizada['prediccion']} (Probabilidad: {prediccion_personalizada['probabilidad']})"
    
    def _personalizar_prediccion(self, username, prediccion_base):
        """Personalizar predicción usando ResponseHandler"""
        # Usar método heredado para personalización por nombre
        prediccion_personalizada = ResponseHandler.personalize_by_name(username, prediccion_base["prediccion"])
        
        # Crear nueva predicción con personalización
        return {
            "prediccion": prediccion_personalizada,
            "tipo": prediccion_base["tipo"],
            "probabilidad": prediccion_base["probabilidad"]
        }
    
    def get_prediccion_generica(self):
        """Obtener predicción genérica usando método heredado"""
        prediccion = self.get_random_choice("predicciones_genericas")
        if not prediccion:
            return "Mi don profético está bloqueado! Intenta más tarde."
        
        frase_mistica = self.get_random_choice("frases_mysticas")
        self.increment_counter("estadisticas", "predicciones_dadas")
        
        return f"🔮 {frase_mistica} {prediccion['prediccion']} (Probabilidad: {prediccion['probabilidad']})"
    
    def responder_a_comentario(self, username, comentario):
        """Responder a comentarios desde perspectiva clarividente"""
        comentario_clean = ResponseHandler.clean_text(comentario)
        comentario_lower = comentario_clean.lower()
        
        # Palabras que indican petición de predicción
        palabras_prediccion = [
            "futuro", "destino", "predice", "prediccion", "que pasara", 
            "que va a pasar", "mi futuro", "clarividente", "adivina",
            "horoscopo", "suerte", "amor", "dinero", "trabajo", "cuando"
        ]
        
        # Si el comentario pide predicción explícitamente
        if ResponseHandler.detect_keywords(comentario_lower, palabras_prediccion):
            return self.get_prediccion_for_user(username)
        
        # Respuestas místicas a comentarios normales
        respuestas_misticas = [
            f"🔮 {username}, las cartas dicen que ese comentario revela tu alma vacía...",
            f"🔮 Mi bola de cristal se empañó al leer tu mensaje, {username}...",
            f"🔮 Los espíritus me dicen que {username} necesita más sabiduría...",
            f"🔮 {username}, el cosmos predice que dirás algo inteligente... algún día...",
            f"🔮 Las fuerzas místicas confirman que {username} está confundido...",
            f"🔮 Mi tercer ojo ve que {username} debería pensarlo dos veces antes de escribir..."
        ]
        
        # Respuestas específicas según el contenido
        if ResponseHandler.detect_keywords(comentario_lower, ["hola", "hi", "saludos"]):
            return f"🔮 {username}, ya sabía que ibas a saludar... mi don es impresionante."
        
        if ResponseHandler.detect_keywords(comentario_lower, ["como estas", "que tal"]):
            return f"🔮 {username}, estoy como las cartas predicen: molesto y sarcástico."
        
        if ResponseHandler.detect_keywords(comentario_lower, ["gracioso", "funny"]):
            return f"🔮 {username}, preveo que tu sentido del humor mejorará... en otra vida."
        
        # Respuesta mística aleatoria personalizada
        respuesta = random.choice(respuestas_misticas)
        return ResponseHandler.personalize_by_name(username, respuesta)
    
    def get_lectura_completa(self, username):
        """Dar una lectura completa de tarot/clarividente"""
        tipos_lectura = ["amor", "dinero", "salud", "trabajo", "familia"]
        lectura_completa = f"🔮 LECTURA COMPLETA PARA {username}:\n\n"
        
        frase_inicio = random.choice([
            "Las cartas del tarot payaso revelan...",
            "Mi bola de cristal agrietada muestra...",
            "Los espíritus del circo susurran...",
            "El cosmos sarcástico indica..."
        ])
        
        lectura_completa += f"{frase_inicio}\n\n"
        
        predicciones_genericas = self.data.get("predicciones_genericas", [])
        for tipo in tipos_lectura:
            predicciones_tipo = [p for p in predicciones_genericas if p["tipo"] == tipo]
            if predicciones_tipo:
                pred = random.choice(predicciones_tipo)
                lectura_completa += f"💫 {tipo.upper()}: {pred['prediccion']} ({pred['probabilidad']})\n"
        
        lectura_completa += f"\n🎭 Consejo final: {username}, el universo dice que dejes de preguntarle a payasos sobre tu futuro."
        
        # Incrementar estadísticas
        self.increment_counter("estadisticas", "predicciones_dadas")
        
        return ResponseHandler.personalize_by_name(username, lectura_completa)
    
    def get_prediccion_por_tipo(self, tipo):
        """Obtener predicción de un tipo específico"""
        predicciones_genericas = self.data.get("predicciones_genericas", [])
        predicciones_tipo = [p for p in predicciones_genericas if p["tipo"].lower() == tipo.lower()]
        
        if not predicciones_tipo:
            tipos_disponibles = list(set(p["tipo"] for p in predicciones_genericas))
            return f"No tengo predicciones de '{tipo}'. Tipos disponibles: {', '.join(tipos_disponibles)}"
        
        prediccion = random.choice(predicciones_tipo)
        frase_mistica = self.get_random_choice("frases_mysticas")
        
        self.increment_counter("estadisticas", "predicciones_dadas")
        
        return f"🔮 PREDICCIÓN DE {tipo.upper()}\n{frase_mistica} {prediccion['prediccion']} (Probabilidad: {prediccion['probabilidad']})"
    
    def agregar_prediccion(self, tipo, prediccion, probabilidad="50%"):
        """Agregar nueva predicción"""
        nueva_prediccion = {
            "tipo": tipo.lower(),
            "prediccion": prediccion,
            "probabilidad": probabilidad
        }
        
        self.add_item_to_list("predicciones_genericas", nueva_prediccion)
        return f"✅ Predicción de {tipo} agregada al oráculo"
    
    def search_prediccion(self, keyword):
        """Buscar predicciones por palabra clave"""
        keyword_lower = keyword.lower()
        matching_predictions = []
        
        for pred in self.data.get("predicciones_genericas", []):
            if keyword_lower in pred["prediccion"].lower() or keyword_lower in pred["tipo"].lower():
                matching_predictions.append(pred)
        
        if not matching_predictions:
            return f"No encontré predicciones sobre '{keyword}'. Pero preveo que seguirás buscando."
        
        pred = random.choice(matching_predictions)
        frase_mistica = self.get_random_choice("frases_mysticas")
        
        return f"🔮 PREDICCIÓN encontrada:\n{frase_mistica} {pred['prediccion']} (Probabilidad: {pred['probabilidad']})"
    
    def get_mystic_stats(self):
        """Obtener estadísticas místicas usando método heredado"""
        base_stats = self.get_stats()
        
        predicciones_dadas = self.get_counter("estadisticas", "predicciones_dadas")
        usuarios_consultados = self.get_counter("estadisticas", "usuarios_consultados")
        predicciones_personales = self.data.get("predicciones_personales", {})
        
        # Análisis por tipos
        tipos = {}
        for pred in self.data.get("predicciones_genericas", []):
            tipo = pred.get("tipo", "unknown")
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        stats = f"{base_stats}\n"
        stats += f"Predicciones dadas: {predicciones_dadas}\n"
        stats += f"Usuarios consultados: {usuarios_consultados}\n"
        stats += f"Predicciones personalizadas: {len(predicciones_personales)}\n"
        
        if tipos:
            stats += "\nTipos de predicciones:\n"
            for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
                stats += f"  - {tipo}: {count}\n"
        
        return stats
    
    def limpiar_predicciones_antiguas(self):
        """Limpiar predicciones personalizadas"""
        predicciones_personales = self.data.get("predicciones_personales", {})
        count = len(predicciones_personales)
        
        self.data["predicciones_personales"] = {}
        self.save_data()
        
        return f"🧹 {count} predicciones limpiadas. Nuevas lecturas disponibles para todos."
    
    def get_available_types(self):
        """Obtener tipos de predicciones disponibles"""
        predicciones = self.data.get("predicciones_genericas", [])
        tipos = list(set(p["tipo"] for p in predicciones))
        return sorted(tipos)

# Ejemplo de uso
if __name__ == "__main__":
    manager = ClarividenteManager()
    
    print("🔮 PROBANDO MODO CLARIVIDENTE...")
    
    # Mostrar estadísticas
    print("\n📊 ESTADÍSTICAS:")
    print(manager.get_mystic_stats())
    
    # Probar predicción genérica
    print("\n🔮 PREDICCIÓN GENÉRICA:")
    print(manager.get_prediccion_generica())
    
    # Probar predicción personalizada
    print("\n🔮 PREDICCIÓN PERSONALIZADA:")
    print(manager.get_prediccion_for_user("TestUser"))
    
    # Probar lectura completa
    print("\n🔮 LECTURA COMPLETA:")
    print(manager.get_lectura_completa("TestUser"))
    
    print("\n✅ Pruebas de clarividente completadas")