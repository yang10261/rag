import chromadb
import google.generativeai as genai
from datetime import datetime

# 調整為你的 Gemini API key
genai.configure(api_key="")

def get_gemini_embedding(texts):
    if isinstance(texts, str):
        texts = [texts]
    embeddings = []
    for text in texts:
        res = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="semantic_similarity"
        )
        embeddings.append(res["embedding"])
    return embeddings

# Chroma client（資料持久化）
client = chromadb.PersistentClient(path="./chroma_db")

# 一篇貼文串的 ID，用它當 Collection 名稱
thread_id = "thread_1234"
try:
    collection = client.get_collection(name=thread_id)
except:
    collection = client.create_collection(name=thread_id)

# 假設這是該串底下的留言
comments = [
    {"user": "Alice432423", "text": "這篇文章太棒了23333！", "id": f"{thread_id}_cmt5"},
    {"user": "Bob", "text": "我也很喜歡這個觀點。", "id": f"{thread_id}_cmt2"},
    {"user": "Cathy", "text": "請問作者的參考資料是什麼？", "id": f"{thread_id}_cmt3"},
    {"user": "Cathy123", "text": "請問作者的參考資料是什麼123？", "id": f"{thread_id}_cmt4"},
]

documents = [c["text"] for c in comments]
metadatas = [{"user": c["user"], "time": datetime.now().isoformat()} for c in comments]
ids = [c["id"] for c in comments]

embeddings = get_gemini_embedding(documents)

# 將留言寫入該貼文串 Collection
collection.add(
    embeddings=embeddings,
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"成功將 {len(comments)} 則留言存入貼文串 {thread_id} 對應的 Collection。")

