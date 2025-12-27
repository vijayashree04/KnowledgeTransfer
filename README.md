# 📚 Centralized Knowledge Transfer Hub

A modern, AI-powered knowledge management system that enables teams to upload, organize, and query documents using semantic search. Built with Streamlit, Supabase, Pinecone, and Google Gemini AI.

## ✨ Features

- **📤 Document Upload**: Support for multiple file formats (PDF, DOCX, TXT, MD, PY, JS, JSON)
- **🤖 AI-Powered Chatbot**: Ask questions and get answers based on your team's documents using semantic search
- **🔍 Vector Search**: Pinecone integration for intelligent document retrieval
- **📝 Automatic Summarization**: AI-generated summaries for uploaded documents
- **👥 Team Management**: Multi-team support with access codes and team leads
- **🔐 Secure Authentication**: User authentication and team-based access control
- **☁️ Cloud Storage**: Supabase integration for scalable document storage
- **📊 Document Repository**: View and manage all team documents in one place

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage
- **Vector Database**: Pinecone (optional, for semantic search)
- **AI/ML**: Google Gemini (text-embedding-004, gemini-2.5-flash)
- **Document Processing**: pypdf, python-docx

## 📋 Prerequisites

- Python 3.11 or higher
- Supabase account and project
- Google Gemini API key
- Pinecone account (optional, for vector search)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd KnowledgeTransfer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

**Activate the virtual environment:**

- **Windows PowerShell:**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

- **Windows CMD:**
  ```cmd
  venv\Scripts\activate.bat
  ```

- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Create `.env` File

Create a `.env` file in the project root with the following variables:

```env
# Supabase Configuration (Required)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# Gemini API Key (Required)
GEMINI_API_KEY=your-gemini-api-key-here

# Pinecone Configuration (Optional - for vector search)
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_INDEX_NAME=kt-docs
```

### 2. Set Up Supabase Database

Run the SQL schema in your Supabase SQL Editor:

```bash
# See supabase_schema.sql for the complete schema
```

The schema includes:
- `teams` table for team management
- `users` table for user authentication
- `documents` table for document metadata

### 3. Create Supabase Storage Bucket

1. Go to Supabase Dashboard → Storage
2. Create a bucket named `documents`
3. Set appropriate permissions (public or private based on your needs)

### 4. Set Up Pinecone Index (Optional)

If using vector search:

1. Create a Pinecone account at [pinecone.io](https://www.pinecone.io)
2. Create an index with:
   - **Name**: `kt-docs` (or your preferred name)
   - **Dimension**: `768` (for Gemini text-embedding-004)
   - **Metric**: `cosine`

## 🏃 Running the Application

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage

### First Time Setup

1. **Create a Team** (via Supabase dashboard or API):
   - Team name
   - Access code (for team members to join)
   - Team lead email

2. **Sign Up**:
   - Click "Sign Up" on the login page
   - Enter your name, email, and password
   - Create your account

3. **Login**:
   - Enter your email and password
   - Enter your team's access code
   - You'll be redirected to the main dashboard

### Uploading Documents

1. Go to the **"📤 Upload Documents"** tab
2. Click "Choose a file" and select your document
3. Click "Process & Upload"
4. The document will be:
   - Uploaded to Supabase Storage
   - Indexed in Pinecone (if enabled)
   - Summarized using AI
   - Stored in the database

### Using the Chatbot

1. Go to the **"🤖 KT Chatbot"** tab
2. Type your question in the chat input
3. The chatbot will:
   - Search for relevant document chunks using vector search
   - Generate an answer based on the retrieved context
   - Display the response

### Viewing Documents

1. Go to the **"📝 Document Summaries"** tab
2. Browse all documents uploaded by your team
3. Click on any document to view:
   - Summary
   - Content preview
   - Upload information

### Team Management (Team Leads Only)

Team leads can:
- View team information
- Update team lead assignment
- Delete documents

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit UI  │
└────────┬────────┘
         │
         ├──► Supabase (Database & Storage)
         │    ├── Teams
         │    ├── Users
         │    └── Documents
         │
         ├──► Pinecone (Vector Database)
         │    └── Document Embeddings
         │
         └──► Google Gemini AI
              ├── Text Embeddings
              ├── Document Summarization
              └── Chat Responses
```

## 📁 Project Structure

```
KnowledgeTransfer/
├── main.py                 # Main Streamlit application
├── auth.py                 # Authentication logic
├── document_store.py       # Document management
├── vector_store.py         # Pinecone vector search
├── gemini_utils.py         # Gemini AI integration
├── team_store.py           # Team management
├── user_store.py           # User management
├── supabase_config.py      # Supabase configuration
├── supabase_schema.sql     # Database schema
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .env                   # Environment variables (create this)
```

## 🔧 Configuration Options

### Chunking Parameters

Documents are automatically chunked for vector search. You can adjust these in `vector_store.py`:

```python
def _chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    # Adjust chunk_size and overlap as needed
```

### Retrieval Parameters

Adjust the number of chunks retrieved in `document_store.py`:

```python
matches = vector_store.query_similar_documents(
    query_text=query,
    team_id=str(team_id),
    team_name=team_name,
    top_k=10  # Number of chunks to retrieve
)
```

## 🐛 Troubleshooting

### "Supabase is not configured" Error

- Ensure `.env` file exists with `SUPABASE_URL` and `SUPABASE_KEY`
- Verify the Supabase project is active
- Check that the database schema is set up correctly

### "Pinecone not available" Warning

- This is normal if Pinecone is not configured
- The system will fall back to using all documents
- To enable: add `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` to `.env`

### Document Upload Fails

- Check Supabase Storage bucket exists and is accessible
- Verify file size is within limits
- Ensure proper permissions on the storage bucket

### Chatbot Not Working

- Verify Gemini API key is set correctly
- Check that documents have been indexed in Pinecone (if using vector search)
- Ensure documents contain text content (not just images)

## 📝 Supported File Formats

- **Text**: `.txt`, `.md`, `.py`, `.js`, `.json`
- **Documents**: `.pdf`, `.docx`, `.doc`
- **Maximum file size**: 200MB

## 🔒 Security Considerations

- Store API keys securely in `.env` file (never commit to version control)
- Use Supabase Row Level Security (RLS) for data access control
- Prefer `SUPABASE_KEY` (anon key) over service role key for client operations
- Regularly rotate API keys

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the web framework
- [Supabase](https://supabase.com/) for backend infrastructure
- [Pinecone](https://www.pinecone.io/) for vector search
- [Google Gemini](https://ai.google.dev/) for AI capabilities

## 📞 Support

For issues and questions, please open an issue on the repository.

---

**Built with ❤️ for efficient knowledge transfer**

