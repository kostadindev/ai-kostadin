from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.models.query import Query
from app.dependencies import get_gemini_model, get_system_message
from langchain.schema import HumanMessage
import asyncio

router = APIRouter()


@router.post("/chat")
async def chat(query: Query, gemini_model=Depends(get_gemini_model)):
    try:
        # Prepare the system and user messages
        system_message = get_system_message()
        user_message = HumanMessage(content=query.question)

        # Async generator that yields tokens from the model's streaming response
        async def token_generator():
            async for chunk in gemini_model.astream([system_message, user_message]):
                # Ensure the chunk is converted to a string before yielding
                yield str(chunk.content)

        return StreamingResponse(token_generator(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
