# Quick Start Cheat Sheet

## 📋 Prerequisites
- [ ] Python 3.8+ installed
- [ ] Anthropic API key (get from https://console.anthropic.com/)

---

## 🚀 5-Minute Setup

### 1️⃣ Open Terminal/Command Prompt

**Windows**: Press `Win+R`, type `cmd`, press Enter
**Mac**: Press `Cmd+Space`, type `terminal`, press Enter
**Linux**: Press `Ctrl+Alt+T`

---

### 2️⃣ Navigate to Project

```bash
cd PLCcmplx/plc-mapper
```

---

### 3️⃣ Install Dependencies

**Windows**:
```bash
pip install -r requirements.txt
```

**Mac/Linux**:
```bash
pip3 install -r requirements.txt
```

---

### 4️⃣ Set API Key

**Windows**:
```bash
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Mac/Linux**:
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

---

### 5️⃣ Run Application

**Windows**:
```bash
python app.py
```

**Mac/Linux**:
```bash
python3 app.py
```

---

### 6️⃣ Open Browser

Go to: **http://localhost:5000**

---

## 🎯 How to Use

1. Click **"Example 1: Circuit Breaker"** to load sample data
2. Click **"Analyze Mappings"** (wait 10-30 seconds)
3. Review results with confidence scores
4. Click **"✓ Accept"** on good matches
5. Click **"Export as CSV"** to download results

---

## 🛑 How to Stop

In terminal window: Press **Ctrl+C**

---

## 📝 Input Formats

**Business Requirements** (one per line):
```
Name | Description
Phase1_Current | Electrical current in Amps for phase 1
```

**PLC Tags** (CSV format):
```
TagName, Address, DataType, CurrentValue
CP_Ph1_I, DB45.DBD10, Float, 23.4
```

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| API key error | Re-run Step 4 with correct key |
| Port 5000 in use | Change port in app.py line 280 |
| pip not found | Use `python -m pip` instead |
| Cannot connect | Make sure app is still running |

---

## 🔄 Next Time You Run It

You only need to repeat steps 4 and 5:

```bash
# Set API key (every new terminal session)
export ANTHROPIC_API_KEY='your-key'  # Mac/Linux
set ANTHROPIC_API_KEY=your-key       # Windows

# Run app
python3 app.py  # Mac/Linux
python app.py   # Windows
```

---

## 💡 Tips

- Don't close the terminal while using the app
- API key is session-specific (set it every time)
- Each analysis costs ~$0.01-0.05 in API credits
- Try the examples first before using your own data
- Add documentation context for better matches

---

## 📁 Project Structure

```
plc-mapper/
├── app.py              ← Flask backend
├── templates/
│   └── index.html     ← Web interface
├── static/
│   ├── style.css      ← Styling
│   └── script.js      ← Frontend logic
└── requirements.txt   ← Dependencies
```

---

## 📞 Get Help

- Read **GETTING_STARTED.md** for detailed guide
- Read **README.md** for technical details
- Check Anthropic docs: https://docs.anthropic.com/
