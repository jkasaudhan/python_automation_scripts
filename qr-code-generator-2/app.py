import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask
from utils import lottie_local, hide_footer
from urllib.request import urlopen
import io

import segno


def configure_page():
    """
    Configures the Streamlit page settings.
    """
    st.set_page_config(
        page_icon="🤳",
        page_title="QR Code Generator",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "## A minimalistic application to generate QR Codes using Python"
        }
    )


def display_title_and_animation():
    """
    Displays the title and the Lottie animation.
    """
    st.title("QR Code Generator")
    hide_footer()
    anim = lottie_local("assets/animations/scanner.json")
    st_lottie(anim, speed=2, reverse=False, loop=True,
              quality="medium", height=300, width=300)


def get_user_input():
    """
    Gets the URL input from the user.
    """
    return st.text_input(label="Enter the URL to convert into a QR code")


def get_gif_input():
    """
    Gets the gif URL input from the user which should be used as a background.
    """
    return st.text_input(label="Enter gif URL which should be used in a background")


def get_qr_code_parameters():
    """
    Gets the QR code parameters from the user.
    """
    col1, col2 = st.columns(2)
    with col1:
        fill_color = st.color_picker('Pick Fill Color', '#000000')
    with col2:
        back_color = st.color_picker('Pick Background Color', '#ffffff')
    return fill_color, back_color


def generate_animated_qr_code(data, gif_file):
    img_path = "animated_qrcode.gif"
    slts_qrcode = segno.make_qr(data)
    # gif = urlopen(gif_url)
    slts_qrcode.to_artistic(
        background=gif_file,
        target=img_path,
        light="white",
        scale=10,
    )
    return img_path


def generate_simple_qr_code(data, fill_color, back_color):
    """
    Generates and saves the QR code based on the user input.
    """
    qr = qrcode.QRCode(version=4, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img_path = "./assets/qrcode.png"
    img.save(img_path)
    return img_path


def generate_logo_qr_code(data, logo_file_path):
    out = io.BytesIO()
    # Nothing special here, let Segno generate the QR code and save it as PNG in a buffer
    segno.make(data, error='h').save(out, scale=5, kind='png')
    out.seek(0)  # Important to let Pillow load the PNG
    img = Image.open(out)
    img = img.convert('RGB')  # Ensure colors for the output
    img_width, img_height = img.size
    logo_max_size = img_height // 3  # May use a fixed value as well
    logo_img = Image.open(logo_file_path)  # The logo
    # Resize the logo to logo_max_size
    logo_img.thumbnail((logo_max_size, logo_max_size),
                       Image.Resampling.LANCZOS)
    # Calculate the center of the QR code
    box = ((img_width - logo_img.size[0]) // 2,
           (img_height - logo_img.size[1]) // 2)
    img.paste(logo_img, box)
    img_path = 'qrcode_with_logo.png'
    img.save(img_path)
    return img_path


def display_qr_code(img_path):
    """
    Displays the generated QR code and provides a download button.
    """
    with open(img_path, "rb") as file:
        image = Image.open(file)
        st.image(image, caption="QR Code")


def display_download_button(file_path, filename="your_qr_code.png", mime_type="image/png"):
    with open(file_path, "rb") as file:
        st.download_button(
            label="Download Image",
            data=file,
            file_name=filename,
            mime=mime_type
        )


def main():
    """
    Main function for the Streamlit app.
    """
    configure_page()
    display_title_and_animation()
    url = get_user_input()
    # gif_url = get_gif_input()

    # Dropdown menu
    options = ["Simple QR code", "QR code with logo", "Animated QR code"]
    selected_option = st.selectbox(
        "Select the type of QR code to generate", options)

    is_simple_qr = selected_option == "Simple QR code"
    is_logo_qr = selected_option == "QR code with logo"
    is_animated_qr = selected_option == "Animated QR code"

    if is_simple_qr:
        fill_color, back_color = get_qr_code_parameters()
    elif is_logo_qr:
        logo = st.file_uploader(
            label="Upload your logo",
            accept_multiple_files=False, type=["png", "jpg", "jpeg"],
        )
    elif is_animated_qr:
        gif_file = st.file_uploader("Choose a GIF file", type="gif")
        # Read the GIF file into memory
        if gif_file:
            # Display the uploaded GIF
            st.image(gif_file, caption="Uploaded GIF",
                     use_column_width=True)

    if st.button("Generate") and url:
        if is_simple_qr:
            img_path = generate_simple_qr_code(url, fill_color, back_color)
            image_name = "your_qr_code.png"
            mime_type = "image/png"
        elif is_logo_qr:
            img_path = generate_logo_qr_code(
                url, logo)
            image_name = "your_qr_code.png"
            mime_type = "image/png"
        elif is_animated_qr:
            img_path = generate_animated_qr_code(
                url, gif_file)
            image_name = "your_qr_code.gif"
            mime_type = "image/gif"

        display_qr_code(img_path)
        display_download_button(img_path, image_name, mime_type)


if __name__ == "__main__":
    main()
