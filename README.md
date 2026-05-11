# 🚀 GitHub File Uploader Pro

A professional desktop application for uploading files and folders to GitHub repositories with a modern, user-friendly interface.

![GitHub Uploader](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **Modern GUI** - Clean, intuitive interface with progress indicators
- **Batch Upload** - Upload multiple files and folders simultaneously
- **Git Integration** - Automatic git init, add, commit, and push workflow
- **Branch Support** - Upload to any branch (main/master/custom)
- **File Preview** - View file contents before uploading
- **Secure Token Handling** - Masked token input with visibility toggle
- **Cross-Platform** - Works on Windows, macOS, and Linux
- **Standalone Executable** - Build a portable .exe with PyInstaller

## 📋 Requirements

- **Python 3.8+** (for running from source)
- **Git** installed and available in system PATH
- **GitHub Personal Access Token** with `repo` scope

### Getting a GitHub Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Select `repo` scope (full control of private repositories)
4. Copy the generated token (you won't see it again!)

## 🚀 Installation

### Option 1: Run from Source

```bash
# Clone or download this repository
git clone https://github.com/yourusername/GitHub-Uploader.git
cd GitHub-Uploader

# Install dependencies
pip install -r requirements.txt

# Run the application
python uploader.py


------------------------------------------------------------------------


📖 How to Use
Enter Repository URL

Format: https://github.com/username/repository.git

Example: https://github.com/johndoe/my-project.git

Enter Personal Access Token

Paste your GitHub token (will be masked for security)

Click the eye icon to toggle visibility

Write Commit Message

Default message includes timestamp

Customize as needed

Select Branch (Optional)

Default: main

Change to master or any other branch name

Add Files/Folders

Click "Add Files" to select individual files

Click "Add Folder" to upload entire directories

Use "Remove Selected" to delete items from list

Click Upload

Watch progress bar and status updates

Upon success, click "View on GitHub" link in success message

🎯 Use Cases
Quick File Sharing - Share code snippets, configs, or documents

Backup Important Files - Automate backups to private repos

Deploy Static Sites - Upload built websites to GitHub Pages

Team Collaboration - Share resources without CLI complexity

CI/CD Pipeline Support - Integrate into automated workflows

🔧 Troubleshooting
"Git not found" Error
Install Git from git-scm.com

Ensure Git is added to system PATH

Restart the application after installation

Authentication Failed
Verify token has repo scope

Generate a new token if expired

Check that repository URL is correct

Push Failed
Ensure you have write access to repository

Check branch name exists (or will be created)

Try pulling latest changes first

Files Not Showing
Verify file paths are correct

Check file permissions

Ensure files aren't empty or identical

🔐 Security Notes
Tokens are never stored permanently

Temporary files are cleaned up after upload

Use token with minimal required permissions

Consider using environment variables for automation

🛠️ Customization
Command Line Arguments (for automation)
python
# Modify uploader.py to accept CLI arguments
import sys
if len(sys.argv) > 1:
    # Auto-upload with provided arguments
    auto_upload(sys.argv[1], sys.argv[2], sys.argv[3])
Environment Variables Support
python
# Add at the beginning of uploader.py
import os
token = os.environ.get('GITHUB_TOKEN', '')
repo = os.environ.get('GITHUB_REPO', '')
📝 License
MIT License - Free to use, modify, and distribute

🤝 Contributing
Contributions welcome! Please:

Fork the repository

Create a feature branch

Submit a pull request

📧 Support
Open an issue on GitHub

Check troubleshooting section

Review GitHub's documentation on PAT

