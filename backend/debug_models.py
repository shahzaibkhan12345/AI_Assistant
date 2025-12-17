# debug_models.py

import google.generativeai as genai
import os

# --- PASTE YOUR API KEY HERE ---
# Make sure to replace the placeholder with your actual key from Google AI Studio
API_KEY = "AIzaSyDMxgehUEjkavYQN-5DMyKvFyoK-8r6Oh4" 
# --------------------------------

if API_KEY == "PASTE_YOUR_GEMINI_API_KEY_HERE":
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!! PLEASE EDIT THIS FILE AND PASTE YOUR API KEY FIRST !!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
else:
    try:
        genai.configure(api_key=API_KEY)
        print("Successfully configured API key.")
        print("\n--- Listing Available Models for generateContent ---\n")

        for m in genai.list_models():
            # We only care about models that can generate text
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
        
        print("\n--- End of List ---")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please double-check that your API key is correct and active.")
