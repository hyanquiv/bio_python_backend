# 🧬 Bio Python Backend - API de Alineamiento de Secuencias

Un backend simple y eficiente desarrollado en Flask para el procesamiento de alineamientos múltiples de secuencias de proteínas. Proporciona una API REST que ejecuta algoritmos de alineamiento y devuelve resultados procesados.

## 📋 Descripción del Backend

Esta API REST permite recibir archivos FASTA con secuencias sin alinear, procesarlas utilizando algoritmos de alineamiento múltiple, y devolver los resultados en formato JSON con codificación base64 para facilitar la transferencia de datos.

## 🏗️ Arquitectura Backend (`app.py`)

### Componentes Principales
- **API REST** con Flask
- **Endpoint único** `/align` para procesamiento
- **Gestión automática** de archivos temporales
- **Ejecución** de algoritmos de alineamiento
- **Respuesta JSON** con datos base64
- **Limpieza automática** de recursos

## 🚀 Características Principales

### ⚡ **API Simple y Eficiente**
- ✅ Endpoint único para todo el procesamiento
- ✅ Manejo automático de archivos temporales
- ✅ Identificadores únicos (UUID) para evitar conflictos
- ✅ Limpieza automática de recursos
- ✅ Manejo de errores robusto

### 🔬 **Procesamiento de Alineamientos**
- **Recepción**: Archivos FASTA via multipart/form-data
- **Procesamiento**: Ejecución de algoritmos MUSCLE y MSA
- **Codificación**: Resultados en base64 para transferencia
- **Respuesta**: JSON con ambos alineamientos

### 📁 **Gestión de Archivos**
- Carpetas automáticas `in/` y `out/`
- Nombres únicos con UUID para evitar colisiones
- Limpieza automática post-procesamiento
- Manejo de errores en operaciones de archivo

## 🔧 Estructura del Código

### **Aplicación Flask**
```python
app = Flask(__name__)

# Crear carpetas si no existen
os.makedirs("in", exist_ok=True)
os.makedirs("out", exist_ok=True)
```

### **Endpoint Principal**
```python
@app.route("/align", methods=["POST"])
def align():
    # Procesamiento completo de alineamiento
```

## 🎯 Flujo de Trabajo

### 1. **Recepción de Archivo**
```python
# Crear ruta única para input
input_filename = f"{uuid.uuid4()}.fasta"
input_path = os.path.join("in", input_filename)

# Guardar input
file = request.files["file"]
file.save(input_path)
```

### 2. **Procesamiento de Alineamiento**
```python
# Ejecutar alineamiento → devuelve 2 paths
muscle_path, msa_path = run_alignment(input_path, os.path.join("out", str(uuid.uuid4())))
```

### 3. **Codificación de Resultados**
```python
# Leer ambos archivos y codificarlos en base64
with open(muscle_path, "rb") as f1, open(msa_path, "rb") as f2:
    muscle_data = base64.b64encode(f1.read()).decode('utf-8')
    msa_data = base64.b64encode(f2.read()).decode('utf-8')
```

### 4. **Limpieza de Recursos**
```python
# Borrar archivos temporales
try:
    os.remove(input_path)
    os.remove(muscle_path)
    os.remove(msa_path)
except Exception as e:
    print(f"Error al limpiar archivos: {e}")
```

### 5. **Respuesta JSON**
```python
# Devolver ambos como JSON base64
return jsonify({
    "aligned_muscle.fasta": muscle_data,
    "aligned_msa.fasta": msa_data
})
```

## 📡 API Reference

### **POST /align**

Procesa un archivo FASTA y devuelve los alineamientos generados.

#### **Request**
- **Método**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parámetros**:
  - `file`: Archivo FASTA con secuencias sin alinear

#### **Response**
```json
{
    "aligned_muscle.fasta": "base64_encoded_content",
    "aligned_msa.fasta": "base64_encoded_content"
}
```

