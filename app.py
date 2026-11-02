import streamlit as st
import fitz
import re

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("AI Resume Analyzer")
st.subheader("Smart Resume Analysis for TechX Solutions")

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    return text

def analyze_resume(text):
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phones = re.findall(r"\+?\d[\d -]{8,12}\d", text)
    
    skills_db = ["python", "pandas", "numpy", "scikit-learn", "machine learning", "deep learning", "openai", "groq", "langchain", "langgraph", "rag", "faiss", "vector db", "streamlit", "fastapi", "docker", "git", "sql", "tensorflow", "pytorch", "hugging face", "prompt engineering"]
    found_skills = [s for s in skills_db if s.lower() in text.lower()]
    
    has_experience = "experience" in text.lower() or "project" in text.lower()
    has_education = "education" in text.lower()
    has_linkedin = "linkedin" in text.lower()
    
    return emails, phones, found_skills, has_experience, has_education, has_linkedin

uploaded = st.file_uploader("Upload Resume PDF", type=["pdf"])

if uploaded:
    resume_text = extract_text_from_pdf(uploaded)
    
    if len(resume_text) < 50:
        st.error("Could not extract text. Please upload a text-based PDF.")
    else:
        st.success(f"Resume extracted successfully: {len(resume_text)} characters")
        
        emails, phones, skills, has_exp, has_edu, has_linkedin = analyze_resume(resume_text)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Contact Info")
            st.write(f"**Email:** {emails[0] if emails else 'Not Found'}")
            st.write(f"**Phone:** {phones[0] if phones else 'Not Found'}")
        
        with col2:
            st.markdown("### Resume Stats")
            st.metric("Total Words", len(resume_text.split()))
            st.metric("Skills Found", len(skills))
        
        with col3:
            st.markdown("### Sections Check")
            st.write(f"Experience/Projects: {'✅ Yes' if has_exp else '❌ No'}")
            st.write(f"Education: {'✅ Yes' if has_edu else '❌ No'}")
            st.write(f"LinkedIn: {'✅ Yes' if has_linkedin else '❌ No'}")
        
        st.markdown("---")
        st.markdown("### Skills Detected")
        if skills:
            st.success(", ".join(skills).title())
        else:
            st.warning("No technical skills detected")
        
        st.markdown("### Suggestions for Improvement")
        suggestions = []
        if len(skills) < 5:
            suggestions.append("Add more relevant technical skills")
        if not has_exp:
            suggestions.append("Add Experience or Projects section")
        if not has_edu:
            suggestions.append("Add Education section")
        if not has_linkedin:
            suggestions.append("Add LinkedIn profile link")
        if len(resume_text.split()) < 250:
            suggestions.append("Resume is too short, add more details")
        
        if suggestions:
            for s in suggestions:
                st.warning(f"- {s}")
        else:
            st.success("Your resume looks well structured!")
        
        with st.expander("View Full Resume Text"):
            st.text(resume_text[:5000])

else:
    st.info("Please upload your resume PDF to start analysis.")





       
         
         
            
       

        

   
        
              
        )

    except Exception as e:
        st.error(f"Prediction error: {e}")
