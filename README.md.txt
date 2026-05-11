# 🚀 رافع الملفات إلى GitHub – النسخة الاحترافية

تطبيق سطح مكتب بواجهة رسومية (GUI) يسمح لك برفع الملفات والمجلدات إلى مستودعات **GitHub** بضغطة زر، دون الحاجة لاستخدام سطر الأوامر.

## ✨ الميزات

- واجهة مستخدم عصرية وسهلة
- رفع عدة ملفات ومجلدات دفعة واحدة
- دعم رفع إلى أي فرع (branch) في المستودع
- معاينة محتوى الملفات قبل الرفع
- إظهار / إخفاء رمز الوصول (Token) للأمان
- شريط تقدم وحالة تشغيلية
- التعامل مع أخطاء المصادقة والدفع (push)
- إنشاء ملف تنفيذي `.exe` مستقل (لنظام Windows)

## 📋 المتطلبات الأساسية

قبل استخدام التطبيق، تأكد من توفر التالي:

| المتطلب | الوصف |
|---------|-------|
| **Python 3.8+** | مطلوب فقط إذا كنت ستشغل الكود المصدري مباشرة |
| **Git** | يجب تثبيت Git وإضافته إلى متغير البيئة `PATH` |
| **GitHub Token** | رمز وصول شخصي (Personal Access Token) مع صلاحية `repo` |

### 🔑 كيف تحصل على Token من GitHub؟

1. سجل الدخول إلى حسابك في GitHub.
2. اذهب إلى **Settings** ← **Developer settings** ← **Personal access tokens** ← **Tokens (classic)**.
3. اضغط **Generate new token (classic)**.
4. أعطِ التوكن اسماً (مثل `GitHub Uploader`).
5. حدد الصلاحيات: فعل على الأقل **`repo`** (للتحكم الكامل بالمستودعات الخاصة والعامة).
6. اضغط **Generate token** ثم انسخ التوكن فوراً (لن يظهر مرة أخرى).

## 📦 التثبيت والتشغيل

### الطريقة الأولى: تشغيل الكود المصدري (للمطورين)

