"""
Azure App Service Deployment Verification & Troubleshooting
"""
import requests
import time
import sys

APP_URL = "https://pythonvenkyapp-f2d5d7fkeufmhfdd.eastus-01.azurewebsites.net"
SCM_URL = "https://pythonvenkyapp-f2d5d7fkeufmhfdd.scm.azurewebsites.net"

def check_app_status():
    """Check if the app is responding"""
    print("=" * 70)
    print("🔍 AZURE APP SERVICE DEPLOYMENT VERIFICATION")
    print("=" * 70)
    
    print(f"\n📍 App URL: {APP_URL}")
    print(f"📍 SCM URL: {SCM_URL}")
    
    # Test 1: Check if the app is reachable
    print("\n" + "-" * 70)
    print("TEST 1: Checking App Availability")
    print("-" * 70)
    
    for attempt in range(3):
        try:
            print(f"\nAttempt {attempt + 1}/3...")
            response = requests.get(APP_URL, timeout=30)
            
            print(f"✅ SUCCESS! Status Code: {response.status_code}")
            print(f"📄 Response Content:")
            print("-" * 70)
            print(response.text[:500])
            print("-" * 70)
            
            if response.status_code == 200:
                print("\n🎉 DEPLOYMENT SUCCESSFUL!")
                return True
            else:
                print(f"\n⚠️  App is running but returned status {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⏱️  Timeout on attempt {attempt + 1}")
            if attempt < 2:
                print("   Waiting 10 seconds before retry...")
                time.sleep(10)
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection Error: {e}")
            if attempt < 2:
                print("   Waiting 10 seconds before retry...")
                time.sleep(10)
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            break
    
    # Test 2: Check SCM endpoint (Kudu)
    print("\n" + "-" * 70)
    print("TEST 2: Checking Kudu/SCM Endpoint")
    print("-" * 70)
    
    try:
        scm_response = requests.get(SCM_URL, timeout=30)
        print(f"✅ SCM is reachable: Status {scm_response.status_code}")
    except Exception as e:
        print(f"❌ SCM Error: {e}")
    
    # Provide troubleshooting steps
    print("\n" + "=" * 70)
    print("🔧 TROUBLESHOOTING STEPS")
    print("=" * 70)
    print("""
1. Check Azure Portal:
   - Go to: https://portal.azure.com
   - Search for: pythonvenkyapp-f2d5d7fkeufmhfdd
   - Check if Status is "Running"

2. Check Deployment Logs:
   - In Azure Portal → Deployment Center → Logs
   - Look for any errors in the deployment

3. Check Application Logs:
   - In Azure Portal → Log stream
   - See real-time logs from your app

4. Verify Configuration:
   - Configuration → General settings
   - Startup Command should be: gunicorn --bind=0.0.0.0 --timeout 600 app:app
   - Python version should be set

5. Check if files are deployed:
   - Go to: https://pythonvenkyapp-f2d5d7fkeufmhfdd.scm.azurewebsites.net/DebugConsole
   - Navigate to site/wwwroot
   - Verify app.py, requirements.txt exist

Common Issues:
- ❌ App not started → Click "Start" in Azure Portal
- ❌ Wrong startup command → Update in Configuration
- ❌ Missing dependencies → Check requirements.txt
- ❌ Cold start delay → First request can take 60+ seconds
""")
    
    return False

if __name__ == "__main__":
    print("\n⏳ Starting deployment verification...\n")
    time.sleep(2)
    
    success = check_app_status()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED - DEPLOYMENT SUCCESSFUL!")
        print("=" * 70)
        sys.exit(0)
    else:
        print("\n" + "=" * 70)
        print("⚠️  DEPLOYMENT VERIFICATION INCOMPLETE")
        print("=" * 70)
        print("Please follow the troubleshooting steps above.")
        sys.exit(1)
