import requests
import sys

# The URL of your Azure App Service (replace with your actual URL)
# Based on your git remote, it should be something like:
# https://<appname>.azurewebsites.net
AZURE_APP_URL = "https://pythonvenkyapp-f2d5d7fkeufmhfdd.eastus-01.azurewebsites.net" 

def check_connection():
    print(f"--- Connecting to Azure App Service at {AZURE_APP_URL} ---")
    try:
        response = requests.get(AZURE_APP_URL, timeout=10)
        
        if response.status_code == 200:
            print("\u2705 SUCCESS: Connection established!")
            print(f"Response Content: {response.text}")
        else:
            print(f"\u26a0\ufe0f WARNING: Connected, but received status code {response.status_code}")
            print(f"Response: {response.reason}")
            
    except requests.exceptions.ConnectionError:
        print("\u274c ERROR: Could not connect to the server. Check if the App Service is running.")
    except Exception as e:
        print(f"\u274c ERROR: An unexpected error occurred: {e}")

if __name__ == "__main__":
    check_connection()
