import requests
import json
import os

class GeminiFlashAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model_name = "gemini-1.5-flash-latest"  # Fixed model name
    
    def generate_content(self, prompt, temperature=0.7, max_tokens=1000):
        """
        Generate content using Gemini Flash model
        """
        url = f"{self.base_url}/models/{self.model_name}:generateContent"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.8,
                "topK": 10
            }
        }
        
        params = {
            "key": self.api_key
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, params=params)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract the generated text with better error handling
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    content = candidate["content"]["parts"][0]["text"]
                    return {
                        "success": True,
                        "content": content,
                        "full_response": result
                    }
                else:
                    return {
                        "success": False,
                        "error": "Invalid response structure",
                        "full_response": result
                    }
            else:
                return {
                    "success": False,
                    "error": "No content generated",
                    "full_response": result
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"JSON decode error: {str(e)}"
            }
        except (KeyError, IndexError) as e:
            return {
                "success": False,
                "error": f"Unexpected response format: {str(e)}"
            }
    
    def list_models(self):
        """
        List available models
        """
        url = f"{self.base_url}/models"
        params = {"key": self.api_key}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to list models: {str(e)}"}

# Example usage
def main():
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Please set your GEMINI_API_KEY environment variable!")
        print("You can set it by running: export GEMINI_API_KEY='your_actual_api_key_here'")
        return
    
    # Initialize the API client
    gemini = GeminiFlashAPI(api_key)
    
    # Example 1: Simple text generation
    print("=== Simple Text Generation ===")
    prompt = "Write a short story about a robot learning to paint."
    result = gemini.generate_content(prompt)
    
    if result["success"]:
        print("Generated content:")
        print(result["content"])
    else:
        print(f"Error: {result['error']}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Code generation
    print("=== Code Generation ===")
    code_prompt = "Write a Python function to calculate the factorial of a number using recursion."
    result = gemini.generate_content(code_prompt, temperature=0.3)
    
    if result["success"]:
        print("Generated code:")
        print(result["content"])
    else:
        print(f"Error: {result['error']}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: List available models
    print("=== Available Models ===")
    models = gemini.list_models()
    if "models" in models:
        for model in models["models"]:
            print(f"- {model['name']}")
    else:
        print(f"Error listing models: {models}")

# Alternative using Google's official client library
def example_with_google_client():
    """
    Example using Google's official generativeai library
    Install with: pip install google-generativeai
    """
    try:
        import google.generativeai as genai
        
        # Get API key from environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("Please set your GEMINI_API_KEY environment variable!")
            return
        
        # Configure the API key
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate content
        response = model.generate_content("Write a haiku about artificial intelligence")
        print("Generated haiku:")
        print(response.text)
        
    except ImportError:
        print("Google GenerativeAI library not installed. Install with: pip install google-generativeai")
    except Exception as e:
        print(f"Error with Google client: {str(e)}")

if __name__ == "__main__":
    # Check if API key is set
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Please set your GEMINI_API_KEY environment variable!")
        print("You can set it by running: export GEMINI_API_KEY='your_actual_api_key_here'")
        print("On Windows: set GEMINI_API_KEY=your_actual_api_key_here")
    else:
        main()
    
    print("\n" + "="*50 + "\n")
    print("Example with Google's official client library:")
    example_with_google_client()
