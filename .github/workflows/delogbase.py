from fastapi import FastAPI
from secrets import token_hex
import json
from mangum import Mangum
app = FastAPI()
with open(fr"db.json", "r", encoding="utf-8") as file:
   db = json.load(file)

with open(fr"db.json", "w", encoding="utf-8") as file:
    json.dump(db, file, ensure_ascii=False, indent=4)


@app.post("/create")
async def sl():
    s = token_hex(18)
    db["databases"].append({"key":s,"data":[]})
    with open(fr"db.json", "w", encoding="utf-8") as file:
     json.dump(db, file, ensure_ascii=False, indent=4)
    return {"status": "created", "content":f"key = {s}"}
@app.post("/write")
async def write(key:str,content:dict):
   for user in db["databases"]:
      if key == user["key"]:
        user["data"].append(content)
        with open(fr"db.json", "w", encoding="utf-8") as file:
         json.dump(db, file, ensure_ascii=False, indent=4)
        return {"status": "saved","content":"the writed memory just saved"}
   return {"status":"error","content":"failed key"}
@app.post("/read")
async def sql(key:str):
   for user in db["databases"]:
      if user["key"] == key:
         return user["data"]
   return {"status": "error","content": "failed key"}

@app.post("/save")
async def rr(key:str,content:tuple):
   for user in db["databases"]:
      if user["key"] == key:
         user["data"] = content
         return {"status": "saved", "content": "the content of command was saved"}
   return {"status": "error","content": "failed key"}
