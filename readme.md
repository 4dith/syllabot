# 🤖 Syllabot: AI-Powered Syllabus Assistant

A demo website where you can view the syllabus of a typical computer science BTech program. It includes a Retrieval-Augmented Generation (RAG) based chatbot designed to answer course-related queries accurately.

## 🚀 Live Demo & Deployment

The current static deployment is hosted here: [https://syllabot.netlify.app/](https://syllabot.netlify.app/)

**Important Technical Note:**

The deployed version is a **static frontend build** that currently performs searches based solely on **keyword matching** against course titles.

The **full-featured Django application** is designed for high-accuracy results, utilizing **semantic search** and **RAG (Retrieval-Augmented Generation)** to analyze the content of syllabus documents. For a demonstration of the full RAG capabilities, please refer to the **Installation** section to run the application locally.

## ✨ Features

1. Browse courses by academic year.
2. View credits, prerequisites, units and topics covered, experiments, and references for each course.
3. Ask the RAG chatbot any question regarding the course contents.
4. Includes custom parsers used to build SQL and vector databases from source markdown files.

## 🛠️ Technologies Used

| **Category** | **Technologies** |
| --- | --- |
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python (Django Framework), LangChain |
| **Database** | SQLITE, Chroma (Vector DB) |
| **LLMs/Embeddings** | Nomic Text Embeddings, Llama 3.2 (1B parameter) |
| **Deployment** | Netlify (Frontend only with limited chat functionality) |

## ⚙️ Installation and Setup

### Prerequisites

1. Install **Python** and **pip**.
2. Install [**Ollama**](https://ollama.com/download) (This manages the local LLMs).
3. Pull embedding model and chat model:
Bash
    
    ```
    ollama pull nomic-embed-text:latest
    ollama pull llama3.2:1b
    ```
    

### Steps

1. Clone the repository:
    
    ```
    git clone <https://github.com/4dith/syllabot.git>
    ```
    
2. Navigate to the project directory:
    
    ```
    cd syllabot
    ```
    
3. Install dependencies:
    
    ```
    pip install -r requirements.txt
    ```
    
4. Start the Ollama application on your PC (it runs in the background).
5. Run the web application locally:
    
    ```
    python manage.py runserver
    ```
    
6. Click the link to the development server (usually `http://127.0.0.1:8000/`) from the output text in your console.

## 📂 Project Structure

```
static-site/ - For deployment of the static demo site (can be ignored for local development)
courses/ - Main Django app (contains models, views, and templates for course data)
courses/rag.py - Contains the RAG functionality using OLLAMA
createDB.py - Script to create a vector embedding database from the SQLITE database
parser.py - Script to create the SQLITE database by parsing source markdown files
```

## ⚖️ License

Distributed under the **MIT License**. See the `LICENSE` file for more information.

## ✉️ Contact

Project Link: [https://github.com/4dith/syllabot](https://github.com/4dith/syllabot)
Email: [adithyavenkatesh.in@gmail.com](mailto:adithyavenkatesh.in@gmail.com)

## 👏 Acknowledgments

We would like to extend our sincere thanks to [**Dr. K Hima Bindu**](https://scholar.google.com/citations?user=U9dQ3QgAAAAJ&hl=en) for their invaluable mentorship and guidance throughout the development of Syllabot.