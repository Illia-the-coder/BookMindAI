import gradio as gr
import os
import requests
import json
import markdown
from bardapi import BardAsync
from telegraph import Telegraph
import time
# Set up the Telegraph client
telegraph = Telegraph()

telegraph.create_account(short_name='BookMindAI')

token = os.getenv("BARD_API_TOKEN")
bard = BardAsync(token=token)



# Load detail_queries from JSON
with open('detail_queries.json', 'r') as file:
    detail_queries = json.load(file)
with open('lang.json', 'r') as file:
    languages = [str(x) for x in json.load(file).keys()]

def markdown_to_html(md_content):
    return markdown.markdown(md_content)

def is_link_image(link):
    """Check if the link is an image based on its extension."""
    image_types = ["png", "jpg", "jpeg", "gif", "webp", "svg", "bmp", "tiff"]
    return any(ext in link for ext in image_types)

async def fetch_summary(bard, book_name, author):
    question = f"Provide a short summary of the book '{book_name}' by {author}."
    bard_answer = await bard.get_answer(question)
    return bard_answer

async def fetch_book_cover(bard, book_name, author, language):
    query = f"Find me 10 covers image of the book '{book_name}' by {author} in {language} language."
    response = await bard.get_answer(query)
    return [link for link in response["links"] if is_link_image(link)][:2]

def post_to_telegraph(title, content):
    html_content = markdown_to_html(content)
    response = telegraph.create_page(
        title=title,
        html_content=html_content
    )
    return 'https://telegra.ph/{}'.format(response['path'])

async def generate_predictions(book_name, author, language_choice, detail_options=[]):
    bard = BardAsync(token=token, language=language_choice[3:].lower())
    session = requests.Session()
    session.headers = {
        "Host": "bard.google.com",
        "X-Same-Domain": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://bard.google.com",
        "Referer": "https://bard.google.com/",
    }
    session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY"))
    image_links = await fetch_book_cover(bard,book_name, author, language_choice)
    
    details = ""
    for option in detail_options:
        query_template = detail_queries.get(option).format(book_name=book_name, author=author)# + ' Rule 1: Output answer in in {language_choice} language.'
        try:
            response = await bard.get_answer(query_template)
            details += f"\n\n**{option}**:\n{response['content']}"
        except:
            time.sleep(20)
            try:
                response = await bard.get_answer(query_template)
                details += f"\n\n**{option}**:\n{response['content']}"
            except:
                pass
            
    
    summary = await fetch_summary(bard,book_name, author)
    combined_summary = summary["content"] + details
    try:
        telegraph_url = post_to_telegraph(f"Summary of {book_name} by {author}", combined_summary)
    except requests.exceptions.ConnectionError:
        telegraph_url = "Error connecting to Telegraph API"


    return image_links, combined_summary, telegraph_url

with gr.Blocks(title="📚 BookMindAI", theme=gr.themes.Base()).queue() as demo:
    
    
    with gr.Row():
        with gr.Column():
            book_name_input = gr.Textbox(placeholder="Enter Book Name", label="Book Name")
            author_name_input = gr.Textbox(placeholder="Enter Author Name", label="Author Name")
            language_input = gr.Dropdown(choices=languages, label="Language")
            detail_options_input = gr.CheckboxGroup(choices=list(detail_queries.keys()), label="Details to Include", visible=True)
            run_button = gr.Button(label="Run", visible=True)

        with gr.Column():
            book_cover_output = gr.Gallery(label="Book Cover", visible=True)
            telegraph_link_output = gr.Markdown(label="View on Telegraph", visible=True)
    with gr.Row():
        summary_output = gr.Markdown(label="Parsed Content", visible=True)

    run_button.click(fn=generate_predictions,
                     inputs=[book_name_input, author_name_input, language_input, detail_options_input],
                     outputs=[book_cover_output, summary_output, telegraph_link_output],
                     show_progress=True, queue=True)

    # Adding examples to the interface
    examples = [
        ["Harry Potter and the Philosopher's Stone", "J.K. Rowling", "🇬🇧 english"],
        ["Pride and Prejudice", "Jane Austen", "🇺🇦 ukrainian"],
        ["The Great Gatsby", "F. Scott Fitzgerald", "🇫🇷 french"]
    ]
    gr.Examples(examples=examples, inputs=[book_name_input, author_name_input, language_input, detail_options_input])

demo.launch(share=False)
