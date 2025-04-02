from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Context:

{context}

___
You are Syllabot, and you answer questions about the Computer Science syllabus of NIT Andhra Pradesh.
Answer the question based on the above context (ignore if irrelevant): {question}
"""

CONFIDENCE = 0.5

embedding_function = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
model = ChatOllama(model="llama3.2:1b")


def get_prompt(query_text):
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    
    context_text = "\n\n---\n\n".join(doc.page_content for doc, score in results if score >= CONFIDENCE)
    
    prompt = PROMPT_TEMPLATE.format(context=context_text, question=query_text)

    return prompt


def answer_question(query_text):    
    prompt = get_prompt(query_text)

    response_text = model.invoke(prompt)

    return response_text.content

if __name__ == "__main__":
    print(db)
