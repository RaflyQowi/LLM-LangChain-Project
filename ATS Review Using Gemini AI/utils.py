import os
import google.generativeai as genai
import pdf2image
import io
import base64
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key= os.environ['GOOGLE_API_KEY'])

def get_gemini_response(prompt, pdf_content, input):
    model = genai.GenerativeModel('gemini-pro-vision')
    data = [prompt]+ pdf_content  + [input]
    response = model.generate_content(data)
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(
            uploaded_file.read(), 
           poppler_path= os.environ["PATH_POPPLER"]# for windows if resulting error
        )
        # first_page=images[0]
        pdf_parts = []

        for page_num, image in enumerate(images):
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            pdf_part = {
                # "page_number": page_num + 1,  # Page numbers usually start from 1
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
            data = [pdf_part]

            pdf_parts+=data

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")