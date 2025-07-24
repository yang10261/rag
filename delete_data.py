import chromadb

# 連接資料庫
client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "multiuser_messages"   # 你要操作的 collection 名稱
collection = client.get_collection(name=collection_name)

# 要刪除的留言 id 清單，可單筆或多筆
delete_ids = ["Alice_1", "Bob_2"]

collection.delete(ids=delete_ids)

print(f"已成功刪除留言 {delete_ids}。")
