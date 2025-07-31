import chromadb
from datetime import datetime
import json

# 初始化持久化資料庫
client = chromadb.PersistentClient(path="./chroma_db")

# 統一使用一個 Collection 來存所有留言
COLLECTION_NAME = "multi_thread_chatroom"
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def insert_comments(comments, embeddings, thread_id):
    """插入多筆留言，metadata 加上 thread_id"""
    documents = [c["text"] for c in comments]
    metadatas = [{
        "thread_id": thread_id,
        "user": c["user"],
        "time": datetime.now().isoformat()
    } for c in comments]
    ids = [c["id"] for c in comments]

    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"✅ 已將 {len(comments)} 則留言寫入 thread '{thread_id}' 中")

def get_comments_by_thread(thread_id):
    """取得指定聊天串所有留言"""
    results = collection.get(where={"thread_id": thread_id})
    comments = []
    for _id, doc, meta in zip(results["ids"], results["documents"], results["metadatas"]):
        comments.append({
            "id": _id,
            "text": doc,
            "metadata": meta
        })
    return comments

def export_thread_to_json(thread_id, output_path=None):
    """匯出指定聊天串留言為 JSON"""
    comments = get_comments_by_thread(thread_id)
    if output_path is None:
        output_path = f"{thread_id}_comments.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)
    print(f"📤 已匯出 thread '{thread_id}' 共 {len(comments)} 則留言到 {output_path}")

def delete_thread(thread_id):
    """刪除指定聊天串所有留言"""
    results = collection.get(where={"thread_id": thread_id})
    ids = results["ids"]
    if ids:
        collection.delete(ids=ids)
        print(f"🗑️ 已刪除 thread '{thread_id}' 共 {len(ids)} 筆留言")
    else:
        print(f"⚠️ 找不到 thread '{thread_id}' 的留言，未刪除任何資料")

def update_comment(comment_id, new_text, new_metadata=None):
    """更新指定留言的內容與語意向量"""
    from google.generativeai import embed_content
    embedding = embed_content(
        model="models/embedding-001",
        content=new_text,
        task_type="semantic_similarity"
    )["embedding"]

    update_kwargs = {
        "ids": [comment_id],
        "documents": [new_text],
        "embeddings": [embedding]
    }
    if new_metadata:
        update_kwargs["metadatas"] = [new_metadata]

    collection.update(**update_kwargs)
    print(f"✏️ 已更新留言 {comment_id}")
