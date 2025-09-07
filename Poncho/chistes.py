import random

class ChisteManager:
    def __init__(self):
        """Inicializar con los chistes dados directamente"""
        self.chistes = []
        self._load_fixed_chistes()
    
    def _load_fixed_chistes(self):
        """Cargar chistes fijos (los que me diste)"""
        chistes_texto = [
            ("¿Qué le regalas a un niño sin brazos por Navidad?", "Nada, no podría abrirlo de todos modos."),
            ("Mami, algo le pasa al conejito...", "Niña, calla y vuelve a cerrar la puerta del horno."),
            ("Papá, ¿por qué el abuelo va tan maquillado?", "¡Que no te acerques al ataúd!"),
            ("¿Cómo llamas a un perro sin patas?", "En realidad no importa cómo lo llames, no va a venir de todos modos."),
            ("A mis parientes mayores les gustaba burlarse de mí en las bodas, diciendo: '¡Tú serás el siguiente!'", 
             "Pero dejaron de hacerlo enseguida cuando empecé a hacer lo mismo yo en los funerales."),
            ("¿Qué es peor que seis niños colgados de un árbol?", "Un niño colgado de seis árboles."),
            ("Incluso la gente que no sirve para nada tiene la capacidad de sacarte una sonrisa.", "Por ejemplo, cuando los empujas por las escaleras."),
            ("Un hombre va a la biblioteca y pide un libro sobre cómo suicidarse.", "El bibliotecario le responde, 'no te lo presto, que no me lo devuelves'."),
            ("¿Dónde fue José Luis después de perderse en un campo minado?", "A todas partes."),
            ("Nunca olvidaré las últimas palabras de mi abuelo justo antes de morir.", "¿Sigues sosteniendo la escalera?."),
            ("No necesitas un paracaídas para hacer paracaidismo.", "Necesitas un paracaídas para hacer paracaidismo dos veces."),
            ("El perro de mi novia se murió, así que le compré otro idéntico.", "Ella me gritó y me dijo: '¿Qué voy a hacer con dos perros muertos?'"),
            ("¿Qué es rojo y malo para los dientes?", "Un ladrillo."),
            ("Mi abuelo decía que mi generación depende demasiado de la última tecnología.", "Así que le desconecté de la respiración asistida."),
            ("¡Tengo un pez que sabe bailar breakdance!", "Vale, solo durante 20 segundos, y solo una vez."),
            ("No eres un completo inútil.", "Siempre puedes ser utilizado como un mal ejemplo."),
            ("Pensé que abrir una puerta para una dama era de buenos modales...", "pero ella simplemente me gritó y salió volando del avión."),
            ("¿Por qué los amigos se parecen mucho a la nieve?", "Si haces pis sobre ellos, desaparecen."),
            ("Dale a un hombre un billete de avión y volará durante un día.", "Empújale desde un avión a 10.000 metros y volará durante el resto de su vida."),
            ("¿Cuál es la diferencia entre un Lamborghini y un cadáver?", "No tengo un Lamborghini en el garaje."),
            ("¿Por qué Michael Jackson no puede acercarse a menos de 500 metros de una escuela?", "Porque está muerto."),
            ("¿Qué es peor que morder una manzana y encontrar un gusano?", "Morder una manzana y encontrar medio gusano."),
            ("¿Qué es mejor que ganar la medalla de oro en los Juegos Paralímpicos?", "Tener brazos y piernas."),
            ("Traté de advertir a mi hijo sobre jugar a la ruleta rusa.", "Le entró por un oído y le salió por el otro."),
            ("Mi terapeuta acaba de morir.", "Era tan bueno que ni siquiera me importa."),
            ("¿Te cuento un chiste verde rápido?", "Una lechuga en una moto."),
            ("¿Por qué los robots no tienen amigos?", "Porque son todos circuitos cerrados."),
        ]
        
        # Convertir a objetos con categoría y rating fijo
        self.chistes = [
            {"categoria": "humor_negro", "setup": setup, "punchline": punchline, "rating": 5}
            for setup, punchline in chistes_texto
        ]
    
    def get_random_joke(self):
        """Obtener un chiste aleatorio"""
        chiste = random.choice(self.chistes)
        return f"{chiste['setup']}\n\n{chiste['punchline']}"
    
    def get_best_jokes(self, limit=5):
        """Obtener los mejores chistes"""
        return [f"{c['setup']}\n{c['punchline']}" for c in self.chistes[:limit]]
    
    def get_chistes_count(self):
        """Obtener número total de chistes"""
        return len(self.chistes)


# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    manager = ChisteManager()
    
    print(f"📊 Total de chistes cargados: {manager.get_chistes_count()}")
    
    print("\n🎭 CHISTES ALEATORIOS:")
    for i in range(3):
        print(f"\n--- Chiste {i+1} ---")
        print(manager.get_random_joke())
