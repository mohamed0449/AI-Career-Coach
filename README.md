Streamlit Website : https://ai-career--coach.streamlit.app/

# ⚡ CareerAI Studio — AI Career Coach & Career Pathway Engine

An intelligent career analytics platform powered by a dynamic **Retrieval-Augmented Generation (RAG)** pipeline, vector search using **FAISS**, localized small language model generation with **SmolLM2-360M-Instruct**, and an executive **Cyber-Glassmorphism UI** built with Streamlit.

---

## 📌 Executive Summary

Traditional resume assessment tools often rely on rigid keyword matching or ungrounded generative LLM prompts that can introduce inaccurate recommendations.

**CareerAI Studio** provides a structured, data-driven alternative. It ingests complex multi-column developer resumes, extracts candidate skills using deterministic parsing rules, retrieves target-market requirements from a vector knowledge base, computes role-readiness scores, identifies competency gaps, and generates personalized learning roadmaps paired with practical capstone projects and recommended learning platforms.

The system combines **deterministic analysis** for candidate profiling and scoring with **LLM-assisted generation** for personalized learning pathways.

---

## 🏗️ Architecture & Core Components

```text
┌───────────────────────────────┐
│      Candidate Resume (PDF)   │
└───────────────┬───────────────┘
                │
                ▼
┌──────────────────────────────────────────────┐
│       Deterministic Extraction Pipeline      │
│                                              │
│ • CamelCase De-glitch & Regex Parsing        │
│ • Skill Normalization                         │
│ • Boundary-Aware Matching                     │
│ • Resume Structure Sanitization               │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
          ┌──────────────────────────┐
          │    Extracted Profile     │
          │                          │
          │ • Detected Skills        │
          │ • Experience Signals     │
          │ • Project Signals        │
          └────────────┬─────────────┘
                       │
                       │
┌──────────────────────┴───────────────────────┐
│              Target Role Input               │
│                                              │
│       Desired Career / Target Position       │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│         Vector Knowledge Base                │
│                                              │
│ • FAISS IndexFlatL2                          │
│ • all-MiniLM-L6-v2                           │
│ • Curated Role Requirements                  │
│ • Core Competency Benchmarks                 │
└──────────────────────┬───────────────────────┘
                       │
                       │ Retrieved Requirements
                       ▼
┌──────────────────────────────────────────────┐
│            Role Match Engine                 │
│                                              │
│ • Core Skill Coverage                        │
│ • Experience Context                         │
│ • Project Relevance                           │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│            Competency Gap Analysis            │
│                                              │
│ • Missing Core Skills                        │
│ • Partial Skill Coverage                     │
│ • Practical Experience Gaps                  │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│      Career Pathway Recommendation Engine    │
│                                              │
│ • Ranked Role Matching                       │
│ • Readiness Tier Classification              │
│ • SmolLM2 Roadmap Generation                 │
│ • Learning Platform Recommendations          │
│ • Portfolio Capstone Projects                │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│       Executive Cyber-Glassmorphism UI       │
│                                              │
│ • KPI Metrics                                │
│ • Match Scores                               │
│ • Skill Gaps                                 │
│ • Learning Roadmap                           │
│ • Dynamic Progress Timeline                  │
└──────────────────────────────────────────────┘
```

---

## 🌟 Key Capabilities

### 1. Deterministic CV Extraction

CareerAI Studio uses **PyPDF** combined with boundary-aware regular expressions and normalization rules to extract candidate information from resumes.

Key features include:

- Candidate identity and contact extraction.
- Technical skill detection.
- Boundary-aware skill matching.
- Canonical skill normalization.
- Handling of multi-column PDF extraction artifacts.
- CamelCase text correction.
- Composite technology recognition.

For example, the system can normalize:

```text
Retrieval-Augmented Generation (RAG)
```

to:

```text
RAG
```

and recognize composite technologies such as:

```text
.NET Web API
ASP.NET Core MVC
```

