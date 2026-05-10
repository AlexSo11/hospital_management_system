"""
Equipo 6

LISTA DE INTEGRANTES (ordenados alfabéticamente por apellidos)
Rizzoli Domínguez Carlos Daniel
Rodriguez Macias Juan Diego
Solís Quiñones Héctor Alejandro
Solís Regín Juan Pablo
Vazquez Delgado Kevin
Verduzco Rosales Luis Enrique

Materia: Bases de Datos
Clave: IL356          Sección: D02
NRC: 204855                 2025 B

NOMBRE DEL PROFESOR:  Mariscal Lugo Luis Felipe
"""
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from dbConfigXAMPP import obtener_conexion, liberar_conexion

class LoginWindow:
    def __init__(self, parent, callback_exito):
        print("Creando ventana de login...")
        self.callback_exito = callback_exito
        self.nombre_doctor = None  # Para guardar el nombre completo del doctor
        
        try:
            self.ventana = tk.Toplevel(parent)
            self.ventana.title("Login - Núcleo de Diagnóstico")
            self.ventana.geometry("500x600")
            self.ventana.resizable(False, False)
            
            # Configurar para que se cierre correctamente
            self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
            
            print("✓ Ventana Toplevel creada")
            
            # Centrar ventana
            self.centrar_ventana()
            
            # Crear interfaz
            self.crear_widgets()
            
            # Hacer modal
            self.ventana.transient(parent)
            self.ventana.grab_set()
            
            # Asegurar que la ventana se muestre
            self.ventana.deiconify()
            self.ventana.lift()
            self.ventana.focus_force()
            
            print("✓ Ventana de login lista")
            
        except Exception as e:
            print(f"✗ Error creando ventana de login: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def cerrar_ventana(self):
        """Cierra la ventana de login"""
        import sys
        self.ventana.destroy()
        sys.exit(0)
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        width = 500
        height = 600
        x = (self.ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (height // 2)
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')
        
    def crear_widgets(self):
        """Crea los widgets de la interfaz con diseño moderno"""
        try:
            # Cargar imagen
            fondo = Image.open("fondo1.jpg")
            
            # Redimensionar manteniendo aspecto
            fondo = fondo.resize((500, 600), Image.Resampling.LANCZOS)
            
            # Aplicar desenfoque para efecto blur
            fondo = fondo.filter(ImageFilter.GaussianBlur(radius=3))
            
            # Oscurecer la imagen para mejor contraste
            enhancer = ImageEnhance.Brightness(fondo)
            fondo = enhancer.enhance(0.5)  # 0.5 = 50% más oscuro
            
            # Convertir a PhotoImage
            self.fondo_img = ImageTk.PhotoImage(fondo)
            
            # Colocar fondo
            fondo_label = tk.Label(self.ventana, image=self.fondo_img)
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            print("✓ Imagen de fondo cargada")
            
        except FileNotFoundError:
            print("Archivo fondo.jpg no encontrado, usando fondo sólido")
            # Fondo alternativo degradado
            self.ventana.configure(bg="#1a1a2e")
            fondo_label = tk.Label(self.ventana, bg="#1a1a2e")
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            self.ventana.configure(bg="#1a1a2e")
        
        # === CONTENEDOR PRINCIPAL SEMI-TRANSPARENTE ===
        # Frame contenedor con efecto de tarjeta
        main_container = tk.Frame(
            self.ventana,
            bg="#ffffff",
            bd=0,
            highlightthickness=0
        )
        main_container.place(relx=0.5, rely=0.5, anchor="center", width=360, height=420)
        
        # Borde sutil para dar profundidad
        border_frame = tk.Frame(
            self.ventana,
            bg="#d1d5db",
            bd=0
        )
        border_frame.place(relx=0.5, rely=0.5, anchor="center", width=361, height=421)
        border_frame.lower()
        main_container.lift()
        
        # === CONTENIDO DEL FORMULARIO ===
        content_frame = tk.Frame(main_container, bg="#ffffff")
        content_frame.pack(expand=True, fill="both", padx=40, pady=30)
        
        # Título
        titulo = tk.Label(
            content_frame,
            text="Sistema de Gestión",
            font=("Arial", 20, "bold"),
            fg="#2c3e50",
            bg="#ffffff"
        )
        titulo.pack(pady=(0, 5))
        
        # Subtítulo
        subtitulo = tk.Label(
            content_frame,
            text="Núcleo de Diagnóstico",
            font=("Arial", 12),
            fg="#7f8c8d",
            bg="#ffffff"
        )
        subtitulo.pack(pady=(0, 30))
        
        # === CAMPO USUARIO ===
        usuario_label = tk.Label(
            content_frame,
            text="Usuario",
            font=("Arial", 10, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
            anchor="w"
        )
        usuario_label.pack(fill="x", pady=(0, 5))
        
        # Frame para el entry con borde personalizado
        usuario_frame = tk.Frame(
            content_frame,
            bg="#e8e8e8",
            bd=0,
            highlightbackground="#bdc3c7",
            highlightthickness=1
        )
        usuario_frame.pack(fill="x", pady=(0, 20))
        
        self.entry_usuario = tk.Entry(
            usuario_frame,
            font=("Arial", 11),
            bg="#ffffff",
            fg="#2c3e50",
            bd=0,
            insertbackground="#3498db"
        )
        self.entry_usuario.pack(fill="x", padx=10, pady=8, ipady=5)
        self.entry_usuario.focus()
        
        # === CAMPO CONTRASEÑA ===
        password_label = tk.Label(
            content_frame,
            text="Contraseña",
            font=("Arial", 10, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, 5))
        
        # Frame para el entry con borde personalizado
        password_frame = tk.Frame(
            content_frame,
            bg="#e8e8e8",
            bd=0,
            highlightbackground="#bdc3c7",
            highlightthickness=1
        )
        password_frame.pack(fill="x", pady=(0, 30))
        
        self.entry_password = tk.Entry(
            password_frame,
            font=("Arial", 11),
            bg="#ffffff",
            fg="#2c3e50",
            bd=0,
            show="●",  # Usar círculo en lugar de asterisco
            insertbackground="#3498db"
        )
        self.entry_password.pack(fill="x", padx=10, pady=8, ipady=5)
        
        # === BOTÓN DE LOGIN ===
        btn_login = tk.Button(
            content_frame,
            text="Iniciar Sesión",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="#ffffff",
            activebackground="#20618b",
            activeforeground="#ffffff",
            bd=0,
            cursor="hand2",
            command=self.iniciar_sesion
        )
        btn_login.pack(fill="x", ipady=12)
        
        # Efecto hover en el botón
        def on_enter(e):
            btn_login['bg'] = '#2980b9'
        
        def on_leave(e):
            btn_login['bg'] = '#3498db'
        
        btn_login.bind("<Enter>", on_enter)
        btn_login.bind("<Leave>", on_leave)
        
        # === FOOTER ===
        footer = tk.Label(
            content_frame,
            text="v1.0 - 2025",
            font=("Arial", 8),
            fg="#95a5a6",
            bg="#ffffff"
        )
        footer.pack(side="bottom", pady=(20, 0))
        
        # === BINDINGS DE TECLADO ===
        self.entry_password.bind('<Return>', lambda e: self.iniciar_sesion())
        self.entry_usuario.bind('<Return>', lambda e: self.entry_password.focus())
        
        # Focus effect para los entry
        def focus_in_usuario(e):
            usuario_frame.config(highlightbackground="#3498db", highlightthickness=2)
        
        def focus_out_usuario(e):
            usuario_frame.config(highlightbackground="#bdc3c7", highlightthickness=1)
        
        def focus_in_password(e):
            password_frame.config(highlightbackground="#3498db", highlightthickness=2)
        
        def focus_out_password(e):
            password_frame.config(highlightbackground="#bdc3c7", highlightthickness=1)
        
        self.entry_usuario.bind("<FocusIn>", focus_in_usuario)
        self.entry_usuario.bind("<FocusOut>", focus_out_usuario)
        self.entry_password.bind("<FocusIn>", focus_in_password)
        self.entry_password.bind("<FocusOut>", focus_out_password)
        
    def iniciar_sesion(self):
        """Valida las credenciales e inicia sesión"""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        print(f"Intentando login: usuario='{usuario}'")
        
        if not usuario or not password:
            messagebox.showwarning(
                "Advertencia", 
                "Por favor ingrese usuario y contraseña",
                parent=self.ventana
            )
            return
        
        # Validar credenciales
        tipo_usuario = self.validar_credenciales(usuario, password)
        
        if tipo_usuario:
            print(f"✓ Credenciales válidas: {tipo_usuario}")
            # Si es doctor, pasar el nombre completo en lugar del usuario
            nombre_a_pasar = self.nombre_doctor if tipo_usuario == "doctor" else usuario
            messagebox.showinfo(
                "Éxito", 
                f"Bienvenido {nombre_a_pasar}",
                parent=self.ventana
            )
            self.ventana.destroy()
            self.callback_exito(nombre_a_pasar, tipo_usuario)
        else:
            print("✗ Credenciales inválidas")
            messagebox.showerror(
                "Error", 
                "Usuario o contraseña incorrectos",
                parent=self.ventana
            )
            self.entry_password.delete(0, tk.END)
            self.entry_password.focus()
    
    def validar_credenciales(self, usuario, password):
        """
        Valida las credenciales contra la base de datos
        Retorna el tipo de usuario si es válido, None si no
        """
        conexion = obtener_conexion()
        if not conexion:
            print("✗ No se pudo obtener conexión")
            return None
        
        try:
            cursor = conexion.cursor()
            
            # Buscar en tabla administrador
            print("Buscando en tabla administrador...")
            cursor.execute(
                "SELECT contrasena FROM administrador WHERE usuario = %s",
                (usuario,)
            )
            resultado = cursor.fetchone()
            
            if resultado:
                print(f"Usuario encontrado en administrador")
                if resultado[0] == password:
                    cursor.close()
                    return "administrador"
                else:
                    print("Contraseña incorrecta")
            
            # Buscar en tabla empleados
            print("Buscando en tabla empleados...")
            cursor.execute(
                "SELECT contrasena FROM empleados WHERE usuario = %s",
                (usuario,)
            )
            resultado = cursor.fetchone()
            
            if resultado:
                print(f"Usuario encontrado en empleados")
                if resultado[0] == password:
                    cursor.close()
                    return "empleado"
                else:
                    print("Contraseña incorrecta")
            
            # Buscar en tabla doctores - AQUÍ OBTENER EL NOMBRE COMPLETO
            print("Buscando en tabla doctores...")
            cursor.execute(
                "SELECT contrasena, nombre FROM doctores WHERE usuario = %s",
                (usuario,)
            )
            resultado = cursor.fetchone()
            
            if resultado:
                print(f"Usuario encontrado en doctores")
                if resultado[0] == password:
                    # Guardar el nombre completo del doctor
                    self.nombre_doctor = resultado[1]
                    cursor.close()
                    return "doctor"
                else:
                    print("Contraseña incorrecta")
            
            print(f"Usuario '{usuario}' no encontrado en ninguna tabla")
            cursor.close()
            return None
            
        except Exception as e:
            print(f"✗ Error al validar credenciales: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                "Error", 
                f"Error al validar credenciales:\n{str(e)}",
                parent=self.ventana
            )
            return None
        finally:
            liberar_conexion(conexion)