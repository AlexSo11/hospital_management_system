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

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from UI.empleados import UIEmpleados
from UI.doctores import UIDoctores
from UI.pacientes import UIPacientes
from UI.citas import UICitas
from UI.medicamentos import UIMedicamentos

class MenuAdministrador:
    def __init__(self, parent, usuario, callback_logout):
        self.usuario = usuario
        self.callback_logout = callback_logout  # Callback para volver al login
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Panel Administrativo - {usuario}")
        self.ventana.geometry("800x800")  # Aumentado para asegurar visibilidad
        self.ventana.resizable(False, False)
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Crear interfaz
        self.crear_widgets()
        
        # Configurar cierre (X de la ventana)
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir_programa)
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        width = 800
        height = 800
        x = (self.ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (height // 2)
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')
        
    def crear_widgets(self):
        """Crea los widgets del menú principal con diseño médico"""        
        try:
            # Intentar cargar imagen de fondo
            fondo = Image.open("fondo1.jpg")  # Puedes usar la misma que login
            fondo = fondo.resize((800, 800), Image.Resampling.LANCZOS)
            fondo = fondo.filter(ImageFilter.GaussianBlur(radius=4))
            
            # Oscurecer más para mejor contraste
            enhancer = ImageEnhance.Brightness(fondo)
            fondo = enhancer.enhance(0.4)
            
            self.fondo_img = ImageTk.PhotoImage(fondo)
            fondo_label = tk.Label(self.ventana, image=self.fondo_img)
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            print("✓ Imagen de fondo cargada")
            
        except:
            print("Sin imagen de fondo, usando colores médicos")
            self.ventana.configure(bg="#e8f4f8")
            fondo_label = tk.Label(self.ventana, bg="#e8f4f8")
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # === HEADER AZUL MÉDICO ===
        header = tk.Frame(self.ventana, bg="#0077be", height=100)
        header.pack(fill="x", side="top")
        
        # Título del sistema
        titulo_sistema = tk.Label(
            header,
            text="SISTEMA DE GESTIÓN HOSPITALARIA",
            font=("Arial", 14, "bold"),
            bg="#0077be",
            fg="white"
        ).pack(pady=(20, 5))
        
        # Subtítulo
        subtitulo = tk.Label(
            header,
            text="Panel de Administración",
            font=("Arial", 10),
            bg="#0077be",
            fg="#e0f0ff"
        )
        subtitulo.pack(pady=(0, 10))
        
        # === CONTENEDOR PRINCIPAL CON SCROLL (por si acaso) ===
        main_container = tk.Frame(self.ventana, bg="#e8f4f8")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # === PANEL PRINCIPAL BLANCO ===
        main_panel = tk.Frame(main_container, bg="#ffffff", relief="flat", bd=1)
        main_panel.pack(fill="both", expand=True, padx=10, pady=10)
        
        # === CONTENIDO DEL PANEL ===
        # Frame superior para bienvenida
        top_frame = tk.Frame(main_panel, bg="#ffffff")
        top_frame.pack(fill="x", padx=30, pady=20)
        
        # Bienvenida
        tk.Label(
            top_frame,
            text=f"Bienvenido/a, {self.usuario}",
            font=("Arial", 16, "bold"),
            fg="#0077be",
            bg="#ffffff"
        ).pack(anchor="w")
        
        tk.Label(
            top_frame,
            text="Seleccione el módulo a gestionar:",
            font=("Arial", 10),
            fg="#5a5a5a",
            bg="#ffffff"
        ).pack(anchor="w", pady=(5, 0))
        
        # Separador decorativo
        separator = tk.Frame(main_panel, height=2, bg="#e0e0e0")
        separator.pack(fill="x", pady=10)
        
        # === BOTONES DE MÓDULOS ===
        modules_frame = tk.Frame(main_panel, bg="#ffffff")
        modules_frame.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Botón EMPLEADOS
        self.crear_boton_modulo(
            modules_frame,
            "GESTIÓN DE EMPLEADOS",
            "Administrar personal del hospital",
            "#0077be",
            self.abrir_empleados
        ).pack(fill="x", pady=8)
        
        # Botón DOCTORES
        self.crear_boton_modulo(
            modules_frame,
            "GESTIÓN DE DOCTORES",
            "Administrar personal médico",
            "#00a8cc",
            self.abrir_doctores
        ).pack(fill="x", pady=8)
        
        # Botón PACIENTES
        self.crear_boton_modulo(
            modules_frame,
            "GESTIÓN DE PACIENTES",
            "Administrar pacientes del hospital",
            "#0ac0e9",
            self.abrir_pacientes
        ).pack(fill="x", pady=8)

        # Botón CITAS
        self.crear_boton_modulo(
            modules_frame,
            "GESTIÓN DE CITAS",
            "Administrar citas médicas",
            "#16a099",
            self.abrir_citas
        ).pack(fill="x", pady=8)

        # Botón MEDICAMENTOS
        self.crear_boton_modulo(
            modules_frame,
            "GESTIÓN DE MEDICAMENTOS",
            "Administrar inventario de medicamentos",
            "#27ae88",
            self.abrir_medicamentos
        ).pack(fill="x", pady=8)
        
        # Espacio flexible para empujar el footer hacia abajo
        spacer = tk.Frame(main_panel, bg="#ffffff", height=20)
        spacer.pack(fill="x")
        
        # === FOOTER CON BOTONES ===
        footer_frame = tk.Frame(main_panel, bg="#ffffff")
        footer_frame.pack(fill="x", side="bottom", padx=30, pady=20)
        
        # Frame para botones de acción
        action_buttons_frame = tk.Frame(footer_frame, bg="#ffffff")
        action_buttons_frame.pack(pady=10)
        
        # Botón cerrar sesión
        btn_logout = tk.Button(
            action_buttons_frame,
            text="Cerrar Sesión",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.cerrar_sesion,
            padx=20,
            pady=8,
            relief="flat"
        )
        btn_logout.pack(side="left", padx=10)
        
        # Efecto hover logout
        btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="#2980b9"))
        btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg="#3498db"))
        
        # Botón salir del programa
        btn_exit = tk.Button(
            action_buttons_frame,
            text="Salir del Programa",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.salir_programa,
            padx=20,
            pady=8,
            relief="flat"
        )
        btn_exit.pack(side="left", padx=10)
        
        # Efecto hover exit
        btn_exit.bind("<Enter>", lambda e: btn_exit.config(bg="#c0392b"))
        btn_exit.bind("<Leave>", lambda e: btn_exit.config(bg="#e74c3c"))
        
        # Info versión
        tk.Label(
            footer_frame,
            text="Núcleo de Diagnóstico v1.0 - 2025",
            font=("Arial", 8),
            fg="#95a5a6",
            bg="#ffffff"
        ).pack(pady=(10, 0))
    
    def crear_boton_modulo(self, parent, titulo, descripcion, color, comando):
        """Crea un botón estilizado para cada módulo"""
        # Frame contenedor del botón
        btn_frame = tk.Frame(parent, bg="#ffffff", height=60)
        btn_frame.pack_propagate(False)
        
        # Frame del botón (simula el botón completo)
        boton = tk.Frame(
            btn_frame,
            bg=color,
            cursor="hand2" if comando else "arrow",
            relief="flat",
            bd=0,
            height=60
        )
        boton.pack(fill="both", expand=True)
        
        # Contenido del botón
        contenido = tk.Frame(boton, bg=color)
        contenido.pack(fill="both", expand=True, padx=20, pady=12)
        
        # Título del módulo
        lbl_titulo = tk.Label(
            contenido,
            text=titulo,
            font=("Arial", 12, "bold"),
            fg="white",
            bg=color,
            anchor="w"
        )
        lbl_titulo.pack(fill="x")
        
        # Descripción
        lbl_desc = tk.Label(
            contenido,
            text=descripcion,
            font=("Arial", 9),
            fg="#f0f0f0",
            bg=color,
            anchor="w"
        )
        lbl_desc.pack(fill="x", pady=(2, 0))
        
        # Hacer todo clickeable si hay comando
        if comando:
            def on_click(e):
                comando()
            
            def on_enter(e):
                # Oscurecer al hacer hover
                if color == "#0077be":
                    new_color = "#005a8f"
                elif color == "#00a8cc":
                    new_color = "#0086a3"
                elif color == "#0ac0e9":
                    new_color = "#1693af"
                elif color == "#16a099":
                    new_color = "#138680"
                elif color == "#27ae88":
                    new_color = "#1f8e6e"
                else:
                    new_color = color
                
                boton.config(bg=new_color)
                contenido.config(bg=new_color)
                lbl_titulo.config(bg=new_color)
                lbl_desc.config(bg=new_color)
            
            def on_leave(e):
                boton.config(bg=color)
                contenido.config(bg=color)
                lbl_titulo.config(bg=color)
                lbl_desc.config(bg=color)
            
            # Bind eventos
            for widget in [boton, contenido, lbl_titulo, lbl_desc]:
                widget.bind("<Button-1>", on_click)
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
        
        return btn_frame
        
    def abrir_empleados(self):
        """Abre el módulo de empleados"""
        print("Abriendo módulo de empleados...")
        try:
            UIEmpleados(self.ventana)
        except Exception as e:
            print(f"Error al abrir empleados: {e}")
            messagebox.showerror(
                "Error",
                f"No se pudo abrir el módulo de empleados:\n{str(e)}",
                parent=self.ventana
            )
        
    def abrir_doctores(self):
        """Abre el módulo de doctores"""
        print("Abriendo módulo de doctores...")
        try:
            UIDoctores(self.ventana)
        except Exception as e:
            print(f"Error al abrir doctores: {e}")
            messagebox.showerror(
                "Error",
                f"No se pudo abrir el módulo de doctores:\n{str(e)}",
                parent=self.ventana
            )

    def abrir_pacientes(self):
        """Abre el módulo de pacientes"""
        print("Abriendo módulo de pacientes...")
        try:
            UIPacientes(self.ventana)
        except Exception as e:
            print(f"Error al abrir pacientes: {e}")
            messagebox.showerror(
                "Error",
                f"No se pudo abrir el módulo de pacientes:\n{str(e)}",
                parent=self.ventana
            )

    def abrir_citas(self):
        """Abre el módulo de citas"""
        print("Abriendo módulo de citas...")
        try:
            UICitas(self.ventana)
        except Exception as e:
            print(f"Error al abrir citas: {e}")
            messagebox.showerror(
                "Error",
                f"No se pudo abrir el módulo de citas:\n{str(e)}",
                parent=self.ventana
            )
    
    def abrir_medicamentos(self):
        """Abre el módulo de medicamentos"""
        print("Abriendo módulo de medicamentos...")
        try:
            UIMedicamentos(self.ventana)
        except Exception as e:
            print(f"Error al abrir medicamentos: {e}")
            messagebox.showerror(
                "Error",
                f"No se pudo abrir el módulo de medicamentos:\n{str(e)}",
                parent=self.ventana
            )
    
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Desea cerrar sesión y volver al login?",
            parent=self.ventana
        )
        if respuesta:
            print("Cerrando sesión del usuario:", self.usuario)
            self.ventana.destroy()
            if self.callback_logout:
                self.callback_logout()
    
    def salir_programa(self):
        """Sale completamente del programa"""
        respuesta = messagebox.askyesno(
            "Salir del Programa",
            "¿Está seguro que desea salir completamente del programa?",
            parent=self.ventana
        )
        if respuesta:
            print("Saliendo del programa...")
            self.ventana.quit()
            self.ventana.destroy()
            import sys
            sys.exit(0)