import pandas as pd
import PySimpleGUI as sg
import pyautogui
import time

time.sleep(5) # Tiempo para ir a la ventana de GLS

pyautogui.write('TEST123456') # Escribe donde este el cursor
pyautogui.press('tab')
pyautogui.write('1')
pyautogui.press('tab')
pyautogui.press('space') # Marcar checkbox
pyautogui.press('tab') # Para llegar a print
pyautogui.press('enter') # Imprimir

# === Función para leer CSV y extraer columna de SKUs ===
def load_skus_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        sku_column = df.iloc[:, 4] # Columna 5 > indice 4
        return sku_column.dropna().tolist()
    except Exception as e:
        sg.popup_error("Error al leer el archivo:", str(e))
        return []

# === Función placeholder para automatizar GLS Ecomm ===
def process_skus_in_gls(sku_list, window):
    for idx, sku in enumerate(sku_list, 1):
        # Aquí iría el código con pyautogui:
        # 1. Pegar SKU
        # 2. Marcar checkbox
        # 3. Pulsar botón Print
        # 4. Esperar a que termine la impresión

        window['PROGRESS-'].update(f'Procesando SKU {idx} de {len(sku_list)}...')

        # Simulación de tiempo de espera (quitar luego)
        import time
        time.sleep(1)

    sg.popup("Proceso completado.")

# === Función principal para la GUI ===
def main():
    sg.theme('SystemDefault')

    layout = [
        [sg.Text("Selecciona el archivo CSV con los SKUs:")],
        [sg.InputText(key='-FILE-', enable_events=True), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
        [sg.Text("SKUs encontrados: "), sg.Text("0", key='-SKU_COUNT-')],
        [sg.Button("Ejecutar", disabled=True), sg.Exit()],
        [sg.Text("", key='-PROGRESS-', size=(40, 1), text_color='blue')]
    ]

    window = sg.Window("Automatizador de impresión GLS Ecomm", layout)

    sku_list = []

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        if event == '-FILE':
            file_path = values['-FILE']
            sku_list = load_skus_from_csv(file_path)
            window['-SKU_COUNT'].update(str(len(sku_list)))
            window['Ejecutar'].update(disabled=False if sku_list else True)

        if event == 'Ejecutar':
            window['-PROGRESS-'].update('Iniciando procesamiento...')
            window.refresh()
            process_skus_in_gls(sku_list, window)

    window.close()

if __name__ == "__main__":
    main()