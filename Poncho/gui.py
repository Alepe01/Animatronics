import tkinter as tk
from tkinter import scrolledtext, messagebox
import time

class ModeControlWindow:
    def __init__(self, parent, callback):
        self.callback = callback
        self.window = tk.Toplevel(parent)
        self.window.title("Control de Modo - Poncho")
        self.window.configure(bg="black")
        self.window.geometry("500x500")
        self.window.resizable(False, False)
        
        # Título
        title_label = tk.Label(self.window, text="🤖 CONTROL DE MODO 🤖", 
                              bg="black", fg="cyan", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Frame para botones
        buttons_frame = tk.Frame(self.window, bg="black")
        buttons_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        # Botón Modo 1: Solo Chat
        self.btn_chat = tk.Button(buttons_frame, text="1️⃣ CONVERSACIÓN CON CHAT", 
                                 command=lambda: self.set_mode(1),
                                 bg="green", fg="white", font=("Arial", 10, "bold"),
                                 height=2, relief="raised", bd=3)
        self.btn_chat.pack(fill="x", pady=5)
        
        # Botón Modo 2: Chat + Audio
        self.btn_audio = tk.Button(buttons_frame, text="2️⃣ CHAT + AUDIO DEL SISTEMA", 
                                  command=lambda: self.set_mode(2),
                                  bg="blue", fg="white", font=("Arial", 10, "bold"),
                                  height=2, relief="raised", bd=3)
        self.btn_audio.pack(fill="x", pady=5)
        
        # Botón Modo 3: Chistes
        self.btn_chistes = tk.Button(buttons_frame, text="3️⃣ CONTAR CHISTE", 
                                    command=lambda: self.set_mode(3),
                                    bg="purple", fg="white", font=("Arial", 10, "bold"),
                                    height=2, relief="raised", bd=3)
        self.btn_chistes.pack(fill="x", pady=5)
        
        # Botón Modo 4: Cantante
        self.btn_cantante = tk.Button(buttons_frame, text="4️⃣ MODO CANTANTE", 
                                     command=lambda: self.set_mode(4),
                                     bg="orange", fg="white", font=("Arial", 10, "bold"),
                                     height=2, relief="raised", bd=3)
        self.btn_cantante.pack(fill="x", pady=5)
        
        # Botón Modo 5: Clarividente
        self.btn_clarividente = tk.Button(buttons_frame, text="5️⃣ CLARIVIDENTE", 
                                         command=lambda: self.set_mode(5),
                                         bg="violet", fg="white", font=("Arial", 10, "bold"),
                                         height=2, relief="raised", bd=3)
        self.btn_clarividente.pack(fill="x", pady=5)
        
        # Botón Modo 6: Acertijos
        self.btn_acertijo = tk.Button(buttons_frame, text="6️⃣ ACERTIJOS", 
                                     command=lambda: self.set_mode(6),
                                     bg="brown", fg="white", font=("Arial", 10, "bold"),
                                     height=2, relief="raised", bd=3)
        self.btn_acertijo.pack(fill="x", pady=5)
        
        # Botón Modo 7: Amenazas
        self.btn_amenazas = tk.Button(buttons_frame, text="7️⃣ MODO TERRORÍFICO", 
                                     command=lambda: self.set_mode(7),
                                     bg="darkred", fg="white", font=("Arial", 10, "bold"),
                                     height=2, relief="raised", bd=3)
        self.btn_amenazas.pack(fill="x", pady=5)
        
        # Label de estado actual
        self.status_label = tk.Label(self.window, text="Modo Actual: Conversación con Chat", 
                                    bg="black", fg="yellow", font=("Arial", 10))
        self.status_label.pack(pady=10)
        
        self.update_button_states()
    
    def set_mode(self, mode):
        global current_mode
        current_mode = mode
        self.callback(mode)
        self.update_button_states()
        
        mode_names = {
            1: "Conversación con Chat",
            2: "Chat + Audio del Sistema", 
            3: "Contar Chiste",
            4: "Modo Cantante",
            5: "Clarividente",
            6: "Acertijos",
            7: "Modo Terrorífico"
        }
        self.status_label.config(text=f"Modo Actual: {mode_names[mode]}")
    
    def update_button_states(self):
        # Resetear colores
        buttons = [
            (self.btn_chat, "green"),
            (self.btn_audio, "blue"), 
            (self.btn_chistes, "purple"),
            (self.btn_cantante, "orange"),
            (self.btn_clarividente, "violet"),
            (self.btn_acertijo, "brown"),
            (self.btn_amenazas, "darkred")
        ]
        
        for btn, color in buttons:
            btn.config(bg=color)
        
        # Resaltar botón activo
        active_colors = {
            1: (self.btn_chat, "lime"),
            2: (self.btn_audio, "cyan"),
            3: (self.btn_chistes, "magenta"),
            4: (self.btn_cantante, "gold"),
            5: (self.btn_clarividente, "pink"),
            6: (self.btn_acertijo, "tan"),
            7: (self.btn_amenazas, "red")
        }
        
        if current_mode in active_colors:
            btn, color = active_colors[current_mode]
            btn.config(bg=color)

class TikTokNPCGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok NPC - Poncho el Payaso")
        self.root.configure(bg="black")
        self.root.geometry("1200x800")
        
        self.mode_window = None
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="black")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título principal
        title_label = tk.Label(main_frame, text="🤡 PONCHO EL PAYASO 🤡", 
                              bg="black", fg="red", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Frame de botones de control
        control_frame = tk.Frame(main_frame, bg="black")
        control_frame.pack(pady=5)
        
        # Botón para abrir control de modo
        control_btn = tk.Button(control_frame, text="🎛️ CONTROL DE MODO", 
                               command=self.open_mode_control,
                               bg="orange", fg="black", font=("Arial", 12, "bold"),
                               relief="raised", bd=3)
        control_btn.pack(side="left", padx=5)
        
        # Botón para configurar audio
        audio_btn = tk.Button(control_frame, text="🔊 CONFIGURAR AUDIO", 
                             command=self.open_audio_config,
                             bg="cyan", fg="black", font=("Arial", 12, "bold"),
                             relief="raised", bd=3)
        audio_btn.pack(side="left", padx=5)
        
        # SECCIÓN DE COMENTARIOS
        comments_frame = tk.Frame(main_frame, bg="black")
        comments_frame.pack(fill="both", expand=True, pady=(10, 10))
        
        tk.Label(comments_frame, text="💬 COMENTARIOS RECIENTES:", 
                bg="black", fg="lime", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.comments_text = scrolledtext.ScrolledText(comments_frame, width=120, height=15,
                                                      bg="gray10", fg="white", 
                                                      font=("Consolas", 11), wrap=tk.WORD,
                                                      insertbackground="white")
        self.comments_text.pack(fill="both", expand=True)
        
        # SECCIÓN DE RESPUESTAS
        response_frame = tk.Frame(main_frame, bg="black")
        response_frame.pack(fill="both", expand=True)
        
        tk.Label(response_frame, text="🗣️ RESPUESTA DE PONCHO:", 
                bg="black", fg="yellow", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.response_text = scrolledtext.ScrolledText(response_frame, width=120, height=8,
                                                      bg="gray20", fg="yellow", 
                                                      font=("Arial", 13, "bold"), wrap=tk.WORD,
                                                      insertbackground="yellow")
        self.response_text.pack(fill="both", expand=True)
    
    def open_mode_control(self):
        """Abrir ventana de control de modo"""
        if self.mode_window is None or not self.mode_window.window.winfo_exists():
            self.mode_window = ModeControlWindow(self.root, self.on_mode_change)
        else:
            self.mode_window.window.lift()
    
    def on_mode_change(self, mode):
        """Callback para cambio de modo - debe ser implementado por la clase principal"""
        pass
    
    def open_audio_config(self):
        """Abrir ventana de configuración de audio"""
        audio_window = tk.Toplevel(self.root)
        audio_window.title("Configuración de Audio")
        audio_window.configure(bg="black")
        audio_window.geometry("600x400")
        audio_window.resizable(False, False)
        
        # Título
        title_label = tk.Label(audio_window, text="🔊 CONFIGURACIÓN DE AUDIO 🔊", 
                              bg="black", fg="cyan", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Información
        info_label = tk.Label(audio_window, 
                             text="Para capturar audio de YouTube/videos, selecciona 'Mezcla Estéreo'", 
                             bg="black", fg="yellow", font=("Arial", 10))
        info_label.pack(pady=5)
        
        # Lista de dispositivos
        devices_frame = tk.Frame(audio_window, bg="black")
        devices_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(devices_frame, text="Dispositivos disponibles:", 
                bg="black", fg="white", font=("Arial", 12, "bold")).pack(anchor="w")
        
        devices_listbox = tk.Listbox(devices_frame, bg="gray20", fg="white", 
                                    font=("Arial", 10), height=8)
        devices_listbox.pack(fill="both", expand=True, pady=5)
        
        # Llenar lista de dispositivos
        try:
            import speech_recognition as sr
            devices = sr.Microphone.list_microphone_names()
            for i, device in enumerate(devices):
                marker = "🔊" if any(k in device.lower() for k in ['stereo', 'mezcla', 'mix', 'loopback']) else "🎤"
                devices_listbox.insert(tk.END, f"{i}: {marker} {device}")
        except:
            devices_listbox.insert(tk.END, "Error cargando dispositivos")
        
        # Botones
        buttons_frame = tk.Frame(audio_window, bg="black")
        buttons_frame.pack(pady=10)
        
        def select_device():
            try:
                selection = devices_listbox.curselection()
                if selection and hasattr(self, 'audio_listener'):
                    device_index = selection[0]
                    if self.audio_listener.select_audio_device(device_index):
                        self.add_system_message(f"🔊 Dispositivo cambiado: {devices[device_index]}")
                    else:
                        self.add_system_message("❌ Error cambiando dispositivo")
            except Exception as e:
                self.add_system_message(f"❌ Error: {e}")
        
        def find_stereo():
            if hasattr(self, 'audio_listener'):
                if self.audio_listener.find_stereo_mix():
                    self.add_system_message("🔊 Mezcla Estéreo configurada correctamente")
                else:
                    self.add_system_message("❌ No se encontró Mezcla Estéreo")
        
        def test_current():
            self.add_system_message("🧪 Probando dispositivo actual...")
            if hasattr(self, 'audio_listener'):
                if self.audio_listener.test_microphone():
                    self.add_system_message("✅ Dispositivo funcionando correctamente")
                else:
                    self.add_system_message("❌ Dispositivo no funciona o sin audio")
        
        tk.Button(buttons_frame, text="✅ USAR SELECCIONADO", command=select_device,
                 bg="green", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        tk.Button(buttons_frame, text="🔊 BUSCAR AUDIO INTERNO", command=find_stereo,
                 bg="blue", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        tk.Button(buttons_frame, text="🧪 PROBAR ACTUAL", command=test_current,
                 bg="purple", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
    
    def add_comment(self, username, comment, msg_type):
        """Agregar comentario a la ventana"""
        self.comments_text.config(state=tk.NORMAL)
        
        timestamp = time.strftime("%H:%M:%S")
        if msg_type == "gift":
            formatted_comment = f"[{timestamp}] 🎁 [REGALO REAL] {username}: {comment}\n"
            self.comments_text.insert(tk.END, formatted_comment)
            self.comments_text.tag_add("real_gift", f"end-2l linestart", f"end-2l lineend")
            self.comments_text.tag_config("real_gift", foreground="#00ff00", font=("Consolas", 11, "bold"))
        elif msg_type == "audio":
            formatted_comment = f"[{timestamp}] 🎤 [AUDIO] {username}: {comment}\n"
            self.comments_text.insert(tk.END, formatted_comment)
            self.comments_text.tag_add("audio", f"end-2l linestart", f"end-2l lineend")
            self.comments_text.tag_config("audio", foreground="#00ffff", font=("Consolas", 11, "bold"))
        else:
            formatted_comment = f"[{timestamp}] 💬 [COMENTARIO] {username}: {comment}\n"
            self.comments_text.insert(tk.END, formatted_comment)
            self.comments_text.tag_add("comment", f"end-2l linestart", f"end-2l lineend")
            self.comments_text.tag_config("comment", foreground="white")
        
        self.comments_text.see(tk.END)
        self.comments_text.config(state=tk.DISABLED)
    
    def add_system_message(self, message):
        """Agregar mensaje del sistema"""
        self.comments_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] ⚙️ [SISTEMA] {message}\n"
        self.comments_text.insert(tk.END, formatted_message)
        self.comments_text.tag_add("system", f"end-2l linestart", f"end-2l lineend")
        self.comments_text.tag_config("system", foreground="#ff6600", font=("Consolas", 11, "bold"))
        self.comments_text.see(tk.END)
        self.comments_text.config(state=tk.DISABLED)
    
    def update_response(self, text):
        """Actualizar respuesta de Poncho"""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        
        timestamp = time.strftime("%H:%M:%S")
        response_with_time = f"[{timestamp}] {text}"
        
        self.response_text.insert(tk.END, response_with_time)
        self.response_text.config(state=tk.DISABLED)