```bash
# استنساخ المشروع
git clone https://github.com/اسم-المستخدم/GitHub-Uploader.git
cd GitHub-Uploader

# إنشاء بيئة افتراضية (مستحسن)
python -m venv venv
source venv/bin/activate      # في Linux/macOS
venv\Scripts\activate         # في Windows

# تثبيت المكتبات المطلوبة
pip install -r requirements.txt

# تشغيل التطبيق
python src/uploader.py


🖥️ كيفية استخدام التطبيق (خطوة بخطوة)
تشغيل التطبيق
إذا كنت تستخدم الكود المصدري: افتح terminal في مجلد المشروع ونفذ python src/uploader.py.

إذا كنت تستخدم الملف التنفيذي: انقر双击 على uploader.exe.

بعد التشغيل، ستظهر النافذة الرئيسية كما في الصورة أدناه (وصف نصي للأزرار والحقول).

https://via.placeholder.com/650x500?text=%D9%84%D9%82%D8%B7%D8%A9+%D8%B4%D8%A7%D8%B4%D8%A9+%D8%A7%D9%84%D8%AA%D8%B7%D8%A8%D9%8A%D9%82
(يمكنك إضافة صورة حقيقية لاحقاً)

الخطوة 1: إدخال رابط المستودع (Repository URL)
اذهب إلى صفحة المستودع على GitHub.

انسخ رابط المستودع بصيغة HTTPS (مثلاً: https://github.com/username/repo.git).

الصقه في الحقل الأول المسمى Repository URL.

💡 ملاحظة: التطبيق يقبل الرابط مع أو بدون .git في النهاية، وسيتم تنسيقه تلقائياً.

الخطوة 2: إدخال رمز الوصول الشخصي (Personal Access Token)
احصل على توكن كما هو موضح في قسم المتطلبات (صلاحية repo).

الصق التوكن في الحقل الثاني المسمى Personal Access Token.

الحقل مخفي بشكل افتراضي (نجوم). يمكنك الضغط على زر العين 👁️ المجاور لإظهار التوكن والتأكد من كتابته بشكل صحيح.

الخطوة 3: كتابة رسالة الإيداع (Commit Message)
يمكنك ترك النص الافتراضي (Upload files via GitHub Uploader - التاريخ والوقت) أو كتابة رسالة مخصصة توضح التغييرات (مثل: "إضافة ملف الإعدادات").

الحقل موجود أسفل التوكن مباشرة وعنوانه Commit Message.

الخطوة 4: تحديد الفرع المستهدف (اختياري)
إذا كنت تريد رفع الملفات إلى فرع معين غير الفرع الافتراضي (مثل develop أو main) اكتب اسم الفرع في الحقل الرابع Target Git Branch (optional).

إذا تركته فارغاً، سيتعرف التطبيق تلقائياً على الفرع الأساسي للمستودع (main أو master).

الخطوة 5: إضافة الملفات والمجلدات
اضغط على الزر ➕ Add Files لفتح نافذة اختيار الملفات. يمكنك تحديد ملف واحد أو عدة ملفات (باستخدام Ctrl أو Shift).

اضغط على الزر 📂 Add Folder لاختيار مجلد كامل. سيتم نسخ المجلد مع كل محتوياته إلى المستودع.

ستظهر العناصر المضافة في القائمة السفلية. يمكنك:

تحديد عنصر (أو عدة عناصر) والضغط على 🗑 Remove Selected لحذفهم من قائمة الرفع.

الضغط على 🗑 Clear All لحذف كل العناصر دفعة واحدة.

⚠️ ملاحظة: التطبيق يحافظ على هيكل المجلدات. مثلاً، إذا أضفت مجلداً باسم docs وبداخله ملف readme.txt، فسيتم رفعه إلى المستودع بنفس الهيكل docs/readme.txt.

الخطوة 6: (اختياري) معاينة الملفات قبل الرفع
حدد ملفاً (أو عدة ملفات) من القائمة.

اضغط على 📖 Read Selected.

ستظهر نافذة جديدة تعرض محتوى الملف النصي. (إذا كان الملف ثنائياً مثل صورة، ستظهر رسالة "Binary file - cannot display").

هذه الميزة مفيدة للتأكد من أن الملف الصحيح سيتم رفعه.

الخطوة 7: بدء الرفع إلى GitHub
بعد التأكد من إدخال جميع البيانات المطلوبة (رابط، توكن، ملفات)، اضغط على الزر الأخضر الكبير 🚀 UPLOAD TO GITHUB.

سيتحول الماوس إلى رمز انتظار، ويظهر شريط تقدم غير محدد أسفل النافذة مع رسالة "Uploading to GitHub...".

تستغرق العملية بضع ثوانٍ حسب حجم الملفات وسرعة الإنترنت.

الخطوة 8: مراقبة النتيجة
في حال النجاح: يظهر مربع حوار بعنوان "✅ Upload Successful" ويخبرك بعدد العناصر المرفوعة ويعرض رابطاً للمستودع على الفرع المحدد. اضغط OK ثم يمكنك فتح الرابط في المتصفح للتحقق.

في حال الفشل: يظهر مربع حوار "❌ Upload Failed" مع شرح الخطأ (مثلاً: "Authentication failed" أو "Push failed").

بعد إغلاق مربع الحوار، يعود التطبيق إلى وضعه الطبيعي ويمكنك تعديل البيانات والمحاولة مرة أخرى.

نصائح إضافية أثناء الاستخدام
يمكنك تغيير التوكن أو الرابط بين عمليات الرفع دون الحاجة لإعادة تشغيل التطبيق.

تحقق من وجود اتصال بالإنترنت قبل الضغط على Upload.

إذا كانت الملفات كبيرة جداً، قد يستغرق الرفع وقتاً أطول. التطبيق لا يعرض شريط تقدم محدد (غير محدد) لأنه يعتمد على عمليات Git التي لا تعطي نسبة مئوية دقيقة.

بعد الرفع الناجح، يمكنك مسح قائمة الملفات بسهولة بالضغط على "Clear All" لبدء رفعة جديدة.

مثال تطبيقي (سيناريو حقيقي)
لديك مجلد باسم my-website يحتوي على index.html و style.css ومجلد images.

تريد رفع هذا المجلد إلى مستودع فارغ باسم my-project على فرع main.

قم بتشغيل التطبيق.

أدخل الرابط https://github.com/your-username/my-project.git والتوكن.

اكتب رسالة: "إطلاق النسخة الأولى من الموقع".

اترك حقل الفرع فارغاً (سيستخدم main).

اضغط "Add Folder" واختر مجلد my-website.

اضغط "Upload".

بعد النجاح، افتح الرابط https://github.com/your-username/my-project/tree/main وستجد الملفات مرفوعة.




# 🚀 GitHub File Uploader Pro


GitHub-Uploader/
├── .gitignore               # Files/folders ignored by Git
├── LICENSE                  # MIT License
├── README.md                # This file
├── requirements.txt         # Dependencies (PyInstaller, Pillow)
├── setup.py                 # Optional installation script
├── src/
│   └── uploader.py          # Main source code
├── assets/
│   └── icon.ico             # App icon (optional)
└── docs/
    └── usage.md             # Additional documentation (optional)

A professional desktop application (GUI) that allows you to upload files and folders to any GitHub repository with just a few clicks – no command line required.

## ✨ Features

- Modern, intuitive graphical interface
- Upload multiple files and folders at once
- Upload to any branch (main, master, custom)
- Preview file contents before uploading
- Show/hide token for security
- Progress bar and status updates
- Handles authentication and push errors gracefully
- Build a standalone `.exe` for Windows

## 📋 Prerequisites

Before using the application, ensure you have:

| Requirement | Description |
|-------------|-------------|
| **Python 3.8+** | Only needed if running from source code |
| **Git** | Git installed and added to your system `PATH` |
| **GitHub Token** | Personal Access Token (classic) with `repo` scope |

### 🔑 How to Get a GitHub Token

1. Log in to your GitHub account.
2. Go to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**.
3. Click **Generate new token (classic)**.
4. Give it a name (e.g., `GitHub Uploader`).
5. Select scopes: at minimum, check **`repo`** (full control of private repositories).
6. Click **Generate token** and copy it immediately – you won't see it again!

## 📦 Installation & Running

### Option 1: Run from Source (for developers)

```bash
# Clone the repository
git clone https://github.com/your-username/GitHub-Uploader.git
cd GitHub-Uploader

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# Install required packages
pip install -r requirements.txt

