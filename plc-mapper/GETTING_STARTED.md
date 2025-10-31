# Getting Started - Complete Beginner's Guide

This guide will walk you through running the PLC Data Mapping Assistant step-by-step, even if you've never done this before.

## Step 1: Check if Python is Installed

### On Windows:
1. Press `Windows + R` keys
2. Type `cmd` and press Enter
3. In the black window that opens, type: `python --version` and press Enter
4. You should see something like `Python 3.9.0` or higher

If you get an error, download Python from: https://www.python.org/downloads/
- **Important**: During installation, check the box that says "Add Python to PATH"

### On Mac:
1. Press `Command + Space` to open Spotlight
2. Type `terminal` and press Enter
3. In the terminal window, type: `python3 --version` and press Enter
4. You should see something like `Python 3.9.0` or higher

If not installed, Mac users can install via Homebrew or download from python.org

### On Linux:
1. Open Terminal (usually Ctrl+Alt+T)
2. Type: `python3 --version` and press Enter
3. Most Linux systems have Python pre-installed

---

## Step 2: Get Your Anthropic API Key (PAYMENT REQUIRED)

The application needs an API key to use Claude AI. **This requires a paid account.**

### ⚠️ IMPORTANT: This is NOT FREE!

You **must** add a payment method and purchase credits before you can use this tool.

### Costs:
- **Minimum purchase**: $5 USD in credits
- **Per analysis**: ~$0.01 to $0.05 per requirement
- **Example**: Analyzing 10 requirements costs approximately $0.10-$0.50
- **Credits**: Don't expire, so you can use them over time

### How to get your API key:

1. **Go to Anthropic's website**: https://console.anthropic.com/
2. **Sign up for an account**:
   - Click "Sign Up" if you don't have an account
   - Use your email to create an account
3. **Add payment method and purchase credits**:
   - Click on "Billing" in the left menu
   - Click "Add payment method"
   - Add your credit card or payment information
   - Purchase at least $5 in credits (minimum amount)
4. **Create your API key**:
   - Click on "API Keys" in the menu
   - Click "Create Key" button
   - Give it a name like "PLC Mapper"
   - **IMPORTANT**: Copy the key that appears (it looks like `sk-ant-...`)
   - Save it somewhere safe (like a text file) - you'll need it in Step 5

**Note**: Without purchasing credits, the API key will not work and the application will fail.

---

## Step 3: Navigate to the Project Folder

### On Windows:
1. Open Command Prompt (Press `Windows + R`, type `cmd`, press Enter)
2. Type these commands one at a time:
   ```bash
   cd C:\Users\YourUsername\PLCcmplx\plc-mapper
   ```
   (Replace `YourUsername` with your actual Windows username)

### On Mac/Linux:
1. Open Terminal
2. Type:
   ```bash
   cd ~/PLCcmplx/plc-mapper
   ```

To verify you're in the right place, type `dir` (Windows) or `ls` (Mac/Linux). You should see files like:
- app.py
- requirements.txt
- README.md
- templates/
- static/

---

## Step 4: Install Required Software

In the same terminal/command prompt window, type:

### On Windows:
```bash
pip install -r requirements.txt
```

### On Mac/Linux:
```bash
pip3 install -r requirements.txt
```

You'll see text scrolling as it installs Flask, Anthropic, and other packages. Wait for it to finish.

---

## Step 5: Set Your API Key

This tells the application to use your Anthropic API key.

### On Windows:
In the Command Prompt, type (replace `your-actual-key-here` with the key you copied in Step 2):
```bash
set ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

**Example**:
```bash
set ANTHROPIC_API_KEY=sk-ant-api03-abc123def456...
```

### On Mac/Linux:
In the Terminal, type:
```bash
export ANTHROPIC_API_KEY='sk-ant-your-actual-key-here'
```

**Example**:
```bash
export ANTHROPIC_API_KEY='sk-ant-api03-abc123def456...'
```

**Important**: Don't close this terminal window! The API key only lasts for this session.

---

## Step 6: Start the Application

In the same terminal window, type:

### On Windows:
```bash
python app.py
```

### On Mac/Linux:
```bash
python3 app.py
```

You should see output like:
```
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**Don't close this window!** The application is now running.

---

## Step 7: Open in Your Browser

1. Open your web browser (Chrome, Firefox, Safari, Edge, etc.)
2. In the address bar, type: `http://localhost:5000`
3. Press Enter

You should see the **PLC Data Mapping Assistant** interface!

---

## Step 8: Try the Examples

Now let's test it:

1. **Click "Example 1: Circuit Breaker"**
   - This will fill in sample data in all three text boxes

