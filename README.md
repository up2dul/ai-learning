# 🎯 Personal Assignments

> Agentic Workflow and AI Agent use cases.

## Table of Contents
- [🎯 Personal Assignments](#-personal-assignments)
  - [Table of Contents](#table-of-contents)
  - [Quick Start](#quick-start)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Install dependencies](#2-install-dependencies)
    - [3. Setup environment variables](#3-setup-environment-variables)
    - [4. Run the commands](#4-run-the-commands)
  - [Learning Path Generator (Agentic Workflow)](#learning-path-generator-agentic-workflow)
    - [Core Concept](#core-concept)
    - [Implementation Flow](#implementation-flow)
    - [Tech Stack](#tech-stack)
  - [CV to Salary (AI Agent)](#cv-to-salary-ai-agent)
    - [Core Concept](#core-concept-1)
    - [Implementation Flow](#implementation-flow-1)
    - [Tech Stack](#tech-stack-1)

## Quick Start

Prerequisites:

- Python 3.12+
- UV (Python package manager)
- PDF file named `cv.pdf` in the project root for salary analysis

### 1. Clone the repository
```bash
git clone https://github.com/up2dul/ai-learning.git

# or if you have SSH access
git clone git@github.com:up2dul/ai-learning.git
```

### 2. Install dependencies
```bash
cd ai-learning
uv sync
```

### 3. Setup environment variables
```bash
cp .env.example .env
```

And fill all the variables with yours:
```
OPENAI_API_KEY=""
TAVILY_API_KEY=""
LANGFUSE_SECRET_KEY=""
LANGFUSE_PUBLIC_KEY=""
LANGFUSE_HOST=""
```

### 4. Run the commands
```bash
# Generate a learning path for any topic
make learning-path

# Analyze your CV and get salary insights  
make salary-analysis
```

## Learning Path Generator (Agentic Workflow)

Generate a comprehensive, structured learning path for any topic with curated resources and realistic timelines.

### Core Concept

Multi-Agent Learning Curriculum Designer that creates progressive learning paths with real-world resources.

- Input any learning topic or skill request
- AI agents collaborate to research, curate, and structure resources
- Generate phase-based curriculum with clear milestones
- Include diverse resource types (courses, tutorials, projects, documentation)
- Provide realistic time estimates and skill progression tracking

### Implementation Flow

1. **Topic analysis and research planning**
  - Parse the learning request and identify key subtopics
  - Plan research strategy for comprehensive coverage

2. **Resource discovery (Web Search Tool)**
  - Search for courses, tutorials, books, and documentation
  - Find beginner to advanced resources
  - Research prerequisite skills and knowledge
  - Look for hands-on projects and exercises
  - Identify popular learning platforms and their offerings

3. **Content evaluation and filtering**
  - Analyze the resources found for quality indicators
  - Check for recency and relevance
  - Identify free vs paid resources
  - Note estimated time commitments

4. **Curriculum structure design**
  - Organize resources into logical learning sequence
  - Define learning milestones and checkpoints
  - Balance theory with practical application
  - Plan project-based learning components

5. **Learning path generation**
  - Create structured curriculum document
  - Include resource links, descriptions, and time estimates
  - Add progress tracking mechanisms
  - Generate study schedules and deadlines

6. **Self-reflection and optimization**
  - Review the generated path for gaps and redundancies
  - Ensure logical progression from basics to advanced
  - Refine based on coherence and completeness

### Tech Stack

- **AI/ML**: OpenAI GPT models with Langfuse integration for tracking
- **Search**: Tavily API for comprehensive resource discovery

## CV to Salary (AI Agent)

Analyze your CV and get focused salary insights with market data and source verification.

### Core Concept

Simple CV Salary Intelligence Agent that provides actionable salary analysis with credible sources.

- Upload CV (PDF format)
- Agent extracts job role and analyzes market positioning
- Real-time salary research with current market data
- Focused report with salary ranges, skills analysis, and source links

### Implementation Flow

1. **CV Processing & Storage**
  - OCR extraction using Mistral API for PDF processing
  - ChromaDB vector storage for structured CV data
  - Automatic job role identification

2. **Real-Time Market Research**
  - Tavily search for current salary data and job postings
  - Location-specific compensation analysis
  - Skills demand assessment

3. **Intelligent Analysis & Report Generation**
  - OpenAI Agents SDK for coordinated analysis
  - Primary salary range with currency and location context
  - Experience level alignment and skills impact analysis
  - Source links for verification and credibility

### Tech Stack

- **AI/ML**: OpenAI Agents SDK, GPT-4o-mini, Mistral OCR
- **Search**: Tavily API for real-time market research
- **Storage**: ChromaDB with OpenAI embeddings
