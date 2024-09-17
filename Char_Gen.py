import json
import requests
from datetime import datetime
import openai
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Owl:
    def __init__(self, features):
        self.features = features
        self.owl_type = features['Type']

    def describe(self):
        description = (
            f"""Please create an image in a detailed, imaginative fantasy art style depicting an owl as a {self.owl_type}. 
            The owl should have {self.features['Owl Color']} feathers, 
            {self.features['Eye Shape']} eyes with {self.features['Eye Color']} color, and 
            wear detailed {self.features['Clothing']}. 
            It is holding a {self.features['Weapon']} in a pose that corresponds with its hobby ({self.features['Hobby']}). 
            The background should be a mystical location ({self.features['Vacation Spot']}) that evokes a sense of adventure. 
            The background should be minimalist to focus attention on the owl character."""
        )
        return description

class OwlImageGenerator:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY  

    def generate_image(self, description):
        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=description,
                quality="standard",
                n=1,  
                size="1024x1024"  
            )

            image_url = response.data[0].url
            return image_url  
        except Exception as e:
            print(f"Error generating the image: {e}")
            return None  

@app.route('/generate_owl', methods=['POST'])
def generate_owl():
    data = request.json

    features = {
        'Type': data.get('Type'),
        'Owl Color': data.get('Owl Color'),
        'Eye Shape': data.get('Eye Shape'),
        'Eye Color': data.get('Eye Color'),
        'Clothing': data.get('Clothing'),
        'Weapon': data.get('Weapon'),
        'Hobby': data.get('Hobby'),
        'Vacation Spot': data.get('Vacation Spot')
    }

    owl = Owl(features)
    description = owl.describe()

    image_generator = OwlImageGenerator()
    image_url = image_generator.generate_image(description)

    if image_url:
        return jsonify({
            'description': description,
            'image_url': image_url  
        })
    else:
        return jsonify({'error': 'Image generation failed'}), 500

if __name__ == "__main__":
    app.run(debug=True)