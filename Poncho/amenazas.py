import random
import json
import os
import time

class AmenazasManager:
    def __init__(self, amenazas_file="amenazas.json"):
        """
        Inicializar el manager del modo amenazas/terrorífico
        """
        self.amenazas_file = amenazas_file
        self.amenazas_sutiles = []
        self.amenazas_directas = []
        self.frases_terrorificas = []
        self.usuarios_asustados = {}  # username: nivel_miedo
        self.load_amenazas()
        print(f" Amenazas Manager inicializado - Modo Terrorífico Activado")
    
    def load_amenazas(self):
        """Cargar amenazas desde archivo JSON o crear por defecto"""
        try:
            if os.path.exists(self.amenazas_file):
                with open(self.amenazas_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.amenazas_sutiles = data.get('amenazas_sutiles', [])
                    self.amenazas_directas = data.get('amenazas_directas', [])
                    self.frases_terrorificas = data.get('frases_terrorificas', [])
                    self.usuarios_asustados = data.get('usuarios_asustados', {})
                print(f"✅ Cargadas amenazas desde {self.amenazas_file}")
            else:
                self._create_default_amenazas()
                self.save_amenazas()
                print(f" Archivo de amenazas creado: {self.amenazas_file}")
        
        except Exception as e:
            print(f"❌ Error cargando amenazas: {e}")
            self._create_default_amenazas()
    
    def _create_default_amenazas(self):
        """Crear amenazas por defecto"""
        
        # Amenazas sutiles - más psicológicas
        self.amenazas_sutiles = [
            "Ya sé dónde vives... en tu casa, obviamente. ¿Dónde más vivirías?",
            "Conozco todos tus secretos... como que comes pizza fría del desayuno.",
            "Te estoy observando... a través de esta pantalla como todos los demás.",
            "Pronto vendré por ti... cuando termine este livestream.",
            "Tus pesadillas serán mi diversión... espero que sueñes conmigo.",
            "Nunca estarás a salvo... de mis chistes malos.",
            "Cada sombra que veas soy yo... o tal vez solo paranoia.",
            "Tu tiempo se acaba... como la batería de tu teléfono.",
            "Sé lo que hiciste el verano pasado... viste mis videos anteriores.",
            "Los payasos nunca olvidan... especialmente las caras de los que no donan.",
            "El circo te llama... pero no para divertirte.",
            "En tus sueños me encontrarás... siendo igual de molesto.",
            "Cada globo rojo que veas será una advertencia... de que tengo mal gusto.",
            "Los espejos reflejarán mi sonrisa... hasta en el baño.",
            "Tu reflejo ya no será el mismo... porque yo estaré ahí atrás."
        ]
        
        # Amenazas más directas pero cómicas
        self.amenazas_directas = [
            "¡Te encontraré y te haré ver todos mis videos!",
            "¡Mi venganza será terrible... como mis chistes!",
            "¡Vendré en la madrugada... a tocar tu timbre hasta que despiertes!",
            "¡Te perseguiré hasta el fin del mundo... o hasta que se me acabe la batería!",
            "¡Mis globos de payaso flotarán hacia tu ventana!",
            "¡Te haré cosquillas hasta que rías... de mis bromas malas!",
            "¡Mi risa siniestra resonará en tu cabeza toda la noche!",
            "¡Mis zapatos gigantes harán ruido bajo tu cama!",
            "¡Te despertarás con mi cara pintada en tu espejo!",
            "¡Todos tus globos se convertirán en mi cara!",
            "¡Te atormentaré con música de circo las 24 horas!",
            "¡Mi nariz roja parpadeará en tu ventana toda la noche!",
            "¡Te enviaré cartas de amor escritas con maquillaje de payaso!",
            "¡Aparecerá mi cara en todas tus selfies!",
            "¡Tus pesadillas tendrán soundtrack de circo!"
        ]
        
        # Frases terroríficas de introducción
        self.frases_terrorificas = [
            "Desde las profundidades del circo abandonado...",
            "Con mi sonrisa congelada en la eternidad...",
            "Mientras mis lágrimas de maquillaje se secan...",
            "En la oscuridad de mi alma payasa...",
            "Con la maldad de mil globos pinchados...",
            "Desde mi trono de pesadillas...",
            "Con el eco de risas macabras...",
            "En el silencio de la carpa vacía...",
            "Mientras afile mis bromas terroríficas...",
            "Con la furia de un payaso despreciado...",
            "Desde mi reino de terror cómico...",
            "Con mis ojos sin alma pero llenos de sarcasmo...",
            "En mi mundo donde solo hay llanto y chistes malos...",
            "Mientras planificó mi venganza ridícula...",
            "Con la intensidad de mil espectáculos fallidos..."
        ]
        
        self.usuarios_asustados = {}
    
    def get_amenaza_personalizada(self, username):
        """Obtener amenaza personalizada para un usuario"""
        username_lower = username.lower()
        
        # Incrementar nivel de miedo del usuario
        if username_lower in self.usuarios_asustados:
            self.usuarios_asustados[username_lower] += 1
        else:
            self.usuarios_asustados[username_lower] = 1
        
        nivel_miedo = self.usuarios_asustados[username_lower]
        frase_intro = random.choice(self.frases_terrorificas)
        
        # Escalada de amenazas según el nivel
        if nivel_miedo <= 2:
            amenaza = random.choice(self.amenazas_sutiles)
        elif nivel_miedo <= 5:
            amenaza = random.choice(self.amenazas_directas)
        else:
            # Amenazas ultra específicas para usuarios frecuentes
            amenaza = self._generar_amenaza_especifica(username, nivel_miedo)
        
        # Personalizar según el nombre
        amenaza = self._personalizar_amenaza_por_nombre(username, amenaza)
        
        self.save_amenazas()
        
        return f" {frase_intro}\n\n{username}, {amenaza}"
    
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
    
    def _personalizar_amenaza_por_nombre(self, username, amenaza_base):
        """Personalizar amenaza según características del nombre"""
        name_lower = username.lower()
        
        # Modificaciones según el nombre
        if len(username) > 15:
            amenaza_base += f" Tu nombre es tan largo que me da pereza escribir toda la amenaza, {username[:8]}..."
        elif len(username) < 4:
            amenaza_base += f" Tu nombre es tan corto como tu valentía."
        
        # Números en el nombre
        if any(char.isdigit() for char in username):
            amenaza_base += " Los números en tu nombre no te protegerán de mi terror."
        
        # Nombres específicos
        nombres_especiales = {
            "admin": " Ser administrador no te dará privilegios en mis pesadillas.",
            "user": " 'User'... ¡Qué creativo! Como mis amenazas.",
            "guest": " Invitado... al hotel del terror.",
            "test": " ¿Test? ¡Vas a reprobar mi examen de miedo!",
            "bot": " ¿Bot? Los robots también pueden temer a los payasos.",
            "anonymous": " Anónimo no significa invisible para mí.",
            "troll": " ¿Troll? ¡Yo soy el monstruo bajo tu puente!",
            "gamer": " Los gamers no pueden pausar la vida real.",
            "streamer": " Tu stream será mi escenario de terror."
        }
        
        for nombre, modificacion in nombres_especiales.items():
            if nombre in name_lower:
                amenaza_base += modificacion
                break
        
        return amenaza_base
    
    def responder_comentario_terrorificamente(self, username, comentario):
        """Responder a comentarios con estilo terrorífico"""
        comentario_lower = comentario.lower()
        
        # Respuestas específicas según el contenido
        if any(palabra in comentario_lower for palabra in ["miedo", "susto", "terror", "asusta"]):
            respuestas_miedo = [
                f"¿Miedo, {username}? ¡Esto apenas empieza!",
                f"El miedo es solo el principio, {username}...",
                f"{username}, el terror verdadero aún no llega.",
                f"¿Te asusto, {username}? ¡Misión cumplida!"
            ]
            return random.choice(respuestas_miedo)
        
        if any(palabra in comentario_lower for palabra in ["no", "no me asustas", "no da miedo"]):
            respuestas_desafio = [
                f"¿No te asusto, {username}? ¡Ya veremos!",
                f"Valiente palabras, {username}... por ahora.",
                f"{username}, los valientes son mis favoritos para atormentar.",
                f"¿Seguro, {username}? La noche es joven..."
            ]
            return random.choice(respuestas_desafio)
        
        if any(palabra in comentario_lower for palabra in ["hola", "hi", "saludos"]):
            return f"Hola {username}... bienvenido a tu pesadilla favorita."
        
        if any(palabra in comentario_lower for palabra in ["gracioso", "divertido", "chistoso"]):
            return f"¿Gracioso, {username}? ¡Mi humor es oscuro como mi alma!"
        
        if any(palabra in comentario_lower for palabra in ["ayuda", "help", "socorro"]):
            return f"No hay ayuda para ti, {username}... solo yo."
        
        if any(palabra in comentario_lower for palabra in ["lindo", "tierno", "cute"]):
            return f"¿Lindo, {username}? ¡Soy adorablemente terrorífico!"
        
        # Amenaza personalizada por defecto
        return self.get_amenaza_personalizada(username)
    
    def get_amenaza_aleatoria(self):
        """Obtener amenaza aleatoria sin personalizar"""
        todas_amenazas = self.amenazas_sutiles + self.amenazas_directas
        if not todas_amenazas:
            return "¡No tengo amenazas! ¡Pero tu existencia ya es suficientemente aterradora!"
        
        frase_intro = random.choice(self.frases_terrorificas)
        amenaza = random.choice(todas_amenazas)
        
        return f"{frase_intro}\n\n{amenaza}"
    
    def get_amenaza_por_categoria(self, tipo):
        """Obtener amenaza por tipo (sutil/directa)"""
        if tipo.lower() == "sutil":
            amenazas = self.amenazas_sutiles
            categoria_nombre = "AMENAZA PSICOLÓGICA"
        elif tipo.lower() == "directa":
            amenazas = self.amenazas_directas
            categoria_nombre = "AMENAZA DIRECTA"
        else:
            return "Tipos disponibles: 'sutil' o 'directa'. ¡Elige tu tipo de terror!"
        
        if not amenazas:
            return f"No tengo amenazas {tipo}. ¡Pero puedo improvisar!"
        
        frase_intro = random.choice(self.frases_terrorificas)
        amenaza = random.choice(amenazas)
        
        return f"{categoria_nombre}\n{frase_intro}\n\n{amenaza}"
    
    def get_top_usuarios_asustados(self):
        """Obtener ranking de usuarios más asustados"""
        if not self.usuarios_asustados:
            return "¡Nadie ha sido lo suficientemente valiente para enfrentarme!"
        
        ranking = sorted(self.usuarios_asustados.items(), key=lambda x: x[1], reverse=True)
        
        resultado = " TOP VÍCTIMAS DEL TERROR:\n\n"
        for i, (username, nivel) in enumerate(ranking[:10], 1):
            emoji = ["👻", "💀", "🎭"][i-1] if i <= 3 else f"{i}."
            resultado += f"{emoji} {username}: {nivel} encuentros terroríficos\n"
        
        return resultado
    
    def get_estadisticas_terror(self):
        """Obtener estadísticas del modo terrorífico"""
        stats = f"📊 Estadísticas del Reino del Terror:\n"
        stats += f"Amenazas sutiles: {len(self.amenazas_sutiles)}\n"
        stats += f"Amenazas directas: {len(self.amenazas_directas)}\n"
        stats += f"Frases terroríficas: {len(self.frases_terrorificas)}\n"
        stats += f"Víctimas registradas: {len(self.usuarios_asustados)}\n"
        
        if self.usuarios_asustados:
            total_encuentros = sum(self.usuarios_asustados.values())
            promedio = total_encuentros / len(self.usuarios_asustados)
            stats += f"Total encuentros terroríficos: {total_encuentros}\n"
            stats += f"Promedio por víctima: {promedio:.1f}\n"
            
            # Usuario más asustado
            usuario_top = max(self.usuarios_asustados, key=self.usuarios_asustados.get)
            nivel_top = self.usuarios_asustados[usuario_top]
            stats += f"Víctima principal: {usuario_top} ({nivel_top} encuentros)\n"
        
        return stats
    
    def reset_usuarios_asustados(self):
        """Resetear contador de usuarios asustados"""
        count = len(self.usuarios_asustados)
        self.usuarios_asustados.clear()
        self.save_amenazas()
        return f"🧹 {count} víctimas liberadas de su terror. ¡Pueden volver a asustarse!"
    
    def agregar_amenaza(self, amenaza, tipo="sutil"):
        """Agregar nueva amenaza"""
        if tipo.lower() == "sutil":
            self.amenazas_sutiles.append(amenaza)
        elif tipo.lower() == "directa":
            self.amenazas_directas.append(amenaza)
        else:
            return "Tipo debe ser 'sutil' o 'directa'"
        
        self.save_amenazas()
        return f"✅ Amenaza {tipo} agregada al arsenal del terror"
    
    def get_frase_terrorifica_aleatoria(self):
        """Obtener solo una frase terrorífica de introducción"""
        if not self.frases_terrorificas:
            return "Desde el vacío de mi existencia..."
        
        return f"{random.choice(self.frases_terrorificas)}"
    
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
        username_lower = username.lower()
        self.usuarios_asustados[username_lower] = self.usuarios_asustados.get(username_lower, 0) + 5
        
        self.save_amenazas()
        
        return f"{intro}\n\n{amenaza}\n\n*risa macabra que se desvanece lentamente*"
    
    def save_amenazas(self):
        """Guardar amenazas en archivo JSON"""
        try:
            data = {
                "amenazas_sutiles": self.amenazas_sutiles,
                "amenazas_directas": self.amenazas_directas,
                "frases_terrorificas": self.frases_terrorificas,
                "usuarios_asustados": self.usuarios_asustados,
                "version": "1.0",
                "description": "Amenazas de Poncho el Payaso Terrorífico"
            }
            
            with open(self.amenazas_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Amenazas guardadas en {self.amenazas_file}")
        
        except Exception as e:
            print(f"❌ Error guardando amenazas: {e}")
    
    def reload_amenazas(self):
        """Recargar amenazas desde archivo"""
        self.load_amenazas()

# --- FUNCIONES DE UTILIDAD ---
def crear_amenazas_personalizadas():
    """Crear amenazas adicionales para diferentes situaciones"""
    amenazas_extra = {
        "amenazas_streamers": [
            "Tu stream será interrumpido por mi risa fantasmal...",
            "Los viewers verán mi cara en tu webcam aunque no esté ahí...",
            "Tus donaciones sonarán con música de circo terrorífica..."
        ],
        "amenazas_noctambulos": [
            "Las 3 AM será mi hora favorita para visitarte...",
            "Cuando todos duerman, yo estaré despierto... pensando en ti...",
            "La madrugada amplifica mis poderes terroríficos..."
        ],
        "amenazas_tecnologicas": [
            "Tu WiFi se cortará justo cuando más lo necesites... soy yo...",
            "Tus notificaciones serán reemplazadas por sonidos de circo...",
            "Tu Autocorrector cambiará todas las palabras por 'payaso'..."
        ]
    }
    
    return amenazas_extra

def test_modo_escalada(manager, username):
    """Probar escalada de amenazas con múltiples interacciones"""
    print(f"\n🧪 PROBANDO ESCALADA DE TERROR PARA {username}:")
    
    for i in range(8):
        print(f"\n--- Interacción {i+1} ---")
        amenaza = manager.get_amenaza_personalizada(username)
        print(amenaza)
        time.sleep(0.5)  # Pausa para simular tiempo real

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    print("💀 Probando modo terrorífico...")
    
    # Crear manager
    amenazas = AmenazasManager()
    
    # Mostrar estadísticas
    print("\n📊 ESTADÍSTICAS:")
    print(amenazas.get_estadisticas_terror())
    
    # Probar amenaza aleatoria
    print("\nAMENAZA ALEATORIA:")
    print(amenazas.get_amenaza_aleatoria())
    
    # Probar amenazas por categoría
    print("\nAMENAZA SUTIL:")
    print(amenazas.get_amenaza_por_categoria("sutil"))
    
    print("\nAMENAZA DIRECTA:")
    print(amenazas.get_amenaza_por_categoria("directa"))
    
    # Probar respuestas a comentarios
    print("\n💬 RESPUESTAS TERRORÍFICAS:")
    comentarios_test = [
        ("Juan", "Hola Poncho"),
        ("Ana", "Me das miedo"),
        ("Pedro", "No me asustas"),
        ("Luis", "Eres gracioso"),
        ("Maria", "¡Ayuda!")
    ]
    
    for usuario, comentario in comentarios_test:
        respuesta = amenazas.responder_comentario_terrorificamente(usuario, comentario)
        print(f"\n{usuario}: '{comentario}'")
        print(f"Poncho: {respuesta}")
    
    # Probar modo psicópata
    print("\nMODO PSICÓPATA:")
    psicopata = amenazas.modo_psicopata_activado("TestUser")
    print(psicopata)
    
    # Mostrar ranking de víctimas
    print("\n" + amenazas.get_top_usuarios_asustados())
    
    # Probar escalada (descomenta para ver escalada completa)
    # test_modo_escalada(amenazas, "Victim")
    
    print("\n✅ Pruebas de modo terrorífico completadas")