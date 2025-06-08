# Speechify Médico

Aplicación de escritorio para convertir capítulos de libros médicos a audio utilizando Google Cloud Text-to-Speech.

## Requisitos
- Python 3.10+
- ffmpeg instalado y accesible en el PATH (requerido por pydub)

## Instalación
```bash
pip install -r requirements.txt
```

Cree un archivo `.env` con la clave de Google Cloud:
```
GOOGLE_APPLICATION_CREDENTIALS=/ruta/a/credenciales.json
```

## Ejecución
```bash
python main.py
```

Los archivos subidos se guardarán en la carpeta `uploads/` y los audios generados en `output_audios/`.
