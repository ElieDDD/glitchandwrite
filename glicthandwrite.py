import streamlit as st
import os
import random
from PIL import Image, ImageEnhance
from PIL import ImageOps
import numpy as np

# Function to apply a glitch effect to an image
def apply_glitch(image):
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Apply random row shifts for glitch effect
    num_rows = img_array.shape[0]
    #shift = random.randint(1, 30)  # Shift by 1 to 30 pixels
    shift = random.randint(1, 20)  # Shift by 1 to 70 pixels
    for i in range(num_rows):
        if random.random() < 0.7:  # i chnaged upeed from 0.1 10% chance to apply a shift to a row
            img_array[i] = np.roll(img_array[i], shift, axis=0)
    
    # Convert back to image
    glitched_image = Image.fromarray(img_array)
    return glitched_image
def apply_stronger_glitch_with_color(image):
    # Ensure the image is in RGB mode
    if image.mode != 'RGB':
        image = ImageOps.colorize(image.convert('L'), black="black", white="white")
    
    # Convert image to numpy array
    img_array = np.array(image)

    # Get dimensions
    if len(img_array.shape) == 2:  # Handle grayscale images
        img_array = np.stack((img_array,) * 3, axis=-1)  # Convert to RGB

    num_rows, num_cols, num_channels = img_array.shape

    # Apply row and column shifts for glitch effect
    for i in range(num_rows):
        if random.random() < 0.2:  # 20% chance to shift a row
            shift = random.randint(-50, 50)
            img_array[i] = np.roll(img_array[i], shift, axis=0)

    for j in range(num_cols):
        if random.random() < 0.1:  # 10% chance to shift a column
            shift = random.randint(-30, 30)
            img_array[:, j] = np.roll(img_array[:, j], shift, axis=0)

    # Introduce RGB channel distortions
    for channel in range(3):  # Loop over RGB channels
        if random.random() < 0.3:  # 30% chance to distort a channel
            distortion = random.randint(-20, 20)
            img_array[:, :, channel] = np.roll(img_array[:, :, channel], distortion, axis=0)

    # Add random colored stripes
    for _ in range(10):  # Add 10 random stripes
        stripe_start = random.randint(0, num_rows - 1)
        stripe_height = random.randint(1, 10)  # Stripe height between 1-10 pixels
        color = np.random.randint(0, 255, size=(1, num_cols, 3), dtype='uint8')  # Random RGB color
        img_array[stripe_start:stripe_start + stripe_height, :, :] = color

    # Add gradient colors to random sections
    for _ in range(5):  # Apply 5 gradient effects
        start_row = random.randint(0, num_rows - 1)
        end_row = min(start_row + random.randint(10, 50), num_rows - 1)
        gradient = np.linspace(0, 255, end_row - start_row, dtype='uint8')
        gradient_color = np.zeros((end_row - start_row, num_cols, 3), dtype='uint8')
        gradient_color[:, :, random.randint(0, 2)] = gradient[:, None]  # Apply gradient to a random channel
        img_array[start_row:end_row, :, :] = np.clip(img_array[start_row:end_row, :, :] + gradient_color, 0, 255)

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
#def save_glitched_image(original_path, glitched_image):
    #glitched_image.save(original_path)

def save_glitched_image(original_path, glitched_image):
    # Save the glitched image directly to the same path
    glitched_image.save(original_path)
    print(f"Image overwritten: {original_path}")


# Streamlit app
def main():
    st.title("Glitch & overwrite dubious data sets")
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
            #glitched_image = apply_glitch(image)
            glitched_image = apply_stronger_glitch_with_color(image)
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
