import google.generativeai as genai
from db_handler import insert_comments, get_comments_by_thread, export_thread_to_json

genai.configure(api_key="AIzaSyAplv2YiY0Cy5EBMXzEgwgrr-cbN31PHeA")

def get_gemini_embedding(texts):
    if isinstance(texts, str):
        texts = [texts]
    return [genai.embed_content(
        model="models/embedding-001",
        content=t,
        task_type="semantic_similarity"
    )["embedding"] for t in texts]

# 模擬多個聊天串
threads = {
    "thread_1001": [
        {"user": "Alice", "text": "今天天氣真好！", "id": "thread_1001_cmt1"},
        {"user": "Bob", "text": "我喜歡陽光的感覺。", "id": "thread_1001_cmt2"},
        {"user": "Cathy", "text": "下午想去公園走走。", "id": "thread_1001_cmt3"},
    ],
    "thread_1002": [
        {"user": "Dan", "text": "Python 的 list comprehension 超方便。", "id": "thread_1002_cmt1"},
        {"user": "Eve", "text": "我最近在學 FastAPI！", "id": "thread_1002_cmt2"},
        {"user": "Frank", "text": "Keras 對新手來說很好上手。", "id": "thread_1002_cmt3"},
    ]
}

# 新增所有聊天串留言
for thread_id, comments in threads.items():
    texts = [c["text"] for c in comments]
    embeddings = get_gemini_embedding(texts)
    insert_comments(comments, embeddings, thread_id)
    export_thread_to_json(thread_id)

# 顯示每個串的留言
for thread_id in threads:
    print(f"\n🧵 聊天串 {thread_id} 留言內容：")
    comments = get_comments_by_thread(thread_id)
    for c in comments:
        print(f"- ({c['metadata']['user']}) {c['text']}")
