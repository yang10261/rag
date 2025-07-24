import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "multiuser_messages"  # 或你的 thread_1234 這類名稱

# 刪除這個貼文串對應的資料庫（Collection）
client.delete_collection(name=collection_name)

print(f"已成功刪除 collection '{collection_name}'，裡面所有留言已清空。")
