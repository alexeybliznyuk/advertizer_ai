from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, ARRAY, BigInteger, Boolean
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel
import uuid


class ActionType(BaseModel):
    __tablename__ = "action_types"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    modified_on = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    modified_by = Column(UUID(as_uuid=True), nullable=True)
    action_type = Column(Text, nullable=False)
    
    # Relationships
    usages = relationship("Usage", back_populates="action_type_ref")


class Usage(BaseModel):
    __tablename__ = "usages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    modified_on = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    modified_by = Column(UUID(as_uuid=True), nullable=True)
    action_id = Column(UUID(as_uuid=True), ForeignKey("action_types.id"), nullable=True)
    
    # Relationships
    action_type_ref = relationship("ActionType", back_populates="usages")
    generation_contexts = relationship("GenerationContext", back_populates="usage")


class ContentBlock(BaseModel):
    __tablename__ = "content_blocks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    modified_on = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    modified_by = Column(UUID(as_uuid=True), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(ARRAY(Text), nullable=False)
    target_audience_description = Column(Text, nullable=True)
    
    # Relationships
    generation_contexts = relationship("GenerationContext", back_populates="content_block")


class GenerationConstant(BaseModel):
    __tablename__ = "generation_constants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    modified_on = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    modified_by = Column(UUID(as_uuid=True), nullable=True)
    max_input_token = Column(Integer, nullable=False)
    max_output_token = Column(Integer, nullable=False)
    max_number_of_generations = Column(Integer, nullable=False)
    
    # Relationships
    templates = relationship("Template", back_populates="generation_constant")


class GeneratedType(BaseModel):
    __tablename__ = "generated_type"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gen_type = Column(String(50), nullable=False)  # 'message' or 'post'
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    modified_on = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    modified_by = Column(UUID(as_uuid=True), nullable=True)
    
    # Relationships
    generation_contexts = relationship("GenerationContext", back_populates="generated_type")


class Template(BaseModel):
    __tablename__ = "templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    modified_on = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    modified_by = Column(UUID(as_uuid=True), nullable=True)
    name = Column(String(100), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    params = Column(ARRAY(Text), nullable=False)
    generation_constant_id = Column(UUID(as_uuid=True), ForeignKey("generation_constants.id"), nullable=False)
    max_input_token = Column(Integer, nullable=False)
    max_output_token = Column(Integer, nullable=False)
    max_number_of_generations = Column(Integer, nullable=False)
    
    # Relationships
    generation_constant = relationship("GenerationConstant", back_populates="templates")
    generation_contexts = relationship("GenerationContext", back_populates="template")


class GenerationContext(BaseModel):
    __tablename__ = "generation_context"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    modified_on = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    modified_by = Column(UUID(as_uuid=True), nullable=True)
    usage_id = Column(UUID(as_uuid=True), ForeignKey("usages.id"), nullable=True)
    user_prompt = Column(Text, nullable=True)
    content_block_id = Column(UUID(as_uuid=True), ForeignKey("content_blocks.id"), nullable=False)
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id"), nullable=False)
    gen_type = Column(UUID(as_uuid=True), ForeignKey("generated_type.id"), nullable=False)
    
    # Relationships
    usage = relationship("Usage", back_populates="generation_contexts")
    content_block = relationship("ContentBlock", back_populates="generation_contexts")
    template = relationship("Template", back_populates="generation_contexts")
    generated_type = relationship("GeneratedType", back_populates="generation_contexts")
    generated_items = relationship("Generated", back_populates="context")


class Generated(BaseModel):
    __tablename__ = "generated"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    modified_on = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    modified_by = Column(UUID(as_uuid=True), nullable=True)
    context_id = Column(UUID(as_uuid=True), ForeignKey("generation_context.id"), nullable=False)
    content = Column(Text, nullable=False)
    course_id = Column(Integer, nullable=False)
    scheduled_time = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relationships
    context = relationship("GenerationContext", back_populates="generated_items")
    generated_afterwards = relationship("GeneratedAfterwards", back_populates="generated_item")


class GenerationStatus(BaseModel):
    __tablename__ = "generation_status"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    modified_on = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    modified_by = Column(UUID(as_uuid=True), nullable=True)
    generated_status = Column(Text, nullable=False)
    
    # Relationships
    generated_afterwards = relationship("GeneratedAfterwards", back_populates="status")


class GeneratedAfterwards(BaseModel):
    __tablename__ = "generated_afterwards"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_on = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    modified_on = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    modified_by = Column(UUID(as_uuid=True), nullable=True)
    generated_id = Column(UUID(as_uuid=True), ForeignKey("generated.id"), nullable=False)
    generation_status_id = Column(UUID(as_uuid=True), ForeignKey("generation_status.id"), nullable=False)
    post_status = Column(Text, nullable=False)
    
    # Relationships
    generated_item = relationship("Generated", back_populates="generated_afterwards")
    status = relationship("GenerationStatus", back_populates="generated_afterwards") 