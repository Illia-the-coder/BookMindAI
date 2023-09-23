

# 📚 BookMindAI: Book Analysis with BookGPT and Palm 2 🤖

BookMindAI is an advanced tool for book analysis that provides a detailed overview of any book. Dive into plot points, relationships between characters, themes, motifs, and much more!

## Features 🌟

- **Detailed Analysis**: Understand the main events, character dynamics, key themes, and literary techniques.
- **Book Cover Retrieval**: View the book's cover.
- **Bookstore Links**: Find out where you can purchase the book.
- **Quick Responses**: Get a detailed analysis in less than 30 seconds!

## Installation 🛠

1. Clone the repository:
   ```bash
   git clone https://github.com/Illia-the-coder/BookMindAI.git
   ```

2. Navigate to the project directory:
   ```bash
   cd BookMindAI
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage 🚀

1. Set the environment variable for the Bard API token:
   ```bash
   export BARD_API_TOKEN=your_token_here
   ```

2. Launch the Gradio interface:
   ```bash
   python app.py
   ```

3. Open the Gradio interface in your browser and start analyzing books!

## How It Works 🧠

1. **Data Input**: The user enters the book title, author's name, language, and additional analysis parameters through the Gradio interface.
2. **Language Selection**: The chosen language is used to configure the Bard API.
3. **Book Cover Retrieval**: A request is sent to the Bard API.
4. **Detailed Analysis**: For each user-selected parameter, a separate request is made to the Bard API.
5. **Short Summary Retrieval**: A request is sent to the Bard API.
6. **Combining Results**: The short summary and detailed analysis are combined.
7. **Publication on Telegraph**: The full book analysis is published on Telegraph.
8. **Displaying Results**: The results are displayed in the Gradio interface.

## License 📄

This project is licensed under the MIT license - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements 🙏

- Thanks to Palm 2 for the powerful model.
- Gradio for the intuitive interface.
- And to all participants who helped make this project a reality!
