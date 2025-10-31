# PLC Data Mapping Assistant

An AI-powered web application that automatically matches business requirements to PLC tag names, reducing manual mapping time from hours to minutes.

## Features

- **AI-Powered Matching**: Uses Claude AI to intelligently match business requirements to PLC tags
- **Confidence Scoring**: Each match includes a confidence score (0-100%) with detailed reasoning
- **Alternative Suggestions**: View alternative matches when primary match isn't suitable
- **Export Functionality**: Export validated mappings as CSV or YAML configuration files
- **Sample Datasets**: Pre-loaded examples for quick testing
- **Clean UI**: Simple, intuitive interface built with Bootstrap

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key (get one at https://console.anthropic.com/)

### Installation

1. Navigate to the project directory:
```bash
cd plc-mapper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your Anthropic API key as an environment variable:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Try the examples by clicking "Example 1: Circuit Breaker" or "Example 2: Temperature Sensors"

4. Click "Analyze Mappings" to see AI-powered matches

5. Review results, accept matches, and export when ready

## Usage

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

1. **Input Data**: Paste your business requirements and PLC tags into the respective text areas
2. **Add Context** (optional): Provide documentation or naming conventions for better matching
3. **Analyze**: Click "Analyze Mappings" to run AI analysis
4. **Review**: Examine matches, confidence scores, and reasoning
5. **Accept/Adjust**: Accept good matches or view alternatives
6. **Export**: Download CSV or YAML configuration files

## How It Works

The application uses Claude AI (claude-3-5-sonnet-20241022) to analyze:

- **Keyword Matching**: Exact matches and common industrial abbreviations
  - I = Current, V = Voltage, T = Temperature, P = Power, Ph = Phase
- **Industrial Patterns**: Prefixes, suffixes, camelCase, underscores
- **Data Type Suitability**: Float for measurements, Boolean for status
- **Value Reasonableness**: Current typically 0-100A, temperature ranges, etc.
- **Pattern Recognition**: Similar prefixes suggest grouping (e.g., CP_Ph1_, CP_Ph2_)

## Export Formats

### CSV Export
```csv
BusinessName, PLCTag, Address, DataType, CurrentValue, Confidence, Notes
Phase1_Current, CP_Ph1_I, DB45.DBD10, Float, 23.4, 95%, Ph1 = Phase 1 | I = Current
```

### YAML Export
```yaml
mappings:
  - business_name: "Phase1_Current"
    plc_tag: "CP_Ph1_I"
    address: "DB45.DBD10"
    data_type: "float"
    unit: "Amperes"
    confidence: 95
```

## File Structure

```
plc-mapper/
├── app.py                 # Flask backend with API routes
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── style.css         # Custom styling
│   └── script.js         # Frontend logic and API calls
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Common Industrial Abbreviations

The AI recognizes these common abbreviations:

- **I** = Current (Amps)
- **V** = Voltage (Volts)
- **T** = Temperature (Celsius/Fahrenheit)
- **P** = Power (Watts/Kilowatts)
- **Ph** = Phase
- **Amb** = Ambient
- **THM** = Thermal
- **CP** = Circuit Panel
- **DB** = Data Block

## Troubleshooting

**Error: "ANTHROPIC_API_KEY environment variable is not set"**
- Make sure you've exported your API key: `export ANTHROPIC_API_KEY='your-key'`

**Error: "No valid requirements found"**
- Check format: Each line should be `Name | Description`
- Make sure there's at least one requirement

**Error: "No valid PLC tags found"**
- Check CSV format: `TagName, Address, DataType, CurrentValue`
- Each line should have all 4 fields separated by commas

**Low confidence scores**
- Add documentation context to provide more information
- Check that PLC tag names follow recognizable patterns
- Verify requirements are clearly described

## Performance

- Handles 20+ requirements and 50+ PLC tags
- Analysis typically completes in 10-30 seconds
- Confidence scores of 80%+ on clear matches

## Security Note

This is a prototype application. For production use:
- Add authentication
- Implement rate limiting
- Store results in a database
- Add input validation and sanitization
- Use HTTPS

## License

This is a prototype application for demonstration purposes.
