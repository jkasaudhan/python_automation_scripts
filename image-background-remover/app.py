import streamlit as st
from PIL import Image, ImageColor
from io import BytesIO
from rembg import remove
import os
from typing import Tuple
from PIL.Image import Image as PILImage
from copy import deepcopy


class ImageProcessor:
    def __init__(self, image):
        self.image = image

    def remove_background(self):
        return remove(self.image)

    @staticmethod
    def change_background(image, background_alpha: float = 1.0, background_hex: str = "#000000"):
        """ 
        image: PIL Image (RGBA)
        matte: PIL Image (grayscale, if 255 it is foreground)
        background_alpha: float
        background_hex: string
        """
        img = deepcopy(image)
        if image.mode != "RGBA":
            img = img.convert("RGBA")

        background_color = ImageColor.getrgb(background_hex)
        background_alpha = int(255 * background_alpha)
        background = Image.new(
            "RGBA", img.size, color=background_color + (background_alpha,))
        background.paste(img, mask=ImageProcessor.matte)
        return background

    @staticmethod
    def matte(img_input):
        # Implement matte logic
        pass


class ImageDownloader:
    @staticmethod
    def download_button(pil_image, filename: str, fmt: str, label="Download"):
        if fmt not in ["jpg", "png"]:
            raise ValueError(
                "Unknown image format (Available: jpg, png - case sensitive)")

        pil_format = "JPEG" if fmt == "jpg" else "PNG"
        file_format = "jpg" if fmt == "jpg" else "png"
        mime = "image/jpeg" if fmt == "jpg" else "image/png"

        buf = BytesIO()
        pil_image.save(buf, format=pil_format)

        return st.download_button(
            label=label,
            data=buf.getvalue(),
            file_name=f'{filename}.{file_format}',
            mime=mime,
        )


class ImageUploader:
    @staticmethod
    def upload_image():
        return st.file_uploader(
            label="Upload your photo here",
            accept_multiple_files=False, type=["png", "jpg", "jpeg"],
        )


class BackgroundColorSelector:
    @staticmethod
    def select_background_color():
        return st.selectbox("Choose background color", [
            "Transparent (PNG)", "White", "Black", "Green", "Red", "Blue"
        ])


class App:
    def __init__(self):
        self.image_processor = None
        self.image_uploader = ImageUploader()
        self.background_selector = BackgroundColorSelector()
        self.image_downloader = ImageDownloader()
        self.hexmap = {
            "Transparent (PNG)": "#000000",
            "Black": "#000000",
            "White": "#FFFFFF",
            "Green": "#22EE22",
            "Red": "#EE2222",
            "Blue": "#2222EE",
        }

    def run(self):
        st.title("Simple image editor")
        st.write(
            "Simply remove the background of your picture and fill it with a plain color")

        uploaded_file = self.image_uploader.upload_image()

        if uploaded_file:
            self.display_original_photo(uploaded_file)

            in_mode = self.background_selector.select_background_color()
            in_submit = st.button("Submit")

            if in_submit:
                self.process_and_display_image(uploaded_file, in_mode)

    def display_original_photo(self, uploaded_file):
        with st.expander("Original photo", expanded=True):
            st.image(uploaded_file)

    def process_and_display_image(self, uploaded_file, in_mode):
        img_input = Image.open(uploaded_file)
        self.image_processor = ImageProcessor(img_input)

        with st.spinner("Magic happening behind the scenes. Please wait..."):
            alpha = 0.0 if in_mode == "Transparent (PNG)" else 1.0
            img_output = self.image_processor.remove_background()
            # img_output = self.image_processor.change_background(
            #     img_without_bg, alpha, in_mode)

        with st.expander("Success!", expanded=True):
            st.image(img_output)
            uploaded_name = os.path.splitext(uploaded_file.name)[0]
            self.image_downloader.download_button(
                pil_image=img_output,
                filename=uploaded_name,
                fmt="png"
            )


if __name__ == "__main__":
    app = App()
    app.run()
