import google.generativeai as genai
from googlesearch import search

genai.configure(api_key="AIzaSyAgSySyvQF_Demn6nI2v0G5iqCOkZu_N8I")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_web_context(query):
    print(f"Searching the web for: {query}...")
    context = ""
    for result in search(query, num_results=3):
        context += f"Source: {result}\n"
    return context

def ask_gemini(query):
    web_data = get_web_context(query)
    prompt = f"Using the following web sources, answer this question: {query}\n\nSources:\n{web_data}"
    
    response = model.generate_content(prompt)
    return response.text

def main():
    print("=== QSkill AI Search Assistant (Gemini) ===")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nWhat do you want to search for? ")
        if user_input.lower() == 'exit':
            break
            
        try:
            answer = ask_gemini(user_input)
            print("\n--- AI Answer ---")
            print(answer)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
