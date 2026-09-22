"""
FastAPI Backend Server for Meeting Scheduler Web UI.
Serves static frontend files and exposes API endpoints for chatting with the agent.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

from agent import chat_with_agent
from tools import BOOKED_MEETINGS, list_scheduled_meetings

app = FastAPI(title="Meeting Scheduler AI Agent UI")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    status: str = "success"


@app.post("/api/chat", response_model=ChatResponse)
async def handle_chat(payload: ChatRequest):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    try:
        reply_text = chat_with_agent(payload.message)
        return ChatResponse(reply=reply_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/meetings")
async def get_meetings():
    return list_scheduled_meetings()


# Serve static web files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