2. **Click the big blue "Analyze Mappings" button**
   - Wait 10-30 seconds (the AI is working!)
   - You'll see a loading spinner

3. **View the results**
   - You'll see a table showing how the AI matched requirements to PLC tags
   - Each match has a confidence score (percentage)
   - Green badges = high confidence (80%+)
   - Yellow badges = medium confidence (60-79%)
   - Red badges = low confidence (<60%)

4. **Accept good matches**
   - Click the green "✓ Accept" button for matches you like
   - The row will turn light green

5. **View alternatives**
   - Click "View Alternatives" to see other possible matches
   - A popup window will show 2nd and 3rd best options

6. **Export your results**
   - Click "Export as CSV" to download a spreadsheet file
   - Or click "Generate YAML Config" for a configuration file
   - The file will download to your default Downloads folder

---

## Step 9: Use Your Own Data

To use your own PLC data:

1. **Click "Clear All"** to remove the example

2. **Enter Business Requirements** (left box):
   - Format: `Name | Description`
   - One per line
   - Example:
     ```
     Motor_Speed | Motor rotation speed in RPM
     Tank_Level | Water tank level in percentage
     ```

3. **Enter PLC Tags** (middle box):
   - Format: `TagName, Address, DataType, CurrentValue`
   - One per line
   - Example:
     ```
     MTR_SPD, DB100.DBD0, Float, 1450.5
     TNK_LVL, DB100.DBD4, Float, 75.2
     ```

4. **Add Documentation** (right box - optional):
   - Paste any relevant information about your PLC system
   - Naming conventions, abbreviations, etc.

5. **Click "Analyze Mappings"** and wait for results!

---

## Step 10: Stop the Application

When you're done:

1. Go back to the terminal/command prompt window
2. Press `Ctrl + C` (hold Ctrl, then press C)
3. The application will stop
4. You can close the terminal window

---

## Common Issues & Solutions

### Issue: "ANTHROPIC_API_KEY environment variable is not set"
**Solution**: Go back to Step 5 and make sure you entered your API key correctly

### Issue: "pip is not recognized" (Windows)
**Solution**: Try using `python -m pip install -r requirements.txt` instead

### Issue: "Port 5000 is already in use"
**Solution**:
- Something else is using port 5000
- Close other programs or restart your computer
- Or edit `app.py` line 280: change `5000` to `5001`

### Issue: "Cannot connect to localhost"
**Solution**:
- Make sure the application is still running (don't close the terminal)
- Try `http://127.0.0.1:5000` instead
- Check if your firewall is blocking the connection

### Issue: "Analysis failed" or "Error processing"
**Solution**:
- Check your API key is valid
- Make sure you have credits left in your Anthropic account
- Check your internet connection

### Issue: Low confidence scores on your data
**Solution**:
- Add more context in the Documentation box
- Make sure your PLC tag names follow some pattern
- Check that requirements are clearly described

---

## Video Tutorial Alternative

If you prefer visual learning, search YouTube for:
- "How to install Python on [Your Operating System]"
- "How to use Terminal/Command Prompt basics"

---

## Need More Help?

1. **Check the README.md file** in the plc-mapper folder for more technical details
2. **Read the error messages** - they often tell you what's wrong
3. **Google the error message** - someone else has probably solved it
4. **Check Anthropic's documentation**: https://docs.anthropic.com/

---

## Quick Reference

**Start the app**:
```bash
# Navigate to folder
cd path/to/PLCcmplx/plc-mapper

# Set API key (do this every time you open a new terminal)
export ANTHROPIC_API_KEY='your-key-here'    # Mac/Linux
set ANTHROPIC_API_KEY=your-key-here         # Windows

# Run the app
python3 app.py    # Mac/Linux
python app.py     # Windows
```

**Open in browser**:
```
http://localhost:5000
```

**Stop the app**:
```
Ctrl + C (in the terminal window)
```

---

## What's Happening Behind the Scenes?

When you click "Analyze Mappings":

1. Your browser sends the data to the Flask server (running on your computer)
2. The server formats a smart prompt for Claude AI
3. It sends the prompt to Anthropic's servers (via internet)
4. Claude AI analyzes each requirement against all PLC tags
5. It returns matches with confidence scores and reasoning
6. Your browser displays the results in a nice table

You're paying Anthropic a tiny amount per API call (fractions of a cent). Check your usage at console.anthropic.com.

---

## Success! 🎉

If you can see the results table after clicking "Analyze Mappings", everything is working!

You now have an AI assistant that can match PLC tags to requirements automatically. This saves hours of manual work!

Enjoy your PLC Data Mapping Assistant!
