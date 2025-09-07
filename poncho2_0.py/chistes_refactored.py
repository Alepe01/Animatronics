from base_manager import BaseManager
from response_handler import ResponseHandler
import random

class ChisteManager(BaseManager):
    """Manager de chistes refactorizado usando BaseManager"""
    
    def __init__(self, chistes_file="chistes.json"):
        super().__init__(chistes_file)
        print(f"😂 Chiste Manager inicializado con {len(self.data.get('chistes', []))} chistes")
    
    def _create_default_data(self):
        """Crear chistes por defecto"""
        self.data = {
            "chistes": [
                {
                    "setup": "¿Qué le regalas a un niño sin brazos por Navidad?",
                    "punchline": "Nada, no podría abrirlo de todos modos.",
                    "categoria": "humor_negro",
                    "rating": 5
                },
                {
                    "setup": "Mami, algo le pasa al conejito...",
                    "punchline": "Niña, calla y vuelve a cerrar la puerta del horno.",
                    "categoria": "humor_negro",
                    "rating": 5
                },
                {
                    "setup": "Papá, ¿por qué el abuelo va tan maquillado?",
                    "punchline": "¡Que no te acerques al ataúd!",
                    "categoria": "humor_negro",
                    "rating": 4
                },
                {
                    "setup": "¿Cómo llamas a un perro sin patas?",
                    "punchline": "En realidad no importa cómo lo llames, no va a venir de todos modos.",
                    "categoria": "humor_negro",
                    "rating": 4
                },
                {
                    "setup": "A mis parientes mayores les gustaba burlarse de mí en las bodas, diciendo: '¡Tú serás el siguiente!'",
                    "punchline": "Pero dejaron de hacerlo enseguida cuando empecé a hacer lo mismo yo en los funerales.",
                    "categoria": "humor_negro",
                    "rating": 5
                },
                {
                    "setup": "¿Qué es peor que seis niños colgados de un árbol?",
                    "punchline": "Un niño colgado de seis árboles.",
                    "categoria": "humor_negro",
                    "rating": 5
                },
                {
                    "setup": "Incluso la gente que no sirve para nada tiene la capacidad de sacarte una sonrisa.",
                    "punchline": "Por ejemplo, cuando los empujas por las escaleras.",
                    "categoria": "humor_negro",
                    "rating": 4
                },
                {
                    "setup": "Un hombre va a la biblioteca y pide un libro sobre cómo suicidarse.",
                    "punchline": "El bibliotecario le responde, 'no te lo presto, que no me lo devuelves'.",
                    "categoria": "humor_negro",
                    "rating": 5
                },
                {
                    "setup": "¿Dónde fue José Luis después de perderse en un campo minado?",
                    "punchline": "A todas partes.",
                    "categoria": "humor_negro",
                    "rating": 4
                },
                {
                    "setup": "Nunca olvidaré las últimas palabras de mi abuelo justo antes de morir.",
                    "punchline": "¿Sigues sosteniendo la escalera?",
                    "categoria": "humor_negro",
                    "rating": 5
                },
                {
                    "setup": "No necesitas un paracaídas para hacer paracaidismo.",
                    "punchline": "Necesitas un paracaídas para hacer paracaidismo dos veces.",
                    "categoria": "humor_negro",
                    "rating": 4
                },
                {
                    "setup": "El perro de mi novia se murió, así que le compré otro idéntico.",
                    "punchline": "Ella me gritó y me dijo: '¿Qué voy a hacer con dos perros muertos?'",
                    "categoria": "humor_negro",
                    "rating": 5
                },
                {
                    "setup": "¿Qué es rojo y malo para los dientes?",
                    "punchline": "Un ladrillo.",
                    "categoria": "humor_negro",
                    "rating": 3
                },
                {
                    "setup": "Mi abuelo decía que mi generación depende demasiado de la última tecnología.",
                    "punchline": "Así que le desconecté de la respiración asistida.",
                    "categoria": "humor_negro",
                    "rating": 5
                },
                {
                    "setup": "¡Tengo un pez que sabe bailar breakdance!",
                    "punchline": "Vale, solo durante 20 segundos, y solo una vez.",
                    "categoria": "humor_negro",
                    "rating": 4
                }
            ],
            "categorias": ["humor_negro", "sarcasmo", "dark"],
            "estadisticas": {
                "chistes_contados": 0,
                "favoritos": []
            },
            "version": "2.0"
        }
    
    def get_random_joke(self):
        """Obtener chiste aleatorio usando método heredado"""
        chiste = self.get_random_choice("chistes")
        if not chiste:
            return "¡No tengo chistes! ¡Mi humor está más seco que mi personalidad!"
        
        # Incrementar contador
        self.increment_counter("estadisticas", "chistes_contados")
        
        # Formatear chiste
        joke_text = f"{chiste['setup']}\n\n{chiste['punchline']}"
        return ResponseHandler.clean_text(joke_text)
    
    def get_joke_by_category(self, categoria):
        """Obtener chiste de una categoría específica"""
        chistes = self.data.get("chistes", [])
        chistes_categoria = [c for c in chistes if c.get("categoria") == categoria.lower()]
        
        if not chistes_categoria:
            return f"No tengo chistes de '{categoria}', pero puedo contarte uno de lo malo que eres!"
        
        chiste = random.choice(chistes_categoria)
        self.increment_counter("estadisticas", "chistes_contados")
        
        return f"{chiste['setup']}\n\n{chiste['punchline']}"
    
    def get_best_jokes(self, limit=5):
        """Obtener los mejores chistes por rating"""
        chistes = self.data.get("chistes", [])
        best_chistes = sorted(chistes, key=lambda x: x.get("rating", 0), reverse=True)
        
        result = "🏆 MIS MEJORES CHISTES:\n\n"
        for i, chiste in enumerate(best_chistes[:limit], 1):
            result += f"{i}. {chiste['setup']}\n   {chiste['punchline']}\n\n"
        
        return result
    
    def add_joke(self, setup, punchline, categoria="custom", rating=3):
        """Agregar nuevo chiste"""
        nuevo_chiste = {
            "setup": setup,
            "punchline": punchline,
            "categoria": categoria.lower(),
            "rating": rating
        }
        
        self.add_item_to_list("chistes", nuevo_chiste)
        return f"✅ Chiste agregado a la categoría '{categoria}'"
    
    def get_joke_stats(self):
        """Obtener estadísticas de chistes usando método heredado"""
        base_stats = self.get_stats()
        
        # Estadísticas específicas
        chistes_contados = self.get_counter("estadisticas", "chistes_contados")
        
        categorias = {}
        ratings = {}
        
        for chiste in self.data.get("chistes", []):
            cat = chiste.get("categoria", "sin_categoria")
            rat = chiste.get("rating", 0)
            
            categorias[cat] = categorias.get(cat, 0) + 1
            ratings[rat] = ratings.get(rat, 0) + 1
        
        stats = f"{base_stats}\n"
        stats += f"Chistes contados: {chistes_contados}\n\n"
        stats += "Categorías:\n"
        for cat, count in sorted(categorias.items()):
            stats += f"  - {cat}: {count}\n"
        
        stats += "\nRatings:\n"
        for rating, count in sorted(ratings.items(), reverse=True):
            stars = "⭐" * rating
            stats += f"  {stars} ({rating}): {count} chistes\n"
        
        return stats
    
    def search_joke(self, keyword):
        """Buscar chistes que contengan una palabra clave"""
        keyword_lower = keyword.lower()
        matching_jokes = []
        
        for chiste in self.data.get("chistes", []):
            setup_lower = chiste["setup"].lower()
            punchline_lower = chiste["punchline"].lower()
            
            if keyword_lower in setup_lower or keyword_lower in punchline_lower:
                matching_jokes.append(chiste)
        
        if not matching_jokes:
            return f"No encontré chistes sobre '{keyword}'. ¡Pero encontré uno sobre lo aburrido que eres!"
        
        chiste = random.choice(matching_jokes)
        return f"{chiste['setup']}\n\n{chiste['punchline']}"
    
    def get_random_sarcastic_response(self):
        """Generar respuesta sarcástica aleatoria"""
        respuestas = [
            "¿Eso era un chiste? Porque no me reí.",
            "Mi humor es más negro que mi alma de payaso.",
            "Si quieres algo gracioso, mírate al espejo.",
            "Mis chistes son como la vida: sin sentido y deprimentes.",
            "¿Te reíste? Perfecto, mi trabajo aquí está hecho.",
        ]
        
        return random.choice(respuestas)
    
    def respond_to_joke_request(self, username, comment):
        """Responder a peticiones de chistes"""
        clean_comment = ResponseHandler.clean_text(comment)
        
        # Detectar peticiones específicas
        if ResponseHandler.detect_keywords(clean_comment, ["chiste", "joke", "gracioso", "divertido"]):
            # Buscar categoría específica
            for categoria in self.data.get("categorias", []):
                if categoria in clean_comment.lower():
                    return self.get_joke_by_category(categoria)
            
            # Chiste aleatorio
            joke = self.get_random_joke()
            return ResponseHandler.personalize_by_name(username, joke)
        
        # Si no es petición de chiste, respuesta sarcástica
        return self.get_random_sarcastic_response()
    
    def rate_last_joke(self, rating):
        """Calificar el último chiste (funcionalidad extra)"""
        try:
            rating = int(rating)
            if 1 <= rating <= 5:
                # Aquí podrías implementar lógica para recordar el último chiste
                return f"✅ Gracias por calificar con {rating} estrellas mi chiste!"
            else:
                return "La calificación debe ser entre 1 y 5 estrellas."
        except:
            return "No entendí tu calificación. Usa números del 1 al 5."
    
    def get_categories(self):
        """Obtener categorías disponibles"""
        return self.data.get("categorias", [])
    
    def get_jokes_count(self):
        """Obtener número total de chistes"""
        return len(self.data.get("chistes", []))

# Ejemplo de uso
if __name__ == "__main__":
    manager = ChisteManager()
    
    print(f"📊 Total de chistes: {manager.get_jokes_count()}")
    print(f"📂 Categorías: {manager.get_categories()}")
    
    print("\n😂 CHISTE ALEATORIO:")
    print(manager.get_random_joke())
    
    print(f"\n📈 ESTADÍSTICAS:")
    print(manager.get_joke_stats())