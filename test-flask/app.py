from flask import Flask, request, jsonify
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

def scrape_text_from_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = ' '.join([p.text for p in soup.find_all('p')])
    
    return text

@app.route('/summarize', methods=['POST'])
def summarize_website():
    url = request.json.get('url')
    text = scrape_text_from_website(url)
    
    inputs = tokenizer(text, truncation=True, padding="longest", return_tensors="pt") #tokenize
    summary_ids = model.generate(inputs['input_ids'], max_length=500, num_beams=4, length_penalty=2.0, early_stopping=True)#summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True) #decode summary
    
    # Return the summary as JSON response
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)
