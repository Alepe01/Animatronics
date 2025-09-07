import re
import random

class ResponseHandler:
    """Manejador común para procesar respuestas y comentarios"""
    
    @staticmethod
    def clean_text(text):
        """Limpiar texto de emojis y caracteres especiales"""
        if not text:
            return ""
        
        # Patrón para eliminar emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u'\U00010000-\U0010ffff'
            u"\u200d"
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
            "]+", flags=re.UNICODE)
        
        return emoji_pattern.sub(r'', text).strip()
    
    @staticmethod
    def detect_keywords(text, keywords):
        """Detectar si el texto contiene alguna palabra clave"""
        if not text or not keywords:
            return False
        
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    @staticmethod
    def personalize_by_name(username, base_text):
        """Personalizar texto según características del nombre"""
        if not username:
            return base_text
        
        name_lower = username.lower()
        additions = []
        
        # Longitud del nombre
        if len(username) > 15:
            additions.append("Tu nombre es tan largo que me da pereza escribirlo completo.")
        elif len(username) < 4:
            additions.append("Tu nombre es tan corto como tu paciencia.")
        
        # Números en el nombre
        if any(char.isdigit() for char in username):
            additions.append("Los números en tu nombre revelan falta de creatividad.")
        
        # Nombres especiales
        special_names = {
            "admin": "Ser admin no te salva de mi sarcasmo.",
            "user": "¡Qué original! ¿También tu contraseña es 'password'?",
            "guest": "Invitado... como el que no invitan a las fiestas.",
            "test": "¿Eres un test? Porque has fallado en mi corazón.",
            "null": "Tu nombre es 'null' como tu personalidad.",
            "bot": "¿Bot? Al menos yo admito que soy artificial.",
            "anonymous": "Anónimo... como el que dejó esa mancha en mi cara.",
            "troll": "¿Troll? ¡Yo soy el monstruo bajo tu puente!",
            "gamer": "Los gamers no pueden pausar la vida real.",
            "streamer": "Tu stream será mi escenario de terror."
        }
        
        for name, addition in special_names.items():
            if name in name_lower:
                additions.append(addition)
                break
        
        # Agregar personalización aleatoria
        if additions:
            return f"{base_text} {random.choice(additions)}"
        return base_text
    
    @staticmethod
    def detect_fake_donation(comment_text):
        """Detectar donaciones falsas mencionadas en comentarios"""
        if not comment_text:
            return False
        
        fake_keywords = [
            "dono", "doné", "donate", "regalo", "te mando", "envío", "envio",
            "dinero", "pesos", "dolares", "dólares", "coins", "monedas",
            "tip", "propina", "gift", "present", "te doy", "aquí tienes"
        ]
        
        return ResponseHandler.detect_keywords(comment_text, fake_keywords)
    
    @staticmethod
    def format_with_timestamp(text):
        """Agregar timestamp a un texto"""
        import time
        timestamp = time.strftime("%H:%M:%S")
        return f"[{timestamp}] {text}"
    
    @staticmethod
    def truncate_text(text, max_length=200):
        """Truncar texto si es muy largo"""
        if not text or len(text) <= max_length:
            return text
        
        return text[:max_length-3] + "..."
    
    @staticmethod
    def extract_username_mentions(text):
        """Extraer menciones de usuarios (@usuario)"""
        if not text:
            return []
        
        pattern = r'@(\w+)'
        mentions = re.findall(pattern, text)
        return mentions
    
    @staticmethod
    def sanitize_input(text):
        """Sanitizar entrada de usuario"""
        if not text:
            return ""
        
        # Limpiar y truncar
        cleaned = ResponseHandler.clean_text(text)
        sanitized = ResponseHandler.truncate_text(cleaned, 500)
        
        # Remover caracteres peligrosos
        sanitized = re.sub(r'[<>"\']', '', sanitized)
        
        return sanitized.strip()
    
    @staticmethod
    def get_similarity(text1, text2):
        """Calcular similitud entre dos textos"""
        if not text1 or not text2:
            return 0.0
        
        from difflib import SequenceMatcher
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

class SarcasticResponder:
    """Generador de respuestas sarcásticas reutilizable"""
    
    SARCASTIC_INTROS = [
        "¡Oh, qué sorpresa!",
        "¡Vaya, vaya!",
        "¡Increíble!",
        "¡Qué genio!",
        "¡Wow!",
        "¡No me digas!",
        "¡Fantástico!",
        "¡Brillante!"
    ]
    
    DISMISSIVE_ENDINGS = [
        "...como si me importara.",
        "...pero no me importa.",
        "...aunque no me sorprende.",
        "...típico de ti.",
        "...qué predecible.",
        "...como era de esperarse.",
        "...obviamente.",
        "...¡qué original!"
    ]
    
    @staticmethod
    def add_sarcasm(text):
        """Agregar sarcasmo a un texto"""
        intro = random.choice(SarcasticResponder.SARCASTIC_INTROS)
        ending = random.choice(SarcasticResponder.DISMISSIVE_ENDINGS)
        
        return f"{intro} {text}{ending}"
    
    @staticmethod
    def mock_comment(comment):
        """Generar burla de un comentario"""
        mock_responses = [
            f"'{comment}'... ¡qué profundo!",
            f"¿En serio dijiste '{comment}'? ¡Qué ingenioso!",
            f"'{comment}' - palabras de un verdadero filósofo.",
            f"¡Wow! '{comment}' - nunca había oído algo tan original.",
            f"'{comment}'... y yo que pensaba que era imposible decir algo más tonto."
        ]
        
        return random.choice(mock_responses)
    
    @staticmethod
    def generate_insult(username):
        """Generar insulto creativo personalizado"""
        insults = [
            f"{username}, tienes la personalidad de una tostada sin mantequilla.",
            f"{username}, eres como un nubarrón en un día soleado.",
            f"{username}, si fueras más aburrido serías una clase de matemáticas.",
            f"{username}, tienes tanto carisma como un calcetín mojado.",
            f"{username}, eres la razón por la que los aliens no nos visitan."
        ]
        
        return random.choice(insults)