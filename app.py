import os
from flask import Flask, request, send_file
from PIL import Image
from rembg import remove

app = Flask(__name__)

@app.route('/procesar_imagen', methods=['POST'])
def procesar_imagen():
    if 'imagen' not in request.files:
        return 'No se ha enviado ninguna imagen', 400

    imagen = request.files['imagen']

    if not imagen.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return 'Formato de imagen no soportado', 400

    # Abrir la imagen con PIL
    img = Image.open(imagen)

    # Guardar la imagen temporalmente para pasarla a rembg
    img = img.resize((240, 288), Image.LANCZOS)
    img.save('temp_input.png')

    # Eliminar fondo con rembg
    input_path = 'temp_input.png'
    output_path = 'temp_output.png'
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input_data = i.read()
            output_data = remove(input_data)    
            o.write(output_data)

    # Abrir la imagen sin fondo con PIL
    img = Image.open(output_path)

    # Cargar la imagen sin fondo con PIL
    background = Image.new("RGB", img.size, (255, 255, 255))

    # Pega la imagen PNG en la nueva imagen blanca
    background.paste(img, mask=img.split()[3])
    

    img = background.resize((240, 288), Image.LANCZOS)

    # Guarda la imagen resultante en formato JPG
    img.save("temp_image.jpg", dpi=(300, 300))

    return send_file('temp_image.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
