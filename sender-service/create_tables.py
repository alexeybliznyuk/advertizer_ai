#!/usr/bin/env python3
"""
Script to create all database tables for sender-service
"""
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

from repository.database import create_tables
from models import Base
from models.sender import Sender, Message
from models.content_models import (
    ActionType, Usage, ContentBlock, GenerationConstant,
    GeneratedType, Template, GenerationContext, Generated,
    GenerationStatus, GeneratedAfterwards
)

def main():
    """Create all database tables"""
    print("Creating database tables...")
    
    try:
        create_tables()
        print("✅ All tables created successfully!")
        print("\nCreated tables:")
        print("- senders")
        print("- messages")
        print("- action_types")
        print("- usages")
        print("- content_blocks")
        print("- generation_constants")
        print("- generated_type")
        print("- templates")
        print("- generation_context")
        print("- generated")
        print("- generation_status")
        print("- generated_afterwards")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 