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
from DB_XAMPP.dbCitas import DBCitas
from datetime import datetime, time

class UICitas:
    def __init__(self, parent, usuario_actual=None):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Citas - Sistema Hospitalario")
        self.ventana.geometry("1040x700")
        self.ventana.configure(bg='#f0f8ff')
        self.ventana.resizable(True, True)
        self.usuario_actual = usuario_actual
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Variables para combobox
        self.pacientes_dict = {}  # {id: nombre}
        self.doctores_dict = {}   # {id: (nombre, especialidad)}
        
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
        """Crea los widgets de la interfaz"""
        
        # Header médico
        header_frame = tk.Frame(self.ventana, bg='#0077be', height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="GESTIÓN DE CITAS MÉDICAS",
            font=("Arial", 16, "bold"),
            bg='#0077be',
            fg='white'
        ).pack(expand=True)
        
        tk.Label(
            header_frame,
            text="Sistema de Agendamiento y Control de Citas",
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
        
        # Pestaña 1: Agendar Cita
        self.frame_agendar = tk.Frame(self.notebook, bg='#ffffff', relief='flat', bd=1)
        self.notebook.add(self.frame_agendar, text="Agendar Cita")
        self.crear_formulario_agendar()
        
        # Pestaña 2: Ver Citas
        self.frame_consultas = tk.Frame(self.notebook, bg='#ffffff', relief='flat', bd=1)
        self.notebook.add(self.frame_consultas, text="Listado de Citas")
        self.crear_tabla_consultas()
        
        # Pestaña 3: Verificar Disponibilidad
        self.frame_disponibilidad = tk.Frame(self.notebook, bg='#ffffff', relief='flat', bd=1)
        self.notebook.add(self.frame_disponibilidad, text="Verificar Disponibilidad")
        self.crear_verificador_disponibilidad()
        
    def crear_formulario_agendar(self):
        """Crea el formulario para agendar citas con nuevo diseño"""
        # Frame principal del formulario
        form_container = tk.Frame(self.frame_agendar, bg='#ffffff')
        form_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Título
        titulo = tk.Label(
            form_container,
            text="Agendar Nueva Cita Médica",
            font=("Arial", 16, "bold"),
            bg='#ffffff',
            fg='#0077be'
        )
        titulo.pack(pady=(0, 25))
        
        # Cargar pacientes y doctores
        self.cargar_pacientes()
        self.cargar_doctores()
        
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
        
        # Campos columna izquierda
        self.combo_paciente = ttk.Combobox(
            left_frame,
            values=list(self.pacientes_dict.values()),
            state="readonly",
            font=("Arial", 10)
        )
        if self.combo_paciente['values']:
            self.combo_paciente.current(0)
        crear_campo(left_frame, "Paciente", self.combo_paciente, True)
        
        # Fecha con calendario
        fecha_frame = tk.Frame(left_frame, bg='#ffffff')
        fecha_frame.pack(fill='x', pady=8)
        
        tk.Label(
            fecha_frame,
            text="Fecha *",
            font=("Arial", 10, "bold"),
            bg='#ffffff',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.entry_fecha = DateEntry(
            fecha_frame,
            font=("Arial", 10),
            width=30,
            background='#0077be',
            foreground='white',
            borderwidth=1,
            date_pattern='yyyy-mm-dd',
            mindate=datetime.now()
        )
        self.entry_fecha.pack(fill='x', pady=2)
        
        # Estado
        self.combo_estado = ttk.Combobox(
            left_frame,
            values=["Programada", "Completada", "Cancelada"],
            state="readonly",
            font=("Arial", 10)
        )
        self.combo_estado.current(0)
        crear_campo(left_frame, "Estado", self.combo_estado, True)
        
        # Campos columna derecha
        doctor_values = [f"{nombre} - {esp}" for nombre, esp in self.doctores_dict.values()]
        self.combo_doctor = ttk.Combobox(
            right_frame,
            values=doctor_values,
            state="readonly",
            font=("Arial", 10)
        )
        if self.combo_doctor['values']:
            self.combo_doctor.current(0)
        crear_campo(right_frame, "Doctor", self.combo_doctor, True)
        
        # Hora
        hora_frame = tk.Frame(right_frame, bg='#ffffff')
        hora_frame.pack(fill='x', pady=8)
        
        tk.Label(
            hora_frame,
            text="Hora *",
            font=("Arial", 10, "bold"),
            bg='#ffffff',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        # Frame para hora y label informativo
        hora_input_frame = tk.Frame(hora_frame, bg='#ffffff')
        hora_input_frame.pack(fill='x', pady=2)
        
        # Horas disponibles de 9:00 a 20:00
        horas_disponibles = [f"{h:02d}:00:00" for h in range(9, 21)]
        self.combo_hora = ttk.Combobox(
            hora_input_frame,
            values=horas_disponibles,
            state="readonly",
            font=("Arial", 10)
        )
        self.combo_hora.pack(side='left')
        self.combo_hora.current(0)
        
        tk.Label(
            hora_input_frame,
            text="(9:00 AM - 8:00 PM)",
            font=("Arial", 8, "italic"),
            bg='#ffffff',
            fg='#7f8c8d'
        ).pack(side='left', padx=5)
        
        # Nota de campos obligatorios
        nota_frame = tk.Frame(campos_frame, bg='#ffffff')
        nota_frame.pack(side='left', padx=10)
        
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
        
        # Botón Agendar
        btn_agendar = tk.Button(
            botones_frame,
            text="Agendar Cita",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#219a52",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.agendar_cita,
            padx=25,
            pady=10,
            relief="flat"
        )
        btn_agendar.pack(side='left', padx=10)
        
        # Efecto hover agendar
        btn_agendar.bind("<Enter>", lambda e: btn_agendar.config(bg="#219a52"))
        btn_agendar.bind("<Leave>", lambda e: btn_agendar.config(bg="#27ae60"))
        
        # Botón Verificar Disponibilidad
        btn_verificar = tk.Button(
            botones_frame,
            text="Verificar Disponibilidad",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.verificar_disponibilidad_actual,
            padx=25,
            pady=10,
            relief="flat"
        )
        btn_verificar.pack(side='left', padx=10)
        
        # Efecto hover verificar
        btn_verificar.bind("<Enter>", lambda e: btn_verificar.config(bg="#2980b9"))
        btn_verificar.bind("<Leave>", lambda e: btn_verificar.config(bg="#3498db"))
        
        # Botón Limpiar
        btn_limpiar = tk.Button(
            botones_frame,
            text="Limpiar Campos",
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

        # Botón Actualizar
        btn_actualizar = tk.Button(
            botones_frame,
            text="Modificar Cita",
            font=("Arial", 11, "bold"),
            bg="#cfe622",
            fg="white",
            activebackground="#a2b41c",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.actualizar_cita,
            padx=25,
            pady=10,
            relief="flat"
        )
        btn_actualizar.pack(side='left', padx=10)
        
        # Efecto hover limpiar
        btn_actualizar.bind("<Enter>", lambda e: btn_actualizar.config(bg="#a2b41c"))
        btn_actualizar.bind("<Leave>", lambda e: btn_actualizar.config(bg="#cfe622"))
        
    def crear_tabla_consultas(self):
        """Crea la tabla para mostrar todas las citas con nuevo diseño"""
        # Frame principal
        main_frame = tk.Frame(self.frame_consultas, bg='#ffffff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="Listado de Citas Programadas",
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
            text="Actualizar Listado",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.cargar_citas,
            padx=15,
            pady=6,
            relief="flat"
        )
        btn_actualizar.pack(side='left')
        
        # Efecto hover actualizar
        btn_actualizar.bind("<Enter>", lambda e: btn_actualizar.config(bg="#2980b9"))
        btn_actualizar.bind("<Leave>", lambda e: btn_actualizar.config(bg="#3498db"))
        
        # Botón Cancelar Cita
        btn_cancelar = tk.Button(
            controles_frame,
            text="Cancelar Cita Seleccionada",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.cancelar_cita_seleccionada,
            padx=15,
            pady=6,
            relief="flat"
        )
        btn_cancelar.pack(side='left', padx=10)
        
        # Efecto hover cancelar
        btn_cancelar.bind("<Enter>", lambda e: btn_cancelar.config(bg="#c0392b"))
        btn_cancelar.bind("<Leave>", lambda e: btn_cancelar.config(bg="#e74c3c"))
        
        # Frame para la tabla
        tabla_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='flat', bd=1)
        tabla_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL)
        
        # Treeview
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
        
        self.tree_citas = ttk.Treeview(
            tabla_frame,
            columns=("ID", "Paciente", "Doctor", "Fecha", "Hora", "Estado"),
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=scroll_y.set,
            #xscrollcommand=scroll_x.set
        )

        # Habilitar doble clic para editar
        self.tree_citas.bind('<Double-1>', self.cargar_cita_para_editar)
        
        # Configurar scrollbars
        scroll_y.config(command=self.tree_citas.yview)
        
        # Definir columnas
        columnas = {
            "ID": 60,
            "Paciente": 200,
            "Doctor": 200,
            "Fecha": 120,
            "Hora": 100,
            "Estado": 140
        }
        
        for col, ancho in columnas.items():
            self.tree_citas.heading(col, text=col)
            self.tree_citas.column(col, width=ancho, anchor=tk.CENTER)
        
        # Empaquetar todo
        self.tree_citas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar datos iniciales
        self.cargar_citas()
        
    def crear_verificador_disponibilidad(self):
        """Crea interfaz para verificar disponibilidad de doctores con nuevo diseño"""
        # Frame principal
        main_frame = tk.Frame(self.frame_disponibilidad, bg='#ffffff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="Verificar Disponibilidad de Doctores",
            font=("Arial", 16, "bold"),
            bg='#ffffff',
            fg='#0077be'
        )
        titulo.pack(pady=(0, 20))
        
        # Frame principal con dos columnas
        contenido_frame = tk.Frame(main_frame, bg='#ffffff')
        contenido_frame.pack(fill='both', expand=True)
        
        # Columna izquierda para controles
        izquierda_frame = tk.Frame(contenido_frame, bg='#ffffff', width=300)
        izquierda_frame.pack(side='left', fill='y', padx=(0, 20))
        izquierda_frame.pack_propagate(False)
        
        # Columna derecha para resultados
        derecha_frame = tk.Frame(contenido_frame, bg='#ffffff')
        derecha_frame.pack(side='right', fill='both', expand=True)
        
        # Título columna izquierda
        titulo_controles = tk.Label(
            izquierda_frame,
            text="Parámetros de Búsqueda",
            font=("Arial", 12, "bold"),
            bg='#ffffff',
            fg='#2c3e50'
        )
        titulo_controles.pack(pady=(0, 20))
        
        # Función para crear campos con estilo
        def crear_campo_disp(parent, label_text, widget):
            # Frame para cada campo
            campo_frame = tk.Frame(parent, bg='#ffffff')
            campo_frame.pack(fill='x', pady=12)
            
            # Label
            lbl = tk.Label(
                campo_frame,
                text=label_text,
                font=("Arial", 10, "bold"),
                bg='#ffffff',
                fg='#2c3e50',
                anchor='w'
            )
            lbl.pack(fill='x', pady=(0, 8))
            
            # Widget
            widget.pack(fill='x', pady=2)
        
        # Doctor
        doctor_values = [f"{nombre} - {esp}" for nombre, esp in self.doctores_dict.values()]
        self.combo_doctor_disp = ttk.Combobox(
            izquierda_frame,
            values=doctor_values,
            state="readonly",
            font=("Arial", 10)
        )
        if self.combo_doctor_disp['values']:
            self.combo_doctor_disp.current(0)
        crear_campo_disp(izquierda_frame, "Doctor", self.combo_doctor_disp)
        
        # Fecha
        self.entry_fecha_disp = DateEntry(
            izquierda_frame,
            font=("Arial", 10),
            width=30,
            background='#0077be',
            foreground='white',
            borderwidth=1,
            date_pattern='yyyy-mm-dd',
            mindate=datetime.now()
        )
        crear_campo_disp(izquierda_frame, "Fecha", self.entry_fecha_disp)
        
        # Botón verificar - centrado en la parte inferior de la columna izquierda
        botones_frame = tk.Frame(izquierda_frame, bg='#ffffff')
        botones_frame.pack(side='bottom', fill='x', pady=20)
        
        btn_verificar = tk.Button(
            botones_frame,
            text="Verificar Horarios Disponibles",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.mostrar_horarios_disponibles,
            padx=20,
            pady=12,
            relief="flat"
        )
        btn_verificar.pack(fill='x')
        
        # Efecto hover verificar
        btn_verificar.bind("<Enter>", lambda e: btn_verificar.config(bg="#2980b9"))
        btn_verificar.bind("<Leave>", lambda e: btn_verificar.config(bg="#3498db"))
        
        # Área de resultados - Ocupa toda la columna derecha
        resultado_frame = tk.LabelFrame(
            derecha_frame,
            text="Horarios Disponibles",
            font=("Arial", 12, "bold"),
            bg='#ffffff',
            fg='#2c3e50',
            padx=15,
            pady=10
        )
        resultado_frame.pack(fill='both', expand=True)
        
        # Frame para el treeview de horarios
        tree_frame = tk.Frame(resultado_frame, bg='#ecf0f1', relief='flat', bd=1)
        tree_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbars para el treeview
        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        
        # Treeview para mostrar horarios (más profesional que Listbox)
        style = ttk.Style()
        style.configure("Horarios.Treeview", 
                       font=('Arial', 10),
                       rowheight=28,
                       background='#ffffff',
                       fieldbackground='#ffffff')
        style.configure("Horarios.Treeview.Heading", 
                       font=('Arial', 11, 'bold'),
                       background='#0077be',
                       foreground='white',
                       relief='flat')
        
        self.tree_horarios = ttk.Treeview(
            tree_frame,
            columns=("Hora", "Estado", "Disponibilidad"),
            show="headings",
            style="Horarios.Treeview",
            yscrollcommand=scroll_y.set,
            #xscrollcommand=scroll_x.set,
            height=15
        )
        
        # Configurar scrollbars
        scroll_y.config(command=self.tree_horarios.yview)
        
        # Definir columnas
        columnas = {
            "Hora": 120,
            "Estado": 150,
            "Disponibilidad": 200
        }
        
        for col, ancho in columnas.items():
            self.tree_horarios.heading(col, text=col)
            self.tree_horarios.column(col, width=ancho, anchor=tk.CENTER)
        
        # Tags para colores
        self.tree_horarios.tag_configure('disponible', background='#d5f4e6', foreground='#27ae60')
        self.tree_horarios.tag_configure('ocupado', background='#fadbd8', foreground='#e74c3c')
        
        # Empaquetar treeview
        self.tree_horarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        #scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Frame para estadísticas
        stats_frame = tk.Frame(resultado_frame, bg='#ffffff')
        stats_frame.pack(fill='x', pady=(10, 0))
        
        self.lbl_stats = tk.Label(
            stats_frame,
            text="Seleccione doctor y fecha para ver disponibilidad",
            font=("Arial", 10, "italic"),
            bg='#ffffff',
            fg='#7f8c8d'
        )
        self.lbl_stats.pack()

    def cargar_pacientes(self):
        """Carga la lista de pacientes activos"""
        exito, resultado = DBCitas.obtener_pacientes_activos()
        if exito:
            self.pacientes_dict = {id_pac: nombre for id_pac, nombre in resultado}
        else:
            messagebox.showerror("Error", resultado, parent=self.ventana)
            
    def cargar_doctores(self):
        """Carga la lista de doctores activos"""
        exito, resultado = DBCitas.obtener_doctores_activos()
        if exito:
            self.doctores_dict = {id_doc: (nombre, esp) for id_doc, nombre, esp in resultado}
        else:
            messagebox.showerror("Error", resultado, parent=self.ventana)
    
    def obtener_id_paciente(self):
        """Obtiene el ID del paciente seleccionado"""
        nombre_seleccionado = self.combo_paciente.get()
        for id_pac, nombre in self.pacientes_dict.items():
            if nombre == nombre_seleccionado:
                return id_pac
        return None
    
    def obtener_id_doctor(self, combo=None):
        """Obtiene el ID del doctor seleccionado"""
        if combo is None:
            combo = self.combo_doctor
            
        seleccion = combo.get()
        nombre_doctor = seleccion.split(" - ")[0] if " - " in seleccion else seleccion
        
        for id_doc, (nombre, esp) in self.doctores_dict.items():
            if nombre == nombre_doctor:
                return id_doc
        return None
    
    def agendar_cita(self):
        """Agenda una nueva cita"""
        if not self.validar_campos():
            return
        
        datos = {
            'id_paciente': self.obtener_id_paciente(),
            'id_doctor': self.obtener_id_doctor(),
            'fecha': self.entry_fecha.get_date(),
            'hora': self.combo_hora.get(),
            'estado': self.combo_estado.get()
        }
        
        exito, mensaje, id_cita = DBCitas.insertar_cita(datos)
        
        if exito:
            messagebox.showinfo(
                "Éxito",
                f"{mensaje}\nID de la cita: {id_cita}",
                parent=self.ventana
            )
            self.limpiar_campos()
            self.cargar_citas()
            self.notebook.select(1)  # Cambiar a pestaña de consultas
        else:
            messagebox.showerror("Error", mensaje, parent=self.ventana)
    
    def validar_campos(self):
        """Valida que los campos obligatorios estén llenos"""
        if not self.combo_paciente.get():
            messagebox.showwarning("Advertencia", "Seleccione un paciente", parent=self.ventana)
            return False
        
        if not self.combo_doctor.get():
            messagebox.showwarning("Advertencia", "Seleccione un doctor", parent=self.ventana)
            return False
        
        if not self.combo_hora.get():
            messagebox.showwarning("Advertencia", "Seleccione una hora", parent=self.ventana)
            return False
        
        # Validar que la fecha no sea anterior a hoy
        fecha_seleccionada = self.entry_fecha.get_date()
        fecha_actual = datetime.now().date()
        
        if fecha_seleccionada < fecha_actual:
            messagebox.showwarning(
                "Fecha Inválida", 
                "No se pueden agendar citas en fechas pasadas.\nPor favor seleccione una fecha actual o futura.",
                parent=self.ventana
            )
            return False
        
        return True
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        if self.combo_paciente['values']:
            self.combo_paciente.current(0)
        if self.combo_doctor['values']:
            self.combo_doctor.current(0)
        self.entry_fecha.set_date(datetime.now())
        self.combo_hora.current(0)
        self.combo_estado.current(0)
    
    def cargar_citas(self):
        """Carga todas las citas en la tabla"""
        for item in self.tree_citas.get_children():
            self.tree_citas.delete(item)
        
        exito, resultado = DBCitas.obtener_todas_citas()
        
        if exito:
            for cita in resultado:
                self.tree_citas.insert("", tk.END, values=(
                    cita['id_cita'],
                    cita['paciente'],
                    cita['doctor'],
                    cita['fecha'],
                    cita['hora'],
                    cita['estado']
                ))
        else:
            messagebox.showerror("Error", resultado, parent=self.ventana)
    
    def cancelar_cita_seleccionada(self):
        """Cancela la cita seleccionada en la tabla"""
        seleccion = self.tree_citas.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione una cita para cancelar",
                parent=self.ventana
            )
            return
        
        item = self.tree_citas.item(seleccion[0])
        id_cita = item['values'][0]
        estado_actual = item['values'][5]
        
        if estado_actual == "Cancelada":
            messagebox.showinfo(
                "Información",
                "Esta cita ya está cancelada",
                parent=self.ventana
            )
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de cancelar la cita #{id_cita}?",
            parent=self.ventana
        )
        
        if respuesta:
            exito, mensaje = DBCitas.cancelar_cita(id_cita)
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=self.ventana)
                self.cargar_citas()
            else:
                messagebox.showerror("Error", mensaje, parent=self.ventana)
    
    def verificar_disponibilidad_actual(self):
        """Verifica disponibilidad para los datos actuales del formulario"""
        if not self.combo_doctor.get() or not self.combo_hora.get():
            messagebox.showwarning(
                "Advertencia",
                "Seleccione doctor y hora para verificar",
                parent=self.ventana
            )
            return
        
        id_doctor = self.obtener_id_doctor()
        fecha = self.entry_fecha.get_date()
        hora = self.combo_hora.get()
        
        disponible, mensaje = DBCitas.verificar_disponibilidad(id_doctor, fecha, hora)
        
        if disponible:
            messagebox.showinfo("Disponible", mensaje, parent=self.ventana)
        else:
            messagebox.showwarning("No Disponible", mensaje, parent=self.ventana)
    
    def actualizar_cita(self):
        """Actualiza una cita existente"""
        # Verificar que haya una cita seleccionada en la tabla
        seleccion = self.tree_citas.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Primero debe seleccionar una cita de la tabla en 'Listado de Citas'",
                parent=self.ventana
            )
            # Cambiar a la pestaña de listado
            self.notebook.select(1)
            return
        
        # Obtener el ID de la cita seleccionada
        item = self.tree_citas.item(seleccion[0])
        id_cita = item['values'][0]
        
        # Validar campos
        if not self.validar_campos():
            return
        
        # Confirmar actualización
        respuesta = messagebox.askyesno(
            "Confirmar Actualización",
            f"¿Está seguro de modificar la cita #{id_cita}?",
            parent=self.ventana
        )
        
        if not respuesta:
            return
        
        # Preparar datos
        datos = {
            'id_paciente': self.obtener_id_paciente(),
            'id_doctor': self.obtener_id_doctor(),
            'fecha': self.entry_fecha.get_date(),
            'hora': self.combo_hora.get(),
            'estado': self.combo_estado.get()
        }
        
        # Actualizar en la base de datos
        exito, mensaje = DBCitas.actualizar_cita(id_cita, datos)
        
        if exito:
            messagebox.showinfo(
                "Éxito",
                f"{mensaje}\nCita #{id_cita} actualizada correctamente",
                parent=self.ventana
            )
            self.limpiar_campos()
            self.cargar_citas()
            self.notebook.select(1)  # Cambiar a pestaña de consultas
        else:
            messagebox.showerror("Error", mensaje, parent=self.ventana)
    
    def cargar_cita_para_editar(self, event=None):
        """Carga los datos de una cita seleccionada en el formulario para editar"""
        seleccion = self.tree_citas.selection()
        if not seleccion:
            return
        
        item = self.tree_citas.item(seleccion[0])
        id_cita = item['values'][0]
        
        # Obtener datos completos de la cita
        exito, cita_data = DBCitas.obtener_cita_por_id(id_cita)
        
        if not exito:
            messagebox.showerror("Error", cita_data, parent=self.ventana)
            return
        
        # Cambiar a la pestaña de agendar
        self.notebook.select(0)
        
        # Cargar datos en el formulario
        # Paciente
        for idx, nombre in enumerate(self.combo_paciente['values']):
            if nombre == cita_data['paciente']:
                self.combo_paciente.current(idx)
                break
        
        # Doctor
        doctor_texto = f"{cita_data['doctor']} - {cita_data['especialidad']}"
        for idx, nombre in enumerate(self.combo_doctor['values']):
            if nombre == doctor_texto:
                self.combo_doctor.current(idx)
                break
        
        # Fecha
        if isinstance(cita_data['fecha'], str):
            from datetime import datetime
            fecha_obj = datetime.strptime(cita_data['fecha'], '%Y-%m-%d')
            self.entry_fecha.set_date(fecha_obj)
        else:
            self.entry_fecha.set_date(cita_data['fecha'])
        
        # Hora
        hora_str = str(cita_data['hora'])
        for idx, hora in enumerate(self.combo_hora['values']):
            if hora == hora_str:
                self.combo_hora.current(idx)
                break
        
        # Estado
        for idx, estado in enumerate(self.combo_estado['values']):
            if estado == cita_data['estado']:
                self.combo_estado.current(idx)
                break
        
        messagebox.showinfo(
            "Editar Cita",
            f"Cita #{id_cita} cargada.\nModifique los campos necesarios y presione 'Modificar Cita'",
            parent=self.ventana
        )

    def mostrar_horarios_disponibles(self):
        """Muestra todos los horarios disponibles para un doctor en una fecha"""
        if not self.combo_doctor_disp.get():
            messagebox.showwarning(
                "Advertencia",
                "Seleccione un doctor",
                parent=self.ventana
            )
            return
        
        # Limpiar treeview
        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)
        
        id_doctor = self.obtener_id_doctor(self.combo_doctor_disp)
        fecha = self.entry_fecha_disp.get_date()
        
        # Horas disponibles de 9:00 a 20:00
        horas = [f"{h:02d}:00" for h in range(9, 21)]
        
        disponibles = []
        ocupadas = []
        
        # Verificar disponibilidad para cada hora
        for hora in horas:
            hora_completa = f"{hora}:00"  # Formato completo para la BD
            disponible, mensaje = DBCitas.verificar_disponibilidad(id_doctor, fecha, hora_completa)
            if disponible:
                disponibles.append(hora)
                self.tree_horarios.insert("", tk.END, values=(
                    hora,
                    "DISPONIBLE",
                    "Cita disponible"
                ), tags=('disponible',))
            else:
                ocupadas.append(hora)
                self.tree_horarios.insert("", tk.END, values=(
                    hora,
                    "OCUPADO",
                    "Horario no disponible"
                ), tags=('ocupado',))
        
        # Actualizar estadísticas
        total_horas = len(horas)
        horas_disponibles = len(disponibles)
        porcentaje = (horas_disponibles / total_horas) * 100 if total_horas > 0 else 0
        
        self.lbl_stats.config(
            text=f"Disponibilidad: {horas_disponibles}/{total_horas} horas ({porcentaje:.1f}%) - " +
                 f"Disponibles: {horas_disponibles} | Ocupadas: {len(ocupadas)}",
            fg='#2c3e50'
        )
        
        # Si no hay horarios disponibles, mostrar mensaje
        if horas_disponibles == 0:
            self.lbl_stats.config(
                text=f"⚠️ No hay horarios disponibles para esta fecha. Total ocupados: {len(ocupadas)}",
                fg='#e74c3c'
            )