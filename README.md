Streamlit Website : https://ai-career--coach.streamlit.app/

# ⚡ CareerAI Studio — Autonomous AI Career Coach & Pathway Engine

An intelligent, production-grade career analytics platform powered by a dynamic **Retrieval-Augmented Generation (RAG)** pipeline, vector search via **FAISS**, localized small language model generation (**SmolLM2-360M-Instruct**), and an executive **Cyber-Glassmorphism UI** built with Streamlit.

---

## 📌 Executive Summary

Traditional resume assessment tools rely on rigid keyword matching or ungrounded generative LLM prompts prone to severe hallucinations. **CareerAI Studio** introduces an autonomous, deterministic, and dynamic alternative. It ingests complex multi-column developer resumes, deterministically parses verified competencies, queries a vector knowledge base for target market requirements, computes dual-factor readiness scores, and autonomously synthesizes zero-filler learning roadmaps paired with real-world capstone projects and trusted learning platforms.

---

## 🏗️ Architecture & Core Components

  ┌───────────────────────────┐
                 │   Candidate Resume (PDF)  │
                 └─────────────┬─────────────┘
                               │
                               ▼
          ┌─────────────────────────────────────────┐
          │    Deterministic Extraction Pipeline    │
          │  • CamelCase De-glitch & Regex Parsing  │
          │  • Exact Substring & Semantic Normalizer│
          └─────────────┬───────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
┌──────────────────┐        ┌──────────────────────────┐
│ Extracted Profile│        │ Target Role (User Input) │
│ • Verified Skills│        └─────────────┬────────────┘
│ • Experience Hits│                      │
└─────────┬────────┘                      ▼
          │                 ┌──────────────────────────┐
          │                 │   Vector Knowledge Base  │
          │                 │   • FAISS (IndexFlatL2)  │
          │                 │   • all-MiniLM-L6-v2     │
          │                 └─────────────┬────────────┘
          │                               │
          │    ┌──────────────────────────┘ (Retrieved Benchmark)
          ▼    ▼
┌──────────────────────────────────────────────────────┐
│            Dual-Factor Scoring Engine                │
│  • Core Benchmark Coverage (85% Weight)              │
│  • Context & Practical Project Relevance (15% Weight)│
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
          ┌───────────────────────────┐
          │ Dynamic Competency Gaps   │
          └─────────────┬─────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│     Dynamic Pathway & Role Recommendation Engine     │
│  • Tiered Job Matching (Ranked by Match %)           │
│  • SmolLM2 LLM Autonomous Phase Synthesis            │
│  • Platform & Capstone Project Attribution           │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│      Executive Cyber-Glassmorphism Interface         │
│  • KPI Metrics • Live Progress • Dynamic Timelines   │
└──────────────────────────────────────────────────────┘
---

## 🌟 Key Capabilities

### 1. Deterministic CV Extraction (Zero Hallucination)
- Uses **PyPDF** combined with boundary regex patterns to extract candidate identities, contact emails, and verified technical competencies without hallucinations.
- Normalizes complex terms, such as mapping `Retrieval-Augmented Generation (RAG)` to `RAG`, or extracting composite frameworks like `.NET Web API` and `ASP.NET Core MVC`.

### 2. FAISS Vector Retrieval (RAG)
- Uses SentenceTransformers (`sentence-transformers/all-MiniLM-L6-v2`) to embed multi-track role specifications into dense 384-dimensional vector spaces.
- Employs **FAISS (IndexFlatL2)** for sub-millisecond retrieval of curated role requirements and foundational competency expectations.

### 3. Dual-Factor Role Match Engine
Instead of arbitrary minimum caps, compatibility scores are calculated mathematically:
$$\text{Role Match Index} = \left( \frac{\text{Matched Core Skills}}{\text{Total Target Skills}} \times 0.85 \right) + (\text{Experience \& Project Context} \times 0.15)$$
- If a profile has zero relevant skills, the match score drops to near zero.
- Strong stacks backed by projects and internships receive proportional, validated scoring.

### 4. Adaptive Tiered Job Matching
- Evaluates qualification tiers dynamically based on candidate scores:
  - **>= 70%**: Senior / Ready Production Roles (e.g., *LLM Application Developer*, *Junior AI Engineer*).
  - **40% - 69%**: Bridge / Intermediate Roles (e.g., *AI Engineering Intern*, *NLP / RAG Research Assistant*).
  - **< 40%**: Foundational Transition Roles (e.g., *Junior Python Developer*, *Data Operations Intern*).
- Calculates an individual similarity percentage for each position and sorts them descendingly.

### 5. Zero-Filler LLM Roadmap Synthesis
- Employs **SmolLM2-360M-Instruct** on localized hardware to construct targeted roadmaps focusing exclusively on verified skill gaps.
- Links every phase with high-authority technical platforms (Coursera, DeepLearning.AI, YouTube) and actionable portfolio capstones.

---

## 🛠️ Engineering Challenges & Iterative Solutions

During end-to-end development, several technical bottlenecks were encountered and resolved:

| # | Challenge Encountered | Root Cause | Engineering Solution Implemented |
|---|----------------------|------------|----------------------------------|
| **1** | **Name Extraction Collisions** | The regex was grabbing job titles like `Aspiring Machine Learning Engineer` below the name. | Introduced exclusion filters for common resume titles (`aspiring`, `engineer`, `developer`, `intern`, `cv`). |
| **2** | **Skill Duplication** | Both `ASP.NET Core MVC` and `ASP.NET Core` were triggering independently. | Enforced explicit boundary matching and strict canonical normalization. |
| **3** | **PDF Table Text Concatenation** | Multi-column PDF extraction fused labels with content (e.g., `ProgrammingPython`, `Machine LearningPyTorch`). | Implemented a CamelCase de-glitcher (`re.sub(r'([a-z])([A-Z])', r'\1 \2', text)`) and explicit header sanitization strips. |
| **4** | **Skewed Match Percentages** | Primitive string parsing of raw text split paragraphs into isolated filler words (`and`, `or`, `tools`), inflating denominator counts and plummeting match scores to 3%. | Streamlined the knowledge base down to 12 curated core skills per track and rebuilt the parser to handle comma-separated tokens cleanly. |
| **5** | **Static / Single-Step LLM Roadmaps** | A single-item JSON prompt example combined with strict token limits caused the LLM to output only the first missing skill and truncate the rest. | Shifted to an iterative, deterministic generation loop that generates a structured learning phase for every detected missing skill. |

---

## 🧰 Tech Stack & Libraries

- **Language:** Python 3.10+
- **User Interface:** Streamlit (Cyber-Glassmorphism CSS)
- **Document Processing:** PyPDF
- **Dense Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Search Engine:** FAISS (Facebook AI Similarity Search - CPU)
- **Language Model:** `HuggingFaceTB/SmolLM2-360M-Instruct`
- **Deep Learning Framework:** PyTorch & Hugging Face Transformers
- **Output Sanitization:** `json_repair` & Regular Expressions

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/mohamed0449/AI-Career-Coach.git
cd AI-Career-Coach
