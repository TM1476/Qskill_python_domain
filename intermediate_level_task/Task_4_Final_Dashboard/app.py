from flask import Flask, render_template, request
from textblob import TextBlob
from google import genai
from googlesearch import search
import time

# Looks for index.html in the same folder
app = Flask(__name__, template_folder='.')

# --- Configuration ---
# Use your verified API Key here
GEMINI_API_KEY = "AIzaSyAgSySyvQF_Demn6nI2v0G5iqCOkZu_N8I"
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('sentiment_text', '')
    try:
        blob = TextBlob(text)
        polarity = round(blob.sentiment.polarity, 2)
        if polarity > 0: result, color = "Positive", "success"
        elif polarity < 0: result, color = "Negative", "danger"
        else: result, color = "Neutral", "secondary"
    except:
        result, color, polarity = "Error", "warning", 0

    return render_template('index.html', sentiment_res=result, pol=polarity, original_text=text, color=color)

@app.route('/search', methods=['POST'])
def ai_search():
    query = request.form.get('search_query', '')
    context = ""
    
    # 1. Fetching Search Results
    try:
        for res in search(query, num_results=3):
            context += f"Source: {res}\n"
    except:
        context = "No live web data found."

    # 2. AI Processing
    try:
        prompt = f"Using these sources, answer briefly: {query}\n\nSources:\n{context}"
        
        # Try gemini-2.0-flash without any prefixes
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        answer = response.text
    except Exception as e:
        # If 2.0 fails, it usually defaults to a quota error (429)
        if "429" in str(e):
            answer = "Quota exceeded. Please wait 60 seconds and try again."
        elif "404" in str(e):
            answer = "Model path error. Ensure you are using 'gemini-2.0-flash' as the model name."
        else:
            answer = f"AI Error: {e}"

    return render_template('index.html', search_answer=answer, user_query=query)

if __name__ == '__main__':
    app.run(debug=True)
