import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask
from utils import lottie_local, hide_footer


def configure_page():
    """
    Configures the Streamlit page settings.
    """
    st.set_page_config(
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
    return st.text_input(label="Enter URL")


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


def generate_qr_code(data, fill_color, back_color):
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


def display_qr_code(img_path):
    """
    Displays the generated QR code and provides a download button.
    """
    with open(img_path, "rb") as file:
        image = Image.open(file)
        st.image(image, caption="QR Code")
        st.download_button(
            label="Download Image",
            data=file,
            file_name="yourqrcode.png",
            mime="image/png"
        )


def main():
    """
    Main function for the Streamlit app.
    """
    configure_page()
    display_title_and_animation()
    data_in = get_user_input()
    fill_color, back_color = get_qr_code_parameters()

    if st.button("Generate") and data_in:
        img_path = generate_qr_code(data_in, fill_color, back_color)
        display_qr_code(img_path)


if __name__ == "__main__":
    main()
