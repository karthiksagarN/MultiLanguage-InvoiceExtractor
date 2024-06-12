### MULTI-LANGUAGE INVOICE EXTRACTOR USING GEMINI-PRO

from dotenv import load_dotenv
load_dotenv() # load the environment variables

import streamlit as st
import os
import base64
from io import BytesIO
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load gemini-pro-vision
model= genai.GenerativeModel("gemini-pro-vision")

def get_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])   # gemini-pro always takes input in form of a list. 
    # first input always describes or instructs how the model should behave.
    return response

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File Not Uploaded")

## initialize the streamlit app

st.set_page_config(page_title="MultiLanguage-InvoiceExtractor")

# Function to set a background image
def set_background(image_file):
    with open(image_file, "rb") as image:
        b64_image = base64.b64encode(image.read()).decode("utf-8")
    css = f"""
    <style>
    .stApp {{
        background: url(data:image/png;base64,{b64_image});
        background-size: cover;
        background-position: centre;
        backgroun-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set the background image
set_background("background_image.png")

st.header("MultiLanguage - Invoice Extractor 📄🤖")

input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
image= ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Image Uploaded.", use_column_width = True)

submit = st.button("Tell me about the invoice")

input_prompt = """
    You are an expert in understanding invoices. We will upload an image as invoice.
    You will have to analyze the invoice image provided to you carefully and answer
    any questions asked related to the invoice image.
"""

# if submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_response(input_prompt, image_data, input)
    st.subheader("Response : ")
    st.write(response.text)