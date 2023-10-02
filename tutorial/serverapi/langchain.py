import os
import sys
from langchain.document_loaders import TextLoader
#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 (salah)
#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
#pip install langchain openai chromadb tiktoken unstructured pypdf
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.callbacks import get_openai_callback

from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from langchain.chains.conversational_retrieval.prompts import QA_PROMPT

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_KEY")

PERSIST = False

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  #loader = TextLoader("/Users/yusril/Desktop/TugasAkhir/Code/Django/restapi/tutorial/serverapi/testing.txt")
  #pdfFileObj = open('/Users/yusril/Desktop/TugasAkhir/Code/Django/restapi/tutorial/serverapi/qna.pdf', 'rb')
  loader = PyPDFLoader("/Users/yusril/Desktop/TugasAkhir/Code/Django/restapi/tutorial/serverapi/qna.pdf") # Use this line if you only need data.txt
  #loader = CSVLoader(file_path='/Users/yusril/Downloads/all_hadiths_clean.csv')
  #loader = DirectoryLoader("/content/data")

  if PERSIST:
    index = VectorstoreIndexCreator(
    vectorstore_kwargs={"persist_directory":"persist"},
    embedding=OpenAIEmbeddings(),
    text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    ).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])


memory = ConversationSummaryMemory(
    llm = OpenAI(model_name='gpt-3.5-turbo'),
    memory_key='chat_history',
    return_messages=True,
    output_key='answer'
)

chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(model="gpt-3.5-turbo"),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
  memory = memory,
  max_tokens_limit = 200,
)
