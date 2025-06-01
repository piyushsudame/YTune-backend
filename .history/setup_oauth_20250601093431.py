from ytmusicapi import YTMusic

def setup_oauth():
    print("Setting up YouTube Music OAuth...")
    YTMusic.setup(filepath="oauth.json")
    print("OAuth setup complete! The credentials have been saved to oauth.json")

if __name__ == "__main__":
    setup_oauth() 
 