rather than treating their individual components as unrelated skills.

> The extraction pipeline is deterministic and designed to minimize unsupported skill inference from resume text.

---

## 2. FAISS Vector Retrieval — RAG

The platform uses **SentenceTransformers** with:

```text
sentence-transformers/all-MiniLM-L6-v2
```

to transform role requirements and competency descriptions into dense vector representations.

The resulting embeddings are stored and searched using:

```text
FAISS — IndexFlatL2
```

This allows the system to retrieve relevant role requirements from a curated knowledge base based on semantic similarity.

### Retrieval Pipeline

```text
Role / Career Query
        │
        ▼
SentenceTransformer
        │
        ▼
384-Dimensional Embedding
        │
        ▼
FAISS IndexFlatL2
        │
        ▼
Relevant Role Requirements
        │
        ▼
Scoring & Gap Analysis
```

---

## 3. Dual-Factor Role Match Engine

Instead of relying on a single keyword count, the system combines **core skill coverage** with **experience and project context**.

The conceptual scoring model is:

$$
\text{Role Match Index}
=
\left(
\frac{\text{Matched Core Skills}}
{\text{Total Target Skills}}
\times 0.85
\right)
+
\left(
\text{Experience \& Project Context}
\times 0.15
\right)
$$

Where:

- **Core Skill Coverage** contributes 85%.
- **Experience & Project Context** contributes 15%.
- The context component is normalized to a value between 0 and 1.

This design ensures that a candidate cannot obtain a high role-match score simply because their resume contains a few generic keywords.

### Example

```text
Target Skills:              12
Matched Skills:              9

Core Coverage = 9 / 12
              = 75%

Context Score = 80%

Final Match
= (75% × 0.85) + (80% × 0.15)
= 75.75%
```

---

## 4. Adaptive Tiered Career Matching

The system classifies candidate readiness using configurable score thresholds.

### Readiness Tiers

| Match Score | Readiness Tier | Example Roles |
|-------------:|----------------|---------------|
| ≥ 70% | High Readiness | Junior AI Engineer, LLM Application Developer |
| 40–69% | Bridge / Intermediate | AI Engineering Intern, NLP / RAG Research Assistant |
| < 40% | Foundational Transition | Junior Python Developer, Data Operations Intern |

These tiers describe **career readiness relative to the selected role**, not necessarily the candidate's formal seniority level.

The system also calculates an individual similarity score for each candidate-role combination and ranks the available positions accordingly.

---

## 5. LLM-Assisted Learning Roadmap Generation

CareerAI Studio uses:

```text
HuggingFaceTB/SmolLM2-360M-Instruct
```

to generate personalized learning phases based on the skill gaps identified by the deterministic analysis layer.

The generation process focuses on:

- Missing technical skills.
- Practical learning objectives.
- Recommended learning resources.
- Portfolio-oriented projects.
- Progressive skill development.

Rather than asking the model to generate an entire roadmap in a single unconstrained response, the system uses an iterative generation approach so that each detected skill gap can receive its own structured learning phase.

### Roadmap Structure

```text
Detected Skill Gap
        │
        ▼
Learning Objective
        │
        ▼
Recommended Resources
        │
        ▼
Practical Exercise
        │
        ▼
Portfolio Capstone Project
        │
        ▼
Next Skill Gap
```

Recommended learning sources may include platforms such as:

- Coursera
- DeepLearning.AI
- YouTube
- Official technical documentation

---

# 🧠 Deterministic + Generative Architecture

One of the central design principles of CareerAI Studio is separating **what must be deterministic** from **what benefits from generative AI**.

### Deterministic Layer

Used for:

- Resume parsing
- Skill extraction
- Skill normalization
- Role requirements
- Match-score calculation
- Gap detection
- Tier classification

### Generative Layer

Used for:

- Learning roadmap synthesis
- Explanations
- Learning-phase descriptions
- Project recommendations

This architecture reduces unnecessary LLM dependence while keeping the generative model focused on tasks where natural-language generation provides value.

---

# 🛠️ Engineering Challenges & Iterative Solutions

During end-to-end development, several technical bottlenecks were identified and addressed.

| # | Challenge | Root Cause | Engineering Solution |
|---|-----------|------------|----------------------|
| **1** | **Name Extraction Collisions** | The regex could interpret job titles such as `Aspiring Machine Learning Engineer` as candidate names. | Added exclusion filters for common resume titles such as `aspiring`, `engineer`, `developer`, `intern`, and `cv`. |
| **2** | **Skill Duplication** | Similar technologies such as `ASP.NET Core MVC` and `ASP.NET Core` could trigger independently. | Implemented boundary-aware matching and canonical skill normalization. |
| **3** | **PDF Table Text Concatenation** | Multi-column PDF extraction could concatenate labels and values, producing text such as `ProgrammingPython` or `Machine LearningPyTorch`. | Added a CamelCase de-glitcher and header sanitization rules. |
| **4** | **Skewed Match Percentages** | Primitive parsing could split raw text into irrelevant tokens such as `and`, `or`, and `tools`, inflating the denominator and reducing match scores. | Reduced the knowledge base to curated core skills and improved parsing of comma-separated requirements. |
| **5** | **Static / Single-Step LLM Roadmaps** | A single JSON generation request combined with strict token limits could cause the model to generate only the first missing skill. | Replaced the single-step approach with an iterative generation loop that processes each detected skill gap independently. |

---

# 🧰 Tech Stack & Libraries

### Programming

- **Python 3.10+**

### User Interface

- **Streamlit**
- Custom Cyber-Glassmorphism CSS

### Document Processing

- **PyPDF**

### Embeddings

```text
sentence-transformers/all-MiniLM-L6-v2
```

### Vector Search

- **FAISS**
- `IndexFlatL2`
- CPU-based vector search

### Language Model

```text
HuggingFaceTB/SmolLM2-360M-Instruct
```

### Machine Learning

- **PyTorch**
- **Hugging Face Transformers**
- **SentenceTransformers**

### Output Processing

- **json_repair**
- Python Regular Expressions

---

# 🚀 Setup & Installation

## 1. Clone the Repository

```bash
git clone https://github.com/mohamed0449/AI-Career-Coach.git
cd AI-Career-Coach
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If the project does not include a `requirements.txt` file yet, install the main dependencies manually:

```bash
pip install streamlit
pip install pypdf
pip install sentence-transformers
pip install faiss-cpu
pip install transformers
pip install torch
pip install json-repair
```

---

## 4. Run the Application

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, typically:

```text
http://localhost:8501
```

---

# 📂 Project Workflow

The complete system follows this pipeline:

```text
Resume PDF
    │
    ▼
PDF Text Extraction
    │
    ▼
Text Cleaning & Normalization
    │
    ▼
Skill Detection
    │
    ▼
Candidate Profile
    │
    ▼
Target Role Retrieval
    │
    ▼
FAISS Semantic Search
    │
    ▼
Role Requirements
    │
    ▼
Match Score Calculation
    │
    ▼
Skill Gap Detection
    │
    ▼
Career Tier Classification
    │
    ▼
LLM-Assisted Roadmap Generation
    │
    ▼
Learning Resources
    │
    ▼
Capstone Projects
    │
    ▼
Streamlit Dashboard
```

---

# 📊 Example Output

The application can provide a structured career analysis containing:

### Candidate Profile

```text
Detected Skills
Experience Signals
Project Signals
```

### Role Matching

```text
Target Role
Match Percentage
Readiness Tier
Matched Skills
Missing Skills
```

### Skill Gap Analysis

```text
Missing Core Skills
Partial Competencies
Recommended Priorities
```

### Learning Roadmap

```text
Phase 1
├── Skill
├── Learning Objective
├── Recommended Resources
└── Practical Project