#### **Códigos de Estado**
- `200`: Procesamiento exitoso
- `400`: Error en el archivo o formato
- `500`: Error interno del servidor

## 🔄 Integración con Algoritmos

### **Función run_alignment()**
El backend depende de una función externa `run_alignment()` que debe:

```python
def run_alignment(input_path, output_base_path):
    """
    Ejecuta algoritmos de alineamiento múltiple
    
    Args:
        input_path (str): Ruta del archivo FASTA de entrada
        output_base_path (str): Ruta base para archivos de salida
    
    Returns:
        tuple: (muscle_path, msa_path) - Rutas de los archivos generados
    """
    # Implementación de algoritmos MUSCLE y MSA
    return muscle_output_path, msa_output_path
```

## 🛠️ Tecnologías Utilizadas

- **Flask**: Framework web minimalista
- **UUID**: Generación de identificadores únicos
- **Base64**: Codificación de archivos binarios
- **OS**: Gestión del sistema de archivos
- **JSON**: Formato de respuesta de la API

## ⚙️ Configuración y Despliegue

### **Instalación**
```bash
pip install flask
```

### **Estructura de Directorios**
```
bio_python_backend/
├── app.py              # Aplicación Flask principal
├── aligner.py          # Módulo de algoritmos de alineamiento
├── in/                 # Carpeta de archivos de entrada (auto-creada)
├── out/                # Carpeta de archivos de salida (auto-creada)
└── requirements.txt    # Dependencias
```

### **Ejecución en Desarrollo**
```bash
python app.py
```
- Servidor disponible en: `http://localhost:5000`
- Modo debug habilitado por defecto

### **Ejecución en Producción**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔒 Consideraciones de Seguridad

### **Validaciones Recomendadas**
- Validación de tipos de archivo (FASTA únicamente)
- Límites de tamaño de archivo
- Sanitización de nombres de archivo
- Rate limiting para prevenir abuso

### **Ejemplo de Validación**
```python
# Validar extensión de archivo
allowed_extensions = {'.fasta', '.fa', '.txt'}
if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
    return jsonify({"error": "Formato de archivo no válido"}), 400

# Validar tamaño de archivo
if len(file.read()) > 10 * 1024 * 1024:  # 10MB máximo
    return jsonify({"error": "Archivo demasiado grande"}), 400
```

## 🚨 Manejo de Errores

### **Tipos de Errores Manejados**
- Errores de lectura/escritura de archivos
- Fallos en algoritmos de alineamiento
- Problemas de codificación base64
- Errores de limpieza de archivos temporales

### **Logging Recomendado**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# En el endpoint
logger.info(f"Procesando archivo: {file.filename}")
logger.error(f"Error en alineamiento: {str(e)}")
```

## 📊 Ejemplo de Uso

### **cURL**
```bash
curl -X POST \
  http://localhost:5000/align \
  -F "file=@sequences.fasta"
```

### **Python Requests**
```python
import requests

url = "http://localhost:5000/align"
files = {"file": open("sequences.fasta", "rb")}
response = requests.post(url, files=files)
result = response.json()
```

### **JavaScript/Fetch**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/align', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🎯 Ventajas del Diseño

### **Simplicidad**
- Un solo endpoint para toda la funcionalidad
- Interfaz clara y directa
- Mínimas dependencias

### **Eficiencia**
- Procesamiento automático de archivos temporales
- Codificación base64 para transferencia segura
- Limpieza automática de recursos

### **Escalabilidad**
- Diseño stateless
- Fácil integración con load balancers
- Compatible con contenedores Docker

### **Mantenibilidad**
- Código limpio y bien estructurado
- Separación de responsabilidades
- Fácil testing y debugging

Este backend proporciona una base sólida y eficiente para el procesamiento de alineamientos de secuencias, manteniendo la simplicidad mientras ofrece todas las funcionalidades necesarias para una aplicación de bioinformática robusta.