import fitz  # PyMuPDF
import google.generativeai as genai
import gradio as gr
import os

# Configure Gemini API key
genai.configure(api_key=os.environ.get("AIzaSyBy0Cg3nFQGcrUtVolNbpB4783WeO5W4dI"))
model = genai.GenerativeModel("gemini-pro")

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file.name)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_quiz(text):
    prompt = f"""
    You are a quiz generator.

    Your task:
    - Create at least 100 multiple choice questions (MCQs) from the given book content.
    - Each question should have 4 options (A, B, C, D).
    - Clearly mark the correct answer.
    - Make sure the questions cover the whole content evenly.

    Book Content:
    {text[:30000]}  # Limit input for safety
    """
    response = model.generate_content(prompt)
    return response.text

def process_pdf(file):
    text = extract_text_from_pdf(file)
    quiz = generate_quiz(text)
    return quiz

ui = gr.Interface(fn=process_pdf, inputs="file", outputs="text", title="PDF to 100-MCQ Quiz Generator")

if __name__ == "__main__":
    ui.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8000)), share=True, debug=True)
