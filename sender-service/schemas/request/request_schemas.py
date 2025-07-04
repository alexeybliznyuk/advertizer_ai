from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Content generation request schemas
# Sender-related schemas have been removed

class ContentBlockCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Content block title")
    description: Optional[str] = Field(None, max_length=1000, description="Content block description")
    tags: list[str] = Field(..., description="Content block tags")
    target_audience_description: Optional[str] = Field(None, description="Target audience description")


class TemplateCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Template name")
    content: str = Field(..., min_length=1, description="Template content")
    params: list[str] = Field(..., description="Template parameters")
    generation_constant_id: str = Field(..., description="Generation constant ID")
    max_input_token: int = Field(..., gt=0, description="Max input tokens")
    max_output_token: int = Field(..., gt=0, description="Max output tokens")
    max_number_of_generations: int = Field(..., gt=0, description="Max number of generations") 