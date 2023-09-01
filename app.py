import gradio as gr
import os
from bardapi import BardAsync

# Retrieve the token from environment variables
token = os.getenv("BARD_API_TOKEN")
# export BARD_API_TOKEN=aQjhgKn_gQ0rR3gHEXgbP-ZaPH13wzBfuEIXEeKNppVappfNr_Jd1l-Slyap6XVZld-ABw.
# Ensure the token is set
if not token:
    raise ValueError("BARD_API_TOKEN environment variable is not set.")

bard = BardAsync(token=token)

def is_link_image(link):
    """Check if the link is an image based on its extension."""
    image_types = ["png", "jpg", "jpeg", "gif", "webp", "svg", "bmp", "tiff"]
    return any(ext in link for ext in image_types)

async def fetch_summary(book_name, author, language):
    """Fetch a comprehensive summary of the book."""
    question = f"""
    Provide a comprehensive summary of the book '{book_name}' by {author} in {language}. This should include:
    - A timeline of major events or plot points.
    - Character relationships and their significance.
    - Key themes and motifs visualized.
    - Any notable literary devices or techniques used by the author.
    - A brief textual summary to accompany the graphics.
    """
    return await bard.get_answer(question)

async def fetch_book_cover(book_name, author, language):
    """Fetch the book cover image."""
    query = f"Find me 10 covers image of the book '{book_name}' by {author} in {language} language."
    response = await bard.get_answer(query)
    return [link for link in response["links"] if is_link_image(link)][:4]

async def fetch_bookstore_links(book_name, author, language):
    """Fetch links to bookstores for purchasing the book."""
    query = f"Find me 4 links on the bookstores for buying this book '{book_name}' by {author} in {language} language."
    response = await bard.get_answer(query)
    return [link for link in response["links"] if not is_link_image(link)]

async def summarize_book(book_name, author, language_choice):
    image_links = await fetch_book_cover(book_name, author, language_choice)  #if book_name not in [x[0] for x in examples] else []
    summary = await fetch_summary(book_name, author, language_choice)
    # bookstore_links = await fetch_bookstore_links(book_name, author, language_choice) if book_name not in [x[0] for x in examples] else []
    
    # bookstore_links_text = (
    #     "# Several links on the bookshelf to find or buy the book:\n"
    #     + "\n".join(bookstore_links)
    #     if bookstore_links
    #     else ""
    # )
    
    return image_links, summary["content"] #, bookstore_links_text

# Gradio Interface
description = """
# 📚 BookGPT: Аналіз Книги

## Цей сервіс дозволяє отримати докладний аналіз будь-якої книги. Введіть назву книги, ім'я автора та бажану мову.

**Особливості**:
- 🔍 Детальний аналіз: Основні події, відносини між персонажами, ключові теми та літературні прийоми.
- 🖼 Обкладинка книги: Перегляньте зображення обкладинки.
- 🧨 Швидкість: Отримайте швидку відповть менше ніж за пів хвилини. 
- Powered by Palm 2 🤖
"""

interface = gr.Interface(
    fn=summarize_book,
    inputs=[
        gr.components.Textbox(placeholder="Enter Book Name", label="Book Name"),
        gr.components.Textbox(placeholder="Enter Author Name", label="Author Name"),
        gr.components.Textbox(placeholder="Enter Language you'd like to see", label="Language")
    ],
    outputs=[
        gr.components.Gallery(label="Book Cover"),
        gr.components.Markdown(label="Parsed Content"),
        # gr.components.Markdown(label="Book Shelf Links"),
    ],
    # examples=examples,
    description=description, title = '📚 BookGPT'
)
interface.launch()
