# from flask import Flask,request
# import requests
# from bs4 import BeautifulSoup
# import html5lib


# app = Flask(__name__)

# @app.route('/')
# def index():
#     return """
#     <form method="POST" action='/scrape'>
#         <label for="url">Enter the URL:</label><br>
#         <input type="text" id="url" name="url"><br>
#         <button type="Submit">Scrape</button>
#     </form>
#     """

# # @app.route('/scrape', methods=['GET', 'POST'])
# # def scrape(): 
# #     if request.method == 'POST':
# #         url = request.form['url']
# #         response = requests.get(url)
# #         if response.status_code == 200:
# #             soup = BeautifulSoup(response.text, 'html5lib')
# #             p_tags = soup.find_all('p')
# #             p_texts = [p.get_text() for p in p_tags]
# #             #p_tags = [(p, p.attrs.get('class')) for p in soup.find_all('p')]

# #             #h2_tags = [(h2, h2.attrs.get('id')) for h2 in soup.find_all('h2')]

# #             #all_tags = sorted(p_tags + h2_tags, key=lambda x: x[1] if x[1] is not None else '')
# #             #all_texts  = [tag.get_text() for tag, _ in p_tags]    
# #         return '\n'.join(p_texts)
# #     else:
# #         return "Error! Unable to access webpage"

# @app.route('/scrape', methods=['POST'])
# def scrape(): 
#     url = request.form['url']
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         # p_tags = soup.find_all('p')
#         # p_texts = [p.get_text() for p in p_tags]
#         html_content = str(soup)
#         #return '\n'.join(p_texts)
#         return(html_content)
#     else:
#         return "Error! Unable to access webpage"



# if __name__ == "__main__":
#     app.run(debug=True)


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
    summary_ids = model.generate(inputs['input_ids'], max_length=50, num_beams=4, length_penalty=2.0, early_stopping=True)#summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True) #decode summary
    
    # Return the summary as JSON response
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)
