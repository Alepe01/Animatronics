import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import random

class TestWindowManager:
    """Ventana de pruebas para simular comentarios y regalos sin TikTok"""
    
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.window = None
        self.auto_mode = False
        self.auto_thread = None
        self.comment_history = []
        
        # Datos de prueba
        self.test_users = [
            "TestUser1", "Ana_123", "Pedro_Gaming", "MariaLuna", "Carlos_Pro",
            "Sofia_Stream", "Luis_Music", "Elena_Art", "Diego_Tech", "Valeria_Fun"
        ]
        
        self.test_comments = [
            "Hola Poncho!", "¿Cómo estás?", "Cuenta un chiste", "Eres gracioso",
            "¿Cuál es mi futuro?", "Dame un acertijo", "Me das miedo", "Canta algo",
            "No me gustas", "Eres aburrido", "¿Qué haces?", "Salúdame",
            "iniciar conversación", "temas", "iniciar entrevista", "escuchar"
        ]
        
        self.test_gifts = [
            ("Rosa", 1), ("Corazón", 1), ("León", 1), ("Estrella", 3),
            ("Dragón", 1), ("Corona", 1), ("Diamante", 2), ("Universo", 1),
            ("Like", 5), ("Pulgar arriba", 2)
        ]
    
    def show_test_window(self):
        """Mostrar ventana de pruebas"""
        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.window = tk.Toplevel(self.parent_app.root)
        self.window.title("Ventana de Pruebas - Poncho Test")
        self.window.configure(bg="black")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        self.setup_test_interface()
        
    def setup_test_interface(self):
        """Configurar interfaz de pruebas"""
        # Header
        header_frame = tk.Frame(self.window, bg="black")
        header_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(header_frame, text="🧪 VENTANA DE PRUEBAS", 
                bg="black", fg="cyan", font=("Arial", 16, "bold")).pack()
        
        tk.Label(header_frame, text="Simula comentarios y regalos sin TikTok", 
                bg="black", fg="gray", font=("Arial", 12)).pack()
        
        # Notebook para pestañas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña 1: Comentarios manuales
        self.setup_manual_tab(notebook)
        
        # Pestaña 2: Regalos manuales
        self.setup_gifts_tab(notebook)
        
        # Pestaña 3: Modo automático
        self.setup_auto_tab(notebook)
        
        # Pestaña 4: Pruebas rápidas
        self.setup_quick_tests_tab(notebook)
        
        # Panel de estado
        self.setup_status_panel()
    
    def setup_manual_tab(self, notebook):
        """Configurar pestaña de comentarios manuales"""
        manual_frame = tk.Frame(notebook, bg="black")
        notebook.add(manual_frame, text="💬 Comentarios")
        
        # Sección de usuario
        user_frame = tk.Frame(manual_frame, bg="gray20")
        user_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(user_frame, text="Usuario:", bg="gray20", fg="white", 
                font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.username_var = tk.StringVar(value="TestUser")
        username_entry = tk.Entry(user_frame, textvariable=self.username_var, 
                                 font=("Arial", 12), width=20)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Botón de usuario aleatorio
        tk.Button(user_frame, text="🎲 Usuario Aleatorio", 
                 command=self.random_username,
                 bg="blue", fg="white").grid(row=0, column=2, padx=5, pady=5)
        
        # Sección de comentario
        comment_frame = tk.Frame(manual_frame, bg="gray20")
        comment_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(comment_frame, text="Comentario:", bg="gray20", fg="white",
                font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        
        # Área de texto para comentario
        self.comment_text = tk.Text(comment_frame, height=4, width=60, 
                                   font=("Arial", 12), wrap=tk.WORD)
        self.comment_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Botones de comentarios rápidos
        quick_frame = tk.Frame(comment_frame, bg="gray20")
        quick_frame.pack(fill="x", padx=5, pady=5)
        
        quick_comments = [
            "Hola Poncho!", "¿Cómo estás?", "Cuenta un chiste", "Eres gracioso",
            "¿Cuál es mi futuro?", "Dame un acertijo"
        ]
        
        for i, comment in enumerate(quick_comments):
            row = i // 3
            col = i % 3
            tk.Button(quick_frame, text=comment, 
                     command=lambda c=comment: self.set_comment(c),
                     bg="gray", fg="white", font=("Arial", 9)).grid(
                         row=row, column=col, padx=2, pady=2, sticky="ew")
        
        # Configurar grid weights
        for i in range(3):
            quick_frame.grid_columnconfigure(i, weight=1)
        
        # Botón enviar
        send_frame = tk.Frame(manual_frame, bg="black")
        send_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(send_frame, text="📤 ENVIAR COMENTARIO", 
                 command=self.send_comment,
                 bg="green", fg="white", font=("Arial", 14, "bold"),
                 height=2).pack(fill="x")
    
    def setup_gifts_tab(self, notebook):
        """Configurar pestaña de regalos"""
        gifts_frame = tk.Frame(notebook, bg="black")
        notebook.add(gifts_frame, text="🎁 Regalos")
        
        # Sección de usuario para regalos
        user_frame = tk.Frame(gifts_frame, bg="gray20")
        user_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(user_frame, text="Donador:", bg="gray20", fg="gold", 
                font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.gift_username_var = tk.StringVar(value="Donador1")
        gift_username_entry = tk.Entry(user_frame, textvariable=self.gift_username_var, 
                                      font=("Arial", 12), width=20)
        gift_username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(user_frame, text="🎲 Donador Aleatorio", 
                 command=self.random_gift_username,
                 bg="orange", fg="white").grid(row=0, column=2, padx=5, pady=5)
        
        # Sección de selección de regalo
        gift_select_frame = tk.Frame(gifts_frame, bg="gray20")
        gift_select_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(gift_select_frame, text="Seleccionar Regalo:", bg="gray20", fg="gold",
                font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        
        # Grid de botones de regalo
        gifts_grid = tk.Frame(gift_select_frame, bg="gray20")
        gifts_grid.pack(fill="both", expand=True, padx=5, pady=5)
        
        for i, (gift_name, default_qty) in enumerate(self.test_gifts):
            row = i // 3
            col = i % 3
            
            gift_btn = tk.Button(gifts_grid, text=f"{gift_name}\n(x{default_qty})", 
                               command=lambda g=gift_name, q=default_qty: self.send_gift(g, q),
                               bg="gold", fg="black", font=("Arial", 10, "bold"),
                               width=12, height=3)
            gift_btn.grid(row=row, column=col, padx=3, pady=3)
        
        # Configurar grid
        for i in range(3):
            gifts_grid.grid_columnconfigure(i, weight=1)
        
        # Regalo personalizado
        custom_frame = tk.Frame(gifts_frame, bg="gray15")
        custom_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(custom_frame, text="Regalo Personalizado:", bg="gray15", fg="gold",
                font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", padx=5)
        
        tk.Label(custom_frame, text="Nombre:", bg="gray15", fg="white").grid(row=1, column=0, padx=5, pady=2)
        self.custom_gift_var = tk.StringVar()
        tk.Entry(custom_frame, textvariable=self.custom_gift_var, width=15).grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(custom_frame, text="Cantidad:", bg="gray15", fg="white").grid(row=2, column=0, padx=5, pady=2)
        self.custom_qty_var = tk.StringVar(value="1")
        tk.Entry(custom_frame, textvariable=self.custom_qty_var, width=15).grid(row=2, column=1, padx=5, pady=2)
        
        tk.Button(custom_frame, text="🎁 Enviar Regalo Personalizado", 
                 command=self.send_custom_gift,
                 bg="purple", fg="white", font=("Arial", 11, "bold")).grid(row=1, column=2, rowspan=2, padx=5, pady=2)
    
    def setup_auto_tab(self, notebook):
        """Configurar pestaña de modo automático"""
        auto_frame = tk.Frame(notebook, bg="black")
        notebook.add(auto_frame, text="🤖 Automático")
        
        # Configuración
        config_frame = tk.Frame(auto_frame, bg="gray20")
        config_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(config_frame, text="⚙️ CONFIGURACIÓN AUTOMÁTICA", bg="gray20", fg="cyan",
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Intervalo
        interval_frame = tk.Frame(config_frame, bg="gray20")
        interval_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(interval_frame, text="Intervalo (segundos):", bg="gray20", fg="white").pack(side="left")
        self.interval_var = tk.StringVar(value="3")
        tk.Entry(interval_frame, textvariable=self.interval_var, width=10).pack(side="left", padx=10)
        
        # Probabilidades
        prob_frame = tk.Frame(config_frame, bg="gray20")
        prob_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(prob_frame, text="Probabilidad Comentario:", bg="gray20", fg="white").grid(row=0, column=0, sticky="w")
        self.comment_prob_var = tk.StringVar(value="70")
        tk.Entry(prob_frame, textvariable=self.comment_prob_var, width=10).grid(row=0, column=1, padx=5)
        tk.Label(prob_frame, text="%", bg="gray20", fg="white").grid(row=0, column=2, sticky="w")
        
        tk.Label(prob_frame, text="Probabilidad Regalo:", bg="gray20", fg="white").grid(row=1, column=0, sticky="w")
        self.gift_prob_var = tk.StringVar(value="30")
        tk.Entry(prob_frame, textvariable=self.gift_prob_var, width=10).grid(row=1, column=1, padx=5)
        tk.Label(prob_frame, text="%", bg="gray20", fg="white").grid(row=1, column=2, sticky="w")
        
        # Controles
        control_frame = tk.Frame(auto_frame, bg="black")
        control_frame.pack(fill="x", padx=10, pady=20)
        
        self.auto_btn = tk.Button(control_frame, text="▶️ INICIAR AUTOMÁTICO", 
                                 command=self.toggle_auto_mode,
                                 bg="green", fg="white", font=("Arial", 14, "bold"),
                                 height=2)
        self.auto_btn.pack(fill="x")
        
        # Estado
        self.auto_status_label = tk.Label(auto_frame, text="Estado: Detenido", 
                                         bg="black", fg="gray", font=("Arial", 12))
        self.auto_status_label.pack(pady=10)
    
    def setup_quick_tests_tab(self, notebook):
        """Configurar pestaña de pruebas rápidas"""
        quick_frame = tk.Frame(notebook, bg="black")
        notebook.add(quick_frame, text="⚡ Pruebas Rápidas")
        
        tk.Label(quick_frame, text="🚀 PRUEBAS PREDEFINIDAS", bg="black", fg="yellow",
                font=("Arial", 14, "bold")).pack(pady=20)
        
        # Botones de pruebas rápidas
        tests = [
            ("💬 Probar Chat Básico", self.test_basic_chat),
            ("🎁 Lluvia de Regalos", self.test_gift_rain),
            ("🎭 Probar Todos los Modos", self.test_all_modes),
            ("😂 Spam de Chistes", self.test_joke_spam),
            ("🔮 Sesión Clarividente", self.test_fortune_session),
            ("⚡ Estrés Test", self.test_stress)
        ]
        
        for test_name, test_func in tests:
            tk.Button(quick_frame, text=test_name, command=test_func,
                     bg="orange", fg="black", font=("Arial", 12, "bold"),
                     width=25, height=2).pack(pady=5)
    
    def setup_status_panel(self):
        """Configurar panel de estado"""
        status_frame = tk.Frame(self.window, bg="gray15")
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = tk.Label(status_frame, text="🟢 Listo para pruebas", 
                                    bg="gray15", fg="lime", font=("Arial", 11))
        self.status_label.pack(side="left", padx=10)
        
        self.count_label = tk.Label(status_frame, text="Enviados: 0", 
                                   bg="gray15", fg="cyan", font=("Arial", 11))
        self.count_label.pack(side="right", padx=10)
    
    def random_username(self):
        """Generar usuario aleatorio"""
        username = random.choice(self.test_users)
        self.username_var.set(username)
    
    def random_gift_username(self):
        """Generar donador aleatorio"""
        username = random.choice(self.test_users)
        self.gift_username_var.set(username)
    
    def set_comment(self, comment):
        """Establecer comentario en el área de texto"""
        self.comment_text.delete("1.0", tk.END)
        self.comment_text.insert("1.0", comment)
    
    def send_comment(self):
        """Enviar comentario al sistema principal"""
        username = self.username_var.get().strip()
        comment = self.comment_text.get("1.0", tk.END).strip()
        
        if not username or not comment:
            messagebox.showwarning("Advertencia", "Usuario y comentario son requeridos")
            return
        
        try:
            # Enviar al sistema principal
            self.parent_app.handle_comment(username, comment, "comment")
            
            # Registrar en historial
            self.comment_history.append(("comment", username, comment, time.time()))
            self.update_status(f"Comentario enviado: {username}")
            
            # Limpiar comentario
            self.comment_text.delete("1.0", tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error enviando comentario: {e}")
    
    def send_gift(self, gift_name, quantity):
        """Enviar regalo al sistema"""
        username = self.gift_username_var.get().strip()
        
        if not username:
            username = f"Donador{random.randint(1, 100)}"
            self.gift_username_var.set(username)
        
        try:
            gift_info = f"{gift_name} x{quantity}"
            self.parent_app.handle_comment(username, gift_info, "gift")
            
            self.comment_history.append(("gift", username, gift_info, time.time()))
            self.update_status(f"Regalo enviado: {username} -> {gift_info}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error enviando regalo: {e}")
    
    def send_custom_gift(self):
        """Enviar regalo personalizado"""
        username = self.gift_username_var.get().strip()
        gift_name = self.custom_gift_var.get().strip()
        
        if not username or not gift_name:
            messagebox.showwarning("Advertencia", "Usuario y nombre del regalo son requeridos")
            return
        
        try:
            quantity = int(self.custom_qty_var.get() or "1")
        except ValueError:
            quantity = 1
        
        self.send_gift(gift_name, quantity)
        
        # Limpiar campos
        self.custom_gift_var.set("")
        self.custom_qty_var.set("1")
    
    def toggle_auto_mode(self):
        """Alternar modo automático"""
        if self.auto_mode:
            self.stop_auto_mode()
        else:
            self.start_auto_mode()
    
    def start_auto_mode(self):
        """Iniciar modo automático"""
        self.auto_mode = True
        self.auto_btn.config(text="⏹️ DETENER AUTOMÁTICO", bg="red")
        self.auto_status_label.config(text="Estado: Ejecutando", fg="lime")
        
        # Iniciar thread automático
        self.auto_thread = threading.Thread(target=self.auto_loop, daemon=True)
        self.auto_thread.start()
    
    def stop_auto_mode(self):
        """Detener modo automático"""
        self.auto_mode = False
        self.auto_btn.config(text="▶️ INICIAR AUTOMÁTICO", bg="green")
        self.auto_status_label.config(text="Estado: Detenido", fg="gray")
    
    def auto_loop(self):
        """Loop del modo automático"""
        while self.auto_mode:
            try:
                # Obtener configuraciones
                interval = float(self.interval_var.get() or "3")
                comment_prob = int(self.comment_prob_var.get() or "70")
                gift_prob = int(self.gift_prob_var.get() or "30")
                
                # Decidir qué enviar
                rand_num = random.randint(1, 100)
                
                if rand_num <= comment_prob:
                    # Enviar comentario
                    username = random.choice(self.test_users)
                    comment = random.choice(self.test_comments)
                    
                    self.parent_app.root.after(0, 
                        lambda: self.parent_app.handle_comment(username, comment, "comment"))
                    
                    self.parent_app.root.after(0, 
                        lambda: self.update_status(f"Auto: {username} -> {comment}"))
                
                elif rand_num <= comment_prob + gift_prob:
                    # Enviar regalo
                    username = random.choice(self.test_users)
                    gift_name, quantity = random.choice(self.test_gifts)
                    gift_info = f"{gift_name} x{quantity}"
                    
                    self.parent_app.root.after(0, 
                        lambda: self.parent_app.handle_comment(username, gift_info, "gift"))
                    
                    self.parent_app.root.after(0, 
                        lambda: self.update_status(f"Auto Regalo: {username} -> {gift_info}"))
                
                # Esperar
                time.sleep(interval)
                
            except Exception as e:
                print(f"Error en modo automático: {e}")
                time.sleep(1)
    
    def update_status(self, message):
        """Actualizar estado"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"🟢 {message}")
            self.count_label.config(text=f"Enviados: {len(self.comment_history)}")
    
    # Pruebas rápidas predefinidas
    def test_basic_chat(self):
        """Probar chat básico"""
        comments = [
            ("Juan", "Hola Poncho"),
            ("Ana", "¿Cómo estás?"),
            ("Pedro", "Cuenta algo gracioso"),
            ("Luis", "¿Qué opinas de la vida?")
        ]
        
        self.execute_test_sequence(comments, "Probando chat básico...")
    
    def test_gift_rain(self):
        """Probar lluvia de regalos"""
        gifts = []
        for i in range(8):
            username = random.choice(self.test_users)
            gift_name, quantity = random.choice(self.test_gifts)
            gifts.append((username, f"{gift_name} x{quantity}", "gift"))
        
        self.execute_test_sequence(gifts, "Lluvia de regalos...", 0.5)
    
    def test_all_modes(self):
        """Probar todos los modos"""
        mode_tests = [
            ("TestUser", "Hola modo chat", "comment"),
            ("TestUser", "Cuenta un chiste", "comment"),
            ("TestUser", "¿Cuál es mi futuro?", "comment"),
            ("TestUser", "Dame un acertijo", "comment"),
            ("TestUser", "Me das miedo", "comment"),
            ("TestUser", "Canta algo", "comment"),
            ("TestUser", "iniciar conversación", "comment"),
            ("TestUser", "iniciar entrevista TestUser", "comment")
        ]
        
        self.execute_test_sequence(mode_tests, "Probando todos los modos...", 2.0)
    
    def test_joke_spam(self):
        """Probar spam de solicitudes de chistes"""
        jokes = [("User" + str(i), "Cuenta un chiste", "comment") for i in range(5)]
        self.execute_test_sequence(jokes, "Spam de chistes...", 1.0)
    
    def test_fortune_session(self):
        """Probar sesión de clarividente"""
        fortune_comments = [
            ("Creyente1", "¿Cuál es mi futuro?"),
            ("Escéptico", "No creo en esas cosas"),
            ("Curioso", "¿Qué me depara el destino?"),
            ("Romántico", "¿Encontraré el amor?"),
            ("Ambicioso", "¿Tendré éxito?")
        ]
        
        comments = [(user, comment, "comment") for user, comment in fortune_comments]
        self.execute_test_sequence(comments, "Sesión clarividente...", 1.5)
    
    def test_stress(self):
        """Prueba de estrés con muchos comentarios"""
        stress_comments = []
        for i in range(20):
            username = f"User{i}"
            comment = random.choice(self.test_comments)
            stress_comments.append((username, comment, "comment"))
        
        self.execute_test_sequence(stress_comments, "Prueba de estrés...", 0.2)
    
    def execute_test_sequence(self, sequence, description, delay=1.0):
        """Ejecutar secuencia de prueba"""
        self.update_status(description)
        
        def run_sequence():
            for username, content, msg_type in sequence:
                if not hasattr(self, 'window') or not self.window.winfo_exists():
                    break
                
                self.parent_app.root.after(0, 
                    lambda u=username, c=content, t=msg_type: self.parent_app.handle_comment(u, c, t))
                
                time.sleep(delay)
            
            if hasattr(self, 'window') and self.window.winfo_exists():
                self.parent_app.root.after(0, lambda: self.update_status("Prueba completada"))
        
        threading.Thread(target=run_sequence, daemon=True).start()

# Integración con el sistema principal
def add_test_window_to_gui(gui_class):
    """Agregar botón de ventana de pruebas a la GUI"""
    
    original_setup_quick_controls = gui_class.setup_quick_controls
    
    def enhanced_setup_quick_controls(self, parent):
        # Llamar al setup original
        original_setup_quick_controls(self, parent)
        
        # Agregar botón de pruebas
        if hasattr(self.mode_controller, 'parent_app') or hasattr(self, 'parent_app'):
            parent_app = getattr(self.mode_controller, 'parent_app', None) or getattr(self, 'parent_app', None)
            
            if parent_app:
                test_btn = tk.Button(parent, text="🧪 VENTANA PRUEBAS", 
                                   command=lambda: TestWindowManager(parent_app).show_test_window(),
                                   bg="purple", fg="white", font=("Arial", 10, "bold"),
                                   width=15, height=1)
                test_btn.pack(pady=2)
    
    gui_class.setup_quick_controls = enhanced_setup_quick_controls

# Ejemplo de uso
if __name__ == "__main__":
    print("🧪 Test Window Manager - Simulador independiente")
    print("Este módulo se integra con el sistema principal")
    
    # Crear ventana de prueba independiente (solo para testing)
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    # Mock app para testing
    class MockApp:
        def __init__(self):
            self.root = root
            
        def handle_comment(self, username, comment, msg_type):
            print(f"📤 {msg_type.upper()}: {username} -> {comment}")
    
    mock_app = MockApp()
    test_manager = TestWindowManager(mock_app)
    test_manager.show_test_window()
    
    print("✅ Ventana de pruebas abierta - Cierra la ventana para terminar")
    root.mainloop()