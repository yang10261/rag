import chromadb
import google.generativeai as genai
from openai import OpenAI

# ========== API 金鑰設定 ==========
# ✅ Gemini Embedding API Key
genai.configure(api_key="")

# ✅ OpenAI GPT 回答用 API Key
client = OpenAI(api_key="")

# ========== 嵌入產生（使用 Gemini） ==========
def get_gemini_embedding(texts):
    if isinstance(texts, str):
        texts = [texts]
    embs = []
    for text in texts:
        res = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="semantic_similarity"
        )
        embs.append(res["embedding"])
    return embs

# ========== 載入 Chroma 資料庫 ==========
client_chroma = chromadb.PersistentClient(path="./chroma_db")
thread_id = "thread_1234"  # Collection 名稱（之前 upload.py 建立過）
collection = client_chroma.get_collection(name=thread_id)

# ========== 問答主迴圈 ==========
while True:
    user_q = input("\n請輸入你的問題（輸入 exit 離開）：")
    if user_q.strip().lower() == "exit":
        break

    # 1. 將問題轉為向量
    q_emb = get_gemini_embedding(user_q)[0]

    # 2. 語意查詢最近的 3 筆資料
    results = collection.query(query_embeddings=[q_emb], n_results=3)
    top_contexts = results['documents'][0]

    # 建立有標註來源的段落
    context_parts = []
    for i in range(len(top_contexts)):
        doc = top_contexts[i]
        doc_id = results['ids'][0][i]
        meta = results['metadatas'][0][i]
        user = meta.get("user", "未知使用者")

        context_parts.append(f"【留言 {doc_id}｜{user}】\n{doc}")

    # 3. 組 prompt
    prompt = (
        "根據以下留言內容作為參考，請回答用戶的問題：\n\n"
        "【相關留言】\n"
        + "\n".join(context_parts)
        + f"\n\n【問題】{user_q}\n請詳細回覆："
    )

    print("\n📦 傳送給 GPT 的 Prompt：\n", prompt)

    # 4. 呼叫 OpenAI GPT 產生回答（新版 SDK 寫法）
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個知識型助手"},
                {"role": "user", "content": prompt}
            ]
        )

        print("\n🤖 AI 回答：\n", response.choices[0].message.content)

    except Exception as e:
        print("⚠️ 發生錯誤：", e)

print("結束程式。")
