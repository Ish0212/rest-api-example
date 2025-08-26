from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="REST API Example", description="Simple CRUD API using FastAPI", version="1.0.0")

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory store
items: List[Item] = []

# Helper to get item by id
def get_item(item_id: int) -> Optional[Item]:
    for item in items:
        if item.id == item_id:
            return item
    return None

@app.get("/items", response_model=List[Item])
def read_items():
    return items

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    if get_item(item.id):
        raise HTTPException(status_code=400, detail="Item already exists")
    items.append(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    item = get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = updated_item.name
    item.description = updated_item.description
    return item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    global items
    item = get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    items = [i for i in items if i.id != item_id]
    return None
