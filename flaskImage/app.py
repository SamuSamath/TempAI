from flask import Flask, render_template, request, jsonify
import os
import random
import boto3
import base64
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-images', methods=['POST'])
def generate_images():
    data = request.json
    company_name = data['company_name']
    font = data['font']
    size = int(data['size'])
    template_height = int(data['template_height'])
    template_width = int(data['template_width'])
    background = data['background']
    product = data['product']
    num_images = int(data['num_images'])

    prompt_data = (
        f"Design a promotional template with high definition image for {company_name} with its name in the image "
        f"featuring the product '{product}' in center with the font style '{font}', "
        f"font size {size}, template width {template_width}px, and template height {template_height}px. "
        f"The background color should be {background}. With clear text with not many images but only one main image "
        f"as the main attraction. Also provide a description about {product} and place it in the center."
    )

  

    output_dir = "static/output"
    os.makedirs(output_dir, exist_ok=True)

    generated_images = []
    for i in range(num_images):
        seed = random.randint(0, 100000)
        payload = {
            "text_prompts": [{"text": prompt_data}],
            "cfg_scale": 12,
            "seed": seed,
            "steps": 80
        }
        body = json.dumps(payload)
        model_id = "stability.stable-diffusion-xl-v1"

        response = brk.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get("body").read().decode("utf-8"))
        artifact = response_body.get("artifacts")[0]
        image_encoded = artifact.get("base64").encode("utf-8")
        image_bytes = base64.b64decode(image_encoded)

        file_name = f"{output_dir}/generated-{seed}.png"
        with open(file_name, "wb") as f:
            f.write(image_bytes)

        generated_images.append(file_name)

    return jsonify({"images": generated_images})

if __name__ == '__main__':
    app.run(debug=True)
