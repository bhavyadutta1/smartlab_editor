class ContentItem:
    def __init__(self, type, content):
        self.type = type
        self.content = content

class Editor:
    def __init__(self):
        self.content_items = []

    def add_paragraph(self):
        content = input("Enter paragraph content: ")
        self.content_items.append(ContentItem('paragraph', content))
        self.generate_html()

    def add_text(self):
        content = input("Enter text content: ")
        self.content_items.append(ContentItem('text', content))
        self.generate_html()

    def add_image(self):
        content = input("Enter image URL: ")
        self.content_items.append(ContentItem('image', content))
        self.generate_html()

    def generate_html(self):
        html_content = ""
        for item in self.content_items:
            if item.type == 'paragraph':
                html_content += f"<p>{item.content}</p>"
            elif item.type == 'text':
                html_content += f"<span>{item.content}</span>"
            elif item.type == 'image':
                html_content += f"<img src='{item.content}' alt='Image' />"
        with open("output.html", "w") as f:
            f.write(f"<!DOCTYPE html><html><head><title>Generated Content</title></head><body>{html_content}</body></html>")

def main():
    editor = Editor()

    while True:
        print("\nMenu:")
        print("1. Add Paragraph")
        print("2. Add Text")
        print("3. Add Image")
        print("4. Generate HTML")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            editor.add_paragraph()
        elif choice == '2':
            editor.add_text()
        elif choice == '3':
            editor.add_image()
        elif choice == '4':
            editor.generate_html()
            print("HTML file generated: output.html")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()