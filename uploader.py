import os
import sys
import shutil
import subprocess
import tempfile
import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import threading
from datetime import datetime

def run_git_command(args, cwd, timeout=60):
    """Run a git command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def validate_repo_url(repo_url):
    """Validate GitHub repository URL format."""
    patterns = [
        r'^https://github\.com/[\w.-]+/[\w.-]+\.git$',
        r'^https://github\.com/[\w.-]+/[\w.-]+$',
        r'^git@github\.com:[\w.-]+/[\w.-]+\.git$',
    ]
    return any(re.match(pattern, repo_url) for pattern in patterns)

def extract_repo_info(repo_url):
    """Extract owner and repo name from URL."""
    # Remove .git suffix if present
    url = repo_url.rstrip('/')
    if url.endswith('.git'):
        url = url[:-4]
    
    # Handle HTTPS URLs
    if url.startswith('https://github.com/'):
        parts = url.replace('https://github.com/', '').split('/')
        if len(parts) >= 2:
            return parts[0], parts[1]
    
    # Handle SSH URLs
    if url.startswith('git@github.com:'):
        parts = url.replace('git@github.com:', '').split('/')
        if len(parts) >= 2:
            return parts[0], parts[1]
    
    return None, None

def upload_files(repo_url, token, commit_msg, file_paths, branch_name=None):
    """Upload files to GitHub repository."""
    
    # Validate repository URL
    if not validate_repo_url(repo_url):
        # Try to auto-correct common issues
        if 'github.com' in repo_url and not repo_url.endswith('.git'):
            repo_url = repo_url + '.git'
            if not validate_repo_url(repo_url):
                return False, "Invalid repository URL format. Use: https://github.com/username/repo.git"
    
    # Build authenticated URL
    if repo_url.startswith("https://"):
        # Remove any existing token from URL
        clean_url = re.sub(r'https://[^@]*@', 'https://', repo_url)
        auth_url = clean_url.replace("https://", f"https://{token}@")
    else:
        auth_url = repo_url
    
    # Create a temporary directory to stage the files
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        # Copy selected files/folders into the temp directory
        copied_count = 0
        for path_str in file_paths:
            src = Path(path_str)
            if not src.exists():
                continue
                
            try:
                if src.is_file():
                    shutil.copy2(src, temp_dir / src.name)
                    copied_count += 1
                elif src.is_dir():
                    dest = temp_dir / src.name
                    shutil.copytree(src, dest)
                    copied_count += 1
            except Exception as e:
                print(f"Error copying {src}: {e}")
        
        if copied_count == 0:
            return False, "No valid files or folders to upload."
        
        # Initialize git repo
        rc, out, err = run_git_command(["init"], cwd=temp_dir)
        if rc != 0:
            raise RuntimeError(f"git init failed: {err}")
        
        # Configure git user (use temporary config)
        run_git_command(["config", "user.name", "GitHub Uploader"], cwd=temp_dir)
        run_git_command(["config", "user.email", "uploader@github.com"], cwd=temp_dir)
        
        # Add remote
        rc, out, err = run_git_command(["remote", "add", "origin", auth_url], cwd=temp_dir)
        if rc != 0:
            raise RuntimeError(f"git remote add failed: {err}")
        
        # Add all files
        rc, out, err = run_git_command(["add", "."], cwd=temp_dir)
        if rc != 0:
            raise RuntimeError(f"git add failed: {err}")
        
        # Check if there's anything to commit
        rc, out, err = run_git_command(["status", "--porcelain"], cwd=temp_dir)
        if rc != 0 or not out:
            return False, "No changes to commit. Files might be identical or empty."
        
        # Commit
        rc, out, err = run_git_command(["commit", "-m", commit_msg], cwd=temp_dir)
        if rc != 0:
            raise RuntimeError(f"git commit failed: {err}")
        
        # Determine target branch
        if branch_name:
            branch = branch_name
        else:
            # Try to fetch remote branches first
            run_git_command(["fetch", "origin"], cwd=temp_dir)
            
            # Check default branch
            rc, out, err = run_git_command(["remote", "show", "origin"], cwd=temp_dir)
            if "HEAD branch:" in out:
                branch = out.split("HEAD branch:")[1].split()[0]
            else:
                branch = "main"  # Default to main
        
        # Push to remote
        rc, out, err = run_git_command(
            ["push", "-u", "origin", f"HEAD:{branch}"], cwd=temp_dir
        )
        if rc != 0:
            if "authentication" in err.lower() or "403" in err:
                raise RuntimeError("Authentication failed. Check your Personal Access Token.")
            elif "non-fast-forward" in err:
                # Try to pull first
                run_git_command(["pull", "origin", branch, "--rebase"], cwd=temp_dir)
                rc, out, err = run_git_command(["push", "-u", "origin", f"HEAD:{branch}"], cwd=temp_dir)
                if rc != 0:
                    raise RuntimeError(f"Push failed after rebase: {err}")
            else:
                raise RuntimeError(f"git push failed: {err}")
        
        owner, repo = extract_repo_info(repo_url)
        if owner and repo:
            github_url = f"https://github.com/{owner}/{repo}/tree/{branch}"
            return True, f"Successfully uploaded {copied_count} item(s) to:\n{github_url}"
        else:
            return True, f"Successfully uploaded {copied_count} item(s) to {repo_url} (branch {branch})."
            
    except Exception as e:
        return False, f"Upload failed: {str(e)}"
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

class ModernProgressBar(ttk.Progressbar):
    """Custom progress bar with better styling."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(mode='indeterminate')

class UploaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GitHub File Uploader Pro")
        self.geometry("650x600")
        self.resizable(True, True)
        self.minsize(550, 500)
        
        # Configure styles
        self.configure(bg='#f0f0f0')
        self.setup_styles()
        
        # Create main container with scrollbar
        self.main_container = tk.Frame(self, bg='#f0f0f0')
        self.main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Create canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(self.main_container, bg='#f0f0f0', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f0f0f0')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        self.bind_mousewheel()
        
        # Build UI in scrollable frame
        self.build_ui()
        
        # Store current upload thread
        self.upload_thread = None
        
    def setup_styles(self):
        """Setup ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), background='#f0f0f0')
        style.configure('Info.TLabel', font=('Arial', 9), background='#f0f0f0', foreground='#666')
        style.configure('Success.TButton', font=('Arial', 10, 'bold'))
        
    def bind_mousewheel(self):
        """Bind mouse wheel for scrolling."""
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        
    def build_ui(self):
        """Build the complete user interface."""
        row = 0
        padx_val = 10
        pady_val = 8
        
        # Title
        title_label = ttk.Label(self.scrollable_frame, text="🚀 GitHub File Uploader Pro", 
                                style='Title.TLabel')
        title_label.grid(row=row, column=0, columnspan=2, pady=(0, 15), sticky='w')
        row += 1
        
        # Repository URL
        ttk.Label(self.scrollable_frame, text="Repository URL:", font=('Arial', 10, 'bold'))\
            .grid(row=row, column=0, sticky='w', padx=padx_val, pady=pady_val)
        
        self.repo_entry = ttk.Entry(self.scrollable_frame, width=60, font=('Arial', 10))
        self.repo_entry.grid(row=row, column=1, sticky='ew', padx=padx_val, pady=pady_val)
        self.repo_entry.insert(0, "https://github.com/username/repository.git")
        
        ttk.Label(self.scrollable_frame, text="Example: https://github.com/username/repo.git", 
                  style='Info.TLabel').grid(row=row+1, column=1, sticky='w', padx=padx_val)
        row += 2
        
        # Personal Access Token
        ttk.Label(self.scrollable_frame, text="Personal Access Token:", font=('Arial', 10, 'bold'))\
            .grid(row=row, column=0, sticky='w', padx=padx_val, pady=pady_val)
        
        token_frame = tk.Frame(self.scrollable_frame, bg='#f0f0f0')
        token_frame.grid(row=row, column=1, sticky='ew', padx=padx_val, pady=pady_val)
        
        self.token_entry = ttk.Entry(token_frame, show="*", width=50, font=('Arial', 10))
        self.token_entry.pack(side='left', fill='x', expand=True)
        
        self.show_token_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(token_frame, text="👁", variable=self.show_token_var, 
                       command=self.toggle_token_visibility, width=3)\
            .pack(side='right', padx=(5, 0))
        
        ttk.Label(self.scrollable_frame, 
                  text="Generate token at: Settings → Developer settings → Personal access tokens → Tokens (classic)\nRequired scope: 'repo'",
                  style='Info.TLabel').grid(row=row+1, column=1, sticky='w', padx=padx_val)
        row += 2
        
        # Commit Message
        ttk.Label(self.scrollable_frame, text="Commit Message:", font=('Arial', 10, 'bold'))\
            .grid(row=row, column=0, sticky='w', padx=padx_val, pady=pady_val)
        
        self.msg_entry = ttk.Entry(self.scrollable_frame, width=60, font=('Arial', 10))
        self.msg_entry.grid(row=row, column=1, sticky='ew', padx=padx_val, pady=pady_val)
        self.msg_entry.insert(0, f"Upload files via GitHub Uploader - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        row += 1
        
        # Target Branch
        ttk.Label(self.scrollable_frame, text="Target Branch (optional):", font=('Arial', 10, 'bold'))\
            .grid(row=row, column=0, sticky='w', padx=padx_val, pady=pady_val)
        
        self.branch_entry = ttk.Entry(self.scrollable_frame, width=60, font=('Arial', 10))
        self.branch_entry.grid(row=row, column=1, sticky='ew', padx=padx_val, pady=pady_val)
        self.branch_entry.insert(0, "main")
        row += 1
        
        # Separator
        ttk.Separator(self.scrollable_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, 
                                                                       sticky='ew', pady=15)
        row += 1
        
        # Files/Folders Section
        ttk.Label(self.scrollable_frame, text="📁 Files & Folders to Upload:", font=('Arial', 10, 'bold'))\
            .grid(row=row, column=0, columnspan=2, sticky='w', padx=padx_val, pady=pady_val)
        row += 1
        
        # Listbox with scrollbar
        list_frame = tk.Frame(self.scrollable_frame, bg='#f0f0f0')
        list_frame.grid(row=row, column=0, columnspan=2, sticky='ew', padx=padx_val, pady=pady_val)
        
        self.file_listbox = tk.Listbox(list_frame, height=8, width=70, selectmode=tk.EXTENDED,
                                       font=('Arial', 9), bg='white', fg='black')
        self.file_listbox.pack(side='left', fill='both', expand=True)
        
        list_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        list_scrollbar.pack(side='right', fill='y')
        self.file_listbox.configure(yscrollcommand=list_scrollbar.set)
        row += 1
        
        # File action buttons
        btn_frame = tk.Frame(self.scrollable_frame, bg='#f0f0f0')
        btn_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="➕ Add Files", command=self.add_files, width=15)\
            .pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📂 Add Folder", command=self.add_folder, width=15)\
            .pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑 Remove Selected", command=self.remove_selected, width=15)\
            .pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📖 Read Selected", command=self.read_files, width=15)\
            .pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑 Clear All", command=self.clear_all, width=15)\
            .pack(side='left', padx=5)
        row += 1
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(self.scrollable_frame, textvariable=self.progress_var, 
                                        style='Info.TLabel')
        self.progress_label.grid(row=row, column=0, columnspan=2, sticky='w', padx=padx_val, pady=(10, 5))
        row += 1
        
        self.progress = ttk.Progressbar(self.scrollable_frame, orient="horizontal", 
                                        mode="indeterminate", length=400)
        self.progress.grid(row=row, column=0, columnspan=2, sticky='ew', padx=padx_val, pady=pady_val)
        row += 1
        
        # Upload button
        self.upload_btn = ttk.Button(self.scrollable_frame, text="🚀 UPLOAD TO GITHUB", 
                                     command=self.start_upload, style='Success.TButton')
        self.upload_btn.grid(row=row, column=0, columnspan=2, pady=20)
        
        # Status bar
        self.status_var = tk.StringVar(value="✅ Ready to upload")
        status_bar = ttk.Label(self.scrollable_frame, textvariable=self.status_var, 
                               relief='sunken', anchor='w')
        status_bar.grid(row=row+1, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        
        # Configure grid weights
        self.scrollable_frame.columnconfigure(1, weight=1)
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(0, weight=1)
        
    def toggle_token_visibility(self):
        """Toggle visibility of token entry."""
        if self.show_token_var.get():
            self.token_entry.configure(show="")
        else:
            self.token_entry.configure(show="*")
            
    def add_files(self):
        """Add files to upload list."""
        paths = filedialog.askopenfilenames(title="Select files to upload")
        for p in paths:
            if p not in self.file_listbox.get(0, tk.END):
                self.file_listbox.insert(tk.END, p)
        self.update_status(f"Added {len(paths)} file(s)")
        
    def add_folder(self):
        """Add folder to upload list."""
        path = filedialog.askdirectory(title="Select folder to upload")
        if path and path not in self.file_listbox.get(0, tk.END):
            self.file_listbox.insert(tk.END, path)
            self.update_status(f"Added folder: {os.path.basename(path)}")
            
    def remove_selected(self):
        """Remove selected items from list."""
        selected = self.file_listbox.curselection()
        for idx in reversed(selected):
            self.file_listbox.delete(idx)
        self.update_status(f"Removed {len(selected)} item(s)")
        
    def clear_all(self):
        """Clear all items from list."""
        if messagebox.askyesno("Clear All", "Remove all items from upload list?"):
            self.file_listbox.delete(0, tk.END)
            self.update_status("Cleared all items")
            
    def start_upload(self):
        """Start upload process in separate thread."""
        repo = self.repo_entry.get().strip()
        token = self.token_entry.get().strip()
        msg = self.msg_entry.get().strip()
        files = list(self.file_listbox.get(0, tk.END))
        branch = self.branch_entry.get().strip()
        
        # Validate inputs
        if not repo:
            messagebox.showerror("Missing Information", "Please enter repository URL")
            return
        if not token:
            messagebox.showerror("Missing Information", "Please enter your Personal Access Token")
            return
        if not files:
            messagebox.showerror("Missing Information", "Please select at least one file or folder")
            return
        if not msg:
            msg = f"Upload via GitHub Uploader - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
        # Validate repository URL format
        if not validate_repo_url(repo):
            if not messagebox.askyesno("Invalid URL Format", 
                                       "The repository URL format seems incorrect.\n"
                                       "Should be like: https://github.com/username/repo.git\n\n"
                                       "Continue anyway?"):
                return
        
        # Disable UI and start upload
        self.disable_ui()
        self.start_progress("Uploading to GitHub...")
        
        # Run upload in thread to prevent UI freezing
        self.upload_thread = threading.Thread(
            target=self.upload_worker,
            args=(repo, token, msg, files, branch),
            daemon=True
        )
        self.upload_thread.start()
        
    def upload_worker(self, repo, token, msg, files, branch):
        """Worker function for upload process."""
        try:
            success, info = upload_files(repo, token, msg, files, branch)
            self.after(0, self.upload_complete, success, info)
        except Exception as e:
            self.after(0, self.upload_complete, False, str(e))
            
    def upload_complete(self, success, info):
        """Handle upload completion."""
        self.stop_progress()
        self.enable_ui()
        
        if success:
            messagebox.showinfo("✅ Upload Successful", info)
            self.update_status("Upload completed successfully!")
            # Optionally clear files list after successful upload
            if messagebox.askyesno("Clear List", "Clear uploaded files from list?"):
                self.clear_all()
        else:
            messagebox.showerror("❌ Upload Failed", info)
            self.update_status("Upload failed. Check error message for details.")
            
    def disable_ui(self):
        """Disable UI elements during upload."""
        self.upload_btn.config(state='disabled')
        for child in self.scrollable_frame.winfo_children():
            if isinstance(child, (ttk.Entry, ttk.Button, tk.Listbox, ttk.Checkbutton)):
                try:
                    child.configure(state='disabled')
                except:
                    pass
                    
    def enable_ui(self):
        """Enable UI elements after upload."""
        self.upload_btn.config(state='normal')
        for child in self.scrollable_frame.winfo_children():
            if isinstance(child, (ttk.Entry, ttk.Button, tk.Listbox, ttk.Checkbutton)):
                try:
                    child.configure(state='normal')
                except:
                    pass
                    
    def start_progress(self, message="Processing..."):
        """Start progress bar with message."""
        self.progress_var.set(message)
        self.progress.start()
        
    def stop_progress(self):
        """Stop progress bar."""
        self.progress.stop()
        self.progress_var.set("Ready")
        
    def update_status(self, message):
        """Update status bar message."""
        self.status_var.set(f"📌 {message}")
        
    def read_files(self):
        """Read and display contents of selected files."""
        selected = self.file_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one file to read.")
            return
            
        content = ""
        for idx in selected:
            path = self.file_listbox.get(idx)
            if os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                        # Truncate very long files
                        if len(file_content) > 10000:
                            file_content = file_content[:10000] + "\n... (truncated)"
                    content += f"{'='*60}\n📄 {path}\n{'='*60}\n{file_content}\n\n"
                except UnicodeDecodeError:
                    content += f"{'='*60}\n📄 {path}\n{'='*60}\n[Binary file - cannot display]\n\n"
                except Exception as e:
                    content += f"{'='*60}\n📄 {path}\n{'='*60}\nError reading file: {e}\n\n"
            else:
                content += f"{'='*60}\n📁 {path}\n{'='*60}\n[Directory - cannot display contents]\n\n"
        
        # Create display window
        win = tk.Toplevel(self)
        win.title("File Viewer")
        win.geometry("800x600")
        
        # Add text widget with scrollbar
        text_frame = tk.Frame(win)
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        text_widget = tk.Text(text_frame, wrap='word', font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        text_widget.insert('1.0', content)
        text_widget.configure(state='disabled')  # Make read-only

if __name__ == "__main__":
    # Check for Git availability
    if shutil.which("git") is None:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Git Not Found", 
            "Git executable not found in PATH.\n\n"
            "Please install Git from: https://git-scm.com/downloads\n\n"
            "After installation, restart this application."
        )
        sys.exit(1)
    
    # Create and run application
    app = UploaderApp()
    app.mainloop()