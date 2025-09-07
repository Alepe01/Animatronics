from base_manager import BaseManager
from response_handler import ResponseHandler, SarcasticResponder
import random

class AmenazasManager(BaseManager):
    """Manager de amenazas refactorizado usando BaseManager"""
    
    def __init__(self, amenazas_file="amenazas.json"):
        super().__init__(amenazas_file)
        print(f"👻 Amenazas Manager inicializado - Modo Terrorífico Activado")
    
    def _create_default_data(self):
        """Crear amenazas por defecto"""
        self.data = {
            "amenazas_sutiles": [
                "Ya sé dónde vives... en tu casa, obviamente. ¿Dónde más vivirías?",
                "Conozco todos tus secretos... como que comes pizza fría del desayuno.",
                "Te estoy observando... a través de esta pantalla como todos los demás.",
                "Pronto vendré por ti... cuando termine este livestream.",
                "Tus pesadillas serán mi diversión... espero que sueñes conmigo.",
                "Nunca estarás a salvo... de mis chistes malos.",
                "Cada sombra que veas soy yo... o tal vez solo paranoia.",
                "Tu tiempo se acaba... como la batería de tu teléfono.",
                "Sé lo que hiciste el verano pasado... viste mis videos anteriores.",
                "Los payasos nunca olvidan... especialmente las caras de los que no donan."
            ],
            "amenazas_directas": [
                "¡Te encontraré y te haré ver todos mis videos!",
                "¡Mi venganza será terrible... como mis chistes!",
                "¡Vendré en la madrugada... a tocar tu timbre hasta que despiertes!",
                "¡Te perseguiré hasta el fin del mundo... o hasta que se me acabe la batería!",
                "¡Mis globos de payaso flotarán hacia tu ventana!",
                "¡Te haré cosquillas hasta que rías... de mis bromas malas!",
                "¡Mi risa siniestra resonará en tu cabeza toda la noche!",
                "¡Mis zapatos gigantes harán ruido bajo tu cama!",
                "¡Te despertarás con mi cara pintada en tu espejo!",
                "¡Todos tus globos se convertirán en mi cara!"
            ],
            "frases_terrorificas": [
                "Desde las profundidades del circo abandonado...",
                "Con mi sonrisa congelada en la eternidad...",
                "Mientras mis lágrimas de maquillaje se secan...",
                "En la oscuridad de mi alma payasa...",
                "Con la maldad de mil globos pinchados...",
                "Desde mi trono de pesadillas...",
                "Con el eco de risas macabras...",
                "En el silencio de la carpa vacía...",
                "Mientras afile mis bromas terroríficas...",
                "Con la furia de un payaso despreciado..."
            ],
            "usuarios_asustados": {},
            "estadisticas": {
                "amenazas_enviadas": 0,
                "usuarios_aterrorizados": 0
            },
            "version": "2.0"
        }
    
    def get_amenaza_personalizada(self, username):
        """Obtener amenaza personalizada usando métodos heredados"""
        # Incrementar nivel de miedo del usuario
        nivel_miedo = self.increment_counter("usuarios_asustados", username)
        self.increment_counter("estadisticas", "amenazas_enviadas")
        
        # Si es usuario nuevo, incrementar contador
        if nivel_miedo == 1:
            self.increment_counter("estadisticas", "usuarios_aterrorizados")
        
        # Seleccionar tipo de amenaza según nivel
        if nivel_miedo <= 2:
            amenaza = self.get_random_choice("amenazas_sutiles")
        elif nivel_miedo <= 5:
            amenaza = self.get_random_choice("amenazas_directas")
        else:
            # Amenazas ultra específicas para usuarios frecuentes
            amenaza = self._generar_amenaza_especifica(username, nivel_miedo)
        
        # Personalizar usando ResponseHandler
        amenaza_personalizada = ResponseHandler.personalize_by_name(username, amenaza)
        frase_intro = self.get_random_choice("frases_terrorificas")
        
        return f"👻 {frase_intro}\n\n{username}, {amenaza_personalizada}"
    
    def _generar_amenaza_especifica(self, username, nivel):
        """Generar amenazas específicas para usuarios frecuentes"""
        amenazas_especificas = [
            f"Ya llevas {nivel} interacciones conmigo, {username}... ¡Eso es obsesión!",
            f"{username}, después de {nivel} veces hablándome, ya eres parte de mi circo del terror.",
            f"¡{nivel} mensajes, {username}! ¡Oficialmente eres mi acosador favorito!",
            f"{username}, con {nivel} interacciones ya conoces todos mis secretos terroríficos.",
            f"¡{nivel} comentarios, {username}! ¡Ya eres mi víctima oficial!"
        ]
        
        return random.choice(amenazas_especificas)
    
    def responder_comentario_terrorificamente(self, username, comentario):
        """Responder a comentarios con estilo terrorífico usando ResponseHandler"""
        comentario_clean = ResponseHandler.clean_text(comentario)
        comentario_lower = comentario_clean.lower()
        
        # Respuestas específicas según el contenido usando detector de keywords
        if ResponseHandler.detect_keywords(comentario_lower, ["miedo", "susto", "terror", "asusta"]):
            respuestas_miedo = [
                f"¿Miedo, {username}? ¡Esto apenas empieza!",
                f"El miedo es solo el principio, {username}...",
                f"{username}, el terror verdadero aún no llega.",
                f"¿Te asusto, {username}? ¡Misión cumplida!"
            ]
            return ResponseHandler.personalize_by_name(username, random.choice(respuestas_miedo))
        
        if ResponseHandler.detect_keywords(comentario_lower, ["no", "no me asustas", "no da miedo"]):
            respuestas_desafio = [
                f"¿No te asusto, {username}? ¡Ya veremos!",
                f"Valientes palabras, {username}... por ahora.",
                f"{username}, los valientes son mis favoritos para atormentar.",
                f"¿Seguro, {username}? La noche es joven..."
            ]
            return random.choice(respuestas_desafio)
        
        if ResponseHandler.detect_keywords(comentario_lower, ["hola", "hi", "saludos"]):
            return f"Hola {username}... bienvenido a tu pesadilla favorita."
        
        if ResponseHandler.detect_keywords(comentario_lower, ["gracioso", "divertido", "chistoso"]):
            return f"¿Gracioso, {username}? ¡Mi humor es oscuro como mi alma!"
        
        if ResponseHandler.detect_keywords(comentario_lower, ["ayuda", "help", "socorro"]):
            return f"No hay ayuda para ti, {username}... solo yo."
        
        if ResponseHandler.detect_keywords(comentario_lower, ["lindo", "tierno", "cute"]):
            return f"¿Lindo, {username}? ¡Soy adorablemente terrorífico!"
        
        # Amenaza personalizada por defecto
        return self.get_amenaza_personalizada(username)
    
    def get_amenaza_aleatoria(self):
        """Obtener amenaza aleatoria sin personalizar"""
        todas_amenazas = self.data.get("amenazas_sutiles", []) + self.data.get("amenazas_directas", [])
        if not todas_amenazas:
            return "¡No tengo amenazas! ¡Pero tu existencia ya es suficientemente aterradora!"
        
        frase_intro = self.get_random_choice("frases_terrorificas")
        amenaza = random.choice(todas_amenazas)
        
        self.increment_counter("estadisticas", "amenazas_enviadas")
        
        return f"👻 {frase_intro}\n\n{amenaza}"
    
    def get_amenaza_por_categoria(self, tipo):
        """Obtener amenaza por tipo (sutil/directa)"""
        if tipo.lower() == "sutil":
            amenazas = self.data.get("amenazas_sutiles", [])
            categoria_nombre = "AMENAZA PSICOLÓGICA"
        elif tipo.lower() == "directa":
            amenazas = self.data.get("amenazas_directas", [])
            categoria_nombre = "AMENAZA DIRECTA"
        else:
            return "Tipos disponibles: 'sutil' o 'directa'. ¡Elige tu tipo de terror!"
        
        if not amenazas:
            return f"No tengo amenazas {tipo}. ¡Pero puedo improvisar!"
        
        frase_intro = self.get_random_choice("frases_terrorificas")
        amenaza = random.choice(amenazas)
        
        self.increment_counter("estadisticas", "amenazas_enviadas")
        
        return f"👻 {categoria_nombre}\n{frase_intro}\n\n{amenaza}"
    
    def get_top_usuarios_asustados(self):
        """Obtener ranking de usuarios más asustados"""
        usuarios_asustados = self.data.get("usuarios_asustados", {})
        if not usuarios_asustados:
            return "¡Nadie ha sido lo suficientemente valiente para enfrentarme!"
        
        ranking = sorted(usuarios_asustados.items(), key=lambda x: x[1], reverse=True)
        
        resultado = "👻 TOP VÍCTIMAS DEL TERROR:\n\n"
        for i, (username, nivel) in enumerate(ranking[:10], 1):
            emoji = ["👻", "💀", "🎭"][i-1] if i <= 3 else f"{i}."
            resultado += f"{emoji} {username}: {nivel} encuentros terroríficos\n"
        
        return resultado
    
    def modo_psicopata_activado(self, username):
        """Modo especial ultra terrorífico"""
        frases_psicopata = [
            f"Hehehe... {username}, has activado mi modo más oscuro...",
            f"{username}, ahora verás de qué soy realmente capaz...",
            f"¡EXCELENTE ELECCIÓN, {username.upper()}! ¡MI VERDADERO YO DESPIERTA!",
            f"{username}, acabas de abrir la caja de Pandora... pero con payasos.",
            f"*sonrisa diabólica* {username}, esto va a ser... interesante."
        ]
        
        amenazas_psicopata = [
            "Cada noche, escucharás el eco de mis zapatos gigantes en tu pasillo...",
            "Mis globos rojos aparecerán en lugares donde nunca los pusiste...",
            "Tu reflejo en el espejo empezará a sonreír cuando tú no lo hagas...",
            "Los niños pequeños señalarán detrás de ti y susurrarán 'el payaso'...",
            "Tus pesadillas tendrán soundtrack de música de circo distorsionada...",
            "Cada vez que veas un globo, recordarás esta conversación...",
            "Las risas de niños sonarán vacías y ecos cuando estés solo...",
            "Mis huellas de zapatos gigantes aparecerán en el polvo de tu casa..."
        ]
        
        intro = random.choice(frases_psicopata)
        amenaza = random.choice(amenazas_psicopata)
        
        # Incrementar significativamente el nivel de miedo
        self.data["usuarios_asustados"][username] = self.data.get("usuarios_asustados", {}).get(username, 0) + 5
        self.save_data()
        
        return f"{intro}\n\n{amenaza}\n\n*risa macabra que se desvanece lentamente*"
    
    def agregar_amenaza(self, amenaza, tipo="sutil"):
        """Agregar nueva amenaza usando método heredado"""
        if tipo.lower() == "sutil":
            self.add_item_to_list("amenazas_sutiles", amenaza)
        elif tipo.lower() == "directa":
            self.add_item_to_list("amenazas_directas", amenaza)
        else:
            return "Tipo debe ser 'sutil' o 'directa'"
        
        return f"✅ Amenaza {tipo} agregada al arsenal del terror"
    
    def get_frase_terrorifica_aleatoria(self):
        """Obtener solo una frase terrorífica de introducción"""
        frase = self.get_random_choice("frases_terrorificas")
        return frase if frase else "Desde el vacío de mi existencia..."
    
    def get_terror_stats(self):
        """Obtener estadísticas del terror usando método heredado"""
        base_stats = self.get_stats()
        
        amenazas_enviadas = self.get_counter("estadisticas", "amenazas_enviadas")
        usuarios_aterrorizados = self.get_counter("estadisticas", "usuarios_aterrorizados")
        usuarios_asustados = self.data.get("usuarios_asustados", {})
        
        stats = f"{base_stats}\n"
        stats += f"Amenazas enviadas: {amenazas_enviadas}\n"
        stats += f"Usuarios aterrorizados: {usuarios_aterrorizados}\n"
        
        if usuarios_asustados:
            total_encuentros = sum(usuarios_asustados.values())
            promedio = total_encuentros / len(usuarios_asustados)
            stats += f"Total encuentros terroríficos: {total_encuentros}\n"
            stats += f"Promedio por víctima: {promedio:.1f}\n"
            
            # Usuario más asustado
            usuario_top = max(usuarios_asustados, key=usuarios_asustados.get)
            nivel_top = usuarios_asustados[usuario_top]
            stats += f"Víctima principal: {usuario_top} ({nivel_top} encuentros)\n"
        
        return stats
    
    def reset_usuarios_asustados(self):
        """Resetear contador de usuarios asustados usando método heredado"""
        usuarios_asustados = self.data.get("usuarios_asustados", {})
        count = len(usuarios_asustados)
        
        self.data["usuarios_asustados"] = {}
        self.save_data()
        
        return f"🧹 {count} víctimas liberadas de su terror. ¡Pueden volver a asustarse!"
    
    def search_amenaza(self, keyword):
        """Buscar amenazas por palabra clave"""
        keyword_lower = keyword.lower()
        matching_threats = []
        
        # Buscar en amenazas sutiles
        for amenaza in self.data.get("amenazas_sutiles", []):
            if keyword_lower in amenaza.lower():
                matching_threats.append(("sutil", amenaza))
        
        # Buscar en amenazas directas
        for amenaza in self.data.get("amenazas_directas", []):
            if keyword_lower in amenaza.lower():
                matching_threats.append(("directa", amenaza))
        
        if not matching_threats:
            return f"No encontré amenazas sobre '{keyword}'. ¡Pero puedo improvisar algo terrorífico!"
        
        tipo, amenaza = random.choice(matching_threats)
        frase_intro = self.get_random_choice("frases_terrorificas")
        
        return f"👻 AMENAZA {tipo.upper()} encontrada:\n{frase_intro}\n\n{amenaza}"

# Ejemplo de uso
if __name__ == "__main__":
    manager = AmenazasManager()
    
    print("👻 PROBANDO MODO TERRORÍFICO...")
    
    # Mostrar estadísticas
    print("\n📊 ESTADÍSTICAS:")
    print(manager.get_terror_stats())
    
    # Probar amenaza aleatoria
    print("\n👻 AMENAZA ALEATORIA:")
    print(manager.get_amenaza_aleatoria())
    
    # Probar amenaza personalizada
    print("\n👻 AMENAZA PERSONALIZADA:")
    print(manager.get_amenaza_personalizada("TestUser"))
    
    print("\n✅ Pruebas de modo terrorífico completadas")