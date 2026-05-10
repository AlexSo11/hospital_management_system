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
from DB_XAMPP.dbCitas import DBCitas
from DB_XAMPP.dbPacientes import DBPacientes
from DB_XAMPP.dbMedicamentos import DBMedicamentos
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

class UIMisCitas:
    def __init__(self, parent, usuario_actual=None):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Mis Citas - Dr. {usuario_actual}")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg='#f0f8ff')
        self.ventana.resizable(True, True)
        self.usuario_actual = usuario_actual
        
        # Obtener ID del doctor
        self.id_doctor = DBCitas.obtener_id_doctor_por_nombre(usuario_actual)
        if not self.id_doctor:
            messagebox.showerror("Error", "No se pudo identificar al doctor", parent=self.ventana)
            self.ventana.destroy()
            return
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Variable para almacenar la cita seleccionada
        self.cita_seleccionada = None
        
        # Crear interfaz
        self.crear_widgets()
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        width = 1200
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
            text=f"MIS CITAS - Dr. {self.usuario_actual}",
            font=("Arial", 16, "bold"),
            bg='#0077be',
            fg='white'
        ).pack(expand=True)
        
        tk.Label(
            header_frame,
            text=f"Citas programadas para hoy - {datetime.now().strftime('%d/%m/%Y')}",
            font=("Arial", 10),
            bg='#0077be',
            fg='#e0f0ff'
        ).pack(pady=(0, 10))
        
        # Frame principal
        main_frame = tk.Frame(self.ventana, bg='#ffffff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
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
            command=self.cargar_mis_citas,
            padx=15,
            pady=6,
            relief="flat"
        )
        btn_actualizar.pack(side='left', padx=5)
        btn_actualizar.bind("<Enter>", lambda e: btn_actualizar.config(bg="#2980b9"))
        btn_actualizar.bind("<Leave>", lambda e: btn_actualizar.config(bg="#3498db"))
        
        # Botón Ver Paciente
        btn_ver_paciente = tk.Button(
            controles_frame,
            text="Ver Información del Paciente",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#219a52",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.ver_info_paciente,
            padx=15,
            pady=6,
            relief="flat"
        )
        btn_ver_paciente.pack(side='left', padx=5)
        btn_ver_paciente.bind("<Enter>", lambda e: btn_ver_paciente.config(bg="#219a52"))
        btn_ver_paciente.bind("<Leave>", lambda e: btn_ver_paciente.config(bg="#27ae60"))
        
        # Botón Generar Receta
        btn_receta = tk.Button(
            controles_frame,
            text="Generar Receta Médica",
            font=("Arial", 10, "bold"),
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.abrir_ventana_receta,
            padx=15,
            pady=6,
            relief="flat"
        )
        btn_receta.pack(side='left', padx=5)
        btn_receta.bind("<Enter>", lambda e: btn_receta.config(bg="#8e44ad"))
        btn_receta.bind("<Leave>", lambda e: btn_receta.config(bg="#9b59b6"))
        
        # Info de citas
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
        
        # Treeview
        style = ttk.Style()
        style.configure("MisCitas.Treeview", 
                       font=('Arial', 10),
                       rowheight=30,
                       background='#ffffff',
                       fieldbackground='#ffffff')
        style.configure("MisCitas.Treeview.Heading", 
                       font=('Arial', 11, 'bold'),
                       background='#0077be',
                       foreground='white',
                       relief='flat')
        
        self.tree_citas = ttk.Treeview(
            tabla_frame,
            columns=("Hora", "Paciente", "Edad", "Sexo", "Teléfono", "Estado"),
            show="headings",
            style="MisCitas.Treeview",
            yscrollcommand=scroll_y.set
        )
        
        # Configurar scrollbars
        scroll_y.config(command=self.tree_citas.yview)
        
        # Definir columnas
        columnas = {
            "Hora": 100,
            "Paciente": 250,
            "Edad": 80,
            "Sexo": 100,
            "Teléfono": 150,
            "Estado": 150
        }
        
        for col, ancho in columnas.items():
            self.tree_citas.heading(col, text=col)
            self.tree_citas.column(col, width=ancho, anchor=tk.CENTER)
        
        # Tags para colores según estado
        self.tree_citas.tag_configure('programada', background='#d5f4e6')
        self.tree_citas.tag_configure('completada', background='#e8f4f8')
        
        # Evento de selección
        self.tree_citas.bind('<<TreeviewSelect>>', self.on_seleccionar_cita)
        
        # Doble clic para ver paciente
        self.tree_citas.bind('<Double-1>', lambda e: self.ver_info_paciente())
        
        # Empaquetar
        self.tree_citas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar datos iniciales
        self.cargar_mis_citas()
        
    def cargar_mis_citas(self):
        """Carga las citas del doctor para hoy"""
        for item in self.tree_citas.get_children():
            self.tree_citas.delete(item)
        
        exito, resultado = DBCitas.obtener_citas_doctor_hoy(self.id_doctor)
        
        if exito:
            for cita in resultado:
                tag = 'programada' if cita['estado'] == 'Programada' else 'completada'
                self.tree_citas.insert("", tk.END, 
                    values=(
                        cita['hora'],
                        cita['paciente'],
                        f"{cita['edad']} años",
                        cita['sexo'],
                        cita['telefono'] or 'N/A',
                        cita['estado']
                    ),
                    tags=(tag,),
                    iid=cita['id_cita']  # Usar ID de cita como identificador
                )
            
            total = len(resultado)
            programadas = sum(1 for c in resultado if c['estado'] == 'Programada')
            self.lbl_info.config(
                text=f"Total: {total} citas | Programadas: {programadas} | Completadas: {total - programadas}"
            )
        else:
            messagebox.showerror("Error", resultado, parent=self.ventana)
            self.lbl_info.config(text="Error al cargar citas")
    
    def on_seleccionar_cita(self, event):
        """Evento cuando se selecciona una cita"""
        seleccion = self.tree_citas.selection()
        if seleccion:
            self.cita_seleccionada = int(seleccion[0])  # ID de la cita
    
    def ver_info_paciente(self):
        """Muestra información completa del paciente de la cita seleccionada"""
        if not self.cita_seleccionada:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione una cita de la lista",
                parent=self.ventana
            )
            return
        
        # Obtener información completa
        exito, info = DBCitas.obtener_info_completa_cita(self.cita_seleccionada)
        
        if not exito:
            messagebox.showerror("Error", info, parent=self.ventana)
            return
        
        # Crear ventana de información
        ventana_info = tk.Toplevel(self.ventana)
        ventana_info.title(f"Información del Paciente - {info['paciente']['nombre']}")
        ventana_info.geometry("600x550")
        ventana_info.configure(bg='#ffffff')
        ventana_info.resizable(False, False)
        
        # Centrar ventana
        ventana_info.update_idletasks()
        x = (ventana_info.winfo_screenwidth() // 2) - 300
        y = (ventana_info.winfo_screenheight() // 2) - 275
        ventana_info.geometry(f'600x550+{x}+{y}')
        
        # Header
        header = tk.Frame(ventana_info, bg='#27ae60', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="INFORMACIÓN DEL PACIENTE",
            font=("Arial", 14, "bold"),
            bg='#27ae60',
            fg='white'
        ).pack(expand=True)
        
        # Contenido
        contenido = tk.Frame(ventana_info, bg='#ffffff')
        contenido.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Función para crear campos
        def crear_info(label, valor, row):
            tk.Label(
                contenido,
                text=label,
                font=("Arial", 10, "bold"),
                bg='#ffffff',
                fg='#2c3e50',
                anchor='w'
            ).grid(row=row, column=0, sticky='w', pady=8, padx=(0, 20))
            
            tk.Label(
                contenido,
                text=valor,
                font=("Arial", 10),
                bg='#ffffff',
                fg='#34495e',
                anchor='w'
            ).grid(row=row, column=1, sticky='w', pady=8)
        
        # Mostrar datos
        pac = info['paciente']
        row = 0
        
        crear_info("ID Paciente:", pac['id'], row); row += 1
        crear_info("Nombre Completo:", pac['nombre'], row); row += 1
        crear_info("Edad:", f"{pac['edad']} años", row); row += 1
        crear_info("Sexo:", pac['sexo'], row); row += 1
        crear_info("Fecha de Nacimiento:", pac['fecha_nacimiento'], row); row += 1
        crear_info("Estatura:", f"{pac['estatura']} m", row); row += 1
        crear_info("Teléfono:", pac['telefono'] or 'No registrado', row); row += 1
        crear_info("Dirección:", pac['direccion'] or 'No registrada', row); row += 1
        
        # Separador
        ttk.Separator(contenido, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky='ew', pady=15
        )
        row += 1
        
        # Información de la cita
        tk.Label(
            contenido,
            text="INFORMACIÓN DE LA CITA",
            font=("Arial", 11, "bold"),
            bg='#ffffff',
            fg='#0077be'
        ).grid(row=row, column=0, columnspan=2, sticky='w', pady=(10, 15))
        row += 1
        
        crear_info("Fecha:", info['fecha'], row); row += 1
        crear_info("Hora:", info['hora'], row); row += 1
        crear_info("Estado:", info['estado'], row); row += 1
        
        # Botón cerrar
        tk.Button(
            ventana_info,
            text="Cerrar",
            font=("Arial", 10, "bold"),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            bd=0,
            cursor="hand2",
            command=ventana_info.destroy,
            padx=30,
            pady=8
        ).pack(pady=20)
    
    def abrir_ventana_receta(self):
        """Abre ventana para seleccionar medicamentos y generar receta"""
        if not self.cita_seleccionada:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione una cita de la lista",
                parent=self.ventana
            )
            return
        
        # Obtener información completa de la cita
        exito, info_cita = DBCitas.obtener_info_completa_cita(self.cita_seleccionada)
        if not exito:
            messagebox.showerror("Error", info_cita, parent=self.ventana)
            return
        
        # Crear ventana de receta
        ventana_receta = tk.Toplevel(self.ventana)
        ventana_receta.title("Generar Receta Médica")
        ventana_receta.geometry("600x750")
        ventana_receta.configure(bg='#ffffff')
        ventana_receta.resizable(False, False)
        
        # Centrar
        ventana_receta.update_idletasks()
        x = (ventana_receta.winfo_screenwidth() // 2) - 300
        y = (ventana_receta.winfo_screenheight() // 2) - 375
        ventana_receta.geometry(f'600x750+{x}+{y}')
        
        # Header
        header = tk.Frame(ventana_receta, bg='#9b59b6', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="GENERAR RECETA MÉDICA",
            font=("Arial", 14, "bold"),
            bg='#9b59b6',
            fg='white'
        ).pack(expand=True)
        
        # Contenido con scroll
        canvas = tk.Canvas(ventana_receta, bg='#ffffff')
        scrollbar = ttk.Scrollbar(ventana_receta, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido
        contenido = tk.Frame(scrollable_frame, bg='#ffffff')
        contenido.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Info paciente
        tk.Label(
            contenido,
            text=f"Paciente: {info_cita['paciente']['nombre']}",
            font=("Arial", 11, "bold"),
            bg='#ffffff',
            fg='#2c3e50'
        ).pack(anchor='w', pady=5)
        
        tk.Label(
            contenido,
            text=f"Fecha: {info_cita['fecha']} | Hora: {info_cita['hora']}",
            font=("Arial", 9),
            bg='#ffffff',
            fg='#7f8c8d'
        ).pack(anchor='w', pady=(0, 20))
        
        # NUEVO: Sección de Diagnóstico
        tk.Label(
            contenido,
            text="Diagnóstico:",
            font=("Arial", 10, "bold"),
            bg='#ffffff',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(10, 5))
        
        frame_diagnostico = tk.Frame(contenido, bg='#f8f9fa', relief='solid', bd=1)
        frame_diagnostico.pack(fill='x', pady=5)
        
        text_diagnostico = tk.Text(
            frame_diagnostico,
            height=4,
            width=60,
            font=("Arial", 10),
            wrap=tk.WORD,
            padx=5,
            pady=5
        )
        text_diagnostico.pack(fill='x', padx=2, pady=2)
        text_diagnostico.insert("1.0", "Ingrese el diagnóstico del paciente...")
        
        # Obtener medicamentos disponibles
        exito_med, medicamentos = DBMedicamentos.obtener_todos_medicamentos()
        
        if not exito_med or not medicamentos:
            tk.Label(
                contenido,
                text="No hay medicamentos disponibles",
                font=("Arial", 10),
                bg='#ffffff',
                fg='#e74c3c'
            ).pack(pady=20)
            return
        
        # Lista para almacenar medicamentos seleccionados con sus indicaciones
        medicamentos_seleccionados = []
        
        # Frame para lista de medicamentos seleccionados
        tk.Label(
            contenido,
            text="Medicamentos a recetar:",
            font=("Arial", 10, "bold"),
            bg='#ffffff',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(10, 5))
        
        # Frame con scrollbar para medicamentos
        frame_lista = tk.Frame(contenido, bg='#f8f9fa', relief='solid', bd=1)
        frame_lista.pack(fill='both', expand=True, pady=5)
        
        scroll_lista = tk.Scrollbar(frame_lista)
        scroll_lista.pack(side='right', fill='y')
        
        listbox_medicamentos = tk.Listbox(
            frame_lista,
            font=("Arial", 9),
            bg='#f8f9fa',
            yscrollcommand=scroll_lista.set,
            height=6
        )
        listbox_medicamentos.pack(side='left', fill='both', expand=True)
        scroll_lista.config(command=listbox_medicamentos.yview)
        
        # Frame para agregar medicamento
        frame_agregar = tk.Frame(contenido, bg='#ffffff')
        frame_agregar.pack(fill='x', pady=10)
        
        tk.Label(
            frame_agregar,
            text="Seleccionar medicamento:",
            font=("Arial", 9, "bold"),
            bg='#ffffff',
            fg='#2c3e50'
        ).grid(row=0, column=0, sticky='w', pady=2)
        
        # Combobox de medicamentos
        medicamentos_nombres = [f"{med['nombre']} ({med['via_administracion']}) - {med['presentacion']}" 
                                for med in medicamentos]
        
        combo_medicamento = ttk.Combobox(
            frame_agregar,
            values=medicamentos_nombres,
            state="readonly",
            font=("Arial", 9),
            width=45
        )
        combo_medicamento.grid(row=1, column=0, pady=5, sticky='ew')
        if medicamentos_nombres:
            combo_medicamento.current(0)
        
        tk.Label(
            frame_agregar,
            text="Indicaciones:",
            font=("Arial", 9, "bold"),
            bg='#ffffff',
            fg='#2c3e50'
        ).grid(row=2, column=0, sticky='w', pady=(10, 2))
        
        text_indicaciones = tk.Text(
            frame_agregar,
            height=3,
            width=45,
            font=("Arial", 9),
            wrap=tk.WORD
        )
        text_indicaciones.grid(row=3, column=0, pady=5)
        text_indicaciones.insert("1.0", "Tomar 1 tableta cada 8 horas durante 7 días")
        
        # Botones para agregar y eliminar
        frame_botones = tk.Frame(frame_agregar, bg='#ffffff')
        frame_botones.grid(row=4, column=0, pady=10)
        
        def agregar_medicamento():
            if not combo_medicamento.get():
                messagebox.showwarning("Advertencia", "Seleccione un medicamento", parent=ventana_receta)
                return
            
            indicaciones = text_indicaciones.get("1.0", tk.END).strip()
            if not indicaciones:
                messagebox.showwarning("Advertencia", "Ingrese las indicaciones", parent=ventana_receta)
                return
            
            idx = combo_medicamento.current()
            medicamento_sel = medicamentos[idx]
            
            # Agregar a la lista
            medicamentos_seleccionados.append({
                'medicamento': medicamento_sel,
                'indicaciones': indicaciones
            })
            
            # Actualizar listbox
            texto_lista = f"{medicamento_sel['nombre']} - {indicaciones[:50]}..."
            listbox_medicamentos.insert(tk.END, texto_lista)
            
            # Limpiar campos
            text_indicaciones.delete("1.0", tk.END)
            text_indicaciones.insert("1.0", "Tomar 1 tableta cada 8 horas durante 7 días")
        
        def eliminar_medicamento():
            seleccion = listbox_medicamentos.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un medicamento de la lista", parent=ventana_receta)
                return
            
            idx = seleccion[0]
            listbox_medicamentos.delete(idx)
            medicamentos_seleccionados.pop(idx)
        
        btn_agregar = tk.Button(
            frame_botones,
            text="+ Agregar",
            font=("Arial", 9, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#219a52",
            bd=0,
            cursor="hand2",
            command=agregar_medicamento,
            padx=15,
            pady=5
        )
        btn_agregar.pack(side='left', padx=5)
        
        btn_eliminar = tk.Button(
            frame_botones,
            text="- Eliminar",
            font=("Arial", 9, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            bd=0,
            cursor="hand2",
            command=eliminar_medicamento,
            padx=15,
            pady=5
        )
        btn_eliminar.pack(side='left', padx=5)
        
        # Botón generar
        def generar():
            # Validar diagnóstico
            diagnostico = text_diagnostico.get("1.0", tk.END).strip()
            if not diagnostico or diagnostico == "Ingrese el diagnóstico del paciente...":
                messagebox.showwarning("Advertencia", "Ingrese el diagnóstico del paciente", parent=ventana_receta)
                return
            
            if not medicamentos_seleccionados:
                messagebox.showwarning("Advertencia", "Agregue al menos un medicamento", parent=ventana_receta)
                return
            
            # Generar PDF con diagnóstico
            resultado = self.generar_receta_pdf(info_cita, medicamentos_seleccionados, diagnostico)
            
            if resultado:
                # Marcar la cita como completada
                exito_actualizar = DBCitas.actualizar_estado_cita(self.cita_seleccionada, 'Completada')
                
                if exito_actualizar:
                    messagebox.showinfo(
                        "Éxito",
                        "Receta generada correctamente y cita marcada como completada",
                        parent=self.ventana
                    )
                    # Recargar la lista de citas
                    self.cargar_mis_citas()
                else:
                    messagebox.showwarning(
                        "Advertencia",
                        "Receta generada pero no se pudo actualizar el estado de la cita",
                        parent=self.ventana
                    )
                
                ventana_receta.destroy()
        
        btn_generar = tk.Button(
            contenido,
            text="Generar Receta PDF",
            font=("Arial", 11, "bold"),
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            bd=0,
            cursor="hand2",
            command=generar,
            padx=30,
            pady=10
        )
        btn_generar.pack(pady=15)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def generar_receta_pdf(self, info_cita, medicamentos_seleccionados, diagnostico):
        """Genera un PDF de receta médica con múltiples medicamentos y diagnóstico."""
        try:
            # Crear carpeta si no existe
            if not os.path.exists("recetas"):
                os.makedirs("recetas")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folio = f"RX-{timestamp}"
            nombre_archivo = f"recetas/receta_{info_cita['paciente']['nombre'].replace(' ', '_')}_{timestamp}.pdf"

            # Documento
            doc = SimpleDocTemplate(
                nombre_archivo,
                pagesize=letter,
                topMargin=0.8*inch,
                bottomMargin=0.8*inch,
                leftMargin=0.8*inch,
                rightMargin=0.8*inch
            )

            elementos = []
            styles = getSampleStyleSheet()

            # ---------------- ESTILOS ----------------
            estilo_header = ParagraphStyle(
                'Header',
                fontName='Helvetica',
                fontSize=10,
                alignment=TA_CENTER,
                leading=12
            )

            estilo_titulo = ParagraphStyle(
                'Titulo',
                fontName='Helvetica-Bold',
                fontSize=18,
                alignment=TA_CENTER,
                spaceAfter=20
            )

            estilo_seccion = ParagraphStyle(
                'Seccion',
                fontName='Helvetica-Bold',
                fontSize=12,
                leading=14,
                spaceBefore=16,
                spaceAfter=6
            )

            estilo_texto = ParagraphStyle(
                'Texto',
                fontName='Helvetica',
                fontSize=10,
                leading=13,
            )

            estilo_folio = ParagraphStyle(
                'Folio',
                fontName='Helvetica',
                fontSize=9,
                alignment=TA_RIGHT
            )

            # ---------------- LOGO ----------------
            try:
                logo = Image("logo_cruz.jpg", width=1.2*inch, height=1.2*inch)
                logo.hAlign = "CENTER"
                elementos.append(logo)
                elementos.append(Spacer(1, 0.1 * inch))
            except:
                pass

            # ---------------- ENCABEZADO ----------------
            elementos.append(Paragraph("NÚCLEO DE DIAGNÓSTICO", estilo_header))
            elementos.append(Paragraph("Av. Principal #123 • Tel: (555) 123-4567", estilo_header))
            elementos.append(Paragraph("Email: info@nucleodiagnostico.com", estilo_header))
            elementos.append(Spacer(1, 0.2*inch))

            # Línea simple
            elementos.append(HRFlowable(width="100%", thickness=1, color=colors.black))
            elementos.append(Spacer(1, 0.2*inch))

            # Folio
            elementos.append(Paragraph(f"<b>Folio:</b> {folio}", estilo_folio))
            elementos.append(Spacer(1, 0.1*inch))

            # ---------------- TÍTULO ----------------
            elementos.append(Paragraph("RECETA MÉDICA", estilo_titulo))

            # ---------------- INFORMACIÓN DEL MÉDICO ----------------
            elementos.append(Paragraph("Información del Médico", estilo_seccion))
            elementos.append(Paragraph(f"<b>Nombre:</b> {info_cita['doctor']['nombre']}", estilo_texto))
            elementos.append(Paragraph(f"<b>Especialidad:</b> {info_cita['doctor']['especialidad']}", estilo_texto))

            # ---------------- INFORMACIÓN DEL PACIENTE ----------------
            elementos.append(Paragraph("Información del Paciente", estilo_seccion))
            elementos.append(Paragraph(f"<b>Nombre:</b> {info_cita['paciente']['nombre']}", estilo_texto))
            elementos.append(Paragraph(f"<b>Edad:</b> {info_cita['paciente']['edad']} años", estilo_texto))
            elementos.append(Paragraph(f"<b>Sexo:</b> {info_cita['paciente']['sexo']}", estilo_texto))
            elementos.append(Paragraph(f"<b>Fecha:</b> {info_cita['fecha']}", estilo_texto))
            elementos.append(Paragraph(f"<b>Hora:</b> {info_cita['hora']}", estilo_texto))

            # ---------------- DIAGNÓSTICO ----------------
            elementos.append(Paragraph("Diagnóstico", estilo_seccion))
            elementos.append(Paragraph(diagnostico, estilo_texto))

            # ---------------- MEDICAMENTOS ----------------
            elementos.append(Paragraph("Tratamiento Recetado", estilo_seccion))
            
            for i, item in enumerate(medicamentos_seleccionados, 1):
                medicamento = item['medicamento']
                indicaciones = item['indicaciones']
                
                try:
                    texto_medicamento = f"{medicamento['nombre']} ({medicamento['presentacion']}) – {medicamento['via_administracion']}"
                except:
                    texto_medicamento = str(medicamento)
                
                elementos.append(Paragraph(f"<b>{i}. Medicamento:</b> {texto_medicamento}", estilo_texto))
                elementos.append(Paragraph(f"<b>Indicaciones:</b> {indicaciones}", estilo_texto))
                elementos.append(Spacer(1, 0.15*inch))

            # ---------------- PIE DE PÁGINA ----------------
            elementos.append(Spacer(1, 0.5*inch))
            elementos.append(HRFlowable(width="100%", thickness=0.7, color=colors.gray))
            elementos.append(Paragraph(
                "Esta receta es válida únicamente para la fecha indicada. "
                "El mal uso de medicamentos puede poner en riesgo su salud.",
                estilo_texto
            ))

            doc.build(elementos)
            
            return True

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}", parent=self.ventana)
            return False