# 🚀 Installation Guide

## The Easy Way (One-Click Install)

### Windows Users

1. **Double-click this file:**
   ```
   INSTALL_AND_SETUP.bat
   ```

2. **Wait 2-3 minutes** while it:
   - Checks for Python (guides you if missing)
   - Installs all required packages
   - Creates a desktop shortcut
   - Launches the app

3. **Done!** Use the desktop shortcut to open the app anytime.

---

### Mac/Linux Users

1. **Open Terminal** in this folder

2. **Run the installer:**
   ```bash
   chmod +x INSTALL_AND_SETUP.sh
   ./INSTALL_AND_SETUP.sh
   ```

3. **Wait 2-3 minutes** for installation

4. **Done!** Run the app with:
   ```bash
   ./launcher.sh
   ```

---

## What Gets Installed

The installer will install these Python packages:
- **PyQt6** - Desktop GUI framework (~40MB)
- **aiohttp** - Async HTTP client
- **pyyaml** - Configuration parser
- **python-dotenv** - Environment variables

**Total download:** ~50MB  
**Installation time:** 1-2 minutes

### Optional Blockchain Dependencies (NOT Required for Demo Mode)

The following packages are **NOT installed by default** because they require C++ build tools and are only needed for future real trading mode:
- **py-clob-client** - Polymarket SDK
- **web3** - Blockchain library

To install these later (if needed):
```bash
pip install -r requirements-blockchain.txt
```

**Note:** This requires C++ build tools on your system.

---

## Troubleshooting

### Windows: "Python is not installed"

The installer will detect this and open the Python download page.

**Steps:**
1. Download Python 3.11+ from python.org
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Run `INSTALL_AND_SETUP.bat` again

### Windows: Script won't run

**Solution:**
- Right-click `INSTALL_AND_SETUP.bat`
- Select "Run as Administrator"

### Mac/Linux: Permission denied

**Solution:**
```bash
chmod +x INSTALL_AND_SETUP.sh
./INSTALL_AND_SETUP.sh
```

### Installation fails

**Try manual installation:**
```bash
# Windows
pip install -r requirements.txt

# Mac/Linux
pip3 install -r requirements.txt
```

---

## After Installation

### Windows
- Use the desktop shortcut: "Polymarket Arbitrage Bot"
- Or double-click `launcher.bat`

### Mac/Linux
- Run: `./launcher.sh`
- Or use desktop shortcut if created

---

## Uninstall

To remove the application:

1. Delete this folder
2. Delete the desktop shortcut
3. (Optional) Uninstall Python packages:
   ```bash
   pip uninstall PyQt6 aiohttp pyyaml python-dotenv
   ```

---

## Need More Help?

Read the full documentation in `README.md`
