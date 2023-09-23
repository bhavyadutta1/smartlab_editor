# app.py
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Store Whiteboard Editor data
whiteboard_data = {
    "num_pages": 1,
    "current_page": 0,
    "pages": [[]]
}

@app.route('/')
def index():
    return render_template('index.html', whiteboard_data=whiteboard_data)

@app.route('/update_content', methods=['POST'])
def update_content():
    page_index = request.json.get('page_index')
    content = request.json.get('content')
    whiteboard_data['pages'][page_index] = content
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
