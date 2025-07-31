import google.generativeai as genai
from db_handler import (
    insert_comments,
    get_comments_by_thread,
    export_thread_to_json,
    delete_thread,
    update_comment
)

# ✅ 設定 Gemini API 金鑰
genai.configure(api_key="你的_Gemini_API_KEY")

def get_gemini_embedding(texts):
    if isinstance(texts, str):
        texts = [texts]
    return [genai.embed_content(
        model="models/embedding-001",
        content=t,
        task_type="semantic_similarity"
    )["embedding"] for t in texts]

# ✅ 建立範例聊天串與留言
thread_id = "thread_demo"
comments = [
    {"user": "Grace", "text": "這是一個測試留言。", "id": f"{thread_id}_cmt1"},
    {"user": "Henry", "text": "你好，我是第二位參與者。", "id": f"{thread_id}_cmt2"}
]
texts = [c["text"] for c in comments]
embeddings = get_gemini_embedding(texts)

# ✅ 1. 插入留言
insert_comments(comments, embeddings, thread_id)

# ✅ 2. 查詢該 thread 所有留言
print(f"\n🔍 查詢 {thread_id} 的留言：")
results = get_comments_by_thread(thread_id)
for c in results:
    print(f"- ({c['metadata']['user']}) {c['text']}")

# ✅ 3. 匯出為 JSON 檔案
export_thread_to_json(thread_id)  # 會產出 thread_demo_comments.json

# ✅ 4. 更新其中一筆留言內容
update_comment(
    comment_id=f"{thread_id}_cmt2",
    new_text="這是一段經過更新的留言內容。",
    new_metadata={"user": "Henry", "time": "2025-07-31T15:00:00", "thread_id": thread_id}
)

# ✅ 5. 查詢更新後內容
print(f"\n📌 查詢更新後留言：")
updated = get_comments_by_thread(thread_id)
for c in updated:
    print(f"- ({c['metadata']['user']}) {c['text']}")

# ✅ 6. 刪除整個聊天串
delete_thread(thread_id)
