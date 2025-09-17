# Luna Travel Assistant 🌍

An intelligent travel assistant powered by Azure OpenAI and Azure AI Search, featuring a modern GUI interface built with Python Tkinter.

## Features ✨

- **AI-Powered Chat**: Leverages Azure OpenAI GPT-4o for intelligent travel recommendations
- **RAG (Retrieval-Augmented Generation)**: Uses Azure AI Search to provide accurate, context-aware responses
- **Modern GUI**: Clean, user-friendly interface with real-time chat
- **Vector Search**: Implements semantic search using text-embedding-ada-002
- **Secure Configuration**: Environment-based credential management

## Technologies Used 🛠️

- **Azure OpenAI**: GPT-4o for chat completions
- **Azure AI Search**: Vector search and document indexing
- **Python**: Core application logic
- **Tkinter**: GUI framework
- **OpenAI Python SDK**: Azure OpenAI integration
- **python-dotenv**: Environment variable management

## Prerequisites 📋

- Python 3.8+
- Azure OpenAI service with GPT-4o deployment
- Azure AI Search service with configured index
- Required Python packages (see requirements.txt)

## Setup Instructions 🚀

1. **Clone the repository**
   ```bash
   git clone https://github.com/abhinav24x/Travel-assistant-app.git
   cd Travel-assistant-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file with your Azure credentials:
   ```env
   OPENAI_ENDPOINT=your_azure_openai_endpoint
   OPENAI_API_KEY=your_azure_openai_key
   CHAT_MODEL=gpt-4o
   EMBEDDING_MODEL=text-embedding-ada-002
   SEARCH_ENDPOINT=your_azure_search_endpoint
   SEARCH_KEY=your_azure_search_key
   INDEX_NAME=your_search_index_name
   ```

4. **Run the application**
   ```bash
   python rag-app.py
   ```

## Usage 💬

1. Launch the application
2. Type your travel-related questions in the input field
3. Press Enter or click "Send"
4. Luna will provide intelligent responses based on your indexed travel data
5. Type "quit" to exit the application

## Architecture 🏗️

The application implements a RAG (Retrieval-Augmented Generation) pattern:

1. **User Query** → Processed by the GUI
2. **Vector Search** → Azure AI Search finds relevant documents
3. **Context Injection** → Retrieved documents enhance the prompt
4. **AI Response** → Azure OpenAI generates contextual answers
5. **Display** → Response shown in the chat interface

## Security 🔒

- API keys stored in environment variables
- `.env` file excluded from version control
- Secure credential handling throughout the application

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- Built as part of Microsoft Learn AI Foundry lab exercises
- Powered by Azure AI services
- Inspired by modern travel assistance needs