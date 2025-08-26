#!/usr/bin/env python3
"""
Railway Deployment Test Script
Run this after deployment to verify everything works
"""

import httpx
import sys
import time

def test_deployment(base_url):
    """Test the deployed application"""
    print(f"🧪 Testing deployment at: {base_url}")
    
    try:
        # Test 1: Health check
        print("1. Testing health endpoint...")
        response = httpx.get(f"{base_url}/api/health", timeout=30)
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
        
        # Test 2: Frontend loads
        print("2. Testing frontend...")
        response = httpx.get(base_url, timeout=30)
        if response.status_code == 200 and "PowerPoint Generator" in response.text:
            print("   ✅ Frontend loads successfully")
        else:
            print(f"   ❌ Frontend test failed: {response.status_code}")
            return False
        
        # Test 3: API endpoint exists (without making actual request)
        print("3. Testing API endpoint availability...")
        response = httpx.options(f"{base_url}/api/generate", timeout=30)
        if response.status_code in [200, 405]:  # 405 is expected for OPTIONS without proper data
            print("   ✅ API endpoint is accessible")
        else:
            print(f"   ❌ API endpoint test failed: {response.status_code}")
            return False
        
        print("\n🎉 All tests passed! Your deployment is working correctly.")
        print(f"🌐 Access your app at: {base_url}")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_deployment.py <your-railway-url>")
        print("Example: python test_deployment.py https://your-app.railway.app")
        sys.exit(1)
    
    url = sys.argv[1].rstrip('/')
    success = test_deployment(url)
    sys.exit(0 if success else 1)
