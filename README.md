# 📦 Automatizador de impresión GLS Ecomm / GLS Ecomm Printing Automator  
**Versión: 1.0 — Julio 2025**

---

## 🇪🇸 Español

### ✅ ¿Qué hace este programa?
Automatiza la entrada y la impresión de múltiples SKUs en el sistema GLS Ecomm, evitando la tarea manual repetitiva.

### 🖥️ Requisitos
- Windows 10 u 11  
- GLS Ecomm abierto y maximizado  
- Archivo CSV con SKUs

### 📝 Formato del CSV
- Separado por punto y coma (`;`)  
- Debe tener una columna llamada exactamente **`Sku`**, por ejemplo:
  Order;Customer;Sku;Status;Date...

### 🚦 Cómo usarlo
1. Abre GLS Ecomm y maximiza la ventana.  
2. Asegúrate de que la casilla **“Include barcode”** esté desmarcada.  
3. Ejecuta `automatica.exe`.  
4. Selecciona el archivo CSV.  
5. Presiona **“Ejecutar”**.  
6. No toques el teclado ni el ratón durante la ejecución.  
7. El programa realizará automáticamente:
 - Ingreso del SKU  
 - Marcado de “Include barcode”  
 - Establecer cantidad = “1”  
 - Impresión  
 - Confirmación en botón “Continue”  
8. Al terminar, aparecerá:
   ✅ Todos los SKUs han sido procesados


### ℹ️ Notas importantes
- La casilla “Include barcode” se marca **solo una vez** al inicio.  
- Si algo falla, revisa que:
- El CSV tenga la columna **Sku**  
- Use punto y coma (`;`) como separador  
- GLS esté visible y maximizado en pantalla

---
