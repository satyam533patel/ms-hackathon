import requests

# Your API Key
API_KEY = "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"

# Comprehensive list of Azure regions
REGIONS = [
    "eastus", "eastus2", "southcentralus", "westus2", "westus3",
    "australiaeast", "southeastasia", "northeurope", "swedencentral",
    "uksouth", "westeurope", "centralus", "southafricanorth",
    "centralindia", "japaneast", "koreacentral", "canadacentral",
    "francecentral", "germanywestcentral", "norwayeast", "brazilsouth",
    "switzerlandnorth", "uaenorth", "westcentralus", "westus", "southindia",
    "eastasia", "australiasoutheast", "japanwest", "koreasouth",
    "canadaeast", "francesouth", "germanynorth", "norwaywest",
    "brazilsoutheast", "switzerlandwest", "uaecentral"
]

# Function to check API key validity for each region
def find_region(api_key):
    for region in REGIONS:
        url = f"https://{region}.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        headers = {
            "Ocp-Apim-Subscription-Key": api_key
        }
        
        try:
            response = requests.post(url, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ API key is valid for region: {region}")
                return region
            elif response.status_code == 401:
                print(f"❌ Unauthorized for region: {region}")
            elif response.status_code == 404:
                print(f"🔍 Region {region} not found.")
            else:
                print(f"⚠️ Unexpected error for {region}: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error checking region {region}: {e}")

    print("❌ No valid region found for this API key.")
    return None


# Run the function
detected_region = find_region(API_KEY)

if detected_region:
    print(f"\n🎉 Your API key is valid for region: {detected_region}")
else:
    print("\n❌ Could not determine the region. Check if your API key is correct.")
