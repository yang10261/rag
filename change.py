import chromadb
import google.generativeai as genai

# 初始化 Gemini API（如有需要，用於重新產生向量）
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

# 連接你的 Chroma 資料庫
client = chromadb.PersistentClient(path="./chroma_db")


collection_name = "thread_1234"


collection = client.get_collection(name=collection_name)

# 假設你想修改留言的內容
target_id = "thread_1234_cmt1"
new_content = "其實我今天沒有出門。"

# （推薦）同步更新嵌入向量
new_embedding = get_gemini_embedding(new_content)

# 執行 update
collection.update(
    ids=[target_id],
    documents=[new_content],
    embeddings=new_embedding
    # 如需同步更新 metadata 也可加 metadatas=[new_meta]
)

# 檢查結果
result = collection.get(ids=[target_id])
print("======= 更新後結果 =======")
print("ID:", result["ids"][0])
print("留言內容：", result["documents"][0])
print("metadata：", result["metadatas"][0])
