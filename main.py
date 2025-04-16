# main.py
import fitz  # PyMuPDF
import google.generativeai as genai
import gradio as gr
import os

# Gemini API Key (Use Koyeb Secret)
genai.configure(api_key=os.environ.get("AIzaSyBy0Cg3nFQGcrUtVolNbpB4783WeO5W4dI"))
model = genai.GenerativeModel("gemini-pro")

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_quiz(text):
    prompt = f"""
    You are a quiz generator. Read this text and create 5 multiple choice questions with 4 options each.
    Mark the correct answer clearly. The quiz should be based only on the information in the text.

    Text:
    {text[:6000]}
    """
    response = model.generate_content(prompt)
    return response.text

def process_pdf(file):
    text = extract_text_from_pdf(file)
    quiz = generate_quiz(text)
    return quiz

ui = gr.Interface(fn=process_pdf, inputs="file", outputs="text", title="PDF to Quiz Generator (Free)")

if __name__ == "__main__":
    ui.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8000)))
    
