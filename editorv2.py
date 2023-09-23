import tkinter as tk
from tkinter import ttk

class ContentItem:
    def __init__(self, type, content):
        self.type = type
        self.content = content

class WhiteboardEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Whiteboard Editor")

        self.content_items = []
        self.current_index = 0

        self.editor_frame = ttk.Frame(root)
        self.editor_frame.pack(padx=10, pady=10)

        self.add_paragraph_button = ttk.Button(self.editor_frame, text="Add Paragraph", command=self.add_paragraph)
        self.add_paragraph_button.grid(row=0, column=0, padx=5)

        self.add_text_button = ttk.Button(self.editor_frame, text="Add Text", command=self.add_text)
        self.add_text_button.grid(row=0, column=1, padx=5)

        self.add_image_button = ttk.Button(self.editor_frame, text="Add Image", command=self.add_image)
        self.add_image_button.grid(row=0, column=2, padx=5)

        self.add_heading_button = ttk.Button(self.editor_frame, text="Add Heading", command=self.add_heading)
        self.add_heading_button.grid(row=0, column=3, padx=5)

        self.previous_button = ttk.Button(self.editor_frame, text="Previous", command=self.previous)
        self.previous_button.grid(row=1, column=0, padx=5, pady=10)

        self.next_button = ttk.Button(self.editor_frame, text="Next", command=self.next)
        self.next_button.grid(row=1, column=1, padx=5, pady=10)

        self.generate_html_button = ttk.Button(self.editor_frame, text="Generate HTML", command=self.generate_html)
        self.generate_html_button.grid(row=1, column=2, padx=5, pady=10)

        self.content_text = tk.Text(self.editor_frame, wrap=tk.WORD)
        self.content_text.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

    def add_paragraph(self):
        content = self.content_text.get("1.0", "end-1c")
        self.content_items.append(ContentItem('paragraph', content))
        self.update_content()

    def add_text(self):
        content = self.content_text.get("1.0", "end-1c")
        self.content_items.append(ContentItem('text', content))
        self.update_content()

    def add_image(self):
        content = self.content_text.get("1.0", "end-1c")
        self.content_items.append(ContentItem('image', content))
        self.update_content()

    def add_heading(self):
        content = self.content_text.get("1.0", "end-1c")
        self.content_items.append(ContentItem('heading', content))
        self.update_content()

    def previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_content()

    def next(self):
        if self.current_index < len(self.content_items) - 1:
            self.current_index += 1
            self.update_content()

    def update_content(self):
        if not self.content_items:
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, "No content yet.")
        else:
            current_item = self.content_items[self.current_index]
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, current_item.content)

    def generate_html(self):
        if self.content_items:
            html_content = ""
            for item in self.content_items:
                if item.type == 'paragraph':
                    html_content += f"<p>{item.content}</p>\n"
                elif item.type == 'text':
                    html_content += f"<span>{item.content}</span>\n"
                elif item.type == 'image':
                    html_content += f"<img src='{item.content}' alt='Image' />\n"
                elif item.type == 'heading':
                    html_content += f"<h2>{item.content}</h2>\n"

            with open("output.html", "w") as f:
                f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>Generated Content</title>\n</head>\n<body>\n{html_content}</body>\n</html>")
            print("HTML file generated: output.html")
        else:
            print("No content to generate.")

def main():
    root = tk.Tk()
    editor = WhiteboardEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()