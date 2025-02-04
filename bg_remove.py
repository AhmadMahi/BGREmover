import os
from io import BytesIO

import streamlit as st
from PIL import Image
from rembg import remove

# Configure the Streamlit app
st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## Remove Background from Your Image")
st.write(
    ":dog: Upload an image to see the background magically removed. You can download the full quality image from the sidebar. "
    "This code is open source and available [here](https://github.com/tyler-simons/BackgroundRemoval) on GitHub. "
    "Special thanks to the [rembg library](https://github.com/danielgatis/rembg) :grin:"
)
st.sidebar.write("## Upload & Download :gear:")

# Maximum allowed file size: 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def convert_image_to_bytes(img: Image.Image) -> bytes:
    """
    Convert a PIL Image to bytes.
    """
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def process_uploaded_image(uploaded_file) -> Image.Image:
    """
    Open the uploaded file as an image.
    """
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception as e:
        st.error(f"Error opening image: {e}")
        return None

def display_images(original: Image.Image, processed: Image.Image) -> None:
    """
    Display the original and processed images side by side.
    """
    col1, col2 = st.columns(2)
    with col1:
        st.write("Original Image :camera:")
        st.image(original)
    with col2:
        st.write("Processed Image :wrench:")
        st.image(processed)

def main():
    # File uploader on the sidebar
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
            return

        original_image = process_uploaded_image(uploaded_file)
        if original_image is None:
            return  # Error message already shown
    else:
        # Use a default image if no file is uploaded.
        default_image_path = "./zebra.jpg"
        if os.path.exists(default_image_path):
            original_image = Image.open(default_image_path)
        else:
            st.warning("No image uploaded and default image not found. Please upload an image.")
            return

    # Remove the background from the image using rembg
    try:
        processed_image = remove(original_image)
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return

    # Display images side by side
    display_images(original_image, processed_image)

    # Provide a download button for the processed image
    st.sidebar.markdown("\n")
    st.sidebar.download_button(
        "Download Processed Image",
        data=convert_image_to_bytes(processed_image),
        file_name="processed.png",
        mime="image/png"
    )

if __name__ == "__main__":
    main()
