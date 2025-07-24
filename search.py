import chromadb
import json

# 初始化 Chroma Client（使用持久化資料庫）
client = chromadb.PersistentClient(path="./chroma_db")

# 列出所有 collection 名稱
collections = client.list_collections()
print("所有 Collection:", [col.name for col in collections])

# 取得第一組 collection 的名稱
collection_name = collections[2].name
collection = client.get_collection(name=collection_name)

# 取得所有資料（文件、metadata、id）
all_data = collection.get()

# 整合成「誰說了什麼」格式
combined = []
for doc, meta, doc_id in zip(all_data['documents'], all_data['metadatas'], all_data['ids']):
    combined.append({
        "user": meta.get("user", "未知使用者"),
        "text": doc,
        "id": doc_id,
        "time": meta.get("time", "無時間標記")
    })

# 輸出成 JSON 檔案
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)

print("✅ 已輸出所有留言到 output.json！")
