import os
import io
import base64
import streamlit as st
from dotenv import load_dotenv
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to images
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert the first page image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App Setup
st.set_page_config(page_title="Resume ATS Tracker", layout="wide")
st.title("CareerCraft: ATS Tracking System")
st.header("Welcome to CareerCraft")

# Image Paths
image1_path = "images/image1.png"
image2_path = "images/image2.png"
image3_path = "images/image3.png"

# Column Layout for Introduction
col1, col2 = st.columns([3, 2])
with col1:
    st.subheader("Your Partner in Career Advancement")
    st.write("CareerCraft is an ATS-Optimized Resume Analyzer that helps you improve your chances of landing interviews.")
with col2:
    st.image(image1_path, width=250)

# Offerings Section
st.header("Wide Range of Offerings")
col3, col4 = st.columns(2)
with col3:
    st.image(image2_path, width=250)
with col4:
    st.write("Our offerings include:")
    st.write("- ATS-Optimized Resume Analysis")
    st.write("- Resume Optimization")
    st.write("- Skill Enhancement")
    st.write("- Interview Preparation")

# Resume ATS Tracking Application
st.header("Resume ATS Tracking Application")
col5, col6 = st.columns([3, 2])
with col5:
    st.write("Embark on your career adventure:")
    input_text = st.text_area("Job Description: ", key="input")
    uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])
    
    if uploaded_file is not None:
        st.success("PDF Uploaded Successfully!")

    # Define prompts for the Generative Model
    input_prompt_evaluation = """
    You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """

    input_prompt_percentage = """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
    Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
    the job description. First, the output should come as percentage, followed by missing keywords, and finally, your thoughts.
    """

    submit_analysis = st.button("Tell Me About the Resume")
    submit_percentage = st.button("Get Percentage Match")

    if submit_analysis:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt_evaluation)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.error("Please upload the resume.")

    elif submit_percentage:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt_percentage)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.error("Please upload the resume.")
with col6:
    st.image(image3_path, width=250)

# FAQ Section
st.header("Frequently Asked Questions")
faq = {
    "How does CareerCraft help?": "CareerCraft analyzes your resume to optimize it for ATS, increasing your chances of landing interviews.",
    "Is the analysis free?": "Yes, you can analyze your resume for free.",
    "How can I improve my resume?": "We provide insights and suggestions based on ATS requirements.",
    "What formats do you support?": "We currently support PDF format for resumes."
}

for question, answer in faq.items():
    st.write(f"**{question}**: {answer}")

# End of the Streamlit App

