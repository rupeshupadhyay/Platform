
# 🐍 PYTHON VIRTUAL ENVIRONMENT + PIP UPGRADE COMMANDS
# =====================================================

# 1️⃣ Check Python version
python --version

# 2️⃣ Create a virtual environment (folder name: venv)
python -m venv venv

# 3️⃣ Activate the virtual environment
# 👉 Windows:
venv\Scripts\activate
# 👉 macOS / Linux:
# source venv/bin/activate

# 4️⃣ Check pip version
pip --version

# 5️⃣ Upgrade pip to the latest version
python -m pip install --upgrade pip

# 6️⃣ Verify pip version after upgrade
pip --version

# 7️⃣ Install your required packages inside venv
pip install fastapi
pip install requests

# 8️⃣ Freeze (export) current dependencies
pip freeze > requirements.txt

# 9️⃣ Install dependencies from file (if available)
pip install -r requirements.txt

# 🔟 Deactivate virtual environment
deactivate

# ✅ OPTIONAL: Check outdated packages
pip list --outdated

# ✅ OPTIONAL: Upgrade a specific package
pip install --upgrade <package-name>

# ✅ Run Application
uvicorn app.main:app --reload

# ✅ find running port and terminating process
netstat -ano | findstr :8000
taskkill /PID 11204 /F