from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Content items will be stored in a list
content_items = []

@app.route('/editor')
def editor():
    return render_template('editor.html')


@app.route('/generate_html', methods=['POST'])
def generate_html():
    # Generate HTML content based on content_items list
    html_content = ""
    for item in content_items:
        if item['type'] == 'paragraph':
            html_content += f"<p>{item['content']}</p>\n"
        elif item['type'] == 'text':
            html_content += f"<span>{item['content']}</span>\n"
        elif item['type'] == 'image':
            html_content += f"<img src='{item['content']}' alt='Image' />\n"
        elif item['type'] == 'heading':
            html_content += f"<h2>{item['content']}</h2>\n"

    # Return the generated HTML content as JSON response
    return jsonify({'html_content': html_content})

if __name__ == '__main__':
    app.run(debug=True)