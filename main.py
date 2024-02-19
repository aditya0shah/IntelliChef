from flask import Flask, render_template, request, send_from_directory, jsonify
from PIL import Image
import datetime
import os
import base64
from io import BytesIO
from tools.recipe_modifier import upload_url, modify_recipe
from tools.recipe_generation import create_recipe

app = Flask(__name__)

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home_page():
    if request.method == 'POST':
        data = request.json
        if data["form_type"] == "modify":
            recipe_url = data["url"]
            query = data["query"]
            upload_url(recipe_url)
            response = modify_recipe(query)
        if data["form_type"] == "generate":
            ingredients = ", ".join(data["ingredients"])
            response = create_recipe(ingredients)
        return jsonify({"response": response})
    return render_template("index.html")

@app.route("/camera", methods=["GET", "POST"])
def camera_view():
    filename=''     # using filename variable to display video feed and captured image alternatively on the same page
    image_data_url = request.form.get('image')
    if request.method == 'POST':
        # Decode the base64 data URL to obtain the image data
        image_data = base64.b64decode(image_data_url.split(',')[1])
        # Create an image from the decoded data
        img = Image.open(BytesIO(image_data))
        # Generate a filename with the current date and time
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = f"img_{timestamp}.png"  # Change file extension to 'png'
        print(filename)
        # Save the image in PNG format
        file_path = os.path.join("files/", filename)
        img.save(file_path, 'PNG')
        error_message = 'Image successfully captured'
        # use if you want to display all the images in the folder
        # image_files = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('camera_view.html', filename=filename)
    return render_template('camera_view.html', filename=filename)

@app.route('/capturedimage/<filename>')
def captured(filename):
    # returned the image path to template where it is rendered
    return send_from_directory("files", path=filename)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port="80")