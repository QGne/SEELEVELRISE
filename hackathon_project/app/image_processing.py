from PIL import Image, ImageEnhance
import openai
import os
import requests
import json
from openai import OpenAI

# Set your API key (you can use Flask's config to retrieve it securely)

# def apply_underwater_effect(filepath):
#     # Open the image
#     img = Image.open(filepath)
#
#     # Apply color enhancements to simulate underwater effect
#     img = ImageEnhance.Color(img).enhance(0.5)  # Reduce color intensity
#     img = ImageEnhance.Brightness(img).enhance(0.8)  # Dim the image slightly
#
#     # Apply a blue-green overlay
#     blue_green = Image.new('RGB', img.size, (0, 70, 150))
#     img = Image.blend(img, blue_green, alpha=0.3)
#
#     # Save the processed image
#     processed_filepath = filepath.replace('.jpg', '_underwater.jpg')  # Change filename for processed image
#     img.save(processed_filepath)
#     return processed_filepath

def apply_underwater_effect(filepath):
    # Open the image
    img = Image.open(filepath)

    # Apply color enhancements to simulate underwater effect
    img = ImageEnhance.Color(img).enhance(0.8)  # Reduce color intensity
    img = ImageEnhance.Brightness(img).enhance(0.9)  # Dim the image slightly

    # Apply a blue-green overlay
    blue_green = Image.new('RGB', img.size, (0, 70, 150))
    img = Image.blend(img, blue_green, alpha=0.1)

    # Save the processed image
    directory, filename = os.path.split(filepath)
    processed_filename = filename.replace('.jpg', '_underwater.jpg')
    processed_filepath = os.path.join(directory, processed_filename)
    img.save(processed_filepath)

    # Return the relative path only
    return f'uploads/{processed_filename}'

def apply_underwater_effect_ai(filepath, elevation_before, elevation_after, api_key):
    openai.api_key = api_key  # Set the API key

    # Convert to PNG if not already in that format
    # if not filepath.endswith('.png'):
    #     filepath = convert_to_png(filepath)

    # Ensure the image is under 4 MB
    # if not check_file_size(filepath):
    #     resize_image(filepath)

    # Define the prompt with elevation details
    prompt = f"A realistic underwater version of this ubran area at elevation {elevation_after} meters, showing the effects of submersion. I want to see water everywhere, lots of water, floods, destruction!!!!"
    client = OpenAI()

    try:
        # Open the specified image file to upload
        with open(filepath, "rb") as image_file:
            # Send the image to OpenAI to create a variation
            response = client.images.create_variation(
                image=image_file,
                n=1,
                size="1024x1024",
                timeout=60
            )
        print("Full API Response:", response)

        # Check if 'data' exists in response and has elements
        if hasattr(response, 'data') and response.data:
            image_url = response.data[0].url
            print("Extracted Image URL:", image_url)

            # Download the generated image
            download_response = requests.get(image_url)
            if download_response.status_code == 200:
                # Save the downloaded image with a new name
                directory, filename = os.path.split(filepath)
                processed_filename = filename.replace('.jpg', '_underwater.jpg')
                processed_filepath = os.path.join(directory, processed_filename)
                with open(processed_filepath, "wb") as f:
                    f.write(download_response.content)
                print("Image downloaded and saved as", processed_filepath)
                return processed_filepath  # Return the local file path
            else:
                print("Error: Failed to download the image from URL.")
                return None
        else:
            print("Error: No data returned from OpenAI API.")
            return None

    except Exception as e:
        print("Exception in apply_underwater_effect_ai:", e)
        return None

    # try:
    #     # Open the specified image file to upload
    #     with open(filepath, "rb") as image_file:
    #         # Send the image to OpenAI to create a variation
    #         response = client.images.create_variation(
    #             image=image_file,
    #             n=1,
    #             size="1024x1024",
    #             timeout = 60
    #         )
    #     print("Full API Response:", response)
    #     # Check for a successful response and retrieve the generated image URL
    #
    #     print("Type of response:", type(response))
    #     print("Response keys:", response.keys() if isinstance(response, dict) else dir(response))
    #     print("Full response:", response)
    #
    #     # Check if 'data' exists in response and has elements
    #     if hasattr(response, 'data') and response.data:
    #         image_url = response.data[0].url
    #         print("Extracted Image URL:", image_url)
    #         return image_url
    #     else:
    #         print("Error: No data returned from OpenAI API.")
    #         return None
    #
    #     print("Generated Image URL:", image_url)
    #
    #     # Download the generated image
    #     download_response = requests.get(image_url)
    #     if download_response.status_code == 200:
    #         # Save the downloaded image with a new name
    #         directory, filename = os.path.split(filepath)
    #         processed_filename = filename.replace('.jpg', '_underwater.jpg')
    #         processed_filepath = os.path.join(directory, processed_filename)
    #         with open(processed_filepath, "wb") as f:
    #             f.write(download_response.content)
    #         print("Image downloaded and saved as", processed_filepath)
    #         return processed_filepath
    #     else:
    #         print("Error: Failed to download the image from URL.")
    #         return None
    #
    # except Exception as e:
    #     print("Exception in apply_underwater_effect_ai:", e)
    #     return None

def apply_underwater_effect_ai2(filepath, elevation_before, elevation_after, api_key):
    # Set the API key for this function
    openai.api_key = api_key

    # Generate an image with DALL-E based on elevation change
    prompt = f"A realistic underwater version of this landscape at elevation {elevation_after} meters, showing the effects of submersion."

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    # Get the URL of the generated image
    image_url = response['data'][0]['url']

    # Download the image from the URL
    response = requests.get(image_url)
    if response.status_code == 200:
        # Save the image to the uploads directory
        directory, filename = os.path.split(filepath)
        processed_filename = filename.replace('.jpg', '_underwater.jpg')
        processed_filepath = os.path.join(directory, processed_filename)
        with open(processed_filepath, 'wb') as f:
            f.write(response.content)
        print(f"Processed image saved to {processed_filepath}")
        return f'uploads/{processed_filename}'
    else:
        print("Error: Failed to retrieve the generated image.")
        return None
