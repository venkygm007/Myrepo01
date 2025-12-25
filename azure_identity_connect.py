from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
import sys

def connect_and_list_subscriptions():
    """
    Connects to Azure using DefaultAzureCredential and lists available subscriptions.
    DefaultAzureCredential will try to authenticate using:
    1. Environment variables (AZURE_CLIENT_ID, etc.)
    2. Managed Identity (if running on Azure)
    3. VS Code / Azure CLI / Interactive Browser
    """
    print("\n--- Connecting to Azure using Identity SDK ---")
    
    try:
        # 1. Initialize the credential
        credential = DefaultAzureCredential()
        
        # 2. Use the credential to create a management client
        subscription_client = SubscriptionClient(credential)
        
        # 3. List subscriptions to verify connection
        print("Fetching your Azure Subscriptions...")
        subscriptions = list(subscription_client.subscriptions.list())
        
        if not subscriptions:
            print("⚠️ No subscriptions found. Ensure you are logged in to Azure.")
            print("Tip: Run 'az login' in your terminal or sign in via the Azure VS Code extension.")
            return

        print(f"✅ SUCCESS: Found {len(subscriptions)} subscription(s):")
        for sub in subscriptions:
            print(f" - {sub.display_name} (ID: {sub.subscription_id})")
            
    except Exception as e:
        print(f"❌ ERROR: Failed to fulfill Azure connection requirement.")
        print(f"Details: {e}")
        print("\nSuggestions:")
        print("1. If you haven't logged in, try running: az login")
        print("2. Ensure you have an active internet connection.")

if __name__ == "__main__":
    connect_and_list_subscriptions()
