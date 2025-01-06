import streamlit as st
import os
import random
from PIL import Image, ImageEnhance
import numpy as np

# Function to apply a glitch effect to an image
def apply_glitch(image):
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Apply random row shifts for glitch effect
    num_rows = img_array.shape[0]
    shift = random.randint(1, 30)  # Shift by 1 to 30 pixels
    for i in range(num_rows):
        if random.random() < 0.1:  # 10% chance to apply a shift to a row
            img_array[i] = np.roll(img_array[i], shift, axis=0)
    
    # Convert back to image
    glitched_image = Image.fromarray(img_array)
    return glitched_image

# Function to pick a random image from a folder
def pick_random_image(folder_path):
    images = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg'))]
    if not images:
        raise ValueError("No image files found in the folder.")
    random_image = random.choice(images)
    image_path = os.path.join(folder_path, random_image)
    return image_path

# Function to save the glitched image, overwriting the original
def save_glitched_image(original_path, glitched_image):
    glitched_image.save(original_path)

# Streamlit app
def main():
    st.title("Glitch image data sets")
    st.button("break another one")
    folder_path = "glics"

    if folder_path and os.path.exists(folder_path):
        try:
            # Pick a random image
            image_path = pick_random_image(folder_path)
            #st.image(image_path, caption="Original Image", use_column_width=True)
            st.image(image_path, "Original Image", 300)
            # Load the image
            image = Image.open(image_path)
            
            # Apply glitch effect
            glitched_image = apply_glitch(image)
            
            # Display the glitched image
            #st.image(glitched_image, "Glitched Image", use_column_width=True)
            width = 300
            st.image(glitched_image, "Glitched Image", width)
            # Overwrite the original image with the glitched version
            save_glitched_image(image_path, glitched_image)
            st.success(f"Glitched image saved and overwritten {image_path}.")
        
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please provide a valid folder path.")

if __name__ == "__main__":
    main()