# Run the application
python src/uploader.py
🖥️ How to Use the Application (Step-by-Step)
Once you launch the app, you'll see the main window. Follow these steps:

Step 1: Enter the Repository URL
Go to your repository on GitHub.

Copy the HTTPS URL (e.g., https://github.com/username/repo.git).

Paste it into the first field labeled Repository URL.

💡 Note: The URL works with or without the .git suffix.

Step 2: Enter Your Personal Access Token
Obtain a token as described in the prerequisites.

Paste the token into the Personal Access Token field.

The field is masked by default (asterisks). Click the 👁️ icon to reveal the token and verify it is correct.

Step 3: Write a Commit Message
You can keep the default message (Upload files via GitHub Uploader - timestamp) or write a custom one (e.g., "Add configuration files").

The field is labeled Commit Message.

Step 4: Choose a Target Branch (Optional)
If you want to upload to a specific branch other than the default (e.g., develop or main), enter the branch name in the Target Git Branch (optional) field.

Leave it empty to automatically detect the repository’s default branch (usually main or master).

Step 5: Add Files and Folders
Click ➕ Add Files to select individual files (you can select multiple using Ctrl or Shift).

Click 📂 Add Folder to select an entire folder – the whole directory structure will be preserved.

The selected items appear in the list below. You can:

Select one or more items and click 🗑 Remove Selected to remove them.

Click 🗑 Clear All to remove all items at once.

⚠️ Note: The app preserves folder structure. For example, if you add a folder docs containing readme.txt, it will be uploaded as docs/readme.txt.

Step 6: (Optional) Preview Files Before Upload
Select a file (or multiple files) from the list.

Click 📖 Read Selected.

A new window will open showing the file content (text files only; binary files show a message).

This helps you verify that you are uploading the correct files.

Step 7: Start the Upload
Double-check that you have entered the repository URL, token, and at least one file/folder.

Click the big green button 🚀 UPLOAD TO GITHUB.

The mouse cursor will change to a wait icon, and an indeterminate progress bar will appear with the message "Uploading to GitHub...".

Step 8: Check the Result
If successful: A dialog titled "✅ Upload Successful" shows the number of uploaded items and provides a link to the repository (on the selected branch). Click OK, then you can open the link in your browser to verify.

If failed: A dialog "❌ Upload Failed" explains the error (e.g., authentication failed, push conflict, etc.).

After closing the dialog, the app resets and you can modify the inputs and try again.

Additional Tips
You can change the token or URL between uploads without restarting the app.

Make sure you have an active internet connection before clicking Upload.

For very large files, the upload may take longer. The progress bar is indeterminate because Git does not provide a percentage.

After a successful upload, you can click "Clear All" to start a fresh upload list.

Real-World Example
You have a folder named my-website containing index.html, style.css, and an images subfolder.

You want to upload this entire folder to an empty repository called my-project on the main branch.

Launch the app.

Enter the URL https://github.com/your-username/my-project.git and your token.

Write commit message: "Initial website release".

Leave the branch field empty (defaults to main).

Click "Add Folder" and select the my-website folder.

Click "Upload".

After success, open the provided link: https://github.com/your-username/my-project/tree/main – you will see all your files uploaded.
