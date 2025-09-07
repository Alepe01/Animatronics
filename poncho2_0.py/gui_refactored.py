import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import time
from response_handler import ResponseHandler

class RefactoredGUI:
    """Interfaz gráfica refactorizada y optimizada"""
    
    def __init__(self, root, mode_controller):
        self.root = root
        self.mode_controller = mode_controller
        self.mode_window = None
        
        self.setup_main_window()
        self.setup_ui_components()
        self.setup_menu()
        
        # Registrar callback para actualizar respuestas
        self.mode_controller.register_poncho_callback(self.on_mode_change_gui)
        
        print("🖼️ GUI Refactorizada inicializada")
    
    def setup_main_window(self):
        """Configurar ventana principal"""
        self.root.title("Poncho el Payaso - Refactorizado v2.0")
        self.root.configure(bg="black")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Icono si está disponible
        try:
            self.root.iconname("Poncho")
        except:
            pass
    
    def setup_menu(self):
        """Crear barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Estadísticas", command=self.show_stats)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Modo
        mode_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modo", menu=mode_menu)
        mode_menu.add_command(label="Control de Modo", command=self.open_mode_control)
        mode_menu.add_command(label="Configurar Audio", command=self.open_audio_config)
        
        # Menú Herramientas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Limpiar Cola", command=self.clear_queue)
        tools_menu.add_command(label="Probar Sistemas", command=self.test_systems)
        tools_menu.add_command(label="Recargar Managers", command=self.reload_managers)
    
    def setup_ui_components(self):
        """Configurar componentes de la UI para sistema dual"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg="black")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header con título y status
        self.setup_header(main_frame)
        
        # Área de contenido principal - MODIFICADA para dos paneles
        content_frame = tk.Frame(main_frame, bg="black")
        content_frame.pack(fill="both", expand=True, pady=10)
        
        # Panel izquierdo: Comentarios (solo Poncho)
        self.setup_comments_panel(content_frame)
        
        # Panel central: Regalos (Robot de Regalos)
        self.setup_gifts_panel(content_frame)
        
        # Panel derecho: Control y respuestas
        self.setup_control_panel(content_frame)
    
    def setup_header(self, parent):
        """Configurar header con título y status"""
        header_frame = tk.Frame(parent, bg="black")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Título principal
        title_label = tk.Label(header_frame, text="🤡 PONCHO EL PAYASO 🤡", 
                              bg="black", fg="red", font=("Arial", 24, "bold"))
        title_label.pack(pady=5)
        
        # Subtítulo con versión
        subtitle_label = tk.Label(header_frame, text="Versión Refactorizada v2.0 - Código Optimizado", 
                                 bg="black", fg="yellow", font=("Arial", 12))
        subtitle_label.pack()
        
        # Status bar
        status_frame = tk.Frame(header_frame, bg="gray20")
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_label = tk.Label(status_frame, text="Estado: Iniciando...", 
                                    bg="gray20", fg="lime", font=("Arial", 10))
        self.status_label.pack(side="left", padx=10)
        
        self.mode_label = tk.Label(status_frame, text="Modo: Conversación", 
                                  bg="gray20", fg="cyan", font=("Arial", 10))
        self.mode_label.pack(side="right", padx=10)
    
    def setup_comments_panel(self, parent):
        """Configurar panel de comentarios (solo para Poncho)"""
        # Frame izquierdo para comentarios - REDUCIDO
        comments_frame = tk.Frame(parent, bg="black")
        comments_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Header de comentarios
        comments_header = tk.Frame(comments_frame, bg="black")
        comments_header.pack(fill="x", pady=(0, 5))
        
        tk.Label(comments_header, text="🤖 PONCHO (COMENTARIOS)", 
                bg="black", fg="lime", font=("Arial", 14, "bold")).pack(side="left")
        
        # Contador de comentarios
        self.comment_count_label = tk.Label(comments_header, text="(0)", 
                                           bg="black", fg="lime", font=("Arial", 12))
        self.comment_count_label.pack(side="right")
        
        # Área de texto para comentarios
        self.comments_text = scrolledtext.ScrolledText(
            comments_frame, 
            width=50, height=20,  # REDUCIDO
            bg="gray10", fg="white", 
            font=("Consolas", 9),  # FUENTE MENOR
            wrap=tk.WORD,
            insertbackground="white",
            state=tk.DISABLED
        )
        self.comments_text.pack(fill="both", expand=True)
        
        # Configurar tags para diferentes tipos de mensajes
        self.setup_text_tags()
    
    def setup_gifts_panel(self, parent):
        """Configurar panel exclusivo para regalos"""
        # Frame central para regalos
        gifts_frame = tk.Frame(parent, bg="black")
        gifts_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Header de regalos
        gifts_header = tk.Frame(gifts_frame, bg="black")
        gifts_header.pack(fill="x", pady=(0, 5))
        
        tk.Label(gifts_header, text="🎁 ROBOT DE REGALOS", 
                bg="black", fg="gold", font=("Arial", 14, "bold")).pack(side="left")
        
        # Contador de regalos
        self.gift_count_label = tk.Label(gifts_header, text="(0 regalos)", 
                                        bg="black", fg="gold", font=("Arial", 12))
        self.gift_count_label.pack(side="right")
        
        # Área de texto para regalos
        self.gifts_text = scrolledtext.ScrolledText(
            gifts_frame, 
            width=50, height=20,
            bg="gray5", fg="gold", 
            font=("Arial", 10, "bold"), 
            wrap=tk.WORD,
            insertbackground="gold",
            state=tk.DISABLED
        )
        self.gifts_text.pack(fill="both", expand=True)
        
        # Configurar tags para diferentes tipos de regalos
        self.setup_gift_tags()
    
    def setup_gift_tags(self):
        """Configurar tags para colorear regalos"""
        self.gifts_text.tag_config("gift_normal", foreground="gold", font=("Arial", 10, "bold"))
        self.gifts_text.tag_config("gift_special", foreground="magenta", font=("Arial", 11, "bold"))
        self.gifts_text.tag_config("gift_combo", foreground="cyan", font=("Arial", 11, "bold"))
        self.gifts_text.tag_config("celebration", foreground="lime", font=("Arial", 12, "bold"))
        self.gifts_text.tag_config("gift_system", foreground="orange", font=("Arial", 10))
    
    def setup_control_panel(self, parent):
        """Configurar panel de control y respuestas"""
        # Frame derecho para control
        control_frame = tk.Frame(parent, bg="black")
        control_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Botones de control rápido
        self.setup_quick_controls(control_frame)
        
        # Área de respuestas
        self.setup_response_area(control_frame)
        
        # Panel de información
        self.setup_info_panel(control_frame)
    
    def setup_quick_controls(self, parent):
        """Configurar controles rápidos incluyendo ventana de pruebas"""
        controls_frame = tk.Frame(parent, bg="gray20")
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Título
        tk.Label(controls_frame, text="🎮 CONTROLES RÁPIDOS", 
                bg="gray20", fg="orange", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Frame para botones
        buttons_frame = tk.Frame(controls_frame, bg="gray20")
        buttons_frame.pack(fill="x", padx=10, pady=5)
        
        # Botones en filas - ACTUALIZADO con ventana de pruebas
        button_configs = [
            [("🗣️ Modo", self.open_mode_control, "blue"),
             ("📊 Audio", self.open_audio_config, "purple")],
            [("⏹️ Parar", self.stop_audio, "red"),
             ("📊 Stats", self.show_stats, "green")],
            [("🧪 Pruebas", self.open_test_window, "purple"),
             ("🔄 Reset", self.reset_system, "orange")]
        ]
        
        for row, button_row in enumerate(button_configs):
            row_frame = tk.Frame(buttons_frame, bg="gray20")
            row_frame.pack(fill="x", pady=2)
            
            for text, command, color in button_row:
                btn = tk.Button(row_frame, text=text, command=command,
                               bg=color, fg="white", font=("Arial", 9, "bold"),
                               width=12, height=1)
                btn.pack(side="left", padx=2, expand=True, fill="x")
    
    def setup_response_area(self, parent):
        """Configurar área de respuestas"""
        # Header de respuestas
        response_header = tk.Frame(parent, bg="black")
        response_header.pack(fill="x", pady=(0, 5))
        
        tk.Label(response_header, text="🗣️ RESPUESTA DE PONCHO", 
                bg="black", fg="yellow", font=("Arial", 14, "bold")).pack(side="left")
        
        # Indicador de estado
        self.response_status = tk.Label(response_header, text="💤", 
                                       bg="black", fg="gray", font=("Arial", 16))
        self.response_status.pack(side="right")
        
        # Área de texto para respuestas
        self.response_text = scrolledtext.ScrolledText(
            parent,
            width=50, height=12,
            bg="gray20", fg="yellow", 
            font=("Arial", 12, "bold"), 
            wrap=tk.WORD,
            insertbackground="yellow",
            state=tk.DISABLED
        )
        self.response_text.pack(fill="both", expand=True, pady=(0, 10))
    
    def setup_info_panel(self, parent):
        """Configurar panel de información"""
        info_frame = tk.Frame(parent, bg="gray15")
        info_frame.pack(fill="x")
        
        tk.Label(info_frame, text="ℹ️ INFORMACIÓN", 
                bg="gray15", fg="cyan", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Labels de información
        self.queue_info_label = tk.Label(info_frame, text="Cola: 0 comentarios", 
                                        bg="gray15", fg="white", font=("Arial", 9))
        self.queue_info_label.pack()
        
        self.audio_info_label = tk.Label(info_frame, text="Audio: Inactivo", 
                                        bg="gray15", fg="white", font=("Arial", 9))
        self.audio_info_label.pack()
        
        # Actualizar info cada segundo
        self.update_info_panel()
    
    def setup_text_tags(self):
        """Configurar tags para colorear texto"""
        # Tags para comentarios
        self.comments_text.tag_config("comment", foreground="white")
        self.comments_text.tag_config("gift", foreground="#00ff00", font=("Consolas", 10, "bold"))
        self.comments_text.tag_config("audio", foreground="#00ffff", font=("Consolas", 10, "bold"))
        self.comments_text.tag_config("system", foreground="#ff6600", font=("Consolas", 10, "bold"))
        self.comments_text.tag_config("error", foreground="#ff4444", font=("Consolas", 10, "bold"))
    
    def open_test_window(self):
        """Abrir ventana de pruebas"""
        try:
            from test_window_manager import TestWindowManager
            
            # Obtener referencia a la aplicación principal
            if hasattr(self.mode_controller, 'parent_app'):
                parent_app = self.mode_controller.parent_app
            elif hasattr(self, 'parent_app'):
                parent_app = self.parent_app
            else:
                # Crear mock app si no existe referencia
                class MockApp:
                    def __init__(self, root, dual_controller):
                        self.root = root
                        self.dual_controller = dual_controller
                    
                    def handle_comment(self, username, comment, msg_type):
                        self.dual_controller.add_comment(username, comment, msg_type)
                
                parent_app = MockApp(self.root, self.mode_controller)
            
            # Crear y mostrar ventana de pruebas
            test_manager = TestWindowManager(parent_app)
            test_manager.show_test_window()
            
            self.add_system_message("🧪 Ventana de pruebas abierta - Puedes simular comentarios y regalos")
            
        except ImportError:
            messagebox.showerror("Error", "test_window_manager.py no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Error abriendo ventana de pruebas: {e}")
    
    def reset_system(self):
        """Resetear sistema"""
        try:
            if hasattr(self.mode_controller, 'clear_poncho_queue'):
                cleared = self.mode_controller.clear_poncho_queue()
                self.add_system_message(f"🔄 Cola de Poncho limpiada: {cleared} comentarios")
            
            if hasattr(self.mode_controller, 'robot_regalo'):
                self.mode_controller.robot_regalo.resetear_racha()
                self.add_system_message("🔄 Racha de regalos reseteada")
            
            self.add_system_message("✅ Sistema reseteado correctamente")
            
        except Exception as e:
            self.add_system_message(f"❌ Error reseteando sistema: {e}")
    
    def open_mode_control(self):
        """Abrir ventana de control de modo optimizada"""
        if self.mode_window is None or not self.mode_window.winfo_exists():
            self.mode_window = ModeControlWindow(self.root, self.mode_controller)
        else:
            self.mode_window.lift()
    
    def open_audio_config(self):
        """Abrir configuración de audio simplificada"""
        audio_window = tk.Toplevel(self.root)
        audio_window.title("Configuración de Audio")
        audio_window.configure(bg="black")
        audio_window.geometry("500x400")
        audio_window.resizable(False, False)
        
        # Contenido simplificado
        tk.Label(audio_window, text="📊 CONFIGURACIÓN DE AUDIO", 
                bg="black", fg="cyan", font=("Arial", 16, "bold")).pack(pady=20)
        
        info_text = """Para capturar audio de YouTube/videos:
        
1. Ve a Configuración de Sonido de Windows
2. Busca 'Mezcla Estéreo' o 'Stereo Mix'
3. Actívalo como dispositivo de grabación
4. Reinicia la aplicación

Nota: No todos los sistemas tienen esta opción."""
        
        tk.Label(audio_window, text=info_text, bg="black", fg="white", 
                font=("Arial", 11), justify="left").pack(pady=20, padx=20)
        
        tk.Button(audio_window, text="Cerrar", command=audio_window.destroy,
                 bg="gray", fg="white", font=("Arial", 12)).pack(pady=20)
    
    def add_comment(self, username, comment, msg_type):
        """Agregar comentario con formato mejorado"""
        self.comments_text.config(state=tk.NORMAL)
        
        timestamp = time.strftime("%H:%M:%S")
        
        # Formatear según tipo
        if msg_type == "gift":
            formatted = f"[{timestamp}] 🎁 [REGALO] {username}: {comment}\n"
            tag = "gift"
        elif msg_type == "audio":
            formatted = f"[{timestamp}] 🎤 [AUDIO] {username}: {comment}\n"
            tag = "audio"
        else:
            formatted = f"[{timestamp}] 💬 {username}: {comment}\n"
            tag = "comment"
        
        # Insertar con tag
        start_pos = self.comments_text.index(tk.END)
        self.comments_text.insert(tk.END, formatted)
        end_pos = self.comments_text.index(tk.END)
        
        self.comments_text.tag_add(tag, f"{start_pos}-1l", f"{end_pos}-1l")
        self.comments_text.see(tk.END)
        self.comments_text.config(state=tk.DISABLED)
        
        # Actualizar contador
        self.update_comment_count()
    
    def add_gift(self, username, gift_info, response):
        """Agregar regalo al panel especializado"""
        self.gifts_text.config(state=tk.NORMAL)
        
        timestamp = time.strftime("%H:%M:%S")
        formatted_gift = f"[{timestamp}] 🎁 {username}: {gift_info}\n"
        formatted_response = f"🤖💛 {response[:100]}{'...' if len(response) > 100 else ''}\n"
        separator = "─" * 50 + "\n"
        
        # Insertar regalo
        start_pos = self.gifts_text.index(tk.END)
        self.gifts_text.insert(tk.END, formatted_gift)
        self.gifts_text.insert(tk.END, formatted_response)
        self.gifts_text.insert(tk.END, separator)
        end_pos = self.gifts_text.index(tk.END)
        
        self.gifts_text.tag_add("gift_normal", f"{start_pos}-1l", f"{end_pos}-1l")
        self.gifts_text.see(tk.END)
        self.gifts_text.config(state=tk.DISABLED)
        
        # Actualizar contador
        self.update_gift_count()
    
    def add_gift_combo(self, info, gift_info, response):
        """Agregar combo de regalos"""
        self.gifts_text.config(state=tk.NORMAL)
        
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] 🎁🎁🎁 COMBO: {gift_info}\n"
        formatted += f"🤖💛 {response[:150]}{'...' if len(response) > 150 else ''}\n"
        formatted += "═" * 50 + "\n"
        
        start_pos = self.gifts_text.index(tk.END)
        self.gifts_text.insert(tk.END, formatted)
        end_pos = self.gifts_text.index(tk.END)
        
        self.gifts_text.tag_add("gift_combo", f"{start_pos}-1l", f"{end_pos}-1l")
        self.gifts_text.see(tk.END)
        self.gifts_text.config(state=tk.DISABLED)
    
    def add_celebration(self, event_info, response):
        """Agregar celebración de racha"""
        self.gifts_text.config(state=tk.NORMAL)
        
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] 🎉🎉🎉 {event_info}\n"
        formatted += f"🤖🔥 {response}\n"
        formatted += "★" * 50 + "\n"
        
        start_pos = self.gifts_text.index(tk.END)
        self.gifts_text.insert(tk.END, formatted)
        end_pos = self.gifts_text.index(tk.END)
        
        self.gifts_text.tag_add("celebration", f"{start_pos}-1l", f"{end_pos}-1l")
        self.gifts_text.see(tk.END)
        self.gifts_text.config(state=tk.DISABLED)
    
    def add_system_message(self, message):
        """Agregar mensaje del sistema"""
        self.comments_text.config(state=tk.NORMAL)
        
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] ⚙️ SISTEMA: {message}\n"
        
        start_pos = self.comments_text.index(tk.END)
        self.comments_text.insert(tk.END, formatted)
        end_pos = self.comments_text.index(tk.END)
        
        self.comments_text.tag_add("system", f"{start_pos}-1l", f"{end_pos}-1l")
        self.comments_text.see(tk.END)
        self.comments_text.config(state=tk.DISABLED)
    
    def update_response(self, text):
        """Actualizar respuesta de Poncho"""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        
        timestamp = time.strftime("%H:%M:%S")
        clean_text = ResponseHandler.clean_text(text)
        response_with_time = f"[{timestamp}] {clean_text}"
        
        self.response_text.insert(tk.END, response_with_time)
        self.response_text.config(state=tk.DISABLED)
        
        # Actualizar status visual
        self.response_status.config(text="🗣️", fg="lime")
        self.root.after(3000, lambda: self.response_status.config(text="💤", fg="gray"))
    
    def update_comment_count(self):
        """Actualizar contador de comentarios"""
        # Contar líneas en el área de comentarios
        content = self.comments_text.get("1.0", tk.END)
        lines = content.count('\n') - 1  # -1 para la línea vacía final
        self.comment_count_label.config(text=f"({max(0, lines)})")
    
    def update_gift_count(self):
        """Actualizar contador de regalos"""
        content = self.gifts_text.get("1.0", tk.END)
        gift_count = content.count("🎁")
        self.gift_count_label.config(text=f"({gift_count} regalos)")
    
    def update_info_panel(self):
        """Actualizar panel de información para sistema dual"""
        try:
            # Actualizar información usando dual controller
            if hasattr(self.mode_controller, 'get_system_status'):
                status = self.mode_controller.get_system_status()
                
                # Información de Poncho
                poncho_info = status.get('poncho', {})
                queue_text = f"Poncho Cola: {poncho_info.get('cola', 0)}"
                if poncho_info.get('procesando', False):
                    queue_text += " (Procesando...)"
                self.queue_info_label.config(text=queue_text)
                
                # Información del Robot de Regalos
                regalo_info = status.get('regalo', {})
                gift_text = f"Regalos: Racha {regalo_info.get('racha_actual', 0)}"
                if regalo_info.get('activo', True):
                    gift_text += " ✅"
                    self.audio_info_label.config(fg="gold")
                else:
                    gift_text += " ❌"
                    self.audio_info_label.config(fg="gray")
                self.audio_info_label.config(text=gift_text)
                
                # Status general
                if poncho_info.get('procesando', False):
                    self.status_label.config(text="Estado: Poncho procesando...", fg="yellow")
                elif poncho_info.get('audio', False):
                    self.status_label.config(text="Estado: Poncho hablando...", fg="lime")
                else:
                    self.status_label.config(text="Estado: Sistema Dual Activo", fg="cyan")
            
        except Exception as e:
            print(f"Error actualizando info panel: {e}")
        
        # Programar próxima actualización
        self.root.after(1000, self.update_info_panel)
    
    def on_mode_change_gui(self, new_mode, old_mode):
        """Callback para cambios de modo en la GUI"""
        mode_name = self.mode_controller.get_mode_name(new_mode)
        self.mode_label.config(text=f"Modo: {mode_name}")
    
    def stop_audio(self):
        """Detener audio actual"""
        if hasattr(self.mode_controller, 'poncho_controller') and hasattr(self.mode_controller.poncho_controller, 'audio_manager'):
            self.mode_controller.poncho_controller.audio_manager.stop_audio()
            self.add_system_message("Audio detenido por el usuario")
    
    def clear_queue(self):
        """Limpiar cola de comentarios"""
        cleared = self.mode_controller.clear_poncho_queue()
        self.add_system_message(f"Cola limpiada: {cleared} comentarios eliminados")
    
    def show_stats(self):
        """Mostrar ventana de estadísticas"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Estadísticas del Sistema")
        stats_window.configure(bg="black")
        stats_window.geometry("600x500")
        
        # Header
        tk.Label(stats_window, text="📊 ESTADÍSTICAS DEL SISTEMA", 
                bg="black", fg="cyan", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Área de texto para estadísticas
        stats_text = scrolledtext.ScrolledText(
            stats_window,
            width=70, height=25,
            bg="gray10", fg="white",
            font=("Consolas", 10)
        )
        stats_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Obtener estadísticas
        try:
            stats = self.get_system_stats()
            stats_text.insert(tk.END, stats)
        except Exception as e:
            stats_text.insert(tk.END, f"Error obteniendo estadísticas: {e}")
        
        stats_text.config(state=tk.DISABLED)
        
        # Botón cerrar
        tk.Button(stats_window, text="Cerrar", command=stats_window.destroy,
                 bg="gray", fg="white", font=("Arial", 12)).pack(pady=10)
    
    def get_system_stats(self):
        """Obtener estadísticas del sistema dual"""
        if hasattr(self.mode_controller, 'get_combined_stats'):
            return self.mode_controller.get_combined_stats()
        else:
            return "Sistema dual no disponible"
    
    def test_systems(self):
        """Probar todos los sistemas"""
        if messagebox.askyesno("Probar Sistemas", "¿Ejecutar pruebas de todos los sistemas?\nEsto cambiará modos automáticamente."):
            self.add_system_message("Iniciando pruebas automáticas...")
            
            # Ejecutar pruebas en thread separado
            import threading
            test_thread = threading.Thread(target=self._run_system_tests, daemon=True)
            test_thread.start()
    
    def _run_system_tests(self):
        """Ejecutar pruebas del sistema"""
        test_cases = [
            (1, "TestUser", "Hola Poncho", "comment"),
            (2, "TestUser", "Cuenta un chiste", "comment"),
            (3, "TestUser", "¿Cuál es mi futuro?", "comment"),
            (4, "TestUser", "Dame un acertijo", "comment"),
            (5, "TestUser", "Me das miedo", "comment"),
            (6, "TestUser", "Canta algo", "comment")
        ]
        
        for mode, username, comment, msg_type in test_cases:
            # Cambiar modo
            self.mode_controller.change_mode(mode)
            
            # Agregar comentario a GUI
            self.root.after(0, lambda u=username, c=comment, t=msg_type: self.add_comment(u, c, t))
            
            # Procesar comentario
            self.mode_controller.add_comment(username, comment, msg_type)
            
            # Pausa entre pruebas
            time.sleep(3)
        
        self.root.after(0, lambda: self.add_system_message("Pruebas automáticas completadas"))
    
    def reload_managers(self):
        """Recargar todos los managers"""
        try:
            if hasattr(self.mode_controller, 'poncho_controller') and hasattr(self.mode_controller.poncho_controller, 'managers'):
                for name, manager in self.mode_controller.poncho_controller.managers.items():
                    if hasattr(manager, 'reload_data'):
                        manager.reload_data()
                        self.add_system_message(f"Manager {name} recargado")
                
                self.add_system_message("Todos los managers recargados exitosamente")
            else:
                self.add_system_message("No se pudieron encontrar los managers para recargar")
        except Exception as e:
            self.add_system_message(f"Error recargando managers: {e}")


class ModeControlWindow:
    """Ventana de control de modo optimizada"""
    
    def __init__(self, parent, mode_controller):
        self.mode_controller = mode_controller
        self.window = tk.Toplevel(parent)
        self.window.title("Control de Modo - Poncho v2.0")
        self.window.configure(bg="black")
        self.window.geometry("600x600")
        self.window.resizable(False, False)
        
        self.setup_window()
        self.update_button_states()
    
    def setup_window(self):
        """Configurar ventana de control"""
        # Header
        header_frame = tk.Frame(self.window, bg="black")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(header_frame, text="🎮 CONTROL DE MODO", 
                bg="black", fg="cyan", font=("Arial", 18, "bold")).pack()
        
        tk.Label(header_frame, text="Selecciona el modo de operación de Poncho", 
                bg="black", fg="gray", font=("Arial", 12)).pack(pady=5)
        
        # Frame para botones de modo
        buttons_frame = tk.Frame(self.window, bg="black")
        buttons_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        # Configuración de modos
        mode_configs = [
            (1, "💬 CONVERSACIÓN CON CHAT", "Respuestas usando OpenAI", "green"),
            (2, "😂 CONTAR CHISTES", "Modo comediante automático", "purple"),
            (3, "🔮 CLARIVIDENTE", "Predicciones del futuro", "violet"),
            (4, "🧩 ACERTIJOS", "Juegos de adivinanzas", "orange"),
            (5, "👻 MODO TERRORÍFICO", "Amenazas y sustos", "darkred"),
            (6, "🎵 MODO CANTANTE", "Reproducir música", "blue")
        ]
        
        self.mode_buttons = {}
        
        for mode, title, description, color in mode_configs:
            # Frame para cada modo
            mode_frame = tk.Frame(buttons_frame, bg="gray20", relief="raised", bd=2)
            mode_frame.pack(fill="x", pady=5)
            
            # Botón principal
            btn = tk.Button(mode_frame, text=title,
                           command=lambda m=mode: self.set_mode(m),
                           bg=color, fg="white", font=("Arial", 12, "bold"),
                           height=2, relief="flat")
            btn.pack(fill="x", padx=5, pady=5)
            
            # Descripción
            tk.Label(mode_frame, text=description,
                    bg="gray20", fg="lightgray", font=("Arial", 10)).pack(pady=(0, 5))
            
            self.mode_buttons[mode] = (btn, color)
        
        # Status actual
        status_frame = tk.Frame(self.window, bg="gray15")
        status_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(status_frame, text="Estado Actual:", 
                bg="gray15", fg="white", font=("Arial", 10, "bold")).pack(side="left")
        
        self.status_label = tk.Label(status_frame, text="Conversación con Chat", 
                                    bg="gray15", fg="yellow", font=("Arial", 10))
        self.status_label.pack(side="right")
    
    def set_mode(self, mode):
        """Cambiar modo"""
        self.mode_controller.change_mode(mode)
        self.update_button_states()
        
        # Actualizar status
        mode_name = self.mode_controller.get_mode_name(mode)
        self.status_label.config(text=mode_name)
    
    def update_button_states(self):
        """Actualizar estados visuales de los botones"""
        current_mode = self.mode_controller.get_current_mode()
        
        # Colores activos
        active_colors = {
            1: "lime", 2: "magenta", 3: "pink", 
            4: "gold", 5: "red", 6: "cyan",
            7: "lightblue", 8: "lightgreen"
        }
        
        for mode, (button, original_color) in self.mode_buttons.items():
            if mode == current_mode:
                button.config(bg=active_colors.get(mode, "white"), 
                             relief="sunken", bd=3)
            else:
                button.config(bg=original_color, relief="flat", bd=2)


# Ejemplo de uso
if __name__ == "__main__":
    # Para probar la GUI independientemente
    root = tk.Tk()
    
    # Mock mode controller para testing
    class MockModeController:
        def __init__(self):
            self.current_mode = 1
            self.managers = {}
            self.callbacks = []
        
        def get_current_mode(self):
            return self.current_mode
        
        def get_mode_name(self, mode=None):
            names = {1: "Chat", 2: "Chistes", 3: "Clarividente"}
            return names.get(mode or self.current_mode, "Desconocido")
        
        def register_poncho_callback(self, callback):
            self.callbacks.append(callback)
        
        def get_system_status(self):
            return {'poncho': {'cola': 0, 'procesando': False, 'audio': False},
                    'regalo': {'activo': True, 'racha_actual': 0}}
        
        def clear_poncho_queue(self):
            return 0
    
    mock_controller = MockModeController()
    gui = RefactoredGUI(root, mock_controller)
    
    print("🧪 Iniciando GUI de prueba...")
    root.mainloop()