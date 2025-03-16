from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm import service as llm_service  # Assuming this handles the LLM text processing

app = FastAPI()

# ✅ CORS settings (Allow frontend to access API)
origins = [
    "http://localhost:3000",    # React frontend dev server
    "http://127.0.0.1:3000",    # Optional alternative
    # Add production URLs if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # ✅ Specific origins allowed (or ["*"] for any)
    allow_credentials=True,
    allow_methods=["*"],          # Allow all methods (or restrict: ["POST"])
    allow_headers=["*"],          # Allow all headers (or specify)
)

# ✅ Request model
class ExecuteRequest(BaseModel):
    text: str

# ✅ Response model
class ExecuteResponse(BaseModel):
    HTML: str

# ✅ Custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )

# ✅ Custom 400 handler
@app.exception_handler(400)
async def bad_request_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=400,
        content={"detail": "Bad request: " + exc.detail if exc.detail else "Invalid input"}
    )

# ✅ POST API to process text
@app.post("/api/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest):
    try:
        input_text = request.text.strip()

        # Basic validation
        if not input_text:
            raise HTTPException(status_code=400, detail="Input 'text' cannot be empty")

        # Call your LLM service
        html_result = llm_service.process_text(input_text)

        # Validate the response from service
        if not html_result:
            raise HTTPException(status_code=404, detail="No result found from LLM processing")

        # Return as JSON
        return ExecuteResponse(HTML=html_result)

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