Phase 2
├── Skill
├── Learning Objective
├── Recommended Resources
└── Practical Project
```

---

# 🎯 Design Philosophy

CareerAI Studio is built around three principles:

### 1. Deterministic Where Accuracy Matters

Important scoring and extraction decisions are handled using explicit rules rather than relying entirely on an LLM.

### 2. Semantic Where Context Matters

Vector retrieval is used to connect candidate profiles with role requirements beyond simple exact keyword matching.

### 3. Generative Where Personalization Matters

The language model is used primarily to transform structured skill gaps into understandable and actionable learning plans.

---

# 🔬 Technical Highlights

- Deterministic resume parsing
- Boundary-aware skill extraction
- Canonical technology normalization
- CamelCase PDF text correction
- Semantic vector retrieval
- FAISS-based similarity search
- Dual-factor role scoring
- Dynamic competency gap detection
- Tier-based career recommendations
- Iterative LLM roadmap generation
- Portfolio-oriented capstone recommendations
- Local small-language-model inference
- Streamlit-based interactive dashboard

---

# 🔒 Design Considerations

CareerAI Studio is designed to minimize unsupported assumptions about a candidate.

The system distinguishes between:

```text
Detected from Resume
        ↓
Scored by Deterministic Rules
        ↓
Retrieved from Knowledge Base
        ↓
Generated by LLM
```

This separation helps prevent the generative model from becoming the primary source of factual candidate information.

The platform should therefore be viewed as a **career decision-support system**, rather than an automated hiring or employment decision-maker.

---

# 🚧 Current Limitations

The current implementation has several practical limitations:

- Resume parsing quality depends on the structure and text layer of the PDF.
- Skill detection depends on the curated competency dictionary.
- Role recommendations depend on the quality and coverage of the knowledge base.
- The small language model has limited generation capacity compared with larger LLMs.
- Learning-resource recommendations may require periodic validation.
- Match scores represent the project's defined scoring methodology and should not be interpreted as objective employment probabilities.

---

# 🔮 Future Development

Potential future improvements include:

- Larger and continuously updated career knowledge bases.
- Job-market data integration.
- Real-time job vacancy retrieval.
- Salary and geographic market analysis.
- Multi-resume comparison.
- Automated CV improvement suggestions.
- LinkedIn profile analysis.
- Skill-demand forecasting.
- Personalized interview preparation.
- Job application tracking.
- Larger local or hosted language models.
- Evaluation benchmarks for extraction accuracy and recommendation quality.
- Automated testing for resume parsing edge cases.

---

# 📈 Evaluation Opportunities

Future versions can evaluate the system using measurable benchmarks such as:

### Resume Extraction

- Skill Precision
- Skill Recall
- F1 Score

### Role Matching

- Ranking Accuracy
- Top-K Retrieval Accuracy
- Agreement with Human Evaluation

### Roadmap Generation

- Relevance
- Completeness
- Skill-Gap Coverage
- Resource Quality

### System Performance

- PDF Processing Time
- Embedding Generation Time
- FAISS Retrieval Latency
- LLM Generation Time

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

To contribute:

```bash
git clone https://github.com/mohamed0449/AI-Career-Coach.git
```

Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

Commit your changes:

```bash
git add .
git commit -m "Add your feature"
```

Push the branch:

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request.

---

# 📜 License

This project is provided for educational, research, and development purposes.

Add the appropriate license file to the repository if you intend to distribute the project publicly.

---

# 👨‍💻 Author

**Mohamed 0449**

GitHub:

https://github.com/mohamed0449/AI-Career-Coach

---

# ⭐ Project Vision

> **CareerAI Studio aims to transform a static resume into a structured, evidence-driven career development pathway.**

By combining deterministic resume analysis, semantic retrieval, mathematical scoring, and lightweight local language models, the system provides a practical bridge between **what a candidate currently knows** and **what they need to learn next**.
