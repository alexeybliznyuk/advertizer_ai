from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel

from repository.database import get_db
from repository.database import create_tables
from service.deepseek_service import DeepSeekService

# Create FastAPI app
app = FastAPI(
    title="Content Generation Service",
    description="Service for managing content generation, templates, and usage tracking",
    version="1.0.0"
)

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()


# Request models
class ContentBlockCreateRequest(BaseModel):
    title: str
    description: str = None
    tags: List[str]
    target_audience_description: str = None


class TemplateCreateRequest(BaseModel):
    name: str
    content: str
    params: List[str]
    generation_constant_id: str
    max_input_token: int
    max_output_token: int
    max_number_of_generations: int


# Response models
class ContentBlockResponse(BaseModel):
    id: str
    title: str
    description: str = None
    tags: List[str]
    target_audience_description: str = None
    created_on: str = None
    updated_on: str = None


class TemplateResponse(BaseModel):
    id: str
    name: str
    content: str
    params: List[str]
    generation_constant_id: str
    max_input_token: int
    max_output_token: int
    max_number_of_generations: int
    created_on: str = None
    updated_on: str = None


class PostCreateRequest(BaseModel):
    course_id: str
    user_prompt: str
    user_id: str


# Response models
class PostCreateResponse(BaseModel):
    session_id: str
    generated_text: str
    status: str


class MessageCreateRequest(BaseModel):
    course_id: str
    user_prompt: str
    user_id: str


# Response models
class MessageCreateResponse(BaseModel):
    session_id: str
    generated_text: str
    status: str


class ValidationRequest(BaseModel):
    session_id: str
    approval_status: str


# Response models
class ValidationResponse(BaseModel):
    session_id: str
    status: str


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "content-generation-service"}


# Content Block endpoints
@app.post("/content-blocks", response_model=ContentBlockResponse, status_code=status.HTTP_201_CREATED)
async def create_content_block(
    request: ContentBlockCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new content block"""
    # TODO: Implement content block creation logic
    return {"message": "Content block creation endpoint - to be implemented"}


@app.get("/content-blocks", response_model=List[ContentBlockResponse])
async def get_all_content_blocks(db: Session = Depends(get_db)):
    """Get all content blocks"""
    # TODO: Implement content block retrieval logic
    return []


# Template endpoints
@app.post("/templates", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    request: TemplateCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new template"""
    # TODO: Implement template creation logic
    return {"message": "Template creation endpoint - to be implemented"}


@app.get("/templates", response_model=List[TemplateResponse])
async def get_all_templates(db: Session = Depends(get_db)):
    """Get all templates"""
    # TODO: Implement template retrieval logic
    return [] 


@app.post("/api/v1/sender/generate/warmup", response_model=PostCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_post_warmup(
    request: PostCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new content block using DeepSeek AI"""
    try:
        service = DeepSeekService()
        
        # Prepare the user input for the AI service
        user_input = [
            {"role": "user", "content": f"Course ID: {request.course_id}, User Prompt: {request.user_prompt}, User ID: {request.user_id}"}
        ]
        
        # Generate content using DeepSeek
        response = service.create_post(user_input)
        
        # Extract the generated text from the response
        generated_text = response.get("choices", [{}])[0].get("message", {}).get("content", "No content generated")
        
        return {
            "session_id": f"session_{request.user_id}_{request.course_id}",
            "generated_text": generated_text,
            "status": "completed"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating content: {str(e)}"
        )


@app.post("/api/v1/sender/generate/personal", response_model=MessageCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_message_personal(
    request: MessageCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new personal message using DeepSeek AI"""
    try:
        service = DeepSeekService()
        
        # Prepare the user input for the AI service
        user_input = [
            {"role": "user", "content": f"Course ID: {request.course_id}, User Prompt: {request.user_prompt}, User ID: {request.user_id}"}
        ]
        
        # Generate content using DeepSeek
        response = service.create_message(user_input)
        
        # Extract the generated text from the response
        generated_text = response.get("choices", [{}])[0].get("message", {}).get("content", "No content generated")
        
        return {
            "session_id": f"session_{request.user_id}_{request.course_id}",
            "generated_text": generated_text,
            "status": "completed"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating content: {str(e)}"
        )


@app.post("/api/v1/sender/validate", response_model=ValidationResponse, status_code=status.HTTP_201_CREATED)
async def validate_session(
    request: ValidationRequest,
    db: Session = Depends(get_db)
):
    """Validate a session with approval status"""
    try:
        return {
            "session_id": request.session_id,
            "status": f"request {request.session_id} is {request.approval_status}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error validating session: {str(e)}"
        )