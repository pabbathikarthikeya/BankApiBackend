from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Account(BaseModel):
    name: str
    balance: float

# Simulated in-memory DB
accounts: Dict[int, Account] = {}
account_id_counter = 1

@app.post("/accounts")
def create_account(account: Account):
    global account_id_counter
    accounts[account_id_counter] = account
    account_id_counter += 1
    return {"id": account_id_counter - 1, "account": account}

@app.get("/accounts")
def get_all_accounts():
    return accounts

@app.put("/accounts/{account_id}")
def update_account(account_id: int, updated_account: Account):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    accounts[account_id] = updated_account
    return {"message": "Account updated", "account": updated_account}

@app.delete("/accounts/{account_id}")
def delete_account(account_id: int):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    del accounts[account_id]
    return {"message": "Account deleted"}
