from fastapi import APIRouter, Depends, HTTPException
from app.models.query import Query
from app.dependencies import get_gemini_model, get_system_message
from langchain.schema import AIMessage, HumanMessage

router = APIRouter()


@router.post("/chat")
async def chat(query: Query, gemini_model=Depends(get_gemini_model)):
    try:
        system_message = get_system_message()
        user_message = HumanMessage(content=query.question)

        # Invoke the model with both the system and user message
        response = gemini_model.invoke([system_message, user_message])

        if isinstance(response, AIMessage):
            return {"answer": response.content}
        else:
            raise HTTPException(
                status_code=500, detail="Unexpected response type from Gemini model.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
