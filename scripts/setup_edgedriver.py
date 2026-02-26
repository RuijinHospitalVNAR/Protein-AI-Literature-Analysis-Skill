"""
Script to download and setup EdgeDriver for Selenium
"""
import requests
import zipfile
import os
import sys
from pathlib import Path

def get_edge_version():
    """Get Microsoft Edge browser version"""
    try:
        import subprocess
        result = subprocess.run(['reg', 'query', 
                           'HKEY_CURRENT_USER\\Software\\Microsoft\\Edge\\BLBeacon', 
                           '/v', 'version'], 
                          capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # Try alternative method
    try:
        result = subprocess.run(['powershell', '-Command', 
                           'Get-AppxPackage -Name "Microsoft.MicrosoftEdge.Stable" | Select-Object -ExpandProperty Version'], 
                          capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    return None

def download_edgedriver(version):
    """Download EdgeDriver for specified version"""
    # Extract major version number
    major_version = version.split('.')[0]
    
    # EdgeDriver download URL
    base_url = "https://msedgedriver.azureedge.net/"
    download_url = f"{base_url}{major_version}/{version}/edgedriver_win64.zip"
    
    print(f"Downloading EdgeDriver version {version}...")
    print(f"Download URL: {download_url}")
    
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        # Save to file
        zip_path = Path("edgedriver_win64.zip")
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded to {zip_path.absolute()}")
        
        # Extract
        print("Extracting EdgeDriver...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall()
        
        # Clean up
        zip_path.unlink()
        print("Extraction complete!")
        
        # Find the executable
        for file in Path('.').glob('msedgedriver.exe'):
            print(f"EdgeDriver executable: {file.absolute()}")
            return str(file.absolute())
        
        print("Error: Could not find msedgedriver.exe")
        return None
        
    except Exception as e:
        print(f"Error downloading EdgeDriver: {e}")
        return None

def main():
    """Main function"""
    print("EdgeDriver Setup Script")
    print("=" * 50)
    
    # Get Edge version
    print("\nDetecting Microsoft Edge version...")
    edge_version = get_edge_version()
    
    if edge_version:
        print(f"Found Edge version: {edge_version}")
    else:
        print("Could not detect Edge version automatically.")
        print("Please enter your Edge version manually (e.g., 144.0.3719.82):")
        edge_version = input().strip()
    
    # Download EdgeDriver
    edgedriver_path = download_edgedriver(edge_version)
    
    if edgedriver_path:
        print("\n" + "=" * 50)
        print("Setup complete!")
        print(f"EdgeDriver location: {edgedriver_path}")
        print("\nTo use EdgeDriver with Selenium:")
        print("1. Add the directory containing msedgedriver.exe to your PATH")
        print("2. Or specify the path in your Python script")
        print("\nExample usage:")
        print("from selenium import webdriver")
        print("from selenium.webdriver.edge.options import Options")
        print("options = Options()")
        print("driver = webdriver.Edge(options=options)")
    else:
        print("\nSetup failed. Please try downloading manually:")
        print("https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")

if __name__ == "__main__":
    main()