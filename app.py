"""
⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢰⣿⡿⠗⠀⠠⠄⡀⠀⠀⠀⠀
⠀⠀⠀⠀⡜⠁⠀⠀⠀⠀⠀⠈⠑⢶⣶⡄
⢀⣶⣦⣸⠀⢼⣟⡇⠀⠀⢀⣀⠀⠘⡿⠃
⠀⢿⣿⣿⣄⠒⠀⠠⢶⡂⢫⣿⢇⢀⠃⠀
⠀⠈⠻⣿⣿⣿⣶⣤⣀⣀⣀⣂⡠⠊⠀⠀
⠀⠀⠀⠃⠀⠀⠉⠙⠛⠿⣿⣿⣧⠀⠀⠀
⠀⠀⠘⡀⠀⠀⠀⠀⠀⠀⠘⣿⣿⡇⠀⠀
⠀⠀⠀⣷⣄⡀⠀⠀⠀⢀⣴⡟⠿⠃⠀⠀
⠀⠀⠀⢻⣿⣿⠉⠉⢹⣿⣿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠉⠁⠀⠀⠀⠉⠁

Desarrollo AlexWhite USER GIT AlexSo11
"""
import tkinter as tk
from tkinter import messagebox
import sys
from dbConfigXAMPP import DatabaseConfig

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar ventana principal temporalmente
        self.usuario_actual = None
        self.tipo_usuario = None
        self.login_window = None
        self.menu_window = None
        
        # Configurar cierre de aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        # Inicializar pool de conexiones
        print("Inicializando conexión a base de datos...")
        if not DatabaseConfig.inicializar_pool():
            messagebox.showerror("Error Fatal", 
                "No se pudo conectar a la base de datos.\n" +
                "Verifique la configuración en dbConfigXAMPP.py\n\n" +
                "Asegúrese de que:\n" +
                "1. XAMPP esté corriendo\n" +
                "2. MySQL esté activo (verde)\n" +
                "3. La base de datos 'nucleo_diagnostico' exista")
            self.root.destroy()
            sys.exit(1)
        
        print("✓ Conexión exitosa!")
        
        # Mostrar ventana de login después de un pequeño delay
        self.root.after(100, self.mostrar_login)
        
    def mostrar_login(self):
        """Muestra la ventana de login"""
        print("Mostrando ventana de login...")
        try:
            from login import LoginWindow
            self.login_window = LoginWindow(self.root, self.on_login_exitoso)
            print("✓ Ventana de login creada")
        except Exception as e:
            print(f"✗ Error al crear ventana de login: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al crear ventana de login:\n{str(e)}")
            self.cerrar_aplicacion()
        
    def on_login_exitoso(self, usuario, tipo):
        """Callback cuando el login es exitoso"""
        print(f"Login exitoso: {usuario} ({tipo})")
        self.usuario_actual = usuario
        self.tipo_usuario = tipo
        
        if tipo == "administrador":
            self.mostrar_menu_administrador()
        elif tipo == "empleado":
            self.mostrar_menu_empleado()
        elif tipo == "doctor":
            self.mostrar_menu_doctor()
        else:
            messagebox.showinfo("Info", f"Bienvenido {usuario}")
            self.cerrar_sesion()
            
    def mostrar_menu_administrador(self):
        """Muestra el menú principal del administrador"""
        print("Mostrando menú de administrador...")
        try:
            from MENUS.menuAdmin import MenuAdministrador
            self.menu_window = MenuAdministrador(self.root, self.usuario_actual, self.cerrar_sesion)
            print("✓ Menú de administrador creado")
        except Exception as e:
            print(f"✗ Error al crear menú: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al crear menú:\n{str(e)}")
            self.cerrar_aplicacion()
    
    def mostrar_menu_empleado(self):
        """Muestra el menú principal del empleado"""
        print("Mostrando menú de empleado...")
        try:
            from MENUS.menuEmpleado import MenuEmpleado
            self.menu_window = MenuEmpleado(self.root, self.usuario_actual, self.cerrar_sesion)
            print("✓ Menú de empleado creado")
        except Exception as e:
            print(f"✗ Error al crear menú: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al crear menú:\n{str(e)}")
            self.cerrar_aplicacion()
    
    def mostrar_menu_doctor(self):
        """Muestra el menú principal del doctor"""
        print("Mostrando menú de doctor...")
        try:
            from MENUS.menuDoctor import MenuDoctor
            self.menu_window = MenuDoctor(self.root, self.usuario_actual, self.cerrar_sesion)
            print("✓ Menú de doctor creado")
        except Exception as e:
            print(f"✗ Error al crear menú: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al crear menú:\n{str(e)}")
            self.cerrar_aplicacion()
    
    def cerrar_sesion(self):
        """Cierra la sesión actual y vuelve al login"""
        print("Cerrando sesión...")
        self.usuario_actual = None
        self.tipo_usuario = None
        
        # Destruir la ventana del menú si existe
        if self.menu_window and hasattr(self.menu_window, 'ventana'):
            try:
                self.menu_window.ventana.destroy()
            except:
                pass
        
        self.menu_window = None
        
        # Mostrar login nuevamente
        self.mostrar_login()
        
    def cerrar_aplicacion(self):
        """Cierra la aplicación correctamente"""
        print("Cerrando aplicación...")
        DatabaseConfig.cerrar_pool()
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass
        sys.exit(0)
        
    def run(self):
        """Inicia la aplicación"""
        print("Iniciando mainloop...")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n\nAplicación interrumpida por el usuario")
            self.cerrar_aplicacion()
        except Exception as e:
            print(f"\n\nError fatal: {e}")
            import traceback
            traceback.print_exc()
            self.cerrar_aplicacion()

if __name__ == "__main__":
    print("=" * 60)
    print("INICIANDO APLICACIÓN - NÚCLEO DE DIAGNÓSTICO")
    print("=" * 60)
    
    try:
        app = App()
        app.run()
    except KeyboardInterrupt:
        print("\n\nAplicación cancelada durante la inicialización")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
