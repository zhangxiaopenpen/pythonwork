from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
directory="article"
loader = DirectoryLoader(directory)
data = loader.load()
# 初始化加载器
text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=128)
# 切割加载的 document
split_docs = text_splitter.split_documents(data)

from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import IPython
import sentence_transformers
EMBEDDING_MODEL = "embedding_module/dataroot/models/shibing624/text2vec-base-chinese"
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
embeddings.client = sentence_transformers.SentenceTransformer(embeddings.model_name, device='cuda')

from langchain.vectorstores import FAISS
db = FAISS.from_documents(split_docs, embeddings)
db.save_local("Faiss_file/") # 指定Faiss的位置
db = FAISS.load_local("Faiss_file/",embeddings=embeddings,allow_dangerous_deserialization=True)
question = "苗族古歌分布在哪些地方？"
similarDocs = db.similarity_search(question, include_metadata=True, k=2)

from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch
class baichuan2_LLM(LLM):
    # 基于本地 Baichuan 自定义 LLM 类
    tokenizer : AutoTokenizer = None
    model: AutoModelForCausalLM = None

    def __init__(self, model_path :str):
        # 从本地初始化模型
        super().__init__()
        print("正在从本地加载模型...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True,offload_folder = "./Baichuan2/offload")
        self.model.generation_config = GenerationConfig.from_pretrained(model_path)
        self.model = self.model.eval()
        print("完成本地模型的加载")

    def _call(self, prompt : str, stop: Optional[List[str]] = None,
                run_manager: Optional[CallbackManagerForLLMRun] = None,
                **kwargs: Any):
         # 重写调用函数
        messages = [
            {"role": "user", "content": prompt}
        ]
         # 重写调用函数
        response= self.model.chat(self.tokenizer, messages)
        return response
        
    @property
    def _llm_type(self) -> str:
        return "baichuan2_LLM"
llm = baichuan2_LLM("./model/Baichuan2-7B-Chat/models")

# 直接调用LangChain的RetrievalQA，实现基于上下文的问答，省去写prompt的步骤
from langchain.chains import RetrievalQA
import IPython

retriever = db.as_retriever()
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

query = "苗族古歌分布在哪些省份？"
print(qa.run(query))

# fastapi框架
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

class MessageBody(BaseModel):
    msg:str

@app.post("/chat")
async def root(msgBody:MessageBody):
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    # query = "苗族古歌分布在哪些省份？"
    print('收到的问题',msgBody.msg)
    aaa = qa.run(msgBody.msg)
    print('回复内容',aaa)
    return {"message": aaa}

if __name__ == "__main__":
    uvicorn.run(app=app,host="0.0.0.0",port=6006)
