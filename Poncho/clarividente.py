import random
import json
import os

class ClarividenteManager:
    def __init__(self, predicciones_file="predicciones.json"):
        """
        Inicializar el manager del modo clarividente
        """
        self.predicciones_file = predicciones_file
        self.predicciones = {}
        self.frases_mysticas = []
        self.predicciones_genericas = []
        self.load_predicciones()
        print(f"🔮 Clarividente Manager inicializado")
    
    def load_predicciones(self):
        """Cargar predicciones desde archivo JSON o crear por defecto"""
        try:
            if os.path.exists(self.predicciones_file):
                with open(self.predicciones_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.predicciones = data.get('predicciones_personales', {})
                    self.frases_mysticas = data.get('frases_mysticas', [])
                    self.predicciones_genericas = data.get('predicciones_genericas', [])
                print(f"✅ Cargadas predicciones desde {self.predicciones_file}")
            else:
                self._create_default_predicciones()
                self.save_predicciones()
                print(f"🔮 Archivo de predicciones creado: {self.predicciones_file}")
        
        except Exception as e:
            print(f"❌ Error cargando predicciones: {e}")
            self._create_default_predicciones()
    
    def _create_default_predicciones(self):
        """Crear predicciones por defecto"""
        self.frases_mysticas = [
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
        ]
        
        self.predicciones_genericas = [
            {
                "tipo": "amor",
                "prediccion": "Veo romance en tu futuro... ¡pero también veo que hueles raro!",
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
                "tipo": "amistad",
                "prediccion": "Un amigo te decepcionará... o tal vez ya lo hizo y no te diste cuenta",
                "probabilidad": "78%"
            },
            {
                "tipo": "estudios",
                "prediccion": "Aprenderás algo nuevo... como que hablarle a un payaso no es normal",
                "probabilidad": "99%"
            },
            {
                "tipo": "peligro",
                "prediccion": "Evita los lugares oscuros... especialmente los circos abandonados",
                "probabilidad": "66%"
            },
            {
                "tipo": "suerte",
                "prediccion": "La suerte estará de tu lado... pero yo no, porque soy grosero",
                "probabilidad": "33%"
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
        ]
        
        # Predicciones específicas para nombres comunes
        self.predicciones = {}
    
    def get_prediccion_for_user(self, username):
        """Obtener predicción específica para un usuario"""
        username_lower = username.lower()
        
        # Si ya tiene predicción guardada, devolverla
        if username_lower in self.predicciones:
            stored = self.predicciones[username_lower]
            frase_mistica = random.choice(self.frases_mysticas)
            return f"🔮 {frase_mistica} {stored['prediccion']} (Probabilidad: {stored['probabilidad']})"
        
        # Crear nueva predicción
        prediccion_base = random.choice(self.predicciones_genericas)
        
        # Personalizar según el nombre
        prediccion_personalizada = self._personalizar_prediccion(username, prediccion_base)
        
        # Guardar para futuras consultas
        self.predicciones[username_lower] = {
            "prediccion": prediccion_personalizada["prediccion"],
            "tipo": prediccion_personalizada["tipo"],
            "probabilidad": prediccion_personalizada["probabilidad"]
        }
        
        frase_mistica = random.choice(self.frases_mysticas)
        self.save_predicciones()
        
        return f"🔮 {frase_mistica} {prediccion_personalizada['prediccion']} (Probabilidad: {prediccion_personalizada['probabilidad']})"
    
    def _personalizar_prediccion(self, username, prediccion_base):
        """Personalizar predicción según el nombre del usuario"""
        prediccion = dict(prediccion_base)
        
        # Modificaciones según características del nombre
        name_lower = username.lower()
        
        # Nombres largos
        if len(username) > 12:
            prediccion["prediccion"] += " Tu nombre es tan largo que el destino se cansó de escribirlo."
        
        # Nombres cortos
        elif len(username) < 4:
            prediccion["prediccion"] += " Tu nombre es tan corto como tu paciencia conmigo."
        
        # Números en el nombre
        if any(char.isdigit() for char in username):
            prediccion["prediccion"] += " Los números en tu nombre revelan falta de creatividad."
        
        # Nombres específicos con burlas
        nombre_burlas = {
            "admin": " Ser admin no te salva de mi sarcasmo.",
            "user": " ¡Qué original! ¿También tu contraseña es 'password'?",
            "guest": " Invitado... como el que no invitan a las fiestas.",
            "test": " ¿Eres un test? Porque has fallado en mi corazón.",
            "null": " Tu nombre es 'null' como tu personalidad.",
            "bot": " ¿Bot? Al menos yo admito que soy artificial.",
            "anonymous": " Anónimo... como el que dejó esa mancha en mi cara."
        }
        
        for nombre, burla in nombre_burlas.items():
            if nombre in name_lower:
                prediccion["prediccion"] += burla
                break
        
        return prediccion
    
    def get_prediccion_generica(self):
        """Obtener predicción genérica sin nombre específico"""
        prediccion = random.choice(self.predicciones_genericas)
        frase_mistica = random.choice(self.frases_mysticas)
        
        return f"🔮 {frase_mistica} {prediccion['prediccion']} (Probabilidad: {prediccion['probabilidad']})"
    
    def responder_a_comentario(self, username, comentario):
        """Responder a comentarios desde perspectiva clarividente"""
        comentario_lower = comentario.lower()
        
        # Palabras que indican petición de predicción
        palabras_prediccion = [
            "futuro", "destino", "predice", "prediccion", "que pasara", 
            "que va a pasar", "mi futuro", "clarividente", "adivina",
            "horoscopo", "suerte", "amor", "dinero", "trabajo", "cuando"
        ]
        
        # Si el comentario pide predicción explícitamente
        if any(palabra in comentario_lower for palabra in palabras_prediccion):
            return self.get_prediccion_for_user(username)
        
        # Respuestas místicas a comentarios normales
        respuestas_misticas = [
            f"🔮 {username}, las cartas dicen que ese comentario revela tu alma vacía...",
            f"🔮 Mi bola de cristal se empañó al leer tu mensaje, {username}...",
            f"🔮 Los espíritus me dicen que {username} necesita más sabiduría...",
            f"🔮 {username}, el cosmos predice que dirás algo inteligente... algún día...",
            f"🔮 Las fuerzas místicas confirman que {username} está confundido...",
            f"🔮 Mi tercer ojo ve que {username} debería pensarlo dos veces antes de escribir...",
            f"🔮 {username}, los antepasados del circo se ríen de tu comentario...",
            f"🔮 La energía universal indica que {username} tiene mal gusto...",
            f"🔮 {username}, mi sabiduría ancestral dice que estás perdido...",
            f"🔮 Los vientos del destino susurran que {username} es peculiar..."
        ]
        
        # Respuestas específicas según el contenido
        if "hola" in comentario_lower or "hi" in comentario_lower:
            return f"🔮 {username}, ya sabía que ibas a saludar... mi don es impresionante."
        
        if "como estas" in comentario_lower or "que tal" in comentario_lower:
            return f"🔮 {username}, estoy como las cartas predicen: molesto y sarcástico."
        
        if "gracioso" in comentario_lower or "funny" in comentario_lower:
            return f"🔮 {username}, preveo que tu sentido del humor mejorará... en otra vida."
        
        # Respuesta mística aleatoria
        return random.choice(respuestas_misticas)
    
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
        
        for tipo in tipos_lectura:
            predicciones_tipo = [p for p in self.predicciones_genericas if p["tipo"] == tipo]
            if predicciones_tipo:
                pred = random.choice(predicciones_tipo)
                lectura_completa += f"💫 {tipo.upper()}: {pred['prediccion']} ({pred['probabilidad']})\n"
        
        lectura_completa += f"\n🎭 Consejo final: {username}, el universo dice que dejes de preguntarle a payasos sobre tu futuro."
        
        return lectura_completa
    
    def get_estadisticas(self):
        """Obtener estadísticas de predicciones"""
        stats = f"📊 Estadísticas del Oráculo Payaso:\n"
        stats += f"Predicciones personalizadas: {len(self.predicciones)}\n"
        stats += f"Frases místicas: {len(self.frases_mysticas)}\n"
        stats += f"Predicciones genéricas: {len(self.predicciones_genericas)}\n"
        
        if self.predicciones:
            tipos = {}
            for pred in self.predicciones.values():
                tipo = pred.get("tipo", "unknown")
                tipos[tipo] = tipos.get(tipo, 0) + 1
            
            stats += "\nTipos más consultados:\n"
            for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
                stats += f"  - {tipo}: {count}\n"
        
        return stats
    
    def save_predicciones(self):
        """Guardar predicciones en archivo JSON"""
        try:
            data = {
                "predicciones_personales": self.predicciones,
                "frases_mysticas": self.frases_mysticas,
                "predicciones_genericas": self.predicciones_genericas,
                "version": "1.0",
                "description": "Predicciones de Poncho el Clarividente"
            }
            
            with open(self.predicciones_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Predicciones guardadas en {self.predicciones_file}")
        
        except Exception as e:
            print(f"❌ Error guardando predicciones: {e}")
    
    def reload_predicciones(self):
        """Recargar predicciones desde archivo"""
        self.load_predicciones()
    
    def limpiar_predicciones_antiguas(self):
        """Limpiar predicciones para permitir nuevas lecturas"""
        count = len(self.predicciones)
        self.predicciones.clear()
        self.save_predicciones()
        return f"🧹 {count} predicciones limpiadas. Nuevas lecturas disponibles."

# --- FUNCIONES DE UTILIDAD ---
def crear_predicciones_personalizadas():
    """Crear archivo con predicciones personalizadas adicionales"""
    predicciones_extra = {
        "frases_mysticas_extra": [
            "Mi nariz roja vibra con energía cósmica...",
            "Los globos del circo susurran secretos...",
            "Mi peluca colorida capta ondas místicas...",
            "Los zapatos gigantes pisan el sendero del destino..."
        ],
        "predicciones_especiales": [
            {
                "tipo": "payaso",
                "prediccion": "Otro payaso entrará en tu vida... ¡espero que sea menos molesto que yo!",
                "probabilidad": "13%"
            },
            {
                "tipo": "circo",
                "prediccion": "El circo te llamará... pero probablemente sea spam telefónico",
                "probabilidad": "87%"
            }
        ]
    }
    
    with open("predicciones_extra.json", 'w', encoding='utf-8') as f:
        json.dump(predicciones_extra, f, ensure_ascii=False, indent=2)
    
    print("📚 Archivo de predicciones extra creado")

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    print("🔮 Probando modo clarividente...")
    
    # Crear manager
    clarividente = ClarividenteManager()
    
    # Mostrar estadísticas
    print("\n📊 ESTADÍSTICAS:")
    print(clarividente.get_estadisticas())
    
    # Probar predicciones para diferentes usuarios
    print("\n🔮 PREDICCIONES PERSONALIZADAS:")
    usuarios_test = ["JuanPerez123", "Ana", "TestUser", "admin", "x", "SuperLargoNombreUsuario"]
    
    for usuario in usuarios_test:
        prediccion = clarividente.get_prediccion_for_user(usuario)
        print(f"\n{usuario}: {prediccion}")
    
    # Probar respuestas a comentarios
    print("\n💬 RESPUESTAS A COMENTARIOS:")
    comentarios_test = [
        ("Maria", "Hola Poncho"),
        ("Pedro", "¿Cuál será mi futuro?"),
        ("Ana", "Eres muy gracioso"),
        ("Luis", "¿Cuándo encontraré el amor?"),
        ("Sofia", "No me gustas")
    ]
    
    for usuario, comentario in comentarios_test:
        respuesta = clarividente.responder_a_comentario(usuario, comentario)
        print(f"\n{usuario}: '{comentario}'")
        print(f"Poncho: {respuesta}")
    
    # Lectura completa
    print("\n🎴 LECTURA COMPLETA:")
    lectura = clarividente.get_lectura_completa("TestUser")
    print(lectura)
    
    print("\n✅ Pruebas de clarividente completadas")