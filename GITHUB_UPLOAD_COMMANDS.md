# 🚀 Exact Commands to Upload to GitHub

## Step 1: Configure Git (Replace with YOUR information)

Copy and paste these commands one by one. **Replace the placeholder information with your actual details**:

```bash
# Configure your name (replace with your actual name)
git config --global user.name "Your Full Name"

# Configure your email (replace with your GitHub email)
git config --global user.email "your.email@example.com"

# Set default branch name to main
git config --global init.defaultBranch main
```

## Step 2: Initialize Git Repository

Run these commands in your terminal from the research_ai folder:

```bash
# Navigate to your project folder
cd /Users/suprithreddy/Desktop/research_ai

# Initialize git repository
git init

# Add remote repository (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-research-platform.git
```

## Step 3: Prepare Files for Upload

```bash
# Create .gitignore file to exclude sensitive files
echo ".env" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".DS_Store" >> .gitignore

# Add all files except those in .gitignore
git add .

# Check what files will be uploaded (review this list)
git status
```

## Step 4: Make First Commit

```bash
# Create your first commit
git commit -m "Initial upload of AI Research Platform for Akcero hackathon

Features:
- Multi-agent AI research system
- Real-time web scraping with 50+ sources
- Professional PDF reports with citations
- Horizontal dashboard interface
- Performance optimized (80% speed improvement)
- Complete documentation (30,000+ words)

Ready for deployment and hackathon submission."
```

## Step 5: Push to GitHub (with Authentication)

When you run this command, it will ask for your username and password:

```bash
# Push to GitHub
git push -u origin main
```

**When prompted:**
- **Username**: Your GitHub username
- **Password**: **USE YOUR PERSONAL ACCESS TOKEN** (not your GitHub password!)
  - Paste the token you created: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Alternative: Set up Token Authentication (Recommended)

To avoid entering credentials every time:

```bash
# Store your credentials (replace with your actual username and token)
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/ai-research-platform.git

# Now push without being prompted for credentials
git push -u origin main
```

**Example** (replace with your actual details):
```bash
git remote set-url origin https://johndoe:ghp_1234567890abcdef@github.com/johndoe/ai-research-platform.git
```

## Step 6: Verify Upload

```bash
# Check that everything was uploaded
git log --oneline

# Check remote connection
git remote -v
```

## 🔧 Troubleshooting

### If you get "Permission denied":
- Make sure your Personal Access Token has `repo` permissions
- Check that your username and token are correct
- Make sure the repository name matches exactly

### If you get "Repository not found":
- Verify your GitHub username is correct
- Make sure the repository name is `ai-research-platform`
- Ensure the repository is public

### If git push fails:
```bash
# If there are conflicts, force push (only for initial upload)
git push -u origin main --force
```

## ✅ Final Verification

1. Go to `https://github.com/YOUR_USERNAME/ai-research-platform`
2. Check that all these files are there:
   - ✅ ai_research_workspace.py
   - ✅ enhanced_display_functions.py
   - ✅ requirements.txt
   - ✅ README.md
   - ✅ HACKATHON_DOCUMENTATION.md
   - ✅ research_workspace/ folder
   - ✅ shared/ folder
   - ✅ .streamlit/ folder
   - ❌ .env (should NOT be there)

3. Repository should be **Public** and accessible to anyone

## 🎯 What to do after upload:

Once uploaded successfully, you can proceed to:
1. Deploy to Streamlit Cloud (share.streamlit.io)
2. Add your API keys in Streamlit secrets
3. Get your live demo URL
4. Submit for hackathon

Your repository URL will be: `https://github.com/YOUR_USERNAME/ai-research-platform`