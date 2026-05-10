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
from DB_XAMPP.dbMedicamentos import DBMedicamentos
from datetime import datetime, timedelta

class UIMedicamentos:
    def __init__(self, parent, usuario_actual=None):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Medicamentos - Sistema Hospitalario")
        self.ventana.geometry("1040x750")
        self.ventana.configure(bg='#f0f8ff')
        self.ventana.resizable(True, True)
        self.usuario_actual = usuario_actual
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Crear interfaz
        self.crear_widgets()
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        width = 1040
        height = 750
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
            text="GESTIÓN DE MEDICAMENTOS",
            font=("Arial", 16, "bold"),
            bg='#0077be',
            fg='white'
        ).pack(expand=True)
        
        tk.Label(
            header_frame,
            text="Sistema de Control y Alertas de Medicamentos",
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
        
        # Pestaña 1: Registrar Medicamento
        self.frame_registrar = tk.Frame(self.notebook, bg='#ffffff', relief='flat', bd=1)
        self.notebook.add(self.frame_registrar, text="Registrar Medicamento")
        self.crear_formulario_registrar()
        
        # Pestaña 2: Ver Medicamentos
        self.frame_consultas = tk.Frame(self.notebook, bg='#ffffff', relief='flat', bd=1)
        self.notebook.add(self.frame_consultas, text="Listado de Medicamentos")
        self.crear_tabla_consultas()
        
        # Pestaña 3: Alertas de Vencimiento
        self.frame_alertas = tk.Frame(self.notebook, bg='#ffffff', relief='flat', bd=1)
        self.notebook.add(self.frame_alertas, text="Alertas de Vencimiento")
        self.crear_panel_alertas()
        
    def crear_formulario_registrar(self):
        """Crea el formulario para registrar medicamentos"""
        # Frame principal del formulario
        form_container = tk.Frame(self.frame_registrar, bg='#ffffff')
        form_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Título
        titulo = tk.Label(
            form_container,
            text="Registro de Nuevo Medicamento",
            font=("Arial", 16, "bold"),
            bg='#ffffff',
            fg='#0077be'
        )
        titulo.pack(pady=(0, 25))

        # Frame principal con distribución mejorada
        main_form_frame = tk.Frame(form_container, bg='#ffffff')
        main_form_frame.pack(fill='both', expand=True)

        # Sección superior: Campos del formulario en 2 columnas
        campos_superior_frame = tk.Frame(main_form_frame, bg='#ffffff')
        campos_superior_frame.pack(fill='x', pady=(0, 20))

        # Columna izquierda para campos principales
        left_frame = tk.Frame(campos_superior_frame, bg='#ffffff')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 15))

        # Columna derecha para campos adicionales
        right_frame = tk.Frame(campos_superior_frame, bg='#ffffff')
        right_frame.pack(side='right', fill='both', expand=True, padx=(15, 0))

        # Función para crear campos con estilo
        def crear_campo(parent, label_text, widget, es_obligatorio=False, padding_y=10):
            # Frame para cada campo
            campo_frame = tk.Frame(parent, bg='#ffffff')
            campo_frame.pack(fill='x', pady=padding_y)
            
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
            lbl.pack(fill='x', pady=(0, 6))
            
            # Widget con altura consistente
            widget.pack(fill='x', pady=1, ipady=2)  # ipady para padding interno consistente

        # Configurar estilo para entries y combobox
        style = ttk.Style()
        style.configure('Custom.TEntry', padding=(8, 6), relief='flat', borderwidth=1)
        style.configure('Custom.TCombobox', padding=(8, 6), relief='flat', borderwidth=1)
        
        # --- COLUMNA IZQUIERDA ---
        # Nombre del medicamento
        self.entry_nombre = ttk.Entry(left_frame, font=("Arial", 10), style='Custom.TEntry')
        crear_campo(left_frame, "Nombre del Medicamento", self.entry_nombre, True)

        # Vía de administración
        self.combo_via = ttk.Combobox(
            left_frame,
            values=[
                "Oral",
                "Intravenosa (IV)",
                "Intramuscular (IM)",
                "Subcutánea",
                "Tópica",
                "Oftálmica",
                "Ótica",
                "Nasal",
                "Rectal",
                "Inhalatoria",
                "Sublingual",
                "Transdérmica"
            ],
            state="readonly",
            font=("Arial", 10),
            style='Custom.TCombobox'
        )
        self.combo_via.current(0)
        crear_campo(left_frame, "Vía de Administración", self.combo_via, True)

        # --- COLUMNA DERECHA ---
        # Presentación
        self.combo_presentacion = ttk.Combobox(
            right_frame,
            values=[
                "Tabletas",
                "Cápsulas",
                "Jarabe",
                "Suspensión",
                "Solución inyectable",
                "Ampolletas",
                "Crema",
                "Pomada",
                "Gel",
                "Gotas",
                "Spray",
                "Parche",
                "Supositorio",
                "Óvulos",
                "Polvo"
            ],
            state="readonly",
            font=("Arial", 10),
            style='Custom.TCombobox'
        )
        self.combo_presentacion.current(0)
        crear_campo(right_frame, "Presentación", self.combo_presentacion, True)

        # Fecha de Caducidad
        fecha_frame = tk.Frame(right_frame, bg='#ffffff')
        fecha_frame.pack(fill='x', pady=10)
        
        tk.Label(
            fecha_frame,
            text="Fecha de Caducidad *",
            font=("Arial", 10, "bold"),
            bg='#ffffff',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 6))
        
        # Frame para el DateEntry con altura consistente
        fecha_input_frame = tk.Frame(fecha_frame, bg='#ffffff')
        fecha_input_frame.pack(fill='x', pady=2)
        
        self.entry_fecha_cad = DateEntry(
            fecha_input_frame,
            font=("Arial", 10),
            background='#0077be',
            foreground='white',
            borderwidth=1,
            date_pattern='yyyy-mm-dd',
            mindate=datetime.now() + timedelta(days=1)
        )
        self.entry_fecha_cad.pack(fill='x', ipady=3)  # ipady para igualar altura con combobox

        # --- SECCIÓN MEDIA: Información importante ---
        info_frame = tk.Frame(main_form_frame, bg='#f8f9fa', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=20, padx=10)

        # Título de información
        info_titulo = tk.Label(
            info_frame,
            text="Información Importante para el Registro",
            font=("Arial", 11, "bold"),
            bg='#e3f2fd',
            fg='#0077be',
            padx=15,
            pady=8
        )
        info_titulo.pack(fill='x')

        # Contenido de información
        info_content = tk.Frame(info_frame, bg='#f8f9fa', padx=20, pady=15)
        info_content.pack(fill='x', expand=True)

        # Puntos informativos
        puntos_info = [
            "• La fecha de caducidad debe ser posterior a la fecha actual",
            "• El sistema generará alertas automáticas 30 días antes del vencimiento",
            "• Los medicamentos vencidos se mostrarán en la pestaña 'Alertas de Vencimiento'",
            "• Verifique cuidadosamente el nombre y presentación del medicamento",
            "• Seleccione la vía de administración correcta para el medicamento"
        ]

        for punto in puntos_info:
            punto_frame = tk.Frame(info_content, bg='#f8f9fa')
            punto_frame.pack(fill='x', pady=3)
            
            tk.Label(
                punto_frame,
                text=punto,
                font=("Arial", 9),
                bg='#f8f9fa',
                fg='#2c3e50',
                justify='left',
                anchor='w'
            ).pack(fill='x')

        # --- SECCIÓN INFERIOR: Nota y botones ---
        inferior_frame = tk.Frame(main_form_frame, bg='#ffffff')
        inferior_frame.pack(fill='x', pady=(10, 0))

        # Nota de campos obligatorios
        nota_frame = tk.Frame(inferior_frame, bg='#ffffff')
        nota_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            nota_frame,
            text="* Campos obligatorios",
            font=("Arial", 9, "italic"),
            bg='#ffffff',
            fg='#e74c3c'
        ).pack()

        # Frame para botones
        botones_frame = tk.Frame(inferior_frame, bg='#ffffff')
        botones_frame.pack(pady=10)

        # Botón Guardar
        btn_guardar = tk.Button(
            botones_frame,
            text="Guardar Medicamento",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#219a52",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.guardar_medicamento,
            padx=25,
            pady=12,
            relief="flat"
        )
        btn_guardar.pack(side='left', padx=15)

        # Efecto hover guardar
        btn_guardar.bind("<Enter>", lambda e: btn_guardar.config(bg="#219a52"))
        btn_guardar.bind("<Leave>", lambda e: btn_guardar.config(bg="#27ae60"))

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
            pady=12,
            relief="flat"
        )
        btn_limpiar.pack(side='left', padx=15)

        # Efecto hover limpiar
        btn_limpiar.bind("<Enter>", lambda e: btn_limpiar.config(bg="#d35400"))
        btn_limpiar.bind("<Leave>", lambda e: btn_limpiar.config(bg="#e67e22"))
        
    def crear_tabla_consultas(self):
        """Crea la tabla para mostrar todos los medicamentos con nuevo diseño"""
        # Frame principal
        main_frame = tk.Frame(self.frame_consultas, bg='#ffffff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="Listado de Medicamentos Registrados",
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
            command=self.cargar_medicamentos,
            padx=15,
            pady=6,
            relief="flat"
        )
        btn_actualizar.pack(side='left')
        
        # Efecto hover actualizar
        btn_actualizar.bind("<Enter>", lambda e: btn_actualizar.config(bg="#2980b9"))
        btn_actualizar.bind("<Leave>", lambda e: btn_actualizar.config(bg="#3498db"))
        
        # Botón Eliminar
        btn_eliminar = tk.Button(
            controles_frame,
            text="Eliminar Seleccionado",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.eliminar_medicamento_seleccionado,
            padx=15,
            pady=6,
            relief="flat"
        )
        btn_eliminar.pack(side='left', padx=10)
        
        # Efecto hover eliminar
        btn_eliminar.bind("<Enter>", lambda e: btn_eliminar.config(bg="#c0392b"))
        btn_eliminar.bind("<Leave>", lambda e: btn_eliminar.config(bg="#e74c3c"))
        
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
        #scroll_x = ttk.Scrollbar(tabla_frame, orient=tk.HORIZONTAL)
        
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
        
        self.tree_medicamentos = ttk.Treeview(
            tabla_frame,
            columns=("ID", "Nombre", "Vía", "Presentación", "Caducidad", "Estado"),
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=scroll_y.set,
        )
        
        # Configurar scrollbars
        scroll_y.config(command=self.tree_medicamentos.yview)
        
        # Definir columnas
        columnas = {
            "ID": 60,
            "Nombre": 250,
            "Vía": 150,
            "Presentación": 150,
            "Caducidad": 120,
            "Estado": 120
        }
        
        for col, ancho in columnas.items():
            self.tree_medicamentos.heading(col, text=col)
            self.tree_medicamentos.column(col, width=ancho, anchor=tk.CENTER)
        
        # Tags para colores
        self.tree_medicamentos.tag_configure('vencido', background='#ffcccc')
        self.tree_medicamentos.tag_configure('por_vencer', background='#fff9cc')
        self.tree_medicamentos.tag_configure('vigente', background='#ccffcc')
        
        # Empaquetar todo
        self.tree_medicamentos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar datos iniciales
        self.cargar_medicamentos()
        
    def crear_panel_alertas(self):
        """Crea el panel de alertas de vencimiento con nuevo diseño"""
        # Frame principal
        main_frame = tk.Frame(self.frame_alertas, bg='#ffffff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="Alertas de Vencimiento de Medicamentos",
            font=("Arial", 16, "bold"),
            bg='#ffffff',
            fg='#0077be'
        )
        titulo.pack(pady=(0, 20))
        
        # Frame para medicamentos próximos a vencer
        frame_proximos = tk.LabelFrame(
            main_frame,
            text="Medicamentos por vencer (próximos 30 días)",
            font=("Arial", 11, "bold"),
            bg='#ffffff',
            fg='#e67e22',
            padx=15,
            pady=10
        )
        frame_proximos.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbars para próximos
        scroll_y_proximos = ttk.Scrollbar(frame_proximos, orient=tk.VERTICAL)
        
        self.tree_proximos = ttk.Treeview(
            frame_proximos,
            columns=("ID", "Nombre", "Presentación", "Caducidad", "Días Restantes"),
            show="headings",
            yscrollcommand=scroll_y_proximos.set,
            height=8
        )
        
        scroll_y_proximos.config(command=self.tree_proximos.yview)
        
        # Configurar columnas próximos
        columnas_proximos = {
            "ID": 60,
            "Nombre": 250,
            "Presentación": 150,
            "Caducidad": 120,
            "Días Restantes": 120
        }
        
        for col, ancho in columnas_proximos.items():
            self.tree_proximos.heading(col, text=col)
            self.tree_proximos.column(col, width=ancho, anchor=tk.CENTER)
        
        self.tree_proximos.tag_configure('alerta', background='#fff9cc')
        
        self.tree_proximos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y_proximos.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para medicamentos vencidos
        frame_vencidos = tk.LabelFrame(
            main_frame,
            text="Medicamentos Vencidos",
            font=("Arial", 11, "bold"),
            bg='#ffffff',
            fg='#e74c3c',
            padx=15,
            pady=10
        )
        frame_vencidos.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbars para vencidos
        scroll_y_vencidos = ttk.Scrollbar(frame_vencidos, orient=tk.VERTICAL)
        
        self.tree_vencidos = ttk.Treeview(
            frame_vencidos,
            columns=("ID", "Nombre", "Presentación", "Caducidad", "Días Vencido"),
            show="headings",
            yscrollcommand=scroll_y_vencidos.set,
            height=8
        )
        
        scroll_y_vencidos.config(command=self.tree_vencidos.yview)
        
        # Configurar columnas vencidos
        columnas_vencidos = {
            "ID": 60,
            "Nombre": 250,
            "Presentación": 150,
            "Caducidad": 120,
            "Días Vencido": 120
        }
        
        for col, ancho in columnas_vencidos.items():
            self.tree_vencidos.heading(col, text=col)
            self.tree_vencidos.column(col, width=ancho, anchor=tk.CENTER)
        
        self.tree_vencidos.tag_configure('vencido', background='#ffcccc')
        
        self.tree_vencidos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y_vencidos.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botón actualizar alertas
        btn_actualizar = tk.Button(
            main_frame,
            text="Actualizar Alertas",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.cargar_alertas,
            padx=15,
            pady=6,
            relief="flat"
        )
        btn_actualizar.pack(pady=10)
        
        # Efecto hover actualizar
        btn_actualizar.bind("<Enter>", lambda e: btn_actualizar.config(bg="#2980b9"))
        btn_actualizar.bind("<Leave>", lambda e: btn_actualizar.config(bg="#3498db"))
        
        # Cargar alertas iniciales
        self.cargar_alertas()

    def guardar_medicamento(self):
        """Guarda el medicamento en la base de datos"""
        if not self.validar_campos():
            return
        
        datos = {
            'nombre': self.entry_nombre.get().strip(),
            'via_administracion': self.combo_via.get(),
            'presentacion': self.combo_presentacion.get(),
            'fecha_caducidad': self.entry_fecha_cad.get_date()
        }
        
        # Verificar que la fecha no sea pasada
        if datos['fecha_caducidad'] <= datetime.now().date():
            messagebox.showerror(
                "Error",
                "La fecha de caducidad debe ser posterior a la fecha actual",
                parent=self.ventana
            )
            return
        
        exito, mensaje, id_medicamento = DBMedicamentos.insertar_medicamento(datos)
        
        if exito:
            messagebox.showinfo(
                "Éxito",
                f"{mensaje}\nID del medicamento: {id_medicamento}",
                parent=self.ventana
            )
            self.limpiar_campos()
            self.cargar_medicamentos()
            self.cargar_alertas()
            self.notebook.select(1)  # Cambiar a pestaña de consultas
        else:
            messagebox.showerror("Error", mensaje, parent=self.ventana)
    
    def validar_campos(self):
        """Valida que los campos obligatorios estén llenos"""
        if not self.entry_nombre.get().strip():
            messagebox.showwarning(
                "Advertencia",
                "El nombre del medicamento es obligatorio",
                parent=self.ventana
            )
            self.entry_nombre.focus()
            return False
        
        if not self.combo_via.get():
            messagebox.showwarning(
                "Advertencia",
                "Seleccione la vía de administración",
                parent=self.ventana
            )
            self.combo_via.focus()
            return False
        
        if not self.combo_presentacion.get():
            messagebox.showwarning(
                "Advertencia",
                "Seleccione la presentación",
                parent=self.ventana
            )
            self.combo_presentacion.focus()
            return False
        
        return True
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.combo_via.current(0)
        self.combo_presentacion.current(0)
        self.entry_fecha_cad.set_date(datetime.now() + timedelta(days=365))
        self.entry_nombre.focus()
    
    def cargar_medicamentos(self):
        """Carga todos los medicamentos en la tabla"""
        for item in self.tree_medicamentos.get_children():
            self.tree_medicamentos.delete(item)
        
        exito, resultado = DBMedicamentos.obtener_todos_medicamentos()
        
        if exito:
            hoy = datetime.now().date()
            for med in resultado:
                fecha_cad = med['fecha_caducidad']
                dias_restantes = (fecha_cad - hoy).days
                
                # Determinar estado y color
                if dias_restantes < 0:
                    estado = "VENCIDO"
                    tag = 'vencido'
                elif dias_restantes <= 30:
                    estado = f"Por vencer ({dias_restantes}d)"
                    tag = 'por_vencer'
                else:
                    estado = "Vigente"
                    tag = 'vigente'
                
                self.tree_medicamentos.insert("", tk.END, values=(
                    med['id_medicamento'],
                    med['nombre'],
                    med['via_administracion'],
                    med['presentacion'],
                    med['fecha_caducidad'],
                    estado
                ), tags=(tag,))
            
            self.lbl_info.config(text=f"Total de medicamentos: {len(resultado)}")
        else:
            messagebox.showerror("Error", resultado, parent=self.ventana)
            self.lbl_info.config(text="Error al cargar datos")
    
    def eliminar_medicamento_seleccionado(self):
        """Elimina el medicamento seleccionado en la tabla"""
        seleccion = self.tree_medicamentos.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione un medicamento para eliminar",
                parent=self.ventana
            )
            return
        
        item = self.tree_medicamentos.item(seleccion[0])
        id_medicamento = item['values'][0]
        nombre = item['values'][1]
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el medicamento:\n\n{nombre}?",
            parent=self.ventana
        )
        
        if respuesta:
            exito, mensaje = DBMedicamentos.eliminar_medicamento(id_medicamento)
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=self.ventana)
                self.cargar_medicamentos()
                self.cargar_alertas()
            else:
                messagebox.showerror("Error", mensaje, parent=self.ventana)
    
    def cargar_alertas(self):
        """Carga las alertas de medicamentos próximos a vencer y vencidos"""
        # Limpiar tablas
        for item in self.tree_proximos.get_children():
            self.tree_proximos.delete(item)
        for item in self.tree_vencidos.get_children():
            self.tree_vencidos.delete(item)
        
        # Cargar próximos a vencer
        exito, resultado = DBMedicamentos.obtener_medicamentos_proximos_vencer(30)
        if exito:
            for med in resultado:
                self.tree_proximos.insert("", tk.END, values=(
                    med['id_medicamento'],
                    med['nombre'],
                    med['presentacion'],
                    med['fecha_caducidad'],
                    f"{med['dias_restantes']} días"
                ), tags=('alerta',))
        
        # Cargar vencidos
        exito, resultado = DBMedicamentos.obtener_medicamentos_vencidos()
        if exito:
            for med in resultado:
                self.tree_vencidos.insert("", tk.END, values=(
                    med['id_medicamento'],
                    med['nombre'],
                    med['presentacion'],
                    med['fecha_caducidad'],
                    f"{med['dias_vencido']} días"
                ), tags=('vencido',))