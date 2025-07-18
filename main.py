import pandas as pd
import PySimpleGUI as sg
import pyautogui
import time

# === Coordenadas fijas capturadas ===
TEXT_FIELD_COORDS        = (218, 365)
LABELS_FIELD_COORDS      = (220, 421)
CHECKBOX_COORDS          = (31, 470)
PRINT_BUTTON_COORDS      = (892, 932)
CONTINUE_BUTTON_COORDS   = (1154, 537)

# === Función para leer CSV y extraer columna de SKUs ===
def load_skus_from_csv(file_path):
    try:
        df = pd.read_csv(file_path, sep=';')
        if 'Sku' not in df.columns:
            sg.popup_error("El CSV no contiene una columna llamada 'Sku'.")
            return []
        return df['Sku'].dropna().astype(str).tolist()
    except Exception as e:
        sg.popup_error("Error al leer el archivo CSV:\n" + str(e))
        return []

# === Automatiza el ingreso de los SKUs en GLS Ecomm ===
def process_skus_in_gls(sku_list, window):
    sg.popup("El proceso comenzará en 5 segundos.\nPor favor, deja la ventana de GLS maximizada y activa.")
    time.sleep(5)

    # ✅ Solo una vez: marcar checkbox
    pyautogui.click(CHECKBOX_COORDS)
    time.sleep(0.3)

    for idx, sku in enumerate(sku_list, 1):
        window['-PROGRESS-'].update(f'Procesando SKU {idx} de {len(sku_list)}...')
        window['Ejecutar'].update(disabled=True)
        window.refresh()

        # Campo de texto: SKU
        pyautogui.click(TEXT_FIELD_COORDS)
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(sku)
        time.sleep(0.3)

        # Campo: Number of labels (siempre 1)
        pyautogui.click(LABELS_FIELD_COORDS)
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write('1')
        time.sleep(0.2)

        # Botón: Print
        pyautogui.click(PRINT_BUTTON_COORDS)
        time.sleep(2)  # Espera que aparezca el popup

        # Botón: Continue del popup
        pyautogui.click(CONTINUE_BUTTON_COORDS)
        time.sleep(0.5)

    sg.popup("✅ Todos los SKUs han sido procesados.")
    window['Ejecutar'].update(disabled=False)
    window['-PROGRESS-'].update("")

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

        if event == '-FILE-':
            file_path = values['-FILE-']
            sku_list = load_skus_from_csv(file_path)
            window['-SKU_COUNT-'].update(str(len(sku_list)))
            window['Ejecutar'].update(disabled=False if sku_list else True)

        if event == 'Ejecutar':
            window['-PROGRESS-'].update('Iniciando procesamiento...')
            window.refresh()
            process_skus_in_gls(sku_list, window)

    window.close()

if __name__ == "__main__":
    main()