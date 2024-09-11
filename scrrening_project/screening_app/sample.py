import pdfplumber
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Preprocess text function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Load a job description as an example
job_description = """
Job Title: Machine Learning Engineer

Job Description:
We are hiring a Machine Learning Engineer who is passionate about data science and skilled in building scalable machine learning models. You will collaborate with our data team to design, develop, and deploy various machine learning solutions.

Key Responsibilities:

Develop and implement machine learning models using Python.
Work on Natural Language Processing (NLP) tasks such as chatbot development and text processing.
Collaborate on projects using Django for web application development.
Integrate machine learning models with IoT systems and other cutting-edge technologies.
Research and apply generative AI techniques.
Deploy scalable machine learning models on cloud platforms.
Ensure cybersecurity best practices in the development and deployment of machine learning applications.
Required Skills:

Strong programming skills in Python.
Experience with Django for building web applications.
Hands-on experience with Natural Language Processing (NLP) and machine learning.
Familiarity with IoT and cybersecurity practices.
Understanding of generative AI techniques and data science principles.
Knowledge of HTML, CSS, JavaScript is a plus.
Strong communication and collaboration skills.
Preferred Qualifications:

Bachelor’s degree in Artificial Intelligence, Data Science, or a related field.
Experience with GitHub for version control.
Certifications in Python for Data Science, Machine Learning, or Generative AI.
"""

# Preprocess the job description
job_description_processed = preprocess_text(job_description)

# Extract text from the resume PDF
resume_pdf_path = "C:/Coding/Automated Resume Screening/scrrening_project/resumes/resume.pdf"

  # Replace with the actual resume file path
resume_text = extract_text_from_pdf(resume_pdf_path)

# Preprocess the resume text
resume_processed = preprocess_text(resume_text)

# Load a RoBERTa model using SentenceTransformer
model = SentenceTransformer('stsb-roberta-large')

# Get RoBERTa embeddings for both the resume and the job description
resume_embedding = model.encode(resume_processed, convert_to_tensor=True)
job_description_embedding = model.encode(job_description_processed, convert_to_tensor=True)

# Calculate cosine similarity using RoBERTa embeddings
similarity = util.pytorch_cos_sim(resume_embedding, job_description_embedding)

# Output the similarity score
print(f"RoBERTa-based Similarity between Resume and Job Description: {similarity.item():.2f}")
