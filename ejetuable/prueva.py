# TRABAJO HECHO POR TOMMY GUEVARA Y KERLY YAGUAL 3SC2
# Adaptado a una interfaz gráfica con Tkinter

import math
import tkinter as tk
from tkinter import ttk  # Usamos widgets 'themed' para un look más moderno

def resolver_ecuacion_segundo_orden(a, b, c):
    """
    Resuelve la ecuación ay'' + by' + cy = 0 y devuelve
    una cadena con los resultados. También guarda en el archivo.
    """
    
    ecuacion_str = f"Ecuación: {a}y'' {b:+}y' {c:+}y = 0\n"
    resultado_str = ""

    discriminante = b**2 - 4*a*c

    # Usar if/elif/else (match-case requiere Python 3.10+ y
    # es mejor usar if/elif para mantener compatibilidad si no se sabe la versión)
    
    if discriminante > 0:
        # Caso 1: Raíces reales y distintas
        r1 = (-b + math.sqrt(discriminante)) / (2*a)
        r2 = (-b - math.sqrt(discriminante)) / (2*a)
        
        resultado_str = (
            "Caso 1: Raíces reales y distintas\n"
            f"Raíz 1: {r1:.0f}\n"
            f"Raíz 2: {r2:.0f}\n"
            f"Solución general: y(x) = C1*e^({r1:.0f}x) + C2*e^({r2:.0f}x)\n"
        )

    elif discriminante == 0:
        # Caso 2: Raíces reales e iguales
        r = -b / (2*a)
        
        resultado_str = (
            "Caso 2: Raíces reales e iguales\n"
            f"Raíz doble: {r:.0f}\n"
            f"Solución general: y(x) = (C1 + C2*x)*e^({r:.0f}x)\n"
        )
        
    else:
        # Caso 3: Raíces complejas
        real = -b / (2*a)
        imag = math.sqrt(-discriminante) / (2*a)
        
        resultado_str = (
            "Caso 3: Raíces complejas\n"
            f"Raíces: {real:.0f} ± {imag:.0f}i\n"
            f"Solución general: y(x) = e^({real:.0f}x) * [C1*cos({imag:.0f}x) + C2*sin({imag:.0f}x)]\n"
        )

    # Escribir en el archivo de log (append)
    try:
        with open("lista_ecuaciones.txt", "a", encoding="utf-8") as archivo:
            archivo.write(ecuacion_str)
            archivo.write(resultado_str)
            archivo.write(f"\n" + "=" * 60 + "\n")
    except IOError as e:
        resultado_str += f"\nERROR: No se pudo escribir en lista_ecuaciones.txt: {e}"

    # Devolver la cadena completa para mostrar en la GUI
    return ecuacion_str + "\n" + resultado_str

def on_resolver_click():
    """
    Se ejecuta cuando el usuario presiona el botón "Resolver".
    Obtiene los valores, valida y muestra el resultado.
    """
    try:
        # Obtener valores de los campos de entrada
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        
        # Validación
        if a == 0:
            mostrar_resultado("Error: El coeficiente 'a' no puede ser 0 para una ecuación de segundo orden.")
            return

        # Calcular la solución
        resultado_completo = resolver_ecuacion_segundo_orden(a, b, c)
        
        # Mostrar el resultado en el widget de texto
        mostrar_resultado(resultado_completo)

    except ValueError:
        # Manejar error si la entrada no es un número
        mostrar_resultado("Error: Por favor ingrese valores numéricos válidos para a, b y c.")
    except Exception as e:
        # Manejar cualquier otro error inesperado
        mostrar_resultado(f"Error inesperado: {e}")

def mostrar_resultado(texto):
    """
    Limpia el cuadro de texto de resultados y muestra el nuevo texto.
    """
    output_text.config(state=tk.NORMAL)  # Habilitar para editar
    output_text.delete("1.0", tk.END)     # Limpiar contenido anterior
    output_text.insert(tk.END, texto)    # Insertar nuevo texto
    output_text.config(state=tk.DISABLED) # Deshabilitar para hacerlo solo lectura

