#Importing all required laibraries 
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()  #loading all the environment variables
from PIL import Image

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    #check if file has been uploaded
    if uploaded_file is not None:
        #Read the files into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type":uploaded_file.type,  #Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('No File Uploaded')
    
    ## Initialize our streamlit app / (Frontend Setup):-

st.set_page_config(page_title = "Calories Advisor")

st.header("Calories Advisor")
uploaded_file = st.file_uploader("Choose an Image...",type = ["jpg","jpeg","ppng"])
image = ""
if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image,caption = "Uploaded Image.",use_column_width= True)

submit = st.button("Provide Me The Total Calories")

#If submit button is clicked :-

if submit:
    image_data = input_image_setup(uploaded_file)

    if image_data is not None:
        input_prompt = """
        As a nutritionist expert, your task involves analyzing food items from images and computing the total calories.
        Additionally, furnish detailed information on each food item, presenting it in the following format:

        1.Item 1 :- no of calories
        2.Item 2 :- no of calories
        3.Item 3 :- no of calories
        ----
        ----

        Conclude by evaluating the overall healthiness of the food and provide a breakdown of the percentage 
        distribution for essential dietary components such as carbohydrates, fats, fibers, sugar, and other vital nutritional elements.
        """

        response = get_gemini_response(input_prompt, image_data)
        st.header("The Response is")
        st.write(response)  
    
