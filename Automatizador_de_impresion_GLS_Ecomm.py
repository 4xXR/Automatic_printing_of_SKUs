import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import time
import keyboard

# Coordenadas capturadas
TEXT_FIELD_COORDS = (218, 365)
LABELS_FIELD_COORDS = (220, 421)
CHECKBOX_COORDS = (31, 470)
PRINT_BUTTON_COORDS = (892, 932)
CONTINUE_BUTTON_COORDS = (1154, 537)

def load_skus_from_csv(path):
    try:
        df = pd.read_csv(path, sep=';')
        if 'Sku' not in df.columns:
            messagebox.showerror("Error", "CSV debe contener columna 'Sku'.")
            return None
        skus = df['Sku'].dropna().astype(str).tolist()
        return skus
    except Exception as e:
        messagebox.showerror("Error al leer CSV", str(e))
        return None
    
def process_skus(skus, status_label, run_button):
    messagebox.showinfo("Inicio", "Comienza en 5 segundos despues del OK. \nDeja GLS maximizado y casilla 'Include barcode' sin marcar. \nPresiona 'q' para detener")
    time.sleep(5)

    # Marcar checkbox una sola vez
    pyautogui.click(CHECKBOX_COORDS)
    time.sleep(0.3)

    for idx, sku in enumerate(skus, 1):
        if keyboard.is_pressed('q'):
            messagebox.showinfo("Detenido", f"🛑 Proceso detenido tras {idx-1} SKUs.")
            break

        status_label.config(text=f"Procesando SKU {idx}/{len(skus)}")
        run_button.config(state=tk.DISABLED)
        root.update_idletasks()

        pyautogui.click(TEXT_FIELD_COORDS); time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a'); pyautogui.press('backspace')
        pyautogui.write(sku); time.sleep(0.3)

        pyautogui.click(LABELS_FIELD_COORDS); time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'a'); pyautogui.press('backspace')
        pyautogui.write('1'); time.sleep(0.2)

        pyautogui.click(PRINT_BUTTON_COORDS); time.sleep(2)
        pyautogui.click(CONTINUE_BUTTON_COORDS); time.sleep(0.5)

    else:
        messagebox.showinfo("Listo", "✅ Todos los SKUs han sido procesados.")

    status_label.config(text="")
    run_button.config(state=tk.NORMAL)

def select_file(path_var, count_label, run_button):
    path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not path:
        return
    path_var.set(path)
    skus = load_skus_from_csv(path)
    if skus is None:
        run_button.config(state=tk.DISABLED)
        count_label.config(text="0")
    else:
        count_label.config(text=str(len(skus)))
        run_button.config(state=tk.NORMAL)
        root.skus = skus

# --- Interfaz gráfica ---
root = tk.Tk()
root.title("Automatizador GLS Ecomm")
root.geometry("500x150")
root.resizable(False, False)

path_var = tk.StringVar()

tk.Label(root, text="Selecciona el archivo CSV con SKUs:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=path_var, width=40, state="readonly").grid(row=1, column=0, padx=10)
tk.Button(root, text="Browse...", command=lambda: select_file(path_var, count_label, run_button)).grid(row=1, column=1, padx=5)

tk.Label(root, text="SKUs encontrados:").grid(row=2, column=0, padx=10, sticky="w")
count_label = tk.Label(root, text="0")
count_label.grid(row=2, column=1, sticky="w")

run_button = tk.Button(root, text="Ejecutar", state=tk.DISABLED, command=lambda: process_skus(root.skus, status_label, run_button))
run_button.grid(row=3, column=0, pady=10)

status_label = tk.Label(root, text="", fg="blue")
status_label.grid(row=4, column=0, columnspan=2)

tk.Button(root, text="Exit", command=root.destroy).grid(row=3, column=1)

root.mainloop()
