import random
import json
import os
import re
from difflib import SequenceMatcher

class AcertijoManager:
    def __init__(self, acertijos_file="acertijos.json"):
        """
        Inicializar el manager del modo acertijos
        """
        self.acertijos_file = acertijos_file
        self.acertijos = []
        self.acertijo_actual = None
        self.intentos_fallidos = {}  # username: numero_intentos
        self.ganadores = {}  # username: numero_aciertos
        self.load_acertijos()
        print(f"🧩 Acertijo Manager inicializado con {len(self.acertijos)} acertijos")
    
    def load_acertijos(self):
        """Cargar acertijos desde archivo JSON o crear por defecto"""
        try:
            if os.path.exists(self.acertijos_file):
                with open(self.acertijos_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.acertijos = data.get('acertijos', [])
                    self.ganadores = data.get('ganadores', {})
                print(f"✅ Cargados {len(self.acertijos)} acertijos desde {self.acertijos_file}")
            else:
                self._create_default_acertijos()
                self.save_acertijos()
                print(f"🧩 Archivo de acertijos creado: {self.acertijos_file}")
        
        except Exception as e:
            print(f"❌ Error cargando acertijos: {e}")
            self._create_default_acertijos()
    
    def _create_default_acertijos(self):
        """Crear acertijos por defecto"""
        self.acertijos = [
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
                "pregunta": "Todos me pisan, todos me usan, pero nadie me ve. ¿Qué soy?",
                "respuestas": ["camino", "el camino", "sendero", "senda"],
                "pistas": ["Conecta lugares", "La gente camina sobre mí", "Puedo ser de tierra"],
                "dificultad": "medio",
                "categoria": "lugares"
            },
            {
                "pregunta": "Tengo dientes pero no como. ¿Qué soy?",
                "respuestas": ["peine", "el peine", "sierra", "engranaje", "cremallera"],
                "pistas": ["Ordeno el cabello", "Tengo muchas puntas", "Soy de plástico"],
                "dificultad": "fácil",
                "categoria": "objetos"
            },
            {
                "pregunta": "En el circo soy el rey, con mi cara pintada y mi nariz colorada. ¡Hago reír a la gente pero a veces doy miedo! ¿Quién soy?",
                "respuestas": ["payaso", "el payaso", "un payaso", "clown"],
                "pistas": ["Trabajo en el circo", "Hago bromas", "Mi nariz es roja"],
                "dificultad": "fácil",
                "categoria": "personajes"
            },
            {
                "pregunta": "Redondo como una pelota, dulce como la miel, me comes en el desayuno con café o con té. ¿Qué soy?",
                "respuestas": ["donut", "dona", "rosquilla", "rosquita"],
                "pistas": ["Tengo un agujero en el centro", "Soy dulce", "Me fríen en aceite"],
                "dificultad": "fácil",
                "categoria": "comida"
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
            },
            {
                "pregunta": "Tengo cola pero no soy animal, tengo cabeza pero no pienso. Me lanzan al aire y decido por ti. ¿Qué soy?",
                "respuestas": ["moneda", "la moneda", "una moneda"],
                "pistas": ["Sirvo para comprar", "Tengo dos caras", "Estoy hecha de metal"],
                "dificultad": "medio",
                "categoria": "objetos"
            },
            {
                "pregunta": "Soy amarillo por fuera, blanco por dentro. Los monos me aman y los niños también. ¿Qué soy?",
                "respuestas": ["plátano", "banana", "el plátano", "la banana"],
                "pistas": ["Crezco en racimos", "Soy tropical", "Tengo potasio"],
                "dificultad": "fácil",
                "categoria": "frutas"
            },
            {
                "pregunta": "Entro seco y salgo mojado, mientras más me secan más mojado quedo. ¿Qué soy?",
                "respuestas": ["té", "el té", "café", "el café", "chocolate"],
                "pistas": ["Soy una bebida", "Me preparan con agua caliente", "Tengo sabor"],
                "dificultad": "difícil",
                "categoria": "bebidas"
            },
            {
                "pregunta": "Tengo ojos pero no veo, tengo papas pero no como. ¿Qué soy?",
                "respuestas": ["papa", "patata", "la papa", "la patata"],
                "pistas": ["Crezco bajo tierra", "Me pueden freír", "Tengo almidón"],
                "dificultad": "medio",
                "categoria": "comida"
            }
        ]
        
        self.ganadores = {}
    
    def get_acertijo_aleatorio(self):
        """Obtener un acertijo aleatorio"""
        if not self.acertijos:
            return "¡No tengo acertijos! ¡Mi cerebro está más vacío que mi corazón!"
        
        self.acertijo_actual = random.choice(self.acertijos)
        self.intentos_fallidos = {}  # Reset intentos
        
        difficulty_emoji = {
            "fácil": "🟢",
            "medio": "🟡", 
            "difícil": "🔴"
        }
        
        emoji = difficulty_emoji.get(self.acertijo_actual["dificultad"], "❓")
        
        return f"🧩 ACERTIJO {emoji}:\n\n{self.acertijo_actual['pregunta']}\n\n¡A ver si no eres tan tonto como pareces!"
    
    def verificar_respuesta(self, username, respuesta):
        """Verificar si la respuesta es correcta"""
        if not self.acertijo_actual:
            return "¡No hay acertijo activo, genio!"
        
        respuesta_limpia = self._limpiar_respuesta(respuesta)
        respuestas_correctas = [self._limpiar_respuesta(r) for r in self.acertijo_actual["respuestas"]]
        
        # Verificar respuesta exacta
        if respuesta_limpia in respuestas_correctas:
            return self._respuesta_correcta(username)
        
        # Verificar respuesta similar (tolerancia para errores menores)
        for respuesta_correcta in respuestas_correctas:
            similarity = SequenceMatcher(None, respuesta_limpia, respuesta_correcta).ratio()
            if similarity > 0.8:  # 80% de similitud
                return self._respuesta_correcta(username)
        
        return self._respuesta_incorrecta(username)
    
    def _limpiar_respuesta(self, respuesta):
        """Limpiar respuesta para comparación"""
        # Convertir a minúsculas y quitar espacios extra
        respuesta_limpia = respuesta.lower().strip()
        
        # Remover artículos y palabras comunes
        palabras_ignorar = ["el", "la", "los", "las", "un", "una", "es", "soy"]
        palabras = respuesta_limpia.split()
        palabras_filtradas = [p for p in palabras if p not in palabras_ignorar]
        
        # Unir palabras o devolver original si queda vacío
        return " ".join(palabras_filtradas) if palabras_filtradas else respuesta_limpia
    
    def _respuesta_correcta(self, username):
        """Manejar respuesta correcta"""
        # Actualizar puntuación
        if username in self.ganadores:
            self.ganadores[username] += 1
        else:
            self.ganadores[username] = 1
        
        # Limpiar intentos fallidos
        if username in self.intentos_fallidos:
            del self.intentos_fallidos[username]
        
        # Guardar progreso
        self.save_acertijos()
        
        # Respuestas de felicitación sarcásticas
        felicitaciones = [
            f"¡Correcto, {username}! ¡Hasta un reloj descompuesto da la hora correcta dos veces al día!",
            f"¡Bien {username}! ¡Por fin usaste esa cosa que tienes entre las orejas!",
            f"¡Exacto, {username}! ¡Veo que no eres tan inútil como pensé!",
            f"¡Correcto, {username}! ¡Felicidades por tener más de dos neuronas funcionando!",
            f"¡Bien {username}! ¡Hasta los monos pueden aprender trucos!",
            f"¡Correcto, {username}! ¡Tu mamá estaría orgullosa... si supiera usar internet!",
            f"¡Exacto, {username}! ¡No todo está perdido contigo!"
        ]
        
        respuesta = random.choice(felicitaciones)
        respuesta += f"\n\n🏆 Llevas {self.ganadores[username]} acertijos correctos."
        
        # Limpiar acertijo actual
        self.acertijo_actual = None
        
        return respuesta
    
    def _respuesta_incorrecta(self, username):
        """Manejar respuesta incorrecta"""
        # Incrementar intentos fallidos
        if username in self.intentos_fallidos:
            self.intentos_fallidos[username] += 1
        else:
            self.intentos_fallidos[username] = 1
        
        intentos = self.intentos_fallidos[username]
        
        # Respuestas de burla escaladas
        if intentos == 1:
            burlas = [
                f"¡Incorrecto, {username}! ¡Pero no te preocupes, todos empezamos siendo tontos!",
                f"¡Fallaste, {username}! ¡Inténtalo de nuevo, a ver si la suerte te acompaña!",
                f"¡Nope, {username}! ¡Tu cerebro necesita más ejercicio!",
                f"¡Error, {username}! ¡Pero hey, al menos participas!",
                f"¡Incorrecto, {username}! ¡Sigue intentando, campeón!"
            ]
        elif intentos == 2:
            burlas = [
                f"¡Otra vez mal, {username}! ¡Tu récord de fracasos va creciendo!",
                f"¡Dos errores, {username}! ¡Impresionante consistencia en ser malo!",
                f"¡Fallaste de nuevo, {username}! ¡Al menos eres constante!",
                f"¡Segundo error, {username}! ¡Vas por buen camino... al fracaso!"
            ]
        elif intentos == 3:
            burlas = [
                f"¡Tres errores, {username}! ¡Eres todo un profesional... del fracaso!",
                f"¡Triple falla, {username}! ¡Tu talento para errar es impresionante!",
                f"¡Tercera vez mal, {username}! ¡Deberías dedicarte a otra cosa!"
            ]
        else:
            burlas = [
                f"¡{intentos} errores, {username}! ¡Ya perdí la cuenta de tus fracasos!",
                f"¡Sigues fallando, {username}! ¡Al menos eres entretenido!",
                f"¡{intentos} intentos y nada, {username}! ¡Eres una obra de arte... del desastre!"
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
        
        return respuesta
    
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
        acertijos_categoria = [a for a in self.acertijos if a.get("categoria", "").lower() == categoria.lower()]
        
        if not acertijos_categoria:
            return f"No tengo acertijos de '{categoria}', ¡pero tengo muchos de lo inútil que eres!"
        
        self.acertijo_actual = random.choice(acertijos_categoria)
        self.intentos_fallidos = {}
        
        difficulty_emoji = {
            "fácil": "🟢",
            "medio": "🟡", 
            "difícil": "🔴"
        }
        
        emoji = difficulty_emoji.get(self.acertijo_actual["dificultad"], "❓")
        
        return f"🧩 ACERTIJO DE {categoria.upper()} {emoji}:\n\n{self.acertijo_actual['pregunta']}\n\n¡A ver si sabes algo de {categoria}!"
    
    def get_ranking(self):
        """Obtener ranking de ganadores"""
        if not self.ganadores:
            return "¡No hay ganadores aún! ¡Todos son igual de inútiles!"
        
        ranking = sorted(self.ganadores.items(), key=lambda x: x[1], reverse=True)
        
        resultado = "🏆 RANKING DE ACERTIJOS:\n\n"
        for i, (username, aciertos) in enumerate(ranking[:10], 1):
            medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
            resultado += f"{medal} {username}: {aciertos} acertijos\n"
        
        return resultado
    
    def get_estadisticas(self):
        """Obtener estadísticas generales"""
        if not self.acertijos:
            return "No hay acertijos disponibles"
        
        categorias = {}
        dificultades = {}
        
        for acertijo in self.acertijos:
            cat = acertijo.get("categoria", "sin categoría")
            dif = acertijo.get("dificultad", "sin dificultad")
            
            categorias[cat] = categorias.get(cat, 0) + 1
            dificultades[dif] = dificultades.get(dif, 0) + 1
        
        stats = f"📊 Estadísticas de Acertijos:\n"
        stats += f"Total: {len(self.acertijos)} acertijos\n"
        stats += f"Jugadores: {len(self.ganadores)}\n"
        
        if self.ganadores:
            total_aciertos = sum(self.ganadores.values())
            stats += f"Acertijos resueltos: {total_aciertos}\n"
        
        stats += f"\nCategorías:\n"
        for cat, count in sorted(categorias.items()):
            stats += f"  - {cat}: {count}\n"
        
        stats += f"\nDificultades:\n"
        for dif, count in sorted(dificultades.items()):
            stats += f"  - {dif}: {count}\n"
        
        return stats
    
    def get_categorias(self):
        """Obtener lista de categorías disponibles"""
        categorias = set(a.get("categoria", "sin categoría") for a in self.acertijos)
        return sorted(categorias)
    
    def agregar_acertijo(self, pregunta, respuestas, pistas=None, dificultad="medio", categoria="personalizado"):
        """Agregar nuevo acertijo"""
        nuevo_acertijo = {
            "pregunta": pregunta,
            "respuestas": respuestas if isinstance(respuestas, list) else [respuestas],
            "pistas": pistas or [],
            "dificultad": dificultad,
            "categoria": categoria
        }
        
        self.acertijos.append(nuevo_acertijo)
        self.save_acertijos()
        print(f"✅ Acertijo agregado: {categoria}")
    
    def responder_comentario_modo_acertijo(self, username, comentario):
        """Responder comentarios en modo acertijo"""
        comentario_lower = comentario.lower()
        
        # Comandos especiales
        if any(cmd in comentario_lower for cmd in ["pista", "ayuda", "hint"]):
            return self.dar_pista()
        
        if any(cmd in comentario_lower for cmd in ["ranking", "puntuacion", "puntaje"]):
            return self.get_ranking()
        
        if any(cmd in comentario_lower for cmd in ["nuevo", "otro", "siguiente"]):
            return self.get_acertijo_aleatorio()
        
        # Si hay acertijo activo, verificar respuesta
        if self.acertijo_actual:
            return self.verificar_respuesta(username, comentario)
        
        # Si no hay acertijo activo, dar uno nuevo
        return self.get_acertijo_aleatorio()
    
    def save_acertijos(self):
        """Guardar acertijos y puntuaciones en archivo JSON"""
        try:
            data = {
                "acertijos": self.acertijos,
                "ganadores": self.ganadores,
                "version": "1.0",
                "description": "Acertijos de Poncho el Payaso"
            }
            
            with open(self.acertijos_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Acertijos guardados en {self.acertijos_file}")
        
        except Exception as e:
            print(f"❌ Error guardando acertijos: {e}")
    
    def reload_acertijos(self):
        """Recargar acertijos desde archivo"""
        self.load_acertijos()

# --- FUNCIONES DE UTILIDAD ---
def crear_acertijos_personalizados():
    """Crear acertijos adicionales"""
    acertijos_extra = [
        {
            "pregunta": "Soy rojo cuando estoy enojado, verde cuando estoy celoso, azul cuando estoy triste. ¿Qué soy?",
            "respuestas": ["semáforo", "el semáforo"],
            "pistas": ["Controlo el tráfico", "Tengo tres colores", "Los autos me obedecen"],
            "dificultad": "medio",
            "categoria": "objetos"
        },
        {
            "pregunta": "Cuanto más tiras de mí, más corto me vuelvo. ¿Qué soy?",
            "respuestas": ["cigarrillo", "cigarro", "puro"],
            "pistas": ["Hago humo", "Soy malo para la salud", "Me encienden"],
            "dificultad": "difícil",
            "categoria": "objetos"
        }
    ]
    
    return acertijos_extra

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    print("🧩 Probando modo acertijos...")
    
    # Crear manager
    acertijos = AcertijoManager()
    
    # Mostrar estadísticas
    print("\n📊 ESTADÍSTICAS:")
    print(acertijos.get_estadisticas())
    
    print(f"\n📂 CATEGORÍAS: {', '.join(acertijos.get_categorias())}")
    
    # Probar acertijo aleatorio
    print("\n🧩 ACERTIJO ALEATORIO:")
    acertijo = acertijos.get_acertijo_aleatorio()
    print(acertijo)
    
    # Simular respuestas
    print("\n💬 SIMULANDO RESPUESTAS:")
    usuarios_respuestas = [
        ("Juan", "reloj"),
        ("Ana", "no sé"),
        ("Pedro", "cronometro"),
        ("Luis", "tiempo"),
        ("Maria", "reloj de pared")
    ]
    
    for usuario, respuesta in usuarios_respuestas:
        resultado = acertijos.verificar_respuesta(usuario, respuesta)
        print(f"\n{usuario}: '{respuesta}'")
        print(f"Poncho: {resultado}")
        
        if "¡Correcto" in resultado:
            break
    
    # Mostrar ranking
    print("\n" + acertijos.get_ranking())
    
    # Probar acertijo por categoría
    print(f"\n🧩 ACERTIJO DE FRUTAS:")
    acertijo_fruta = acertijos.get_acertijo_by_categoria("frutas")
    print(acertijo_fruta)
    
    print("\n✅ Pruebas de acertijos completadas")