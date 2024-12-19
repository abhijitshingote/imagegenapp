from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import os
from dotenv import load_dotenv
import requests
import base64
from io import BytesIO

load_dotenv()
app = Flask(__name__)

runpod_key = os.getenv('RUNPOD_KEY')
endpoint_id = os.getenv('ENDPOINT_ID')

# Folder to store generated and saved images
OUTPUT_FOLDER = "static/generated"
SAVED_FOLDER = "static/saved"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(SAVED_FOLDER, exist_ok=True)


def filter_none_values(data):
    return {key: value for key, value in data.items() if value is not None}


def run_inference(prompt, respb64=None):
    url = f"https://api.runpod.ai/v2/{endpoint_id}/runsync"
    headers = {
        "accept": "application/json",
        "authorization": runpod_key,
        "content-type": "application/json"
    }
    input = {
        "prompt": prompt,
        "input_image": respb64
    }
    data = {"input": filter_none_values(input)}

    response = requests.post(url, headers=headers, json=data)
    return response


def get_img(response):
    resp = response.json()
    imgb64 = resp['output']['images'][0]
    image_data = base64.b64decode(imgb64)
    image = Image.open(BytesIO(image_data))
    return image


@app.route("/", methods=["GET", "POST"])
def home():
    image_path = None
    prompt = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        image_path = generate_image(prompt)

    return render_template("index.html", image_path=image_path, prompt=prompt)


@app.route("/save/<filename>")
def save_image(filename):
    """Save the generated image to the saved folder."""
    source_path = os.path.join(OUTPUT_FOLDER, filename)
    destination_path = os.path.join(SAVED_FOLDER, filename)
    if os.path.exists(source_path):
        os.rename(source_path, destination_path)
    return redirect(url_for("home"))


@app.route("/saved")
def saved_images():
    """Display all saved images."""
    saved_files = os.listdir(SAVED_FOLDER)
    return render_template("saved.html", saved_files=saved_files)


@app.route("/static/saved/<filename>")
def serve_saved_image(filename):
    """Serve saved images."""
    return send_from_directory(SAVED_FOLDER, filename)

@app.route("/static/generated/<filename>")
def serve_image(filename):
    """Serve generated images."""
    return send_from_directory(OUTPUT_FOLDER, filename)

def generate_image(prompt):
    """Generate an image with the given text prompt."""
    response = run_inference(prompt)
    image = get_img(response)

    # Draw the prompt text on the image
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), prompt, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (512 - text_width) // 2
    y = (512 - text_height) // 2

    draw.text((x, y), prompt, fill="black", font=font)

    # Save the image
    image_name = f"generated_{prompt.replace(' ', '_')}.png"
    image_path = os.path.join(OUTPUT_FOLDER, image_name)
    image.save(image_path)
    return image_name


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
