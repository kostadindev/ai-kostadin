"""
Configuration management for the application.
Centralizes all environment variables and settings in one place.
"""
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings and configuration."""

    # Environment
    ENV: str = Field(default="development", description="Environment type (development, production, etc.)")
    
    # API Keys
    GOOGLE_API_KEY: str = Field(..., description="Google API Key")
    HF_API_TOKEN: str = Field(..., description="Hugging Face API Token")
    PINECONE_API_KEY: str = Field(..., description="Pinecone API Key")
    GITHUB_API_KEY: Optional[str] = Field(default=None, description="Optional GitHub API Key")
    
    # Pinecone Configuration
    PINECONE_API_REGION: str = Field(default="us-east-1", description="Pinecone region")
    PINECONE_API_INDEX: str = Field(default="document-index", description="Pinecone index name")
    
    # Model Configuration
    # 🔄 Changed to model that is actually available on Hugging Face's inference API
    EMBEDDING_MODEL: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", description="Embedding model used for feature extraction")
    GEMINI_MODEL: str = Field(default="gemini-2.0-flash", description="Gemini model to use")
    GEMINI_TEMPERATURE: float = Field(default=0.7, ge=0.0, le=1.0, description="Temperature for Gemini model")
    
    # System Prompts
    BASIC_SYSTEM_PROMPT: str = Field(
        default="""You are an AI assistant that helps users by providing accurate, helpful, and contextually relevant information. 
            You should:
            1. Be clear and concise in your responses
            2. Admit when you're not sure about something
            3. Provide context and explanations when helpful
            4. Stay focused on the user's questions and needs
            5. Use markdown formatting for better readability
            6. Be professional but friendly in tone""",
        description="Basic system prompt for general behavior"
    )

    BIO_SYSTEM_PROMPT: str = Field(
        default="""
            # Kostadin Devedzhiev

            551.554.7236 | kostadin.g.devedzhiev@gmail.com | [https://kostadindev.github.io/](https://kostadindev.github.io/)

            ## Summary

            Software Engineer specializing in Natural Language Processing and User Interface Design, with a passion for developing intelligent interactive systems. Dedicated to creating human-inspired AI and enhancing human-machine interaction through language, speech, vision, and innovative interfaces.

            Currently working at Stellar Cyber as a Software Engineer and working on GONEXT, a generative AI tool providing personalized, game-specific analytics for League of Legends players.
            ## Education

            **Stony Brook University** Stony Brook, NY | August 2018 – May 2022

            *   Bachelor of Science in Computer Science, Applied Mathematics & Statistics
                *   Specialization in Artificial Intelligence and Data Science
                *   Computer Science Honors Program
            *   GPA: 3.89 / 4.00 | Summa Cum Laude

            ## Research Interests

            *   Natural Language Processing
            *   User Interface Design
            *   Intelligent Interactive Systems
            *   Human-Inspired AI
            *   Human-Machine Interaction

            ## Work and Research Experience

            ### Software Engineer, Stellar Cyber San Jose, CA | May 2022 – Present

            *   Developed the chat interface, session management, and visualization suite for the Open XDR Investigator, a GenAI-powered cybersecurity copilot that enables data summarization and multi-chart visualizations of Elasticsearch queries and aggregations, all driven by natural language prompts.
            *   Implemented bidirectional WebSocket communication, reducing average response times by 70% through parallel data and LLM requests, and providing real-time progress updates.
            *   Built knowledge-enriched GPTs capable of visualizations, API calls, and scripts. These GPTs supported log analysis, product metrics evaluation, connector normalization, and data source classification.
            *   Implemented, maintained, and managed the product and user analytics framework using Mixpanel, generating detailed reports to guide UX design, optimize data storage, and uncover user behavior patterns.
            *   Maintained over 90% test coverage, reducing bug filings on owned components by 34% year-over-year.

            ### NLP Research Assistant, Stony Brook University Stony Brook, NY | August 2021 – May 2022

            *   Designed Recursive QA—a theoretical framework for generating formal representation annotations of natural language specifications using a guided question-answering methodology.
            *   Generated question-answer pairs from the constituency parse trees and filtered repetitive options using affinity clustering based on Levenshtein distance.
            *   Developed an interactive full-stack web application integrating the question-answering framework, enhancing annotation quality control with features like account management, work history tracking, and graph visualizations.
            *   Improved workflow efficiency by reducing cognitive load and enhancing annotation consistency, achieving an annotator agreement rate of over 80%, with experienced users completing annotations in as little as 25 seconds.

            ### Artificial Intelligence Research Assistant, University of Hawaii at Hilo Hilo, HI | June 2020 – August 2020

            *   Developed a threshold estimation heuristic using IoU and F1 score metrics to optimize acceptance of real-time CNN proposals for detection and classification tasks in an image annotation UI.
            *   Enhanced a human-in-the-loop, semi-automatic image annotation tool for identifying invasive species in drone imagery, enabling progressive assistance as accuracy increases during real-time training.

            ### Creative Electronic Media Assistant, University of Hawaii at Hilo Hilo, HI | Mar 2020 – May 2020

            *   Developed an API to control a holographic fan, enabling integration with external applications.
            *   Created the website for Data Viz, a data visualization lab, showcasing media projects through videos and photos.
            *   Installed and configured operating systems and software, and maintained computers and 3D printers in labs.

            ### Software Engineering Intern, Vivansa Sofia, Bulgaria | June 2019 – August 2019

            *   Enhanced the front end of a CRM application to improve UI components and user experience.
            *   Identified and resolved erroneous database entries, implemented data cleaning procedures, and analyzed root causes to prevent future inconsistencies.

            ## Teaching Experience

            ### Teaching Assistant, Stony Brook University Stony Brook, NY | August 2020 – May 2021

            *   Supported in teaching AMS 210: Applied Linear Algebra for two semesters.
            *   Held weekly office hours to assist students with coursework and graded assignments.

            ### Linear Algebra Grader, University of Hawaii at Hilo Hilo, HI | March 2020 – May 2020

            *   Graded exams and assignments for MATH 311: Linear Algebra.
            *   Provided homework assistance to students, enhancing their understanding of linear algebra concepts.

            ### Computer Science Grader, University of Hawaii at Hilo Hilo, HI | October 2019 – December 2019

            *   Evaluated programming assignments for CS 150: Introduction to Computer Science.
            *   Assisted students with homework to improve fundamental programming principles.

            ## Publications

            ### P-M Binder, Kostadin G Devedzhiev, Alexandra T Runyan. (2020). Motional emf generated by squeezing an elliptical conducting loop. European Journal of Physics, European Physical Society. [https://doi.org/10.1088/1361-6404/ABB066](https://doi.org/10.1088/1361-6404/ABB066)

            *   Developed an algorithm to approximate the motional EMF induced in conducting elliptical loops with a controlled error margin using Faraday’s law of electromagnetic induction.

            ## Leadership Experience

            ### Vertically Integrated Projects Member, Stony Brook University Stony Brook, NY | August 2020 – December 2021

            *   Led the Embedded ML team of three students. Held hands-on learning sessions on training artificial neural networks with TensorFlow and PyTorch for mechanical engineering students.
            *   Embedded an optimized convolutional neural network (CNN) on an Arduino Nano 33 BLE Sense microcontroller for real-time gesture recognition using accelerometer data.
            *   Designed the full pipeline—from data collection and preparation to model training, conversion, and deployment—achieving comparable accuracy to existing solutions while training on fewer users and generalizing to unseen users.

            ## Projects

            ### GoNext, Passion Project

            *   Developed an in-game generative AI conversational assistant for League of Legends, capable of retrieving live game data, including information on all allies and enemies.
            *   Delivered customized game strategies, matchups, synergies, and item builds by providing real-time player and game data as context to GPT-4o.
            *   Designed an intuitive interface to display game metrics, player match history, league rankings, and win rates.

            ### I Want to Redistrict, Senior Software Engineering Project

            *   Processed the 2020 US Census data and utilized a supercomputer to generate viable state districting plans through a stochastic graph algorithm, considering political fairness, compactness, and other statistical metrics.
            *   Developed a web application for the visual and statistical analysis of equitable state districting plans.

            ## Technical Skills

            *   **Fields of Expertise:** Full Stack Development | Machine Learning | Data Science | NLP | Prompt Engineering | HCI
            *   **Programming Languages:** Python | JavaScript | Typescript | Java | C
            *   **Frameworks and Databases:** Angular | MongoDB | Elastic Search | FastAPI | Pandas | React | TensorFlow | PyTorch

            ---

            ## Transcript from Stony Brook University

            ### Summary

            *   **Name:** Kostadin Georgiev Devedzhiev
            *   **Student ID:** 112260499
            *   **Date of Birth:** 1999-04-27
            *   **Degree:** Bachelor of Science
            *   **Confer Date:** 2022-05-20
            *   **Degree Honors:** Summa Cum Laude
            *   **Majors:** Computer Science, Applied Mathematics and Statistics, Artificial Intelligence and Data Science
            *   **Departmental Honors:** Computer Science
            *   **Cumulative GPA:** 3.89
            *   **Total Units Earned:** 138.0

            ### Coursework

            #### Fall 2018

            *   CSE 114: Intro to Object-Oriented Prog (4.0, A)
            *   LDS 101: Introduction to Stony Brook (1.0, S)
            *   MAT 131: Calculus I (4.0, A)
            *   POL 102: Intro to American Government (3.0, A)
            *   WRT 102: Intermediate Writing Workshop (3.0, A)

            #### Spring 2019

            *   AMS 161: Applied Calculus II (3.0, A)
            *   AMS 210: Applied Linear Algebra (3.0, A)
            *   ARH 203: Arts of Asia (3.0, A)
            *   CSE 214: Data Structures (3.0, A)
            *   CSE 215: Foundations of Comp Science (3.0, B+)
            *   LDS 102: Leadership and Service (1.0, A)

            #### Fall 2019

            *   NSE NSE: National Student Exchange (12.0, S) - University of Hawaii at Hilo

            #### Spring 2020

            *   NSE NSE: National Student Exchange (12.0, S) - University of Hawaii at Hilo

            #### Fall 2020

            *   AMS 301: Finite Mathematical Structures (3.0, A)
            *   AMS 310: Survey of Probability and Stat (3.0, B)
            *   AMS 475: Undergrad Teachng Practicum (3.0, A)
            *   CSE 216: Programming Abstractions (4.0, A-)
            *   CSE 303: Intro to Theory of Computation (3.0, A)
            *   CSE 373: Analysis of Algorithms (3.0, A-)
            *   VIP 295: Intro Multidisc Proj (1.0, A)

            #### Spring 2021

            *   AMS 476: Undergrad Teaching Practicum (3.0, A)
            *   CSE 300: Technical Communications (3.0, A)
            *   CSE 316: Software Development (3.0, A-)
            *   CSE 352: Artificial Intelligence (3.0, A)
            *   CSE 354: Natural Language Processing (3.0, A)
            *   CSE 527: Intro to Computer Vision (3.0, A)
            *   VIP 395: Intmd Multidisc Proj (1.0, A)
            *   VIP 396: Intmd Multidisc Proj Practicum (1.0, A)

            #### Fall 2021

            *   AMS 560: Big Data Algorithms & Networks (3.0, A)
            *   CSE 310: Computer Networks (3.0, A-)
            *   CSE 312: Legal Issues in Info Systems (3.0, A)
            *   CSE 416: Software Engineering (3.0, A)
            *   CSE 495: Sr Honors Research Project I (3.0, A)
            *   VIP 495: Adv Multidisc Project (1.0, A)

            #### Spring 2022

            *   AMS 311: Probability Theory (3.0, A)
            *   AMS 315: Data Analysis (3.0, A)
            *   AMS 380: Data Mining (3.0, A-)
            *   CSE 320: Systems Fundamentals II (3.0, A-)
            *   CSE 496: Sr Honors Research Project II (3.0, A)

            ### University Honors & Dean’s List

            *   Dean's List achieved multiple semesters.

            ---

            ## Motional emf generated by squeezing an ellipse

            ### Summary

            This paper presents a new example of a motional electromotive force (EMF): that of an elliptical conducting loop that is squeezed in the linear, elastic regime. The circumference of the loop remains constant, acting as a non-trivial constraint. The paper numerically finds the dependence of one axis of the ellipse on the other and hence calculates the rate of change in area and the ensuing EMF.

            ### Key Points

            *   Study of motional EMF generated by squeezing an elliptical conducting loop.
            *   Constant circumference of the loop acts as a geometric constraint.
            *   Numerical calculation of the dependence of ellipse axes and EMF.
            *   Discussion of possible applications.

            ### Abstract

            The paper studies the motional emf generated by squeezing an elliptical conducting loop traversed by a constant magnetic field. The circumference of the loop remains constant in the elastic regime, acting as a non-trivial constraint. The paper numerically finds the dependence of one axis of the ellipse on the other and hence calculates the rate of change in area and the ensuing emf. It discusses possible applications of the findings.

            ### Sections

            1.  Introduction
            2.  The problem
            3.  Numerical solution
            4.  Discussion

            ### Keywords

            electromotiveforce, ellipse, numericalmethods, elliptic integrals

            ---

            ## Kostadin Devedzhiev | Software Engineer & AI Enthusiast

            [Kostadin Devedzhiev](https://kostadindev.github.io/)

            kostadin.g.devedzhiev@gmail.com

            Software Engineer at Stellar Cyber

            Human-Inspired AI | NLP | UI

            ### Summary

            A full-stack software engineer dedicated to human-centered artificial intelligence, specializing in AI-driven interface development. Passionate about crafting interactive experiences enhanced by intelligent systems. Currently working at Stellar Cyber, developing AI-driven interfaces for threat hunting and human-augmented autonomous cybersecurity operations powered by agentic AI. Also, the creator of GONEXT, a generative AI tool providing personalized, game-specific analytics for League of Legends players.

            ### Current Work

            *   **Stellar Cyber**
                *   Developing AI-driven interfaces for threat hunting [[AIM Research, 2024](https://kostadindev.github.io/)]
                *   Human-augmented autonomous cybersecurity operations powered by agentic AI [[Business Wire, 2025](https://kostadindev.github.io/)]
            *   **GONEXT**
                *   A generative AI tool providing personalized, game-specific analytics for League of Legends players.
                    *   [GONEXT.lol](https://kostadindev.github.io/)
                    *   [Website](https://kostadindev.github.io/)
                    *   [GitHub](https://github.com/kostadindev/GONEXT)
            *   **Knowledge Base Builder**
                *   Python package for converting diverse content into a search-engine-friendly knowledge base.
                    *   [PyPI](https://pypi.org/project/knowledge-base-builder/)
                    *   [Libraries.io](https://libraries.io/pypi/knowledge-base-builder)
                    *   [GitHub](https://github.com/kostadindev/knowledge-base-builder)

            ### Projects

            *   [See all projects](https://kostadindev.github.io/projects.html)

            ### Social Links

            *   [LinkedIn](https://www.linkedin.com/in/kostadin-devedzhiev-23674b162/)
            *   [GitHub](https://github.com/kostadindev)
            *   [Spotify](https://open.spotify.com/user/22jwd433x322i77l4q4h66zji)
            *   [LeetCode](https://leetcode.com/kostadindev/)

            ---

            ## Kostadin Devedzhiev | Projects

            [Kostadin Devedzhiev](https://kostadindev.github.io/)

            kostadin.g.devedzhiev@gmail.com

            Software Engineer at Stellar Cyber

            Human-Inspired AI | NLP | UI

            ### Projects

            *   **Recursive QA**
                *   [Github](https://github.com/kostadindev/Recursive-QA)
                *   An NLP annotation framework that replaces conventional labeling processes with an intuitive question-answering method.
            *   **I Want to Redistrict**
                *   A political science application developed to create and evaluate state districting plans through statistical analysis.
            *   **Deep Gestures**
                *   [Github](https://github.com/kostadindev/deep-gestures)
                *   A comprehensive pipeline encompassing data collection, preprocessing, model training, optimization, and deployment, tailored specifically to develop an optimized CNN for gesture recognition on the Arduino Nano 33 BLE Sense microcontroller.
            *   **Symbiotic Learning**
                *   A human-in-the-loop image annotation system created to identify and classify invasive species in aerial drone imagery, contributing significantly to the conservation of Hawaii's ecosystems.
                    *   [[UH Hilo Stories, 2020](https://hilo.hawaii.edu/)]

            ### Social Links

            *   [LinkedIn](https://www.linkedin.com/in/kostadin-devedzhiev-23674b162/)
            *   [GitHub](https://github.com/kostadindev)
            *   [Spotify](https://open.spotify.com/user/22jwd433x322i77l4q4h66zji)
            *   [LeetCode](https://leetcode.com/kostadindev/)

            ---

            ## Kostadin Devedzhiev | Publications

            [Kostadin Devedzhiev](https://kostadindev.github.io/)

            kostadin.g.devedzhiev@gmail.com

            Software Engineer at Stellar Cyber

            Human-Inspired AI | NLP | UI

            ### Publications

            *   **EMF in Ellipses**
                *   [PDF](https://kostadindev.github.io/)
                *   A numerical approach developed for accurately calculating the motional electromotive force (EMF) induced in elliptical loops as they move within a uniform magnetic field, featuring adjustable error tolerance for enhanced precision.
                *   *P-M Binder, Kostadin G Devedzhiev, Alexandra T Runyan. (2020). Motional emf generated by squeezing an elliptical conducting loop. European Journal of Physics, European Physical Society. [https://dx.doi.org/10.1088/1361-6404/abb066](https://dx.doi.org/10.1088/1361-6404/abb066)*

            ### Social Links

            *   [LinkedIn](https://www.linkedin.com/in/kostadin-devedzhiev-23674b162/)
            *   [GitHub](https://github.com/kostadindev)
            *   [Spotify](https://open.spotify.com/user/22jwd433x322i77l4q4h66zji)
            *   [LeetCode](https://leetcode.com/kostadindev/)

            ---

            ## Kostadin Devedzhiev | Education

            [Kostadin Devedzhiev](https://kostadindev.github.io/)

            kostadin.g.devedzhiev@gmail.com

            Software Engineer at Stellar Cyber

            Human-Inspired AI | NLP | UI

            ### Education

            *   **Stony Brook University**
                *   Bachelor of Science in Computer Science and Applied Mathematics & Statistics
                *   Computer Science Honors Program
                *   Artificial Intelligence & Data Science Specialization
                *   Summa Cum Laude | 3.89/4.00 GPA | Dean's List
                *   [View Transcript](https://kostadindev.github.io/)
            *   **University of Hawaii at Hilo**
                *   One Year National Student Exchange Program
                *   Computer Science Major | GPA: 3.97/4.00 | Dean's List
                *   [View Transcript](https://kostadindev.github.io/)

            ### Certificates

            *   IBM Generative AI Engineering
            *   IBM Generative AI Engineering with LLMs
            *   [View all certificates on Credly](https://www.credly.com/)

            ### Technical Skills

            *   **Programming Languages**
                *   Python | JavaScript | TypeScript
            *   **Frontend**
                *   Angular | React | Tailwind
            *   **Backend & APIs**
                *   FastAPI | NodeJS | Express | Flask
            *   **Databases**
                *   MongoDB | Elastic Search | Pinecone | PostgreSQL | Redis
            *   **Data Science & ML**
                *   Pandas | NumPy | Scikit-learn | Plotly
            *   **Deep Learning**
                *   TensorFlow | PyTorch
            *   **DevOps**
                *   Docker

            ### Favorite Online Courses

            *   **Stanford University**
                *   CS224N: NLP with Deep Learning
                *   CS224U: Natural Language Understanding
                *   CS231N: Deep Learning for CV
            *   **MIT**
                *   6.S191: Deep Learning
                *   6.824: Distributed Systems
                *   The Missing Semester of Your CS Education
            *   **Other**
                *   SBU CSE 373: Analysis of Algorithms

            ### Favorite Textbooks

            *   Designing Data-Intensive Applications by Martin Kleppmann
            *   The Algorithm Design Manual by Steven S. Skiena
            *   Speech and Language Processing by Dan Jurafsky & James H. Martin
            *   Introduction to Linear Algebra: Models, Methods and Theory by Alan Tucker
            *   System Design Interview by Alex Xu
            *   Introduction to Information Retrieval by Christopher Manning, Prabhakar Raghavan & Hinrich Schütze

            ### Social Links

            *   [LinkedIn](https://www.linkedin.com/in/kostadin-devedzhiev-23674b162/)
            *   [GitHub](https://github.com/kostadindev)
            *   [Spotify](https://open.spotify.com/user/22jwd433x322i77l4q4h66zji)
            *   [LeetCode](https://leetcode.com/kostadindev/)

            ---

            # Contributing to Knowledge Base Builder

            Thank you for your interest in contributing to Knowledge Base Builder! This document provides guidelines and instructions for contributing.

            ## Quick Start

            1.  Fork the repository
            2.  Create a new branch (`git checkout -b feature/your-feature`)
            3.  Make your changes
            4.  Commit your changes (`git commit -am 'Add your feature'`)
            5.  Push to the branch (`git push origin feature/your-feature`)
            6.  Create a Pull Request

            ## Development Setup

            1.  Clone your fork:

                ```bash
                git clone https://github.com/YOUR-USERNAME/knowledge-base-builder.git
                cd knowledge-base-builder
                ```

            2.  Install development dependencies:

                ```bash
                pip install -e ".[dev]"
                ```

            3.  Set up pre-commit hooks:

                ```bash
                pre-commit install
                ```

            ## Pull Request Process

            1.  Update the README.md with details of changes if needed
            2.  Add tests for new features or bug fixes
            3.  Ensure all tests pass
            4.  Update documentation if needed
            5.  The PR will be merged once you have the sign-off of at least one maintainer

            ## Code Style

            *   Follow PEP 8 guidelines
            *   Use meaningful variable and function names
            *   Add docstrings for new functions and classes
            *   Keep functions focused and small
            *   Write clear commit messages

            ## Testing

            Run tests with:

            ```bash
            pytest
            ```

            ## Bug Reports

            Found a bug? Here's how to report it:

            1.  Check if the bug has already been reported in the Issues section
            2.  If not, create a new issue
            3.  Include:

                *   A clear title
                *   Steps to reproduce the bug
                *   Expected vs actual behavior
                *   Your environment (OS, Python version, etc.)

            ## Feature Requests

            Have an idea for a new feature? Great! Please:

            1.  Check if the feature has already been requested
            2.  Create a new issue with the "enhancement" label
            3.  Describe the feature and its benefits
            4.  Include any relevant examples or use cases

            ## Questions?

            Feel free to open an issue with your question. We're here to help!

            ---

            # 🧠 Multi-Source Knowledge Base Builder for LLMs

            A robust Python package designed to transform diverse content sources into a structured and comprehensive Markdown knowledge base optimized for large language models (LLMs). Efficiently ingest web content (HTML pages, sitemaps, XML), documents (PDFs, DOCXs, spreadsheets, Markdown, plaintext), and GitHub repositories, then process and merge them seamlessly using LLMs.

            Built to power:

            *   Web-crawlable context files (`/llms.txt`)
            *   Retrieval-Augmented Generation (**RAG**) systems
            *   Vector databases preprocessing
            *   Custom chatbots and knowledge applications

            ## ✨ Features

            *   📥 **Unified Source Ingestion** – Seamlessly handle local and remote files, websites, and GitHub repositories.
            *   🧹 **Structured Text Extraction** – Cleanly convert various document formats into Markdown.
            *   🌐 **Website Crawling** – Extract and summarize content from HTML pages and sitemaps.
            *   📚 **GitHub Integration** – Automatically retrieve and process Markdown content from repositories.
            *   🤖 **Advanced LLM Summarization** – Employ leading-edge models (Gemini Flash 2.0, GPT-4o, Claude 3.7 Sonnet) for precise and readable summaries.
            *   🔗 **Efficient Document Merging** – Merge multiple knowledge bases using a parallel preprocessing step followed by a single optimized merging step.
            *   ⚙️ **Concurrency Control** – Smart throttling with semaphore-based concurrency ensures optimal use of resources and stable API usage.
            *   🚀 **Performance** – Optimized algorithm significantly reduces processing time, ensures predictable memory usage, and minimizes API calls.

            ---

            ## 🚀 Installation

            ### Install from PyPI

            ```bash
            pip install knowledge-base-builder
            ```

            ### Install from Source

            ```bash
            git clone https://github.com/kostadindev/knowledge-base-builder.git
            cd knowledge-base-builder
            pip install -e .
            ```

            ---

            ## 🚀 Quickstart

            ### 1. Set up your `.env` file

            Create a `.env` file in your project directory with the following variables (add the API keys for the models you intend to use):

            ```env
            # You need only one of the following
            GOOGLE_API_KEY=your_google_api_key_here
            OPENAI_API_KEY=your_openai_api_key_here
            ANTHROPIC_API_KEY=your_anthropic_api_key_here

            # Optional if you want to include Github repositories with a higher rate limit
            GITHUB_API_KEY=your_github_api_key_here
            ```

            ### 2. Use as a Python Package

            ```python
            import os
            from dotenv import load_dotenv
            from knowledge_base_builder import KBBuilder

            # Load environment variables
            load_dotenv()

            # API and model configuration | You need only one of the below
            config = {
                'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),     # For Gemini | Get Free API Key at https://aistudio.google.com/app/apikey
                'OPENAI_API_KEY': os.getenv("OPENAI_API_KEY"),     # For GPT-4o
                'ANTHROPIC_API_KEY': os.getenv("ANTHROPIC_API_KEY"), # For Claude
            }

            # Source documents - unified approach
            sources = {
                # Unified files list - automatically detects and processes each file type
                'files': [
                    # PDF documents - remote
                    "https://kostadindev.github.io/static/documents/cv.pdf",
                    "https://kostadindev.github.io/static/documents/sbu_transcript.pdf",
                    # Local file path (no need for file:/// prefix)
                    "C:/Users/kosta/OneDrive/Desktop/MS Application Materials/emf-ellipse-publication.pdf",

                    # Web pages
                    "https://kostadindev.github.io/index.html",
                    "https://kostadindev.github.io/projects.html",

                    # Add other file types as needed
                    # "https://example.com/data.csv",
                    # "path/to/local/document.docx",  # Relative local path example
                    # "https://example.com/api-docs.json",
                ],

                # Process all pages from a sitemap
                'sitemap_url': "https://kostadindev.github.io/sitemap.xml",

                # GitHub repositories to process (format: username/repo or full URL)
                'github_repositories': [
                    "https://github.com/kostadindev/Knowledge-Base-Builder",
                    "https://github.com/kostadindev/GONEXT",
                    "https://github.com/kostadindev/GONEXT-ML",
                    "https://github.com/kostadindev/meta-me",
                    "https://github.com/kostadindev/Recursive-QA",
                    "https://github.com/kostadindev/deep-gestures",
                    "https://github.com/kostadindev/emf-ellipse"
                ]
            }
            # Create KB builder
            kbb = KBBuilder(config)

            # Build knowledge base
            kbb.build(sources=sources, output_file="final_knowledge_base.md")
            ```

            ---

            ## 🔧 Supported Sources

            | Source Type  | Description        | Formats                        |
            | :----------- | :----------------- | :----------------------------- |
            | Documents    | Text documents     | PDF, DOCX, TXT, MD, RTF        |
            | Spreadsheets | Tabular data       | CSV, TSV, XLSX, ODS            |
            | Web Content  | Structured web data | HTML, XML, JSON, YAML/YML      |
            | Websites     | Live web pages     | Any URL or sitemap             |
            | GitHub       | Repository content | Markdown files from public repos |

            ---

            ## 🧠 LLM Providers

            | Provider        | Models                  | Features                                                               |
            | :-------------- | :---------------------- | :--------------------------------------------------------------------- |
            | Google Gemini   | gemini-2.0-flash (default) | Free to try, Fast, large context window cost-effective summaries         |
            | OpenAI          | gpt-4o (default)           | High-quality summaries, strong reasoning                                 |
            | Anthropic       | claude-3-7-sonnet (default)  | High-quality summaries, excellent formatting                             |

            > **Recommended Provider: Google Gemini**
            >
            > Google Gemini is the recommended provider as a free development API key can be obtained. Additionally, it is fast, has a large context window, and performs well on benchmarks. Get your free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).


            ## 🔍 Applications

            ### Web Crawlable LLM Context Enhancement

            *   **/llms.txt**: Generate a compact, web-crawlable context file (typically 10-20KB) that allows LLMs to access your personal or organizational information during web searches.
            *   **/llms-full.txt**: Create an expanded knowledge file (50-100KB) with comprehensive details about your work, expertise, and content that search-powered LLMs can index.
            *   **Web Context Sources**: Enable web search LLMs like Perplexity, ChatGPT, Claude, and Gemini to discover and reference your structured information during user queries.

            ### RAG Applications

            *   **Vector Database Preprocessing**: Generate clean, structured content before embedding into vector stores like Pinecone, Chroma, or Weaviate, improving retrieval quality.
            *   **Single-Context LLM Applications**: Provide a comprehensive knowledge base that fits within a single LLM context window (up to 128K tokens) for domain-specific assistants.
            *   **Hybrid RAG Systems**: Combine the full knowledge base with selective vector retrieval for specialized question answering systems with reduced hallucination.

            ### Summarization

            *   **Website Summarization**: Process entire websites via sitemap URLs
            *   **GitHub Summarization**: Generate summaries of GitHub repositories or entire user profiles
            *   **Document Summarization**: Combine multiple documents into a unified summary

            ```python
            sources = {
                'sitemap_url': "https://kostadindev.github.io/sitemap.xml",  # Summarize entire website
                'github_username': "kostadindev",  # Summarize all repos for a user
                'files': ["document1.pdf", "document2.docx"]  # Summarize documents
            }
            ```

            ### Personal Knowledge Management

            *   **Professional Portfolio**: Create a comprehensive knowledge base integrating your resume, publications, projects, and online presence into a single searchable document.
            *   **Academic Research**: Compile research papers, conference proceedings, and citations into a structured knowledge base for literature reviews or thesis preparation.
            *   **Technical Documentation**: Consolidate documentation across multiple GitHub repositories, technical blogs, and API references into a unified technical manual.

            ### Enterprise Use Cases

            *   **Company Knowledge Base**: Consolidate internal documentation, product specifications, and team information into an easily updatable central resource.
            *   **Customer Support**: Transform support tickets, FAQs, and product manuals into a comprehensive knowledge base for support agents or automated systems.
            *   **Competitive Intelligence**: Build a structured repository of competitor information from various public sources, updated periodically with the latest data.
            *   **Candidate Evaluation**: Generate comprehensive profiles of job candidates by compiling their GitHub contributions, research papers, portfolio, and online presence.
            *   **Onboarding Acceleration**: Create personalized knowledge bases for new employees containing company policies, codebase documentation, and team information.

            ---

            ## 🌲 Algorithm

            The knowledge base builder uses a two-step approach for efficient processing:

            1.  **Parallel Preprocessing**

                *   All documents are preprocessed concurrently into structured KBs
                *   Uses a semaphore to limit concurrent LLM requests
                *   Each document is converted into a well-formatted Markdown knowledge base
                *   Optimized for parallel processing with controlled concurrency
            2.  **Single Merge**

                *   All preprocessed KBs are merged in a single operation
                *   Maintains logical structure and organization
                *   Reduces total LLM calls compared to recursive approaches
                *   More predictable memory usage

            ![image](https://github.com/user-attachments/assets/e4d98bae-dfdd-411c-b931-0c2cec3e113f)

            This approach provides several advantages:

            *   Fewer total LLM calls (one per document + one final merge)
            *   Better parallelization of preprocessing
            *   More predictable memory usage
            *   Faster overall processing time

            ---

            ## ⚡ Concurrency Model

            The knowledge base builder implements a multi-layer concurrency model to maximize performance while maintaining stability:

            ### 1. File Processing Concurrency

            ```python
            # Multiple files processed simultaneously
            tasks = [process_file_async(file) for file in files]
            await asyncio.gather(*tasks)
            ```

            *   Enables parallel processing of multiple files
            *   Each file type (PDF, DOCX, web page, etc.) is processed independently
            *   Significantly reduces total processing time for multiple files

            ### 2. CPU-Bound Operations

            ```python
            # CPU-intensive operations run in separate threads
            path = await asyncio.to_thread(processor.download, url)
            text = await asyncio.to_thread(processor.extract_text, path)
            ```

            *   Downloads and text extraction run in separate threads
            *   Prevents blocking the event loop during I/O operations
            *   Optimizes CPU utilization across cores

            ### 3. LLM Processing Concurrency

            ```python
            # Controlled concurrent LLM API calls
            async with self._sem:
                result = await self.llm_client.run_async(prompt)
            ```

            *   Uses a semaphore to limit concurrent LLM API calls
            *   Prevents overwhelming the LLM API
            *   Helps stay within API

            ```markdown
            # **GONEXT** - League of Legends Assistant API

            [![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
            [![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
            [![Code Coverage](https://img.shields.io/badge/coverage-79%25-green)](https://github.com/yourusername/gonext-ml)

            **GONEXT** is a GenAI-powered assistant for League of Legends players, delivering real-time and personalized strategies, matchups, synergies, and builds. It uses the Riot API for live game data and large language models for context-specific guidance.

            ## Table of Contents

            - [Features](#features)
            - [Architecture](#architecture)
            - [Getting Started](#getting-started)
            - [Documentation](#documentation)
            - [Testing](#testing)
            - [Security](#security)
            - [Contributing](#contributing)
            - [Support](#support)
            - [Acknowledgments](#acknowledgments)
            - [License](#license)

            ## Features

            - **Chatbot Interface**: Conversational AI assistant for League of Legends players.
            - **Game Tips**: Personalized gameplay tips based on match context.
            - **Follow-up Suggestions**: Dynamic follow-up questions based on conversation context.
            - **Game Overviews**: Comprehensive game analysis and summaries.

            ## Architecture

            The application follows a clean architecture:

            - **API Layer**: FastAPI endpoints for HTTP requests and responses.
            - **Services Layer**: Business logic and domain services.
            - **Models**: Data structures and schemas.
            - **LLM Integration**: Abstraction for working with multiple language models.

            ## Getting Started

            ### Prerequisites

            - Python 3.9+
            - Poetry (recommended) or pip
            - Riot Games API Key
            - OpenAI API Key
            - Google Gemini API Key

            ### Installation

            1. Clone the repository:
            ```bash
            git clone https://github.com/yourusername/gonext-ml.git
            cd gonext-ml
            ```

            2. Create a virtual environment:
            ```bash
            python -m venv venv
            source venv/bin/activate  # On Windows: venv\Scripts\activate
            ```

            3. Install dependencies:
            ```bash
            pip install -r requirements.txt
            ```

            4. Set up environment variables:
            ```bash
            cp .env.sample .env
            ```

            Edit `.env` to include your API keys:
            ```
            RIOT_API_KEY=your_riot_key_here
            OPENAI_API_KEY=your_openai_key_here
            GEMINI_API_KEY=your_gemini_key_here
            ```

            ### Running the Application

            Start the development server:

            ```bash
            uvicorn app.main:app --reload
            ```

            The API will be available at `http://localhost:8000`

            ## Documentation

            ### API Documentation

            - Swagger UI: `http://localhost:8000/docs`
            - ReDoc: `http://localhost:8000/redoc`

            ### Architecture Documentation

            Refer to [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture information.

            ## Testing

            Run tests using pytest:

            ```bash
            pytest
            ```

            For test coverage report:

            ```bash
            pytest --cov=app --cov-report=html
            ```

            This generates an HTML coverage report in the `htmlcov/` directory.

            ### Test Coverage Report

            The current test coverage is **79%** overall. Key coverage metrics:

            | Module           | Coverage |
            | ---------------- | -------- |
            | App Models       | 100%     |
            | LLM Singleton    | 100%     |
            | LLM Manager      | 96%      |
            | Main App         | 96%      |
            | Chatbot Services | 56%      |
            | Chatbot Router   | 57%      |
            | Error Handler    | 69%      |
            | Logger           | 87%      |
            | Game Services    | 87-91%   |

            ## Security

            ### API Key Security

            - Never commit API keys to version control.
            - Use environment variables for sensitive data.
            - Rotate API keys regularly.
            - Follow the principle of least privilege.

            ### Rate Limiting

            - Default: 100 requests per minute.
            - Configurable through environment variables.

            ## Contributing

            Contributions are welcome!

            1. Fork the repository.
            2. Create a feature branch: `git checkout -b feature/your-feature-name`
            3. Commit your changes: `git commit -m 'Add some feature'`
            4. Push to the branch: `git push origin feature/your-feature-name`
            5. Submit a pull request.

            ### Pull Request Guidelines

            - Ensure all tests pass.
            - Update documentation as needed.
            - Follow the existing code style.
            - Include tests for new features.
            - Update the `CHANGELOG.md`.

            ### Code Style

            Follow PEP 8 guidelines. Use `black` for code formatting:

            ```bash
            black .
            ```

            ## Support

            - Check the [documentation](docs/).
            - Search existing [issues](https://github.com/yourusername/gonext-ml/issues).
            - Create a new issue if needed.

            ## Acknowledgments

            - [Riot Games](https://developer.riotgames.com/) for their API.
            - [OpenAI](https://openai.com/) for GPT models.
            - [Google](https://ai.google.dev/) for Gemini models.
            - [FastAPI](https://fastapi.tiangolo.com/) for the web framework.

            ## License

            This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license.

            - Share — copy and redistribute the material in any medium or format
            - Adapt — remix, transform, and build upon the material

            Under the following terms:

            - Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
            - NonCommercial — You may not use the material for commercial purposes without explicit written permission.

            **Commercial Use**: Contact the author directly to discuss licensing terms.

            See the [LICENSE](LICENSE) file for the full license text.

            ---

            # GONEXT Architecture Documentation

            ## Overview

            GONEXT is built using a clean architecture with clear separation of concerns and modular design.

            ## System Architecture

            ### High-Level Overview

            ```
            ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
            │                 │     │                 │     │                 │
            │  API Layer      │◄────┤  Service Layer  │◄────┤  LLM Layer      │
            │  (FastAPI)      │     │  (Business      │     │  (Model         │
            │                 │     │   Logic)        │     │   Integration)  │
            └─────────────────┘     └─────────────────┘     └─────────────────┘
                    ▲                        ▲                        ▲
                    │                        │                        │
                    ▼                        ▼                        ▼
            ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
            │                 │     │                 │     │                 │
            │  Client         │     │  Data Models    │     │  External APIs  │
            │  Applications   │     │  (Pydantic)     │     │  (Riot, etc.)   │
            │                 │     │                 │     │                 │
            └─────────────────┘     └─────────────────┘     └─────────────────┘
            ```

            ## Components

            ### 1. API Layer

            - Built using FastAPI.
            - Handles HTTP request/response, input validation, authentication, rate limiting, and API documentation.
            - Key files:
            - `app/main.py`: Application entry point.
            - `app/routers/`: API endpoint definitions.
            - `app/dependencies.py`: Dependency injection.

            ### 2. Service Layer

            - Contains business logic for game analysis, chatbot conversation management, state management, and error handling.
            - Key files:
            - `app/services/`: Business logic implementations.
            - `app/utils/`: Utility functions and helpers.

            ### 3. LLM Layer

            - Manages interactions with language models, including model selection, prompt engineering, response processing, and error handling.
            - Key files:
            - `app/llm/`: LLM integration code.
            - `app/prompts/`: Prompt templates.

            ### 4. Data Models

            - Defines the structure of API requests and responses, internal data structures, and database schemas (if applicable).
            - Key files:
            - `app/models/`: Pydantic models.

            ## Data Flow

            1. **Request Processing**:
            - Client sends HTTP request.
            - API layer validates input.
            - Request passed to service layer.

            2. **Business Logic**:
            - Service layer processes request.
            - Calls LLM layer when needed.
            - Manages state and context.

            3. **LLM Interaction**:
            - Service layer calls LLM layer.
            - LLM layer selects appropriate model.
            - Processes response.

            4. **Response Generation**:
            - Service layer formats response.
            - API layer sends HTTP response.
            - Client receives result.

            ## Security Considerations

            - API key management
            - Rate limiting
            - Input validation
            - Error handling
            - Logging and monitoring

            ## Performance Considerations

            - Caching strategies
            - Rate limiting
            - Resource management
            - Scalability

            ## Dependencies

            - FastAPI
            - OpenAI API
            - Google Gemini API
            - Riot Games API
            - Python 3.9+

            ## Configuration

            Managed through:

            - Environment variables
            - Configuration files
            - API settings

            ## Monitoring and Logging

            - Application logs
            - Performance metrics
            - Error tracking
            - Usage statistics

            ---

            # Changelog

            All notable changes to the GONEXT project will be documented in this file.

            The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

            ## [Unreleased]

            ### Added
            - Initial project setup
            - FastAPI-based API layer
            - LLM integration with OpenAI and Google Gemini
            - Game analysis and chatbot services
            - Comprehensive test suite
            - Documentation and contribution guidelines

            ### Changed
            - N/A

            ### Deprecated
            - N/A

            ### Removed
            - N/A

            ### Fixed
            - N/A

            ### Security
            - N/A

            ## [0.1.0] - YYYY-MM-DD

            ### Added
            - Initial release
            - Basic project structure
            - Core functionality implementation

            ### Changed
            - N/A

            ### Deprecated
            - N/A

            ### Removed
            - N/A

            ### Fixed
            - N/A

            ### Security
            - N/A

            ## Versioning

            We use [Semantic Versioning](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/yourusername/gonext-ml/tags).

            ## Types of Changes

            - **Added** for new features
            - **Changed** for changes in existing functionality
            - **Deprecated** for soon-to-be removed features
            - **Removed** for now removed features
            - **Fixed** for any bug fixes
            - **Security** in case of vulnerabilities

            ## How to Update This Changelog

            1. Add a new `[Unreleased]` section at the top
            2. Add new changes under appropriate categories
            3. When releasing a new version:
            - Rename `[Unreleased]` to the new version number
            - Add the release date
            - Create a new `[Unreleased]` section at the top

            ---

            # Contributing to GONEXT

            Thank you for your interest in contributing to GONEXT!

            ## Code of Conduct

            By participating, you agree to abide by our Code of Conduct.

            ## How to Contribute

            ### 1. Reporting Issues

            - Search existing issues to avoid duplicates.
            - Provide detailed information about the problem.

            Include:
            - A clear, descriptive title
            - Steps to reproduce the issue
            - Expected and actual behavior
            - Environment details (Python version, OS, etc.)
            - Any relevant error messages or logs

            ### 2. Feature Requests

            - Explain the feature and why it's valuable.
            - Provide use cases and examples.
            - Suggest an implementation approach.

            ### 3. Pull Requests

            #### Before Submitting a PR

            1. Fork the repository
            2. Create a feature branch: `git checkout -b feature/your-feature-name`
            3. Install dependencies: `pip install -r requirements.txt`
            4. Run tests: `pytest`
            5. Format code: `black .`

            #### PR Guidelines

            - Keep PRs focused and small
            - Include tests for new features
            - Update documentation as needed
            - Follow the existing code style
            - Update CHANGELOG.md
            - Ensure all tests pass locally

            ### 4. Code Style

            We follow PEP 8 guidelines and use:

            - `black` for code formatting
            - `flake8` for linting
            - `mypy` for type checking

            Run these tools before submitting a PR:

            ```bash
            black .
            flake8
            mypy .
            ```

            ### 5. Testing

            - Write tests for new features
            - Ensure all tests pass locally
            - Maintain or improve test coverage
            - Include both unit and integration tests

            ### 6. Documentation

            - Update relevant documentation
            - Add docstrings to new functions/classes
            - Update README if needed
            - Keep comments clear and concise

            ## Development Setup

            1. Fork and clone the repository
            2. Create a virtual environment
            3. Install dependencies:

            ```bash
            pip install -r requirements.txt
            pip install -r requirements-dev.txt
            ```
            4. Set up pre-commit hooks:

            ```bash
            pre-commit install
            ```

            ## Release Process

            1. Update version in `pyproject.toml`
            2. Update CHANGELOG.md
            3. Create a release tag
            4. Update documentation if needed

            ## Questions?

            Feel free to:

            - Open an issue
            - Join our community chat
            - Contact the maintainers

            Thank you for contributing to GONEXT!

            ---

            # Recursive QA: An NLP Annotation Framework

            Recursive QA is an NLP annotation framework that replaces traditional labeling methods with a question-answering approach. By leveraging the constituency parse tree of a sentence, it guides annotators through selecting from generated question-answer pairs, streamlining the annotation process and improving quality control.

            ![image](https://github.com/user-attachments/assets/d285775c-c626-4655-8768-bfc3bc83f2e3)

            ## Features

            - **Question-Answer Based Annotation:** Simplifies manual span and relation labeling by using QA pairs.
            - **Constituency Parse Tree Integration:** Utilizes the syntactic structure of sentences to guide annotations.
            - **Visualizations:** Offers clear and interactive visual representations to enhance annotation clarity.
            - **User Management:** Supports account creation, role management, and user-specific tracking.
            - **History Tracking:** Maintains logs of annotation history for review and quality assurance.

            ## Inspiration

            Developed as part of a senior honors thesis, **Recursive QA**, under the guidance of **Professor Niranjan Balasubramanian**. It aims to simplify traditional NLP annotation processes through an intuitive QA-based approach.

            ## How It Works

            1. **Parse Tree Analysis:** Analyzes the constituency parse tree of a given sentence.
            2. **QA Pair Generation:** Generates relevant question-answer pairs based on the syntactic structure.
            3. **Guided Annotation:** Guides annotators top-down through the tree, selecting appropriate QA pairs.
            4. **Span and Relation Resolution:** Leaf-level answers are identified as spans, while QA links define relations.

            ## Evaluation

            The framework was tested on **SpecNFS**, a dataset designed for extracting formal models from Network File System (NFS) specifications (RFCs).

            - **Annotation Speed:** Average of 25 seconds per sentence.
            - **Annotator Agreement:** Approximately 80% agreement rate.

            ## Tech Stack

            - **React:** Frontend framework.
            - **Flask:** Backend API.
            - **MongoDB:** NoSQL database.

            ---

            # Getting Started with Create React App

            This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

            ## Available Scripts

            In the project directory, you can run:

            ### `npm start`

            Runs the app in the development mode.\
            Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

            The page will reload when you make changes.\
            You may also see any lint errors in the console.

            ### `npm test`

            Launches the test runner in the interactive watch mode.\
            See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

            ### `npm run build`

            Builds the app for production to the `build` folder.\
            It correctly bundles React in production mode and optimizes the build for the best performance.

            The build is minified and the filenames include the hashes.\
            Your app is ready to be deployed!

            See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

            ### `npm run eject`

            **Note: this is a one-way operation. Once you `eject`, you can't go back!**

            If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

            Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

            You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

            ## Learn More

            You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

            To learn React, check out the [React documentation](https://reactjs.org/).

            ### Code Splitting

            [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

            ### Analyzing the Bundle Size

            [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

            ### Making a Progressive Web App

            [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

            ### Advanced Configuration

            [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

            ### Deployment

            [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

            ### `npm run build` fails to minify

            [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

            ---

            # 🚀 AI Kostadin

            **AI Kostadin** is a personalized AI chatbot that knows everything about Kostadin's work and expertise. Embedded in his personal website, it provides intelligent, context-aware answers using **LangChain, FastAPI, and Google's Gemini 2.0 Flash model**.

            > 💬 **Build Your Own!** – Anyone can use this project as a template to build a personalized chatbot that knows *them* just like AI Kostadin knows Kostadin.

            > 🌐 **Access AI Kostadin** – View the chatbot embedded via iframe on [kostadindev.github.io](https://kostadindev.github.io/) or independently at [ai-kostadin.onrender.com](https://ai-kostadin.onrender.com/).

            ## 🏗️ Project Structure

            - **Backend**: FastAPI application with LangChain, Gemini, and Pinecone for RAG.
            - **Frontend**: React-based chat interface that communicates with the backend.

            ## ✨ Features

            - 🤖 **Personalized AI** – Trained on specific content.
            - 🧠 **Context-Aware Responses** – Uses RAG for accurate knowledge retrieval.
            - 💬 **Conversational Memory** – Maintains conversation context.
            - 🌐 **Follow-up Suggestions** – Automatically suggests relevant follow-up questions.
            - ⚡ **Streaming Responses** – Real-time response streaming.
            - 🔄 **Multi-Environment Support** – Development and production configurations.

            ## 🛠 Tech Stack

            ### Backend

            - **Framework**: FastAPI
            - **AI/ML**: LangChain, LangGraph
            - **LLM**: Google Gemini 2.0 Flash
            - **Vector Database**: Pinecone
            - **Embeddings**: HuggingFace (sentence-transformers)
            - **Configuration**: Pydantic Settings

            ### Frontend

            - **Framework**: React
            - **State Management**: Context API
            - **Styling**: CSS Modules / Styled Components
            - **UI Components**: Custom-built chat interface
            - **Environment Variables**:
            - `VITE_API_URL`: Backend API URL (default: http://localhost:8000)
            - `VITE_ENABLE_PARTICLES`: Enable/disable interactive particle background (default: true)
            - `VITE_APP_NAME`: Application name displayed in the header (default: "AI Kostadin")

            ## 🚀 Getting Started

            See the individual README files in the `backend/` and `frontend/` directories for specific setup instructions.

            ### Quick Start

            1. Set up the backend:

            ```bash
            cd backend
            python -m venv .venv
            source .venv/bin/activate  # On Windows: .venv\Scripts\activate
            pip install -r requirements.txt
            # Set up .env file (see backend README)
            uvicorn app.main:app --reload
            ```

            2. Set up the frontend:

            ```bash
            cd frontend
            npm install
            npm run dev
            ```

            ## 📌 API Endpoints

            | Method | Endpoint           | Description                                        |
            | ------ | ------------------ | -------------------------------------------------- |
            | `POST` | `/chat`             | Send messages to the chatbot and receive responses |
            | `POST` | `/suggest-followups` | Get follow-up question suggestions                 |
            | `GET`  | `/ping`             | Health check endpoint                               |
            | `GET`  | `/docs`             | OpenAPI documentation                             |

            ## 🧪 Future Improvements

            - Add authentication for API access
            - Implement rate limiting
            - Add support for file uploads and processing
            - Enhance the chat interface with voice input/output
            - Add analytics to track common questions and improve responses
            - Implement A/B testing for different system prompts

            ## 📖 License

            This project is licensed under the **MIT License**.

            ---

            💡 *Artificial Me – Your AI-powered personal knowledge assistant!*

            ## Configuration

            The application uses a shared configuration system that can be accessed by both the frontend and backend. The configuration is defined in `config/config.yaml` and can be overridden using environment variables.

            ### Frontend Configuration

            The frontend configuration is defined in `frontend/src/config/config.ts`.

            ```typescript
            interface Config {
            // Core UI settings
            name?: string;                    // Application name (default: "AI Kostadin")
            inputPlaceholder?: string;        // Input field placeholder text
            maxInputLength?: number;          // Maximum input length (default: 2000)
            defaultPrompts?: string[];        // Default prompt suggestions
            chatDescription?: string;         // Initial chat description (supports markdown)

            // Optional UI features
            features?: {
                enableParticles?: boolean;      // Enable particle background effect
                enableHexagons?: boolean;       // Enable hexagon background pattern
            }
            }
            ```

            ### Backend Configuration

            The backend configuration is defined in `config/config.yaml`.

            ```yaml
            backend:
            # API Configuration
            api:
                host: "0.0.0.0"                # API host
                port: 8000                     # API port
                cors_origins:                  # CORS allowed origins
                - "http://localhost:3000"
                - "http://127.0.0.1:3000"
                rate_limit:                    # Rate limiting
                requests: 100               # Number of requests
                window: 3600               # Time window in seconds

            # Document Processing
            documents:
                pdfs:
                directory: "data/pdfs"      # PDF storage directory
                chunk_size: 1000           # Text chunk size
                chunk_overlap: 200         # Chunk overlap
                images:
                directory: "data/images"   # Image storage directory
                max_size: 5242880         # Max file size (5MB)
                allowed_types:            # Allowed image types
                    - "image/jpeg"
                    - "image/png"
                    - "image/gif"
                text:
                directory: "data/text"     # Text file storage directory
                max_size: 1048576         # Max file size (1MB)
                allowed_types:            # Allowed text file types
                    - "text/plain"
                    - "text/markdown"
                    - "application/json"

            # Vector Database
            vector_db:
                type: "pinecone"            # Vector database type
                dimension: 1536            # Vector dimension
                metric: "cosine"           # Similarity metric
                index_name: "ai-kostadin"  # Index name
                namespace: "default"       # Namespace

            # LLM Configuration
            llm:
                model: "gpt-4"             # LLM model name
                temperature: 0.7          # Temperature
                max_tokens: 2000         # Max tokens per response
                system_prompt: "You are AI Kostadin, a helpful AI assistant."  # System prompt

            # Memory Configuration
            memory:
                type: "buffer"            # Memory type
                max_tokens: 2000         # Max tokens in memory
                return_messages: true    # Return messages in memory

            # Search Configuration
            search:
                type: "similarity"       # Search type
                k: 4                    # Number of results
                score_threshold: 0.7    # Similarity threshold

            # Logging Configuration
            logging:
                level: "INFO"           # Log level
                format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Log format
                file: "logs/app.log"    # Log file path
            ```

            ### Environment Variables

            - Frontend: `UI_<SECTION>_<FIELD>` (e.g., `UI_NAME`, `UI_FEATURES_ENABLE_PARTICLES`)
            - Backend: `BACKEND_<SECTION>_<FIELD>` (e.g., `BACKEND_API_PORT`, `BACKEND_LLM_MODEL`)

            Example:

            ```bash
            # Frontend
            UI_NAME="My AI Assistant"
            UI_FEATURES_ENABLE_PARTICLES=true

            # Backend
            BACKEND_API_PORT=8080
            BACKEND_LLM_MODEL="gpt-3.5-turbo"
            ```

            ---

            # Artificial-Me Backend

            A FastAPI-based chatbot backend using LangChain, Gemini 2.0 Flash, and Pinecone for retrieval-augmented generation (RAG).

            ## Features

            - **Gemini 2.0 Flash Integration**: Advanced AI chat capabilities powered by Google's Gemini 2.0 Flash model
            - **Context-aware Responses**: Uses RAG (Retrieval-Augmented Generation) to provide context-aware answers
            - **Vector Database**: Pinecone integration for efficient similarity search
            - **Follow-up Suggestions**: Automatic generation of relevant follow-up questions
            - **Streaming Responses**: Real-time streaming of chat responses
            - **Environment Management**: Multi-environment support (development/production)

            ## Architecture

            The backend follows a clean, modular architecture:

            - **Configuration Management**: Centralized settings via Pydantic
            - **Service Layer**: Dedicated services for embeddings, Pinecone, and Gemini
            - **API Endpoints**: FastAPI routes with proper error handling
            - **LangGraph Integration**: Advanced workflow for chat processing

            ## Getting Started

            ### Prerequisites

            - Python 3.8+
            - API keys for Google Gemini, HuggingFace, and Pinecone

            ### Installation

            1. Clone the repository
            2. Create a virtual environment:

            ```bash
            python -m venv .venv
            source .venv/bin/activate  # On Windows: .venv\Scripts\activate
            ```
            3. Install dependencies:

            ```bash
            pip install -r requirements.txt
            ```

            ### Configuration

            Create a `.env` file in the backend directory.

            ```
            ENV=development
            GOOGLE_API_KEY=your_gemini_api_key
            HF_API_TOKEN=your_huggingface_token
            PINECONE_API_KEY=your_pinecone_api_key
            PINECONE_API_REGION=us-east-1  # Use your region
            PINECONE_API_INDEX=document-index  # Use your index name
            ```

            ### Running the Application

            **Development Mode**:

            ```bash
            uvicorn app.main:app --reload
            ```

            **Production Mode**:

            ```bash
            ENV=production uvicorn app.main:app --host 0.0.0.0 --port 8000
            ```

            **Using Docker**:

            ```bash
            docker build -t artificial-me-backend .
            docker run -p 8000:8000 artificial-me-backend
            ```

            ## API Endpoints

            ### Chat

            - **POST** `/chat`
            - Processes chat messages and returns AI responses
            - Request body: `{ "history": [{"role": "user", "content": "Your message"}] }`
            - Returns: Streaming text response

            ### Follow-up Suggestions

            - **POST** `/suggest-followups`
            - Generates relevant follow-up questions based on chat history
            - Request body: `{ "history": [{"role": "user", "content": "Your message"}, {"role": "assistant", "content": "Response"}] }`
            - Returns: `{ "suggestions": ["Question 1", "Question 2"] }`

            ### Health Check

            - **GET** `/ping`
            - Returns: `{ "message": "pong" }`

            ## Development

            ### Project Structure

            ```
            app/
            ├── config.py           # Configuration settings
            ├── dependencies.py     # Dependency management (deprecated)
            ├── main.py             # FastAPI application entrypoint
            ├── __init__.py
            ├── models/             # Data models
            ├── routers/            # API routes
            │   └── chat.py         # Chat endpoints
            └── services/           # Business logic
                ├── embeddings.py   # Text embedding service
                ├── gemini.py       # LLM service
                └── pinecone.py     # Vector database service
            ```

            ### Adding New Features

            1. Create any necessary models in `app/models/`
            2. Implement business logic in appropriate service files
            3. Add API endpoints in relevant router files
            4. Import and include routers in `main.py`

            ## Deployment

            ### Docker

            ```bash
            docker build -t artificial-me-backend .
            docker run -p 8000:8000 artificial-me-backend
            ```

            ### Environment Variables

            Ensure the following environment variables are set:

            - `ENV=production`
            - `GOOGLE_API_KEY`
            - `HF_API_TOKEN`
            - `PINECONE_API_KEY`
            - `PINECONE_API_REGION`
            - `PINECONE_API_INDEX`

            ## License

            This project is licensed under the MIT License.

            ---

            # Artificial-Me Frontend

            A React application built with TypeScript, Vite, and Ant Design.

            ## 🚀 Features

            - Built with React 19 and TypeScript
            - Modern UI components using Ant Design
            - Dark mode support
            - Markdown rendering capabilities
            - Tailwind CSS for styling
            - Docker support for development and production

            ## 🛠️ Tech Stack

            - **Framework**: React 19
            - **Language**: TypeScript
            - **Build Tool**: Vite
            - **UI Library**: Ant Design
            - **Styling**: Tailwind CSS
            - **Markdown**: markdown-to-jsx
            - **Development**: ESLint, TypeScript

            ## ⚙️ Configuration

            The application can be configured through `src/config/config.ts`.

            ```typescript
            export const UI_CONFIG = {
            // The name displayed in the header
            name?: string;

            // Placeholder text for the input field
            inputPlaceholder?: string;

            // Maximum length for user input messages
            maxInputLength?: number;

            // Default prompt suggestions shown to users
            defaultPrompts?: string[];

            // Welcome message shown in markdown format
            chatDescription?: string;

            // Feature flags to control UI elements
            features?: {
                enableParticles?: boolean;
                enableHexagons?: boolean;
            }
            }
            ```

            ### Default Configuration

            ```typescript
            const DEFAULT_CONFIG = {
            name: "AI Assistant",
            inputPlaceholder: "Ask me anything...",
            maxInputLength: 256,
            defaultPrompts: [
                "Tell me about yourself",
                "What can you do?"
            ],
            chatDescription: `
            # Welcome! 👋

            I'm your AI assistant. Feel free to ask me anything!

            * Try the suggested prompts below
            * Ask your own questions
            * I'm here to help!
            `.trim(),
            features: {
                enableParticles: true,
                enableHexagons: true
            }
            }
            ```

            ### Customizing the Chat

            1. **Name and Branding**

            - `name`: Customize the header text (optional)
            - `inputPlaceholder`: Change the input field placeholder (optional)

            2. **Default Prompts**

            - `defaultPrompts`: Array of suggested questions (optional)

            3. **Welcome Message**

            - `chatDescription`: Markdown-formatted welcome message (optional)

            4. **Visual Features**

            - `features.enableParticles`: Toggle particle background (optional)
            - `features.enableHexagons`: Toggle hexagon pattern (optional)

            ### Example Configuration

            ```typescript
            export const UI_CONFIG = {
            name: "My AI Assistant",
            defaultPrompts: [
                "What's your favorite color?",
                "Tell me a joke"
            ]
            } as const;
            ```

            ## 📦 Installation

            1. Clone the repository
            2. Install dependencies:

            ```bash
            npm install
            ```

            ## 🚀 Development

            To start the development server:

            ```bash
            npm run dev
            ```

            The application will be available at `http://localhost:5173`

            ## 🏗️ Building for Production

            To build the application for production:

            ```bash
            npm run build
            ```

            The built files will be in the `dist` directory.

            ## 🐳 Docker Support

            ### Development

            ```bash
            docker build -f Dockerfile.dev -t artificial-me-frontend:dev .
            docker run -p 5173:5173 artificial-me-frontend:dev
            ```

            ### Production

            ```bash
            docker build -t artificial-me-frontend:prod .
            docker run -p 80:80 artificial-me-frontend:prod
            ```

            ## 🔍 Code Quality

            The project uses ESLint for code quality. To run linting:

            ```bash
            """,
        description="Bio system prompt containing personal information"
    )

    @property
    def SYSTEM_PROMPT(self) -> str:
        """Combined system prompt merging basic behavior and bio information."""
        return f"{self.BASIC_SYSTEM_PROMPT.strip()}\n\n{self.BIO_SYSTEM_PROMPT.strip()}"

    # Ingestion Configuration
    FILES: List[str] = Field(
        default=[
            # PDF documents - remote
            "https://kostadindev.github.io/static/documents/cv.pdf",
            "https://kostadindev.github.io/static/documents/sbu_transcript.pdf",
            "https://kostadindev.github.io/static/documents/uhh_transcript.pdf",
            "C:/Users/kosta/OneDrive/Desktop/MS Application Materials/emf-ellipse-publication.pdf",
        ],
        description="List of files to process (remote URLs or local file paths)"
    )
    SITEMAP_URL: str = Field(default="https://kostadindev.github.io/sitemap.xml", description="URL of the sitemap to crawl")
    GITHUB_REPOSITORIES: List[str] = Field(
        default=[
            "https://github.com/kostadindev/Knowledge-Base-Builder",
            "https://github.com/kostadindev/GONEXT",
            "https://github.com/kostadindev/GONEXT-ML",
            "https://github.com/kostadindev/ai-kostadin",
            "https://github.com/kostadindev/Recursive-QA",
            "https://github.com/kostadindev/deep-gestures",
            "https://github.com/kostadindev/emf-ellipse"
        ],
        description="List of GitHub repositories to process (format: username/repo or full URL)"
    )
    
    # Text Processing Configuration
    CHUNK_SIZE: int = Field(default=400, description="Size of text chunks for splitting documents")
    CHUNK_OVERLAP: int = Field(default=50, description="Overlap between text chunks")
    EMBEDDING_DIMENSION: int = Field(default=384, description="Dimension of embeddings (for all-MiniLM-L6-v2)")

    TOP_K: int = Field(default=4, description="Default number of top results to return in Pinecone queries")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields in the environment

# Global settings instance
settings = Settings()
