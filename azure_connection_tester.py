import requests
import os
from dotenv import load_dotenv

# Load environment variables if a .env file exists
load_dotenv()

def connect_to_azure_app_service():
    """
    A simple program to verify connectivity to an Azure App Service.
    """
    # 1. Configuration
    # Replace this with your actual Azure App Service URL
    # or set it as an environment variable 'AZURE_APP_URL'
    app_url = os.getenv("AZURE_APP_URL", "https://pythonvenkyapp-f2d5d7fkeufmhfdd.eastus-01.azurewebsites.net")
    
    print(f"\n\ud83d\ude80 Initializing Connection to: {app_url}...")
    
    try:
        # 2. Perform a GET request to the App Service
        # This 'connects' to the application layer of your App Service
        response = requests.get(app_url, timeout=15)
        
        # 3. Analyze the response
        if response.status_code == 200:
            print("\u2705 SUCCESS: Successfully connected to Azure App Service!")
            print(f"Status Code: {response.status_code}")
            print("-" * 40)
            print("Preview of content from Azure:")
            print(response.text[:200] + "..." if len(response.text) > 200 else response.text)
            print("-" * 40)
        else:
            print(f"\u26a0\ufe0f WARNING: Connection established but server returned status: {response.status_code}")
            print(f"Response: {response.reason}")
            
    except requests.exceptions.RequestException as e:
        print("\u274c ERROR: Failed to connect to Azure App Service.")
        print(f"Reason: {e}")
        print("\nPossible causes:")
        print("1. The App Service URL is incorrect.")
        print("2. The App Service is stopped or in 'Always On' startup.")
        print("3. There is a network/firewall issue blocking the connection.")

if __name__ == "__main__":
    connect_to_azure_app_service()
