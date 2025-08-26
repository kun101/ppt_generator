#!/usr/bin/env python3
"""
Test the API endpoints to debug the 405 error.
"""

import requests
import json

def test_health_endpoint():
    """Test the health endpoint."""
    try:
        response = requests.get('http://127.0.0.1:8000/api/health')
        print(f"Health endpoint status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Error testing health endpoint: {e}")

def test_generate_endpoint():
    """Test the generate endpoint with OPTIONS to check CORS."""
    try:
        # First test OPTIONS (preflight)
        options_response = requests.options('http://127.0.0.1:8000/api/generate')
        print(f"OPTIONS status: {options_response.status_code}")
        print(f"OPTIONS headers: {dict(options_response.headers)}")
        
        # Test POST without data (should get validation error, not 405)
        post_response = requests.post('http://127.0.0.1:8000/api/generate')
        print(f"POST status: {post_response.status_code}")
        print(f"POST response: {post_response.text}")
        
    except Exception as e:
        print(f"Error testing generate endpoint: {e}")

if __name__ == "__main__":
    print("🧪 Testing API endpoints...\n")
    test_health_endpoint()
    print()
    test_generate_endpoint()
