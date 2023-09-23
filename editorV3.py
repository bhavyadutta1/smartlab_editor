import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askinteger

class ContentItem:
    def __init__(self, type, content):
        self.type = type
        self.content = content

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

        self.previous_button = ttk.Button(self.editor_frame, text="Previous", command=self.previous)
        self.previous_button.grid(row=1, column=0, padx=5, pady=10)

        self.next_button = ttk.Button(self.editor_frame, text="Next", command=self.next)
        self.next_button.grid(row=1, column=1, padx=5, pady=10)

        self.generate_html_button = ttk.Button(self.editor_frame, text="Generate HTML", command=self.generate_html)
        self.generate_html_button.grid(row=1, column=2, padx=5, pady=10)

        self.num_pages_button = ttk.Button(self.editor_frame, text="Set Number of Pages", command=self.set_num_pages)
        self.num_pages_button.grid(row=1, column=3, padx=5, pady=10)

        self.navigation_frame = ttk.Frame(self.editor_frame)
        self.navigation_frame.grid(row=2, column=0, columnspan=4, padx=5, pady=10, sticky="w")

        self.content_text = tk.Text(self.editor_frame, wrap=tk.WORD)
        self.content_text.grid(row=3, column=0, columnspan=4, padx=5, pady=10)

        self.update_content()

    def set_num_pages(self):
        self.num_pages = askinteger("Set Number of Pages", "Enter the number of pages you want to create:", parent=self.root)
        if self.num_pages is not None:
            self.current_page = 0
            self.pages = [[] for _ in range(self.num_pages)]
            self.update_content()

    def add_paragraph(self):
        content = self.content_text.get("1.0", "end-1c")
        self.pages[self.current_page].append(ContentItem('paragraph', content))
        self.update_content()

    def add_text(self):
        content = self.content_text.get("1.0", "end-1c")
        self.pages[self.current_page].append(ContentItem('text', content))
        self.update_content()

    def add_image(self):
        content = self.content_text.get("1.0", "end-1c")
        self.pages[self.current_page].append(ContentItem('image', content))
        self.update_content()

    def add_heading(self):
        content = self.content_text.get("1.0", "end-1c")
        self.pages[self.current_page].append(ContentItem('heading', content))
        self.update_content()

    def previous(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_content()

    def next(self):
        if self.current_page < self.num_pages - 1:
            self.current_page += 1
            self.update_content()

    def update_content(self):
        if not self.pages[self.current_page]:
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, "No content yet.")
        else:
            current_items = self.pages[self.current_page]
            content = ""
            for item in current_items:
                content += f"{item.content}\n"
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, content)

        self.update_navigation_bar()

    def update_navigation_bar(self):
        for widget in self.navigation_frame.winfo_children():
            widget.destroy()

        if self.num_pages > 1:
            previous_button = ttk.Button(self.navigation_frame, text="Previous", command=self.previous)
            previous_button.pack(side="left")

            next_button = ttk.Button(self.navigation_frame, text="Next", command=self.next)
            next_button.pack(side="left")

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

                # Add draggable navigation buttons for previous and next
                prev_button = '<button id="prevBtn" onclick="previousPage()">Previous</button>'
                next_button = '<button id="nextBtn" onclick="nextPage()">Next</button>'
                
                with open(f"page_{i + 1}.html", "w") as f:
                    f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Generated Content</title>
</head>
<body>
    {html_content}
    <script>
        function previousPage() {{
            window.location.href = 'page_{i}.html';
        }}
        function nextPage() {{
            window.location.href = 'page_{i + 2}.html';
        }}
    </script>
    {prev_button}
    {next_button}
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
