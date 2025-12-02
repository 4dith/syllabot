from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are Syllabot, a helpful assistant for answering questions about the Computer Science syllabus at NIT Andhra Pradesh.
Based only on the course details below, answer the question. If you cannot find the answer, say so. Note that the course details are not visible to the user who asked the question.

Course Details:

{context}

Question: {question}

Answer:
"""

embedding_function = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
model = ChatOllama(model="llama3.2:1b")


def get_prompt(query_text):
    results = db.similarity_search_with_relevance_scores(query_text, k=1)
    context_text = "\n\n---\n\n".join(doc.page_content for doc, score in results)
    prompt = PROMPT_TEMPLATE.format(context=context_text, question=query_text)
    return prompt


def answer_question(query_text):    
    prompt = get_prompt(query_text)
    print(prompt)
    response_text = model.invoke(prompt)
    print(response_text.content)
    return response_text.content

if __name__ == "__main__":
    print(db)
