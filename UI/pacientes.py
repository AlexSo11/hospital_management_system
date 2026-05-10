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
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from DB_XAMPP.dbPacientes import DBPacientes
from datetime import datetime

class UIPacientes:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Pacientes - Sistema Hospitalario")
        self.ventana.geometry("1040x700")
        self.ventana.configure(bg='#f0f8ff')
        self.ventana.resizable(True, True)
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Crear interfaz
        self.crear_widgets()
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        width = 1040
        height = 700
        x = (self.ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (height // 2)
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')
        
    def crear_widgets(self):
        """Crea los widgets de la interfaz con nuevo diseño"""
        
        # Header médico
        header_frame = tk.Frame(self.ventana, bg='#0077be', height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="GESTIÓN DE PACIENTES",
            font=("Arial", 16, "bold"),
            bg='#0077be',
            fg='white'
        ).pack(expand=True)
        
        tk.Label(
            header_frame,
            text="Sistema de Registro y Consulta de Pacientes",
            font=("Arial", 10),
            bg='#0077be',
            fg='#e0f0ff'
        ).pack(pady=(0, 10))
        
        # Frame principal
        main_frame = tk.Frame(self.ventana, bg='#f0f8ff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Frame principal con notebook (pestañas)
        notebook_frame = tk.Frame(main_frame, bg='#f0f8ff')
        notebook_frame.pack(fill='both', expand=True)
        
        # Style configuration
        style = ttk.Style()
        style.configure('Custom.TNotebook', background='#f0f8ff', borderwidth=0)
        style.configure('Custom.TNotebook.Tab', padding=[15, 5], font=('Arial', 10, 'bold'))
        
        self.notebook = ttk.Notebook(notebook_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña 1: Insertar Paciente
        self.frame_insertar = tk.Frame(self.notebook, bg='#ffffff', relief='flat', bd=1)
        self.notebook.add(self.frame_insertar, text="Registrar Paciente")
        self.crear_formulario_insertar()
        
        # Pestaña 2: Consultas Generales
        self.frame_consultas = tk.Frame(self.notebook, bg='#ffffff', relief='flat', bd=1)
        self.notebook.add(self.frame_consultas, text="Listado de Pacientes")
        self.crear_tabla_consultas()
        
    def crear_formulario_insertar(self):
        """Crea el formulario para insertar paciente con nuevo diseño"""
        # Frame principal del formulario
        form_container = tk.Frame(self.frame_insertar, bg='#ffffff')
        form_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Título
        titulo = tk.Label(
            form_container,
            text="Registro de Nuevo Paciente",
            font=("Arial", 16, "bold"),
            bg='#ffffff',
            fg='#0077be'
        )
        titulo.pack(pady=(0, 25))
        
        # Frame para campos del formulario (2 columnas)
        campos_frame = tk.Frame(form_container, bg='#ffffff')
        campos_frame.pack(fill='both', expand=True)
        
        # Columna izquierda
        left_frame = tk.Frame(campos_frame, bg='#ffffff')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Columna derecha
        right_frame = tk.Frame(campos_frame, bg='#ffffff')
        right_frame.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        # Función para crear campos con estilo
        def crear_campo(parent, label_text, widget, es_obligatorio=False):
            # Frame para cada campo
            campo_frame = tk.Frame(parent, bg='#ffffff')
            campo_frame.pack(fill='x', pady=8)
            
            # Label
            label_text = label_text + (" *" if es_obligatorio else "")
            lbl = tk.Label(
                campo_frame,
                text=label_text,
                font=("Arial", 10, "bold" if es_obligatorio else "normal"),
                bg='#ffffff',
                fg='#2c3e50' if es_obligatorio else '#34495e',
                anchor='w'
            )
            lbl.pack(fill='x', pady=(0, 5))
            
            # Widget
            widget.pack(fill='x', pady=2)
            
        # Configurar estilo para entries
        style = ttk.Style()
        style.configure('Custom.TEntry', padding=8, relief='flat', borderwidth=1)
        
        # Campos columna izquierda
        self.entry_nombre = ttk.Entry(left_frame, font=("Arial", 10))
        crear_campo(left_frame, "Nombre Completo", self.entry_nombre, True)
        
        self.entry_direccion = ttk.Entry(left_frame, font=("Arial", 10))
        crear_campo(left_frame, "Dirección", self.entry_direccion)
        
        self.entry_telefono = ttk.Entry(left_frame, font=("Arial", 10))
        crear_campo(left_frame, "Teléfono", self.entry_telefono)
        
        # Fecha de Nacimiento con calendario
        fecha_frame = tk.Frame(left_frame, bg='#ffffff')
        fecha_frame.pack(fill='x', pady=8)
        
        tk.Label(
            fecha_frame,
            text="Fecha de Nacimiento *",
            font=("Arial", 10, "bold"),
            bg='#ffffff',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.entry_fecha_nac = DateEntry(
            fecha_frame,
            font=("Arial", 10),
            width=30,
            background='#0077be',
            foreground='white',
            borderwidth=1,
            date_pattern='yyyy-mm-dd',
            maxdate=datetime.now(),
            mindate=datetime(1900, 1, 1)
        )
        self.entry_fecha_nac.pack(fill='x', pady=2)
        
        # Campos columna derecha
        self.combo_sexo = ttk.Combobox(
            right_frame,
            values=["Masculino", "Femenino", "Otro"],
            state="readonly",
            font=("Arial", 10)
        )
        self.combo_sexo.current(0)
        crear_campo(right_frame, "Sexo", self.combo_sexo, True)
        
        self.entry_edad = ttk.Entry(right_frame, font=("Arial", 10))
        crear_campo(right_frame, "Edad (años)", self.entry_edad, True)
        
        self.entry_estatura = ttk.Entry(right_frame, font=("Arial", 10))
        crear_campo(right_frame, "Estatura (metros)", self.entry_estatura, True)
        
        # Nota de campos obligatorios
        nota_frame = tk.Frame(campos_frame, bg='#ffffff')
        nota_frame.pack(fill='x', pady=(20, 0))
        
        tk.Label(
            nota_frame,
            text="* Campos obligatorios",
            font=("Arial", 9, "italic"),
            bg='#ffffff',
            fg='#e74c3c'
        ).pack()
        
        # Frame para botones
        botones_frame = tk.Frame(form_container, bg='#ffffff')
        botones_frame.pack(pady=30)
        
        # Botón Guardar
        btn_guardar = tk.Button(
            botones_frame,
            text="Guardar Paciente",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#219a52",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.guardar_paciente,
            padx=25,
            pady=10,
            relief="flat"
        )
        btn_guardar.pack(side='left', padx=10)
        
        # Efecto hover guardar
        btn_guardar.bind("<Enter>", lambda e: btn_guardar.config(bg="#219a52"))
        btn_guardar.bind("<Leave>", lambda e: btn_guardar.config(bg="#27ae60"))
        
        # Botón Limpiar
        btn_limpiar = tk.Button(
            botones_frame,
            text="🗑️ Limpiar Campos",
            font=("Arial", 11, "bold"),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.limpiar_campos,
            padx=25,
            pady=10,
            relief="flat"
        )
        btn_limpiar.pack(side='left', padx=10)
        
        # Efecto hover limpiar
        btn_limpiar.bind("<Enter>", lambda e: btn_limpiar.config(bg="#d35400"))
        btn_limpiar.bind("<Leave>", lambda e: btn_limpiar.config(bg="#e67e22"))
        
    def crear_tabla_consultas(self):
        """Crea la tabla para mostrar todos los pacientes con nuevo diseño"""
        # Frame principal
        main_frame = tk.Frame(self.frame_consultas, bg='#ffffff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="Listado de Pacientes Registrados",
            font=("Arial", 16, "bold"),
            bg='#ffffff',
            fg='#0077be'
        )
        titulo.pack(pady=(0, 15))
        
        # Frame para controles
        controles_frame = tk.Frame(main_frame, bg='#ffffff')
        controles_frame.pack(fill='x', pady=(0, 15))
        
        # Botón Actualizar
        btn_actualizar = tk.Button(
            controles_frame,
            text="🔄 Actualizar Listado",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.cargar_pacientes,
            padx=15,
            pady=6,
            relief="flat"
        )
        btn_actualizar.pack(side='left')
        
        # Efecto hover actualizar
        btn_actualizar.bind("<Enter>", lambda e: btn_actualizar.config(bg="#2980b9"))
        btn_actualizar.bind("<Leave>", lambda e: btn_actualizar.config(bg="#3498db"))
        
        # Info cantidad
        self.lbl_info = tk.Label(
            controles_frame,
            text="Cargando...",
            font=("Arial", 9),
            bg='#ffffff',
            fg='#7f8c8d'
        )
        self.lbl_info.pack(side='right')
        
        # Frame para la tabla
        tabla_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='flat', bd=1)
        tabla_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tabla_frame, orient=tk.HORIZONTAL)
        
        # Treeview con estilo mejorado
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                       font=('Arial', 9),
                       rowheight=25,
                       background='#ffffff',
                       fieldbackground='#ffffff')
        style.configure("Custom.Treeview.Heading", 
                       font=('Arial', 10, 'bold'),
                       background='#0077be',
                       foreground='white',
                       relief='flat')
        
        self.tree_pacientes = ttk.Treeview(
            tabla_frame,
            columns=("ID", "Nombre", "Dirección", "Teléfono", "F. Nacimiento", 
                     "Sexo", "Edad", "Estatura"),
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        # Configurar scrollbars
        scroll_y.config(command=self.tree_pacientes.yview)
        scroll_x.config(command=self.tree_pacientes.xview)
        
        # Definir columnas
        columnas = {
            "ID": 60,
            "Nombre": 200,
            "Dirección": 180,
            "Teléfono": 120,
            "F. Nacimiento": 120,
            "Sexo": 80,
            "Edad": 80,
            "Estatura": 100
        }
        
        for col, ancho in columnas.items():
            self.tree_pacientes.heading(col, text=col)
            self.tree_pacientes.column(col, width=ancho, anchor=tk.CENTER)
        
        # Empaquetar todo
        self.tree_pacientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Cargar datos iniciales
        self.cargar_pacientes()
        
    def guardar_paciente(self):
        """Guarda el paciente en la base de datos"""
        if not self.validar_campos():
            return
        
        # Obtener datos del formulario
        telefono = self.entry_telefono.get().strip()
        
        # Validar que el teléfono no esté repetido (solo si se ingresó teléfono)
        if telefono:  # Solo validar si se ingresó un teléfono
            telefono_existe = DBPacientes.verificar_telefono_existente(telefono)
            if telefono_existe:
                messagebox.showerror(
                    "Teléfono ya registrado", 
                    f"El teléfono {telefono} ya está registrado para otro paciente.\n\n"
                    f"Por favor, verifique el número o deje el campo vacío si el paciente no tiene teléfono.",
                    parent=self.ventana
                )
                self.entry_telefono.focus()
                self.entry_telefono.select_range(0, tk.END)
                return
        
        # Mapear sexo a formato de base de datos
        sexo_map = {"Masculino": "M", "Femenino": "F", "Otro": "Otro"}
        
        datos = {
            'nombre': self.entry_nombre.get().strip(),
            'direccion': self.entry_direccion.get().strip(),
            'telefono': telefono,
            'fecha_nacimiento': self.entry_fecha_nac.get_date(),
            'sexo': sexo_map[self.combo_sexo.get()],
            'edad': int(self.entry_edad.get().strip()),
            'estatura': float(self.entry_estatura.get().strip())
        }
        
        exito, mensaje, id_paciente = DBPacientes.insertar_paciente(datos)
        
        if exito:
            messagebox.showinfo("Éxito", 
                            f"{mensaje}\n\nID del paciente: {id_paciente}", 
                            parent=self.ventana)
            self.limpiar_campos()
            self.cargar_pacientes()
            # Cambiar a pestaña de listado
            self.notebook.select(1)
        else:
            messagebox.showerror("Error", 
                            mensaje, 
                            parent=self.ventana)
    
    def validar_campos(self):
        """Valida que los campos obligatorios estén llenos"""
        if not self.entry_nombre.get().strip():
            messagebox.showwarning("Advertencia", 
                                 "El nombre es obligatorio", 
                                 parent=self.ventana)
            self.entry_nombre.focus()
            return False
        
        if not self.entry_edad.get().strip():
            messagebox.showwarning("Advertencia", 
                                 "La edad es obligatoria", 
                                 parent=self.ventana)
            self.entry_edad.focus()
            return False
        
        try:
            int(self.entry_edad.get().strip())
        except ValueError:
            messagebox.showwarning("Advertencia", 
                                 "La edad debe ser un número entero válido", 
                                 parent=self.ventana)
            self.entry_edad.focus()
            return False
        
        if not self.entry_estatura.get().strip():
            messagebox.showwarning("Advertencia", 
                                 "La estatura es obligatoria", 
                                 parent=self.ventana)
            self.entry_estatura.focus()
            return False
        
        try:
            float(self.entry_estatura.get().strip())
        except ValueError:
            messagebox.showwarning("Advertencia", 
                                 "La estatura debe ser un número válido (ej: 1.75)", 
                                 parent=self.ventana)
            self.entry_estatura.focus()
            return False
        
        return True
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_fecha_nac.set_date(datetime.now())
        self.combo_sexo.current(0)
        self.entry_edad.delete(0, tk.END)
        self.entry_estatura.delete(0, tk.END) 
        self.entry_nombre.focus()
    
    def cargar_pacientes(self):
        """Carga todos los pacientes en la tabla"""
        for item in self.tree_pacientes.get_children():
            self.tree_pacientes.delete(item)
        
        exito, resultado = DBPacientes.obtener_todos_pacientes()
        
        if exito:
            for pac in resultado:
                self.tree_pacientes.insert("", tk.END, values=(
                    pac['id_paciente'],
                    pac['nombre'],
                    pac['direccion'] or 'N/A',
                    pac['telefono'] or 'N/A',
                    pac['fecha_nacimiento'],
                    pac['sexo'],
                    f"{pac['edad']} años",
                    f"{pac['estatura']} m"
                ))
            self.lbl_info.config(text=f"Total de pacientes: {len(resultado)}")
        else:
            messagebox.showerror("Error", 
                               resultado, 
                               parent=self.ventana)
            self.lbl_info.config(text="Error al cargar datos")