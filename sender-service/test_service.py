#!/usr/bin/env python3
"""
Simple test script for sender-service
"""
import requests
import json
import time

BASE_URL = "http://localhost:8007"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_create_sender():
    """Test creating a sender"""
    sender_data = {
        "name": "Test Sender",
        "email": "test@example.com",
        "description": "Test sender for testing"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/senders", json=sender_data)
        print(f"Create sender: {response.status_code}")
        if response.status_code == 201:
            print(f"Created sender: {response.json()}")
            return response.json()["id"]
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Create sender failed: {e}")
        return None

def test_get_senders():
    """Test getting all senders"""
    try:
        response = requests.get(f"{BASE_URL}/senders")
        print(f"Get senders: {response.status_code}")
        if response.status_code == 200:
            senders = response.json()
            print(f"Found {len(senders)} senders")
            return senders
        else:
            print(f"Error: {response.text}")
            return []
    except Exception as e:
        print(f"Get senders failed: {e}")
        return []

def test_send_email(sender_id):
    """Test sending an email"""
    email_data = {
        "sender_id": sender_id,
        "recipient_email": "recipient@example.com",
        "subject": "Test Email",
        "content": "This is a test email from sender-service"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/send-email", json=email_data)
        print(f"Send email: {response.status_code}")
        if response.status_code == 200:
            print(f"Email sent: {response.json()}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Send email failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing sender-service...")
    
    # Test health
    if not test_health():
        print("Health check failed, service may not be running")
        return
    
    # Test create sender
    sender_id = test_create_sender()
    if not sender_id:
        print("Failed to create sender")
        return
    
    # Test get senders
    test_get_senders()
    
    # Test send email
    test_send_email(sender_id)
    
    print("Tests completed!")

if __name__ == "__main__":
    main() 