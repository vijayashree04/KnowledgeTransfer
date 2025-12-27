# Step-by-Step Setup Guide

Follow these instructions carefully to set up and run the Knowledge Transfer Hub.

---

## Step 1: Check Python Installation

1. Open your terminal/command prompt (PowerShell on Windows)
2. Check if Python is installed:
   ```bash
   python --version
   ```
   You should see Python 3.11 or higher. If not, install Python from [python.org](https://www.python.org/downloads/)

---

## Step 2: Navigate to Project Directory

1. Open terminal/command prompt
2. Navigate to your project folder:
   ```bash
   cd C:\Users\vijay\Desktop\Knowledge-Stream
   ```
   (Adjust the path if your project is in a different location)

---

## Step 3: Install Dependencies

### Option A: Using `uv` (if you have it installed)

1. Check if `uv` is installed:
   ```bash
   uv --version
   ```

2. If installed, run:
   ```bash
   uv sync
   ```

### Option B: Using `pip` (Standard Method)

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   
   **Windows PowerShell:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **Windows CMD:**
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   **Mac/Linux:**
   ```bash
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install streamlit google-genai google-generativeai python-dotenv watchdog
   ```

   Wait for installation to complete. You should see "Successfully installed..." messages.

---

## Step 4: Set Up Gemini API Key (Optional but Recommended)

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Set it as an environment variable:

   **Windows PowerShell:**
   ```powershell
   $env:GEMINI_API_KEY="your_api_key_here"
   ```
   
   **Windows CMD:**
   ```cmd
   set GEMINI_API_KEY=your_api_key_here
   ```
   
   **Mac/Linux:**
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

   **Note:** Replace `your_api_key_here` with your actual API key.

   **Alternative:** Create a `.env` file in the project root with:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

   **Note:** If you skip this step, the app will use a fallback key (for development only).

---

## Step 5: Create Your First Team

1. Make sure you're in the project directory and virtual environment is activated (if using one)

2. Run the team creation script:
   ```bash
   python create_team.py
   ```

3. You'll be prompted to enter:
   - **Team Name:** Enter a name (e.g., "Engineering Team", "Product Team")
   - **Access Code:** Enter a code that team members will use to login (e.g., "ENG2024", "PROD123")
   
   **Example:**
   ```
   Enter team name: Engineering Team
   Enter access code (will be used during login): ENG2024
   ```

4. You'll see a success message with the team details:
   ```
   ✅ Team created successfully!
      Team ID: team_1_1234567890.123
      Team Name: Engineering Team
      Access Code: ENG2024
   ```

5. **Important:** Save the access code! Team members will need it to login.

6. To create more teams, run `python create_team.py` again.

7. To list all teams:
   ```bash
   python create_team.py list
   ```

---

## Step 6: Run the Application

1. Make sure you're still in the project directory

2. Make sure your virtual environment is activated (if using one)

3. Start the Streamlit app:
   ```bash
   streamlit run main.py
   ```

4. You should see output like:
   ```
   You can now view your Streamlit app in your browser.

   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

5. The application will automatically open in your default web browser. If it doesn't, manually open:
   ```
   http://localhost:8501
   ```

---

## Step 7: Login to the Application

1. In the browser, you'll see the login page

2. Fill in the login form:
   - **Username:** Enter any username (e.g., "john", "jane")
   - **Password:** Enter any password (e.g., "password123")
   - **Team Access Code:** Enter the access code you created in Step 5 (e.g., "ENG2024")

3. Click the **Login** button

4. If the access code is correct, you'll be logged in and see the main dashboard

5. If you see an error "Invalid access code", make sure:
   - You're using the exact access code (case-sensitive)
   - You created the team successfully in Step 5
   - You can verify by running `python create_team.py list`

---

## Step 8: Using the Application

### Upload Documents

1. Click on the **"📤 Upload Documents"** tab
2. Click **"Choose a file"** and select a text file (.txt, .md, .py, .js, .json)
3. Click **"Process & Upload"** button
4. Wait for the file to upload and summary to generate
5. You'll see a success message and a preview of the summary

### View Document Summaries

1. Click on the **"📝 Document Summaries"** tab
2. You'll see all documents uploaded by your team
3. Click on any document to expand and view its summary and content preview

### Use the Chatbot

1. Click on the **"🤖 KT Chatbot"** tab
2. Type a question in the chat input (e.g., "What is the deployment process?")
3. Press Enter or click send
4. The chatbot will answer based on your team's uploaded documents

---

## Step 9: Create Additional Teams (Optional)

To create separate hubs for different teams:

1. Stop the application (press `Ctrl+C` in the terminal)

2. Create another team:
   ```bash
   python create_team.py
   ```
   
   Example:
   - Team Name: `Product Team`
   - Access Code: `PROD2024`

3. Restart the application:
   ```bash
   streamlit run main.py
   ```

4. Login with the new team's access code

5. Each team will only see their own documents

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:** 
- Make sure you activated your virtual environment
- Reinstall dependencies: `pip install streamlit google-genai google-generativeai python-dotenv watchdog`

### Problem: "Port 8501 is already in use"

**Solution:**
- Streamlit will automatically use the next available port (8502, 8503, etc.)
- Check the terminal output for the actual URL
- Or stop the other application using port 8501

### Problem: "Invalid access code" error

**Solution:**
- Verify the access code is correct (case-sensitive)
- List teams: `python create_team.py list`
- Create a new team if needed: `python create_team.py`

### Problem: API errors when uploading/summarizing

**Solution:**
- Check if your `GEMINI_API_KEY` is set correctly
- The app has a fallback key, but it may have rate limits
- Set your own API key (see Step 4)

### Problem: Application won't start

**Solution:**
- Make sure you're in the correct directory
- Check Python version: `python --version` (needs 3.11+)
- Verify all files are present (main.py, auth.py, document_store.py, etc.)

---

## Quick Reference Commands

```bash
# Navigate to project
cd C:\Users\vijay\Desktop\Knowledge-Stream

# Activate virtual environment (if using)
.\venv\Scripts\Activate.ps1

# Create a team
python create_team.py

# List teams
python create_team.py list

# Run the application
streamlit run main.py

# Stop the application
Ctrl+C (in terminal)
```

---

## Next Steps

- Upload documents for your team
- Share the access code with team members
- Use the chatbot to ask questions about your documents
- Create separate teams for different groups/projects

---

## Need Help?

- Check the `SETUP.md` file for more detailed information
- Verify all files are in place (main.py, auth.py, document_store.py, team_store.py, etc.)
- Make sure Python 3.11+ is installed
- Ensure all dependencies are installed correctly