def on_limpiar_click():
    """
    Limpia todos los campos de entrada y el área de resultados.
    """
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    entry_c.delete(0, tk.END)
    
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Los resultados aparecerán aquí.")
    output_text.config(state=tk.DISABLED)
    
    # Poner el foco de nuevo en el campo 'a'
    entry_a.focus_set()

# --- Configuración de la Ventana Principal ---
root = tk.Tk()
root.title("Resolutor de Ecuaciones Diferenciales")
root.geometry("500x550") # Tamaño inicial
root.minsize(400, 500)  # Tamaño mínimo

# Estilo
style = ttk.Style(root)
style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'

# Frame principal con padding
main_frame = ttk.Frame(root, padding="20 20 20 20")
main_frame.pack(fill=tk.BOTH, expand=True)

# --- Título y Descripción ---
title_label = ttk.Label(main_frame, text="Resolutor de Ecuaciones Diferenciales", 
                        font=("Arial", 16, "bold"))
title_label.pack(pady=(0, 5))

desc_label = ttk.Label(main_frame, text="Para la ecuación: ay'' + by' + cy = 0", 
                       font=("Arial", 11))
desc_label.pack(pady=(0, 20))

# --- Frame de Entradas (Inputs) ---
input_frame = ttk.Frame(main_frame)
input_frame.pack(fill=tk.X, pady=5)

# Configurar columnas para que se expandan
input_frame.columnconfigure(1, weight=1)

# Coeficiente 'a'
label_a = ttk.Label(input_frame, text="Coeficiente a (y''):", font=("Arial", 10))
label_a.grid(row=0, column=0, padx=5, pady=8, sticky=tk.W)
entry_a = ttk.Entry(input_frame, font=("Arial", 10), width=15)
entry_a.grid(row=0, column=1, padx=5, pady=8, sticky=tk.EW)

# Coeficiente 'b'
label_b = ttk.Label(input_frame, text="Coeficiente b (y'):", font=("Arial", 10))
label_b.grid(row=1, column=0, padx=5, pady=8, sticky=tk.W)
entry_b = ttk.Entry(input_frame, font=("Arial", 10), width=15)
entry_b.grid(row=1, column=1, padx=5, pady=8, sticky=tk.EW)

# Coeficiente 'c'
label_c = ttk.Label(input_frame, text="Coeficiente c (y):", font=("Arial", 10))
label_c.grid(row=2, column=0, padx=5, pady=8, sticky=tk.W)
entry_c = ttk.Entry(input_frame, font=("Arial", 10), width=15)
entry_c.grid(row=2, column=1, padx=5, pady=8, sticky=tk.EW)

# --- Frame de Botones ---
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=tk.X, pady=10)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

# Botón Resolver
resolver_btn = ttk.Button(button_frame, text="Resolver", command=on_resolver_click,
                          style='Accent.TButton')
resolver_btn.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)

# Botón Limpiar
limpiar_btn = ttk.Button(button_frame, text="Limpiar", command=on_limpiar_click)
limpiar_btn.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

# Definir un estilo 'Accent' para el botón principal
style.configure('Accent.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#0078d4')

# --- Frame de Resultados (Output) ---
output_frame = ttk.Frame(main_frame)
output_frame.pack(fill=tk.BOTH, expand=True, pady=10)

# Widget de Texto para mostrar resultados
output_text = tk.Text(output_frame, height=10, width=60, wrap=tk.WORD, 
                      font=("Courier New", 10), relief=tk.SOLID, borderwidth=1,
                      bg="#f0f0f0", state=tk.DISABLED)
output_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Scrollbar para el texto
scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)

# --- Créditos y estado inicial ---
footer_label = ttk.Label(main_frame, 
                         text="TRABAJO HECHO POR TOMMY GUEVARA Y KERLY YAGUAL 3SC2", 
                         font=("Arial", 8))
footer_label.pack(side=tk.BOTTOM, pady=(10, 0))

# Poner texto inicial y poner el foco
on_limpiar_click()

# --- Iniciar el bucle principal de la aplicación ---
root.mainloop()