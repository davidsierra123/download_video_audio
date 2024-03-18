from flask import Flask, render_template, request, jsonify, send_file
from pytube import YouTube
from pathlib import Path
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descargar_audio', methods=['GET'])
def descargar_audio():
    url = request.args.get('url')
    fileName = request.args.get('fileName')

    if not url:
        return jsonify({'error': 'Por favor, proporcione un enlace de YouTube.'}), 400

    try:
        yt = YouTube(url)
        audio_title = yt.title

        # Carpeta de descargas del usuario
        downloads_folder = str(Path.home() / "Downloads")

        # Crear carpeta si no existe
        os.makedirs(downloads_folder, exist_ok=True)

        # Nombre del archivo de audio basado en el título del video de YouTube
        audio_file_path = os.path.join(downloads_folder, f"{fileName}.mp3")

        # Descargar el audio
        audio = yt.streams.filter(only_audio=True).first()
        audio.download(output_path=downloads_folder, filename=f"{fileName}.mp3")

        # Devolver el archivo de audio descargado y el nombre del archivo original
        return send_file(audio_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/descargar_video', methods=['GET'])
def descargar_video():
    url = request.args.get('url')
    fileName = request.args.get('fileName')

    if not url:
        return jsonify({'error': 'Por favor, proporcione un enlace de YouTube.'}), 400

    try:
        yt = YouTube(url)
        video_title = yt.title

        # Carpeta de descargas del usuario
        downloads_folder = str(Path.home() / "Downloads")

        # Crear carpeta si no existe
        os.makedirs(downloads_folder, exist_ok=True)

        # Nombre del archivo de video basado en el título del video de YouTube
        video_file_path = os.path.join(downloads_folder, f"{fileName}.mp4")

        # Descargar el video
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video.download(output_path=downloads_folder, filename=f"{fileName}.mp4")

        # Devolver el archivo de video descargado y el nombre del archivo original
        return send_file(video_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
