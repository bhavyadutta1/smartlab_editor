import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, colorchooser

class ContentItem:
    def __init__(self, type, content, bg_color="white"):
        self.type = type
        self.content = content
        self.bg_color = bg_color

class WhiteboardEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Whiteboard Editor")

        self.num_pages = 1  # Number of pages to create
        self.current_page = 0  # Current page index
        self.pages = [[] for _ in range(self.num_pages)]  # List to hold content for each page

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

        self.bg_color_button = ttk.Button(self.editor_frame, text="Background Color", command=self.choose_bg_color)
        self.bg_color_button.grid(row=1, column=0, padx=5, pady=10)

        self.previous_button = ttk.Button(self.editor_frame, text="Previous", command=self.previous)
        self.previous_button.grid(row=1, column=1, padx=5, pady=10)

        self.next_button = ttk.Button(self.editor_frame, text="Next", command=self.next)
        self.next_button.grid(row=1, column=2, padx=5, pady=10)

        self.generate_html_button = ttk.Button(self.editor_frame, text="Generate HTML", command=self.generate_html)
        self.generate_html_button.grid(row=1, column=3, padx=5, pady=10)

        self.num_pages_button = ttk.Button(self.editor_frame, text="Set Number of Pages", command=self.set_num_pages)
        self.num_pages_button.grid(row=1, column=4, padx=5, pady=10)

        self.content_text = tk.Text(self.editor_frame, wrap=tk.WORD)
        self.content_text.grid(row=2, column=0, columnspan=5, padx=5, pady=10)

        self.update_content()

    def set_num_pages(self):
        self.num_pages = simpledialog.askinteger("Set Number of Pages", "Enter the number of pages you want to create:",
                                                parent=self.root)
        if self.num_pages is not None:
            self.current_page = 0
            self.pages = [[] for _ in range(self.num_pages)]
            self.update_content()

    def add_paragraph(self):
        content = self.content_text.get("1.0", "end-1c")
        bg_color = self.pages[self.current_page][-1].bg_color if self.pages[self.current_page] else "white"
        self.pages[self.current_page].append(ContentItem('paragraph', content, bg_color))
        self.update_content()

    def add_text(self):
        content = self.content_text.get("1.0", "end-1c")
        bg_color = self.pages[self.current_page][-1].bg_color if self.pages[self.current_page] else "white"
        self.pages[self.current_page].append(ContentItem('text', content, bg_color))
        self.update_content()

    def add_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
        if file_path:
            bg_color = self.pages[self.current_page][-1].bg_color if self.pages[self.current_page] else "white"
            self.pages[self.current_page].append(ContentItem('image', file_path, bg_color))
            self.update_content()

    def add_heading(self):
        content = self.content_text.get("1.0", "end-1c")
        bg_color = self.pages[self.current_page][-1].bg_color if self.pages[self.current_page] else "white"
        self.pages[self.current_page].append(ContentItem('heading', content, bg_color))
        self.update_content()

    def previous(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_content()

    def next(self):
        if self.current_page < self.num_pages - 1:
            self.current_page += 1
            self.update_content()

    def choose_bg_color(self):
        bg_color = colorchooser.askcolor()[1]
        if bg_color:
            if self.pages[self.current_page]:
                self.pages[self.current_page][-1].bg_color = bg_color
            self.update_content()

    def update_content(self):
        if not self.pages[self.current_page]:
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, "No content yet.")
        else:
            current_items = self.pages[self.current_page]
            content = ""
            for item in current_items:
                content += f"<div style='background-color:{item.bg_color}'>{item.content}</div>\n"
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, content)

    def generate_html(self):
        if any(self.pages):
            for i, page in enumerate(self.pages):
                if not page:
                    continue
                html_content = ""
                for item in page:
                    if item.type == 'paragraph':
                        html_content += f"<p>{item.content}</p>\n"
                    elif item.type == 'text':
                        html_content += f"<span>{item.content}</span>\n"
                    elif item.type == 'image':
                        html_content += f"<img src='{item.content}' alt='Image' />\n"
                    elif item.type == 'heading':
                        html_content += f"<h2>{item.content}</h2>\n"

                with open(f"page_{i + 1}.html", "w") as f:
                    f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Generated Content</title>
</head>
<body>
    {html_content}
    <div id="navigation">
        {f'<a href="page_{i}.html">Previous</a>' if i > 0 else ''}
        {f'<a href="page_{i + 2}.html">Next</a>' if i < len(self.pages) - 1 else ''}
    </div>
</body>
</html>
""")
                print(f"HTML file generated for Page {i + 1}: page_{i + 1}.html")
        else:
            print("No content to generate.")

def main():
    root = tk.Tk()
    editor = WhiteboardEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
