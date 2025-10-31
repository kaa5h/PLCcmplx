# PLC Data Mapping Assistant - PROTOTYPE

> **🎯 This is a DEMO/PROTOTYPE version with simulated matching - No API keys or payment required!**

A web application that demonstrates automated matching of business requirements to PLC tag names using pattern recognition algorithms.

## ✨ Features

- **Pattern Matching**: Smart keyword and abbreviation matching
- **Confidence Scoring**: Each match includes a confidence score (0-100%) with reasoning
- **Alternative Suggestions**: View alternative matches when primary match isn't perfect
- **Export Functionality**: Export validated mappings as CSV or YAML configuration files
- **Sample Datasets**: Pre-loaded examples for instant testing
- **Clean UI**: Simple, intuitive interface built with Bootstrap
- **No API Required**: Works completely offline with no external dependencies

## 🚀 Quick Start (Super Simple!)

### Prerequisites

- Python 3.8 or higher (that's it!)

### Installation & Run

1. **Navigate to the project directory:**
```bash
cd plc-mapper
```

2. **Install dependencies (just Flask and PyYAML):**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Open your browser:**
```
http://localhost:5000
```

5. **Try it out:**
   - Click "Example 1: Circuit Breaker"
   - Click "Analyze Mappings"
   - See the results!

That's it! No API keys, no payment, no complicated setup!

## 📖 Usage

### Input Formats

**Business Requirements** (one per line):
```
Requirement_Name | Description
```
Example:
```
Phase1_Current | Electrical current in Amps for phase 1
Total_Power | Total power consumption in Kilowatts
```

**PLC Tags** (CSV format):
```
TagName, Address, DataType, CurrentValue
```
Example:
```
CP_Ph1_I, DB45.DBD10, Float, 23.4
P_tot, DB45.DBD20, Float, 5.2
```

**Documentation** (optional):
```
Any relevant context, naming conventions, or manual excerpts
```

### Workflow

1. **Input Data**: Paste your business requirements and PLC tags
2. **Add Context** (optional): Provide documentation for better matching
3. **Analyze**: Click "Analyze Mappings" to run pattern matching
4. **Review**: Examine matches, confidence scores, and reasoning
5. **Accept/Adjust**: Accept good matches or view alternatives
6. **Export**: Download CSV or YAML configuration files

## 🔍 How It Works (Mock Algorithm)

The prototype uses a simple but effective pattern matching algorithm:

1. **Keyword Matching**: Direct word matches between requirements and tags
2. **Abbreviation Recognition**: Knows common industrial abbreviations
   - I = Current, V = Voltage, T = Temperature, P = Power, Ph = Phase
3. **Number Matching**: Matches phase numbers (Phase1 → Ph1)
4. **Data Type Checking**: Float for measurements, Boolean for status
5. **Value Range Validation**: Checks if values are reasonable
6. **Confidence Scoring**: Combines all factors into a 0-100% score

## 📊 Sample Data Included

### Example 1: Circuit Breaker Panel
- 4 requirements (Phase currents + Total power)
- 6 PLC tags with various patterns
- Tests multi-phase matching

### Example 2: Temperature Monitoring
- 3 requirements (Ambient, Motor, Oil temps)
- 5 PLC tags with different naming conventions
- Tests abbreviation recognition

## 📁 Project Structure

```
plc-mapper/
├── app.py                 # Flask backend with pattern matching
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend logic
├── requirements.txt      # Just Flask + PyYAML
└── README.md            # This file
```

## 🎓 Common Industrial Abbreviations Recognized

The algorithm recognizes these common patterns:

- **I** = Current (Amps)
- **V** = Voltage (Volts)
- **T** = Temperature (Celsius/Fahrenheit)
- **P** = Power (Watts/Kilowatts)
- **Ph** = Phase
- **Amb** = Ambient
- **THM** = Thermal
- **CP** = Circuit Panel
- **DB** = Data Block
- **Mtr/Mot** = Motor
- **Lvl** = Level
- **Spd** = Speed

## ❓ Troubleshooting

**Port 5000 already in use?**
- Edit `app.py` line 307, change `5000` to another port like `5001`

**Dependencies won't install?**
- Try: `python -m pip install -r requirements.txt`
- Or: `pip3 install -r requirements.txt`

**Can't access http://localhost:5000?**
- Try: `http://127.0.0.1:5000`
- Make sure Flask is still running in the terminal

## 🆚 Prototype vs Production

This is a **PROTOTYPE** to demonstrate the concept.

**For production use, you would want to:**
- Use real AI (like Claude, GPT-4, or local LLMs) for better matching
- Add user authentication
- Store mappings in a database
- Add more sophisticated matching algorithms
- Implement rate limiting
- Use HTTPS

**To upgrade to real AI:**
- See `COST_AND_ALTERNATIVES.md` for options
- Claude API, OpenAI API, or local LLMs
- Better accuracy but requires API costs or powerful hardware

## 💰 Cost

**This prototype: $0** (completely free!)

Just need Python installed. No API keys, no payment, no cloud services.

## 🎯 Perfect For

- **Demos & Presentations**: Show the concept without setup hassle
- **Testing the Workflow**: See if this approach works for your needs
- **Learning**: Understand how PLC tag matching could work
- **Prototyping**: Build on this foundation for custom solutions
- **Offline Use**: Works without internet connection

## ⚡ Performance

- Instant results (no API latency)
- Handles 50+ requirements and 100+ PLC tags easily
- Works on any computer that can run Python
- No external dependencies or network calls

## 🔧 Customization

Want to improve the matching? Edit `app.py`:

- Add more abbreviations to `ABBREVIATIONS` dictionary (line 11)
- Adjust scoring weights in `calculate_match_score()` (line 67)
- Add custom pattern recognition logic
- Modify confidence thresholds

## 📝 License

This is a prototype/demo application for educational and demonstration purposes.

## 🤝 Contributing

This is a simple prototype. Feel free to:
- Fork it
- Improve the matching algorithm
- Add new features
- Share feedback

## 🙋 FAQ

**Q: Is this production-ready?**
A: No, it's a prototype to demonstrate the concept.

**Q: Can I use real AI instead?**
A: Yes! See `COST_AND_ALTERNATIVES.md` for integration options.

**Q: How accurate is the matching?**
A: Decent for simple patterns, but real AI would be much better for complex cases.

**Q: Can I customize it for my industry?**
A: Absolutely! Edit the abbreviations and scoring logic in `app.py`.

**Q: Does it save my data?**
A: No, everything is in-memory. Refresh the page and it's gone.

---

**Ready to try it?**

```bash
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000 and click "Example 1"!
