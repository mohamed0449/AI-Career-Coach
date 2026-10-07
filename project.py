import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from json_repair import repair_json
import os
import re
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="CareerAI Studio", page_icon="⚡", layout="wide")

# 2. ستايل Modern Cyber-Glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: #060913;
        color: #F8FAFC;
    }

    .top-navbar {
        background: linear-gradient(90deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.7) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 28px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6);
    }

    .brand-title {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .kpi-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }

    .kpi-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 10px 25px -10px rgba(0, 0, 0, 0.5);
    }

    .kpi-label {
        font-size: 13px;
        color: #94A3B8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-val {
        font-size: 22px;
        font-weight: 700;
        margin-top: 4px;
        color: #F8FAFC;
    }

    .glass-panel {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
    }

    .stButton > button {
        background: linear-gradient(135deg, #0284C7 0%, #2563EB 50%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.5) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px -5px rgba(37, 99, 235, 0.7) !important;
    }

    .tag-chip {
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
    }
    .tag-match {
        background: rgba(14, 165, 233, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .tag-gap {
        background: rgba(244, 63, 94, 0.12);
        color: #FB7185;
        border: 1px solid rgba(251, 113, 133, 0.3);
    }

    .timeline-node {
        position: relative;
        padding-left: 26px;
        padding-bottom: 20px;
        border-left: 2px solid rgba(56, 189, 248, 0.35);
    }
    .timeline-node::before {
        content: '';
        position: absolute;
        left: -7px;
        top: 2px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #0284C7;
        box-shadow: 0 0 12px #38BDF8;
    }
    .timeline-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 18px;
    }
    .timeline-title {
        font-weight: 700;
        font-size: 15px;
        color: #38BDF8;
        margin-bottom: 4px;
    }
    .timeline-meta {
        font-size: 13px;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .timeline-resource {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
    }
    .timeline-project {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 12px;
        font-weight: 600;
    }

    .role-capsule {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .role-title {
        color: #F1F5F9;
        font-weight: 600;
        font-size: 14px;
    }
    .role-badge {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 20px;
        padding: 3px 10px;
        font-size: 12px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# 3. الهيدر
st.markdown("""
<div class="top-navbar">
    <div>
        <h1 class="brand-title">⚡ CareerAI Studio</h1>
        <p style="margin:4px 0 0 0; color:#94A3B8; font-size:14px;">Next-Gen Autonomous Candidate Analytics & LLM Dynamic Pathway Engine</p>
    </div>
    <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); padding: 6px 14px; border-radius: 20px; color: #38BDF8; font-size: 12px; font-weight: 700;">
        FAISS V-DB + LLM GENERATION ACTIVE
    </div>
</div>
""", unsafe_allow_html=True)

# 4. تهيئة محرك الـ RAG والنموذج اللغوي (LLM)
@st.cache_resource
def init_system_models():
    embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    kb_folder = "knowledge_base"
    documents = []
    
    if os.path.exists(kb_folder):
        for file in sorted(os.listdir(kb_folder)):
            if file.endswith(".txt"):
                with open(os.path.join(kb_folder, file), "r", encoding="utf-8") as f:
                    documents.append(f.read())
                    
    embeddings = embed_model.encode(documents, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    return embed_model, index, documents, tokenizer, model

embed_model, index, documents, tokenizer, model = init_system_models()

def get_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_candidate_data(text):
    # 1. استخراج البريد الإلكتروني
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    email = email_match.group(0) if email_match else "mhmd2004221@gmail.com"
    
    # 2. استخراج الاسم بدقة
    full_name = "Mohamed Gomaa Mohamed"
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    ignore_titles = ["aspiring", "engineer", "developer", "scientist", "intern", "student", "resume", "cv", "data science"]
    for l in lines[:4]:
        cleaned = re.sub(r'[^a-zA-Z\s]', '', l).strip()
        words = cleaned.split()
        if 2 <= len(words) <= 4 and not any(t in cleaned.lower() for t in ignore_titles):
            full_name = cleaned
            break

    # 3. تنظيف النصوص الملتصقة الناتجة عن استخراج جداول الـ PDF
    # وضع مسافة بين الكلمات الصغيرة التي تليها حروف كبيرة (CamelCase / Label Glitch)
    normalized_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # تنظيف عناوين الأقسام الشهيرة في الـ CV إذا التصقت
    section_headers = [
        "Technical Skills", "Programming", "Data Science", 
        "Machine Learning", "Generative AI", "Frameworks & Web", 
        "Deployment & Tools", "Languages"
    ]
    for header in section_headers:
        normalized_text = re.sub(re.escape(header), ' ', normalized_text, flags=re.IGNORECASE)

    text_lower = normalized_text.lower()

    # 4. قائمة المهارات المعيارية النظيفة المطابقة لسيرتك الذاتية بالكامل
    target_skills_catalog = [
        # Programming Languages
        "Python", "SQL", "C++", "C#", "Java", "JavaScript", "PHP", "HTML/CSS",
        
        # Data Science & Analytics
        "NumPy", "Pandas", "SciPy", "SQLAlchemy", "Matplotlib", "Seaborn", "Decision Support Systems",
        
        # Machine Learning & Deep Learning
        "PyTorch", "TensorFlow", "scikit-learn", "Machine Learning", "Regression", 
        "Classification", "CNNs", "Reinforcement Learning",
        
        # Generative AI & LLMs
        "LLMs", "Retrieval-Augmented Generation (RAG)", "FAISS", "Embeddings", 
        "LangChain", "Prompt Engineering",
        
        # Frameworks & Web
        "ASP.NET Core MVC", ".NET Web API", "FastAPI", "Streamlit", "Laravel", "Django",
        
        # Tools & Deployment
        "Git & GitHub", "Docker", "REST APIs", "Linux/Shell Scripting", "Pytest", "LaTeX", "VS Code"
    ]

    verified_skills = []

    for skill in target_skills_catalog:
        skill_clean = skill.lower()
        
        # مطابقة مخصصة للحالات الخاصة
        if skill == "Retrieval-Augmented Generation (RAG)":
            if "retrieval-augmented generation" in text_lower or re.search(r'\brag\b', text_lower):
                verified_skills.append(skill)
        elif skill == "HTML/CSS":
            if "html" in text_lower or "css" in text_lower:
                verified_skills.append(skill)
        elif skill == "Git & GitHub":
            if "git" in text_lower or "github" in text_lower:
                verified_skills.append(skill)
        elif skill == "Linux/Shell Scripting":
            if "linux" in text_lower or "shell" in text_lower:
                verified_skills.append(skill)
        elif skill == "C++":
            if "c++" in text_lower:
                verified_skills.append(skill)
        elif skill == "C#":
            if "c#" in text_lower:
                verified_skills.append(skill)
        elif skill == ".NET Web API":
            if ".net web api" in text_lower or "web api" in text_lower:
                verified_skills.append(skill)
        else:
            # مطابقة كاملة للكلمة لتجنب الاشتقاقات الخاطئة
            pattern = r'\b' + re.escape(skill_clean) + r'\b'
            if re.search(pattern, text_lower):
                verified_skills.append(skill)

    # إزالة أي تكرار مع الحفاظ على الترتيب الأصلي
    clean_unique_skills = []
    for s in verified_skills:
        if s not in clean_unique_skills:
            clean_unique_skills.append(s)

    return full_name, email, clean_unique_skills

def parse_retrieved_requirements(doc_text):
    skills = []
    req_match = re.search(r'Core Requirements:(.*?)(Curated Learning Steps:|Learning Roadmap:|$)', doc_text, re.DOTALL)
    if req_match:
        raw_reqs = req_match.group(1).strip()
        for item in raw_reqs.replace("\n", ",").split(","):
            clean = re.sub(r'\(.*?\)', '', item).strip().rstrip(".").strip()
            if clean and len(clean) > 1 and clean.lower() not in ["and", "or"]:
                skills.append(clean)
                
    unique_skills = []
    for s in skills:
        if not any(s.lower() == u.lower() for u in unique_skills):
            unique_skills.append(s)
    return unique_skills

def is_skill_present(req_skill, user_skills, full_text):
    req_lower = req_skill.lower().strip()
    full_lower = full_text.lower()
    
    if req_lower in full_lower:
        return True
        
    for u_skill in user_skills:
        u_lower = u_skill.lower().strip()
        if req_lower in u_lower or u_lower in req_lower:
            return True
            
    synonyms = {
        "asp.net core": ["asp.net core mvc", ".net web api"],
        "restful architecture": ["rest apis", "restful api", "web api"],
        "sql server": ["sql", "mysql", "postgresql"],
        "statistics": ["decision support systems", "data analysis"],
        "vector databases": ["faiss", "chromadb", "retrieval-augmented generation (rag)", "rag"],
        "rag systems": ["retrieval-augmented generation (rag)", "rag"],
        "jupyter notebooks": ["python", "pandas"]
    }
    
    if req_lower in synonyms:
        for syn in synonyms[req_lower]:
            if syn in full_lower or any(syn in u.lower() for u in user_skills):
                return True
                
    return False

# 5. محرك التوليد الديناميكي للـ Roadmap باستخدام الـ LLM
def generate_dynamic_roadmap_llm(missing_skills, target_role):
    if not missing_skills:
        return [{
            "title": "Production Deployment & Advanced Benchmarking",
            "focus": "All foundational competencies verified! Focus on deploying scalable systems and open-source contributions.",
            "resource": "GitHub & Official Architecture Docs",
            "project": "End-to-end production portfolio capstone."
        }]

    # قاعدة مصادر ومنصات ذكية ومعتمدة لكل مهارة
    platform_map = {
        "pytorch": ("YouTube (Daniel Bourke 24-Hour PyTorch) & PyTorch Docs", "Train a custom neural network from scratch with custom training loops."),
        "transformers": ("Coursera (DeepLearning.AI NLP Specialization)", "Build text generation and fine-tune a BERT/GPT model via HuggingFace."),
        "langchain": ("DeepLearning.AI Short Courses & LangChain Docs", "Build a production RAG chain with vector memory and output parsing."),
        "prompt engineering": ("Coursera (Prompt Engineering by Vanderbilt University)", "Develop advanced CoT (Chain-of-Thought) and Few-Shot structured pipelines."),
        "fine-tuning": ("YouTube (Umar Jamil / Hugging Face PEFT Guide)", "Fine-tune a 1B/3B open LLM using LoRA/QLoRA on custom domain data."),
        "fastapi": ("YouTube (freeCodeCamp FastAPI & Docker Full Course)", "Deploy asynchronous REST endpoints with validation and Docker container."),
        "docker": ("YouTube (TechWorld with Nana Docker Course)", "Multi-stage Dockerfile packaging for API and DB orchestration."),
        "entity framework": ("Microsoft Learn & YouTube (Milan Jovanovic .NET)", "Build optimized database migrations with Fluent API and Repository Pattern."),
        "html5": ("freeCodeCamp Responsive Web Design Certification", "Build accessible, responsive UI layout with semantic HTML5 elements."),
        "css3": ("freeCodeCamp & Kevin Powell CSS Mastery", "Implement custom modern CSS grid, flexbox, and glassmorphism components."),
        "backend architecture": ("YouTube (Nick Chapsas Clean Architecture)", "Architect a modular backend following Clean Architecture & CQRS principles."),
        "statistics": ("Coursera (Imperial College Mathematics for Machine Learning)", "Conduct rigorous A/B hypothesis testing and statistical modeling."),
        "scikit-learn": ("Coursera (Machine Learning Specialization by Andrew Ng)", "Implement end-to-end regression and classification pipelines with cross-validation."),
        "feature engineering": ("Kaggle Feature Engineering Course & Scikit-Learn Docs", "Engineer custom domain features, target encoding, and outlier pipelines."),
        "business intelligence": ("Coursera (Google Data Analytics Certificate) / Power BI", "Build an interactive KPI business dashboard connecting live database data.")
    }

    generated_steps = []
    
    # المرور على كل مهارة ناقصة وبناء خطوة خاصة بها
    for idx, skill in enumerate(missing_skills, 1):
        skill_lower = skill.lower()
        res_info = "Coursera / YouTube (Specialized Technical Tutorials)"
        proj_info = f"Build an end-to-end practical application focusing on {skill}."

        for key, (r_val, p_val) in platform_map.items():
            if key in skill_lower:
                res_info = r_val
                proj_info = p_val
                break

        # تشغيل الموديل لتوليد وصف تقني موجز ودقيق للمهارة الحالية
        prompt = f"Describe in one concise technical sentence what a software engineer learns in {skill} for the role of {target_role}:"
        messages = [{"role": "user", "content": prompt}]
        formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(formatted_prompt, return_tensors="pt", truncation=True, max_length=512).to(model.device)

        try:
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=40,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id
                )
            new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
            focus_text = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
            # تنظيف أي نص زائد
            focus_text = focus_text.split("\n")[0].strip()
            if len(focus_text) < 15 or "candidate" in focus_text.lower():
                focus_text = f"Mastering core principles, APIs, and production patterns of {skill}."
        except Exception:
            focus_text = f"Mastering core principles, APIs, and production patterns of {skill}."

        generated_steps.append({
            "title": f"Mastering {skill}",
            "focus": focus_text,
            "resource": res_info,
            "project": proj_info
        })

    return generated_steps

# 6. بنك الوظائف الديناميكي
def compute_dynamic_job_matches(target_role, user_skills, raw_text, overall_match_pct):
    job_catalog = {
        "AI Engineer / LLM Engineer": {
            "Senior / Ready Roles": [
                {"title": "Junior AI Engineer", "skills": ["Python", "Machine Learning", "PyTorch", "Docker"]},
                {"title": "LLM Application Developer", "skills": ["Python", "Retrieval-Augmented Generation (RAG)", "LLMs", "LangChain"]},
                {"title": "GenAI Solutions Engineer", "skills": ["FastAPI", "Vector Databases", "Prompt Engineering", "Python"]}
            ],
            "Bridge / Intermediate Roles": [
                {"title": "AI Engineering Intern", "skills": ["Python", "Machine Learning", "Git", "GitHub"]},
                {"title": "NLP / RAG Research Assistant", "skills": ["Python", "Retrieval-Augmented Generation (RAG)", "Data Analysis"]},
                {"title": "Applied ML Associate", "skills": ["Python", "Machine Learning", "SQL", "Pandas"]}
            ],
            "Foundational Roles": [
                {"title": "Junior Python Developer", "skills": ["Python", "SQL", "Git", "REST APIs"]},
                {"title": "Data Operations Intern", "skills": ["SQL", "Data Analysis", "Python"]},
                {"title": "AI Model Evaluation Specialist", "skills": ["Python", "LLMs", "Data Analysis"]}
            ]
        },
        "Data Scientist": {
            "Senior / Ready Roles": [
                {"title": "Associate Data Scientist", "skills": ["Python", "SQL", "Machine Learning", "Scikit-Learn"]},
                {"title": "Predictive Modeling Specialist", "skills": ["Python", "Machine Learning", "Statistics", "Pandas"]},
                {"title": "Business Intelligence Analyst", "skills": ["SQL", "Data Analysis", "Business Intelligence", "Pandas"]}
            ],
            "Bridge / Intermediate Roles": [
                {"title": "Data Science Intern", "skills": ["Python", "Pandas", "NumPy", "SQL"]},
                {"title": "Data Analyst (Decision Support)", "skills": ["Decision Support Systems", "Data Analysis", "SQL"]},
                {"title": "Machine Learning Intern", "skills": ["Python", "Machine Learning", "Git"]}
            ],
            "Foundational Roles": [
                {"title": "Junior SQL & Reporting Analyst", "skills": ["SQL", "Data Analysis", "Git"]},
                {"title": "Data Wrangling Assistant", "skills": ["Python", "Pandas", "Data Cleaning"]},
                {"title": "Statistical Research Intern", "skills": ["Statistics", "Data Analysis"]}
            ]
        },
        "Full-Stack Developer (.NET / Python)": {
            "Senior / Ready Roles": [
                {"title": ".NET Core Backend Developer", "skills": ["C#", "ASP.NET Core MVC", "REST APIs", "SQL"]},
                {"title": "Full-Stack Web Engineer", "skills": ["C#", "JavaScript", "ASP.NET Core MVC", "HTML5"]},
                {"title": "RESTful API Integration Specialist", "skills": ["REST APIs", ".NET Web API", "SQL", "Docker"]}
            ],
            "Bridge / Intermediate Roles": [
                {"title": "Software Engineering Intern", "skills": ["C#", "Python", "SQL", "Git"]},
                {"title": "Junior Backend Developer", "skills": ["ASP.NET Core MVC", "SQL", "REST APIs"]},
                {"title": "Web Development Intern", "skills": ["HTML5", "CSS3", "JavaScript", "PHP"]}
            ],
            "Foundational Roles": [
                {"title": "Junior Database & Web Support", "skills": ["SQL", "Git", "C#"]},
                {"title": "Frontend Integration Trainee", "skills": ["HTML5", "CSS3", "JavaScript"]},
                {"title": "API Testing Assistant", "skills": ["REST APIs", "Git", "Postman"]}
            ]
        }
    }

    role_jobs = job_catalog.get(target_role, job_catalog["AI Engineer / LLM Engineer"])
    
    if overall_match_pct >= 70:
        candidate_pool = role_jobs["Senior / Ready Roles"]
    elif overall_match_pct >= 40:
        candidate_pool = role_jobs["Bridge / Intermediate Roles"]
    else:
        candidate_pool = role_jobs["Foundational Roles"]

    ranked_jobs = []
    for item in candidate_pool:
        job_skills = item["skills"]
        matched_job_skills = [s for s in job_skills if is_skill_present(s, user_skills, raw_text)]
        sim_pct = round((len(matched_job_skills) / len(job_skills)) * 100) if job_skills else overall_match_pct
        ranked_jobs.append({
            "title": item["title"],
            "similarity": sim_pct
        })

    return sorted(ranked_jobs, key=lambda x: x["similarity"], reverse=True)

# 7. الشريط الجانبي
with st.sidebar:
    st.markdown("### ⚙️ Intake Workspace")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    
    target_role = st.selectbox(
        "Target Career Pathway:",
        [
            "AI Engineer / LLM Engineer",
            "Data Scientist",
            "Full-Stack Developer (.NET / Python)"
        ]
    )
    
    analyze_btn = st.button("RUN DEEP DIAGNOSTIC ⚡", use_container_width=True)
    st.markdown("---")
    st.caption("RAG: FAISS Vector DB | Roadmap: Dynamic LLM Generation")

# 8. المعالجة التحليلية والتوليد بالـ LLM
if uploaded_file is not None and analyze_btn:
    with st.spinner("Retrieving RAG knowledge & generating dynamic AI roadmap..."):
        try:
            raw_text = get_pdf_text(uploaded_file)
            name, email, current_skills = extract_candidate_data(raw_text)

            query_vec = embed_model.encode([target_role], convert_to_numpy=True)
            _, indices = index.search(query_vec, k=1)
            retrieved_doc = documents[indices[0][0]]

            kb_required_skills = parse_retrieved_requirements(retrieved_doc)

            matched_from_kb = []
            missing_skills = []
            for s in kb_required_skills:
                if is_skill_present(s, current_skills, raw_text):
                    matched_from_kb.append(s)
                else:
                    missing_skills.append(s)

            total_req = len(kb_required_skills)
            base_skill_ratio = (len(matched_from_kb) / total_req) if total_req > 0 else 0.5

            cv_text_lower = raw_text.lower()
            context_relevance = 0.0
            if "intern" in cv_text_lower or "experience" in cv_text_lower:
                context_relevance += 0.08
            if "project" in cv_text_lower:
                context_relevance += 0.07

            computed_score = (base_skill_ratio * 0.85) + (context_relevance * 0.15)
            match_percentage = min(100, max(0, round(computed_score * 100)))

            suggested_jobs = compute_dynamic_job_matches(target_role, current_skills, raw_text, match_percentage)

            # توليد الخريطة حصرياً للمهارات الناقصة بواسطة النموذج اللغوي
            generated_roadmap = generate_dynamic_roadmap_llm(missing_skills, target_role)

            total_missing = len(missing_skills)
            if total_missing <= 2:
                estimated_time = "2 - 3 Weeks"
            elif total_missing <= 5:
                estimated_time = "4 - 6 Weeks"
            elif total_missing <= 8:
                estimated_time = "6 - 8 Weeks"
            else:
                estimated_time = "8 - 12 Weeks"

            # عرض المؤشرات الرقمية
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-card">
                    <div class="kpi-label">Candidate</div>
                    <div class="kpi-val" style="color:#38BDF8; font-size:18px; line-height:1.2;">{name}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Role Match Index</div>
                    <div class="kpi-val" style="color:#10B981;">{match_percentage}%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Verified Stack</div>
                    <div class="kpi-val">{len(current_skills)} Skills</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Time to Readiness</div>
                    <div class="kpi-val" style="color:#F59E0B;">~{estimated_time}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(match_percentage / 100)

            col_left, col_right = st.columns([1.05, 0.95], gap="large")

            with col_left:
                st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
                st.markdown("### 🎯 Skill Spectrum Analysis")
                
                st.markdown("<p style='color:#38BDF8; font-weight:700; margin-bottom:6px;'>VERIFIED COMPETENCIES</p>", unsafe_allow_html=True)
                cur_html = "".join([f'<span class="tag-chip tag-match">✓ {s}</span>' for s in current_skills])
                st.markdown(cur_html, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<p style='color:#FB7185; font-weight:700; margin-bottom:6px;'>TARGET COMPETENCY GAPS (FROM RAG)</p>", unsafe_allow_html=True)
                if missing_skills:
                    miss_html = "".join([f'<span class="tag-chip tag-gap">! {s}</span>' for s in missing_skills])
                    st.markdown(miss_html, unsafe_allow_html=True)
                else:
                    st.success("Zero gaps detected for standard requirements!")

                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
                st.markdown("### 💼 Dynamic Market Opportunities")
                st.caption(f"Ranked opportunities based on current qualification tier ({match_percentage}% Match)")
                
                for job in suggested_jobs:
                    st.markdown(f"""
                    <div class="role-capsule">
                        <div class="role-title">✦ {job['title']}</div>
                        <div class="role-badge">{job['similarity']}% Match</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_right:
                st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
                st.markdown("### 🗺️ AI Generated Roadmap (Zero Filler)")
                st.caption("Custom-synthesized by LLM exclusively targeting your missing skill gaps:")
                
                for idx, step in enumerate(generated_roadmap, 1):
                    title = step.get("title", f"Sprint {idx}")
                    focus = step.get("focus", "Applied skill mastery")
                    res = step.get("resource", "Coursera / YouTube")
                    proj = step.get("project", "Hands-on implementation")
                    
                    st.markdown(f"""
                    <div class="timeline-node">
                        <div class="timeline-card">
                            <div class="timeline-title">PHASE {idx}: {title}</div>
                            <div class="timeline-meta">{focus}</div>
                            <div style="margin-top:6px;">
                                <span class="timeline-resource">📚 {res}</span>
                                <span class="timeline-project">🛠️ {proj}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown(f"""
                <div style="background: rgba(99, 102, 241, 0.1); border-left: 3px solid #818CF8; padding: 12px 16px; border-radius: 8px;">
                    <b style="color:#818CF8;">Executive Summary:</b><br>
                    <span style="font-size:13px; color:#CBD5E1;">
                    Targeting key sprints on [<b>{', '.join(missing_skills[:3]) if missing_skills else 'Advanced Capstones'}</b>] will bridge the gap in approximately <b>{estimated_time}</b>.
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("🔬 Inspect Raw Structured JSON (Output Parser)"):
                st.json({
                    "candidate_name": name,
                    "target_role": target_role,
                    "role_match_index": f"{match_percentage}%",
                    "current_skills": current_skills,
                    "missing_skills": missing_skills,
                    "recommended_roadmap": generated_roadmap,
                    "suggested_jobs": [f"{j['title']} ({j['similarity']}%)" for j in suggested_jobs]
                })

        except Exception as e:
            st.error(f"Execution Error: {e}")
else:
    st.info("👈 Please upload your PDF resume and select your target role from the sidebar to begin analysis.")