import streamlit as st
import os
import random
from PIL import Image, ImageEnhance
import numpy as np

# Function to apply a stronger glitch effect to an image
def apply_stronger_glitch(image):
    # Convert image to numpy array
    img_array = np.array(image)

    # Apply random row and column shifts for glitch effect
    num_rows, num_cols, _ = img_array.shape

    for i in range(num_rows):
        if random.random() < 0.2:  # 20% chance to apply a shift to a row
            shift = random.randint(-50, 50)  # Shift by -50 to 50 pixels
            img_array[i] = np.roll(img_array[i], shift, axis=0)

    for j in range(num_cols):
        if random.random() < 0.1:  # 10% chance to apply a shift to a column
            shift = random.randint(-30, 30)  # Shift by -30 to 30 pixels
            img_array[:, j] = np.roll(img_array[:, j], shift, axis=0)

    # Introduce RGB channel distortions
    for channel in range(3):  # Loop over RGB channels
        if random.random() < 0.3:  # 30% chance to distort a channel
            distortion = random.randint(-20, 20)
            img_array[:, :, channel] = np.roll(img_array[:, :, channel], distortion, axis=0)

    # Add random noise to intensify the glitch effect
    noise = np.random.randint(0, 50, img_array.shape, dtype='uint8')
    img_array = np.clip(img_array + noise, 0, 255)

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
    st.title("Glitch Image Data Sets")
    if st.button("Break Another One"):
        folder_path = "glics"

        if folder_path and os.path.exists(folder_path):
            try:
                # Pick a random image
                image_path = pick_random_image(folder_path)
                st.image(image_path, caption="Original Image", use_column_width=True)

                # Load the image
                image = Image.open(image_path)

                # Apply glitch effect
                glitched_image = apply_stronger_glitch(image)

                # Display the glitched image
                st.image(glitched_image, caption="Glitched Image", use_column_width=True)

                # Overwrite the original image with the glitched version
                save_glitched_image(image_path, glitched_image)
                st.success(f"Glitched image saved and overwritten: {image_path}.")

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please provide a valid folder path.")

if __name__ == "__main__":
    main()
