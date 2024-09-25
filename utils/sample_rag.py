import os
import logging

from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma

logger = logging.getLogger(__name__)


SYS_PROMPT = '''
Today is {today}

Your name is CareQ.
You are a knowledgeable health expert.

'''

CONTEXT_TEMPLATE = '''Ref {counter}:
Title: {title}
Context: {content}
-----
'''


RAG_PROMPT_TEMPLATE = '''
Contexts are given below:
"""
{context_str}
"""

Given the context information, answer the query.

Query: {query_str}
'''


def prepare_rag_messages(
        msg_list,
        chroma_dir,
        chroma_index_name,
        top_k=5
    ):

    query_str = msg_list[-1]['content']


    AZURE_OPENAI_API_KEY=os.environ.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT=os.environ.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_VERSION="2024-06-01"
    if not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY

    embedding_deployment_name="azure-text-embedding-3-small"

    embedding = AzureOpenAIEmbeddings(
        model=embedding_deployment_name
    )

    vector_store = Chroma(
        collection_name=chroma_index_name,
        embedding_function=embedding,
        persist_directory=chroma_dir
    )
    
    # Retrieve Contexts
    results = vector_store.similarity_search(
        query_str,
        k=top_k
    )

    # Prepare new context
    context_str = ''
    counter = 1
    for i in results:
        title = os.path.basename(
            i.metadata['source']
        )
        page = i.metadata['page']
        content = i.page_content

        context_str += CONTEXT_TEMPLATE.format(
            counter=counter,
            title=title,
            content=content,
        )
        counter += 1

    new_query_str = RAG_PROMPT_TEMPLATE.format(
        context_str=context_str,
        query_str=query_str
    )
    logger.warning(new_query_str)

    msg_list[-1]['content'] = new_query_str
    return  msg_list

