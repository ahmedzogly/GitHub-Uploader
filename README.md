# 🚀 GitHub File Uploader Pro

A professional desktop application for uploading files and folders to GitHub repositories with a modern and user-friendly interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![GitHub](https://img.shields.io/badge/GitHub-API-black.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

---

# ✨ Features

- 🎨 Modern and clean GUI
- 📂 Upload files and folders easily
- ⚡ Batch upload support
- 🔄 Automatic Git workflow
  - `git init`
  - `git add`
  - `git commit`
  - `git push`
- 🌿 Multi-branch support
- 👀 File preview before upload
- 🔐 Secure GitHub token handling
- 🖥️ Cross-platform support
- 📦 Build standalone executable using PyInstaller
- 📊 Progress bar and upload status tracking
- 🔗 Direct GitHub repository access after upload

---

# 📸 Preview

> Add screenshots of the application here

```bash
assets/
├── preview1.png
├── preview2.png
└── preview3.png
```

---

# 📋 Requirements

- Python 3.8+
- Git installed and added to PATH
- GitHub Personal Access Token (PAT)

---

# 🔑 Getting a GitHub Token

1. Open GitHub Settings
2. Go to:
   - `Developer settings`
   - `Personal access tokens`
   - `Tokens (classic)`
3. Click:
   - `Generate new token (classic)`
4. Enable:
   - ✅ `repo`
5. Copy the token safely

⚠️ GitHub will only show the token once.

---

# 🚀 Installation

## Option 1 — Run From Source

```bash
# Clone repository
git clone https://github.com/yourusername/GitHub-Uploader.git

# Open project
cd GitHub-Uploader

# Install dependencies
pip install -r requirements.txt

# Run application
python src/uploader.py
```

---

## Option 2 — Build Executable (.exe)

```bash
pip install pyinstaller

pyinstaller --onefile --windowed --icon=assets/icon.ico src/uploader.py
```

Generated executable will be located in:

```bash
dist/
```

---

# 📖 How To Use

## 1️⃣ Enter Repository URL

Example:

```bash
https://github.com/username/repository.git
```

---

## 2️⃣ Enter GitHub Token

- Paste your Personal Access Token
- Token field is masked automatically
- Click 👁️ to show/hide token

---

## 3️⃣ Write Commit Message

Example:

```bash
Initial upload
```

Default commit message includes timestamp automatically.

---

## 4️⃣ Select Branch

Default branch:

```bash
main
```

You can also use:

```bash
master
development
feature/new-ui
```

---

## 5️⃣ Add Files or Folders

- 📄 Add individual files
- 📁 Add complete folders
- ❌ Remove selected items anytime

---

## 6️⃣ Click Upload

The application will:

```bash
git init
git add .
git commit -m "message"
git push
```

You can monitor:
- Upload progress
- Git status
- Success/error logs

---

# 🎯 Use Cases

## 🚀 Quick File Sharing

Upload projects instantly without terminal commands.

---

## 💾 Backup Important Files

Store local files securely in private repositories.

---

## 🌐 Deploy Static Websites

Upload:
- HTML
- CSS
- JS
- React/Vue build folders

Directly to GitHub Pages repositories.

---

## 👥 Team Collaboration

Share resources with teammates easily.

---

## ⚙️ CI/CD Support

Can be integrated into automation workflows.

---

# 🛠️ Technologies Used

- Python
- Tkinter / CustomTkinter
- Git CLI
- GitHub
- PyInstaller
- Pillow

---

# 📂 Project Structure

```bash
GitHub-Uploader/
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
│
├── src/
│   └── uploader.py
│
├── assets/
│   └── icon.ico
│
└── docs/
    └── usage.md
```

---

# 📦 requirements.txt

```txt
customtkinter
pillow
pyinstaller
```

---

# ⚠️ Troubleshooting

## ❌ Git Not Found

### Solution

Install Git from:

```bash
https://git-scm.com/
```

Then:
- Add Git to PATH
- Restart application

---

## ❌ Authentication Failed

### Solution

- Verify token permissions
- Ensure `repo` scope is enabled
- Generate a new token if expired

---

## ❌ Push Failed

### Solution

- Verify repository access
- Ensure branch exists
- Pull latest changes first

---

## ❌ Files Not Uploading

### Solution

- Check file permissions
- Ensure files exist
- Verify paths are correct

---

# 🔐 Security Notes

- Tokens are never stored permanently
- Temporary files are removed automatically
- Sensitive fields are masked
- Recommended to use environment variables for automation

---

# 🌍 Environment Variables Support

```python
import os

token = os.environ.get("GITHUB_TOKEN", "")
repo = os.environ.get("GITHUB_REPO", "")
```

---

# ⚡ Automation Support

Example CLI automation:

```python
import sys

if len(sys.argv) > 1:
    auto_upload(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3]
    )
```

---

# 🧩 Future Improvements

- Drag & Drop support
- Dark/Light mode toggle
- Multi-repository upload
- GitHub Actions integration
- Release management
- Commit history viewer
- Upload scheduling

---

# 🤝 Contributing

Contributions are welcome.

## Steps

1. Fork the repository
2. Create feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added feature"
```

4. Push branch

```bash
git push origin feature-name
```

5. Open Pull Request

---

# 📧 Support

If you encounter any issue:

- Open a GitHub issue
- Review troubleshooting section
- Check GitHub documentation

---

# ⭐ Show Your Support

If you like this project:

⭐ Star the repository  
🍴 Fork the project  
🛠️ Contribute improvements

---

# 📜 License

MIT License

```text
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software
and associated documentation files (the "Software"),
to deal in the Software without restriction,
including without limitation the rights to use,
copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software.
```

---

# 👨‍💻 Author

Developed with ❤️ by Your Name

GitHub:
```bash
https://github.com/yourusername
```

---

# 🔥 Final Notes

GitHub File Uploader Pro is designed to simplify GitHub uploads for developers, freelancers, teams, and beginners who prefer a graphical interface instead of terminal commands.

Enjoy fast, secure, and professional GitHub uploads 🚀
