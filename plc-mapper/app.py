from flask import Flask, render_template, request, jsonify
import json
import csv
import yaml
import re
from io import StringIO

app = Flask(__name__)

# Common industrial abbreviations mapping
ABBREVIATIONS = {
    'current': ['i', 'curr', 'amp', 'a'],
    'voltage': ['v', 'volt', 'u'],
    'temperature': ['t', 'temp', 'thm', 'thermal'],
    'power': ['p', 'pwr', 'w'],
    'phase': ['ph', 'phase'],
    'motor': ['mtr', 'motor', 'mot', 'm'],
    'ambient': ['amb', 'ambient', 'room'],
    'oil': ['oil', 'hydraulic'],
    'total': ['tot', 'total', 'sum'],
    'status': ['stat', 'status', 'sts'],
    'level': ['lvl', 'level', 'lv'],
    'speed': ['spd', 'speed', 'rpm']
}

@app.route('/')
def index():
    return render_template('index.html')

def parse_requirements(requirements_text):
    """Parse requirements from text format: 'Name | Description'"""
    requirements = []
    for line in requirements_text.strip().split('\n'):
        line = line.strip()
        if line and '|' in line:
            parts = line.split('|', 1)
            requirements.append({
                'name': parts[0].strip(),
                'description': parts[1].strip() if len(parts) > 1 else ''
            })
    return requirements

def parse_plc_tags(plc_tags_text):
    """Parse PLC tags from CSV format: 'TagName, Address, DataType, CurrentValue'"""
    plc_tags = []
    lines = plc_tags_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if line:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 4:
                plc_tags.append({
                    'tag_name': parts[0],
                    'address': parts[1],
                    'data_type': parts[2],
                    'current_value': parts[3]
                })
    return plc_tags

def extract_keywords(text):
    """Extract keywords from text and normalize them"""
    # Convert to lowercase and split on non-alphanumeric characters
    words = re.findall(r'\w+', text.lower())
    return words

def calculate_match_score(requirement, tag):
    """
    Mock AI matching algorithm that calculates confidence score
    based on keyword matching and patterns
    """
    req_name = requirement['name'].lower()
    req_desc = requirement['description'].lower()
    tag_name = tag['tag_name'].lower()

    req_keywords = extract_keywords(req_name + ' ' + req_desc)
    tag_keywords = extract_keywords(tag_name)

    score = 0
    reasoning = []

    # Direct keyword matches (high confidence)
    for req_word in req_keywords:
        if req_word in tag_keywords:
            score += 30
            reasoning.append(f"Direct keyword match: '{req_word}' found in tag name")

    # Abbreviation matches (medium confidence)
    for concept, abbrevs in ABBREVIATIONS.items():
        req_has_concept = any(word in req_keywords for word in [concept] + abbrevs)
        tag_has_abbrev = any(abbrev in tag_keywords for abbrev in abbrevs)

        if req_has_concept and tag_has_abbrev:
            score += 25
            matching_abbrev = next(abbrev for abbrev in abbrevs if abbrev in tag_keywords)
            reasoning.append(f"'{matching_abbrev}' in tag matches '{concept}' in requirement")

    # Phase/number matching
    phase_numbers = re.findall(r'(?:phase|ph)\s*(\d+)', req_name.lower() + ' ' + req_desc.lower())
    tag_numbers = re.findall(r'(?:ph|phase)(\d+)', tag_name)

    if phase_numbers and tag_numbers:
        if phase_numbers[0] == tag_numbers[0]:
            score += 20
            reasoning.append(f"Phase {phase_numbers[0]} number match")

    # Data type appropriateness
    data_type = tag['data_type'].lower()
    if 'current' in req_desc or 'voltage' in req_desc or 'temperature' in req_desc or 'power' in req_desc:
        if 'float' in data_type or 'real' in data_type:
            score += 10
            reasoning.append(f"{tag['data_type']} data type appropriate for measurements")

    if 'status' in req_desc or 'state' in req_desc:
        if 'bool' in data_type:
            score += 10
            reasoning.append(f"{tag['data_type']} data type appropriate for status")

    # Value reasonableness (basic check)
    try:
        value = float(tag['current_value'])
        if 'temperature' in req_desc and 0 < value < 200:
            score += 5
            reasoning.append(f"Value {value}°C is reasonable for temperature")
        elif 'current' in req_desc and 0 < value < 1000:
            score += 5
            reasoning.append(f"Value {value}A is reasonable for current")
        elif 'power' in req_desc and 0 < value < 10000:
            score += 5
            reasoning.append(f"Value {value}W is reasonable for power")
    except:
        pass

    # Cap score at 100
    score = min(score, 100)

    # If no reasoning, add a generic one
    if not reasoning:
        reasoning.append("No strong pattern matches found")
        score = max(score, 30)  # Minimum score for any tag

    return score, reasoning

def find_best_match(requirement, plc_tags, documentation):
    """
    Mock AI function that finds the best matching PLC tag
    Uses simple keyword matching and pattern recognition
    """
    matches = []

    # Calculate match score for each tag
    for tag in plc_tags:
        score, reasoning = calculate_match_score(requirement, tag)
        matches.append({
            'tag': tag,
            'score': score,
            'reasoning': reasoning
        })

    # Sort by score
    matches.sort(key=lambda x: x['score'], reverse=True)

    # Get best match
    best = matches[0]

    # Get alternatives (2nd and 3rd best)
    alternatives = []
    for match in matches[1:3]:
        if match['score'] > 40:  # Only include decent alternatives
            alternatives.append({
                'tag_name': match['tag']['tag_name'],
                'confidence': match['score'],
                'reasoning': match['reasoning']
            })

    return {
        'requirement_name': requirement['name'],
        'requirement_description': requirement['description'],
        'best_match': {
            'tag_name': best['tag']['tag_name'],
            'confidence': best['score'],
            'reasoning': best['reasoning'],
            'details': best['tag']
        },
        'alternatives': alternatives
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze requirements and find matching PLC tags using mock AI"""
    try:
        data = request.json
        requirements = parse_requirements(data['requirements'])
        plc_tags = parse_plc_tags(data['plc_tags'])
        documentation = data.get('documentation', '')

        if not requirements:
            return jsonify({'error': 'No valid requirements found'}), 400

        if not plc_tags:
            return jsonify({'error': 'No valid PLC tags found'}), 400

        # Simulate processing time (like real AI would take)
        import time
        time.sleep(0.5)  # Small delay to feel realistic

        results = []
        for req in requirements:
            match = find_best_match(req, plc_tags, documentation)
            results.append(match)

        return jsonify(results)

    except Exception as e:
        print(f"Error in analyze: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/export/csv', methods=['POST'])
def export_csv():
    """Export validated mappings as CSV"""
    try:
        data = request.json
        mappings = data.get('mappings', [])

        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['BusinessName', 'PLCTag', 'Address', 'DataType', 'CurrentValue', 'Confidence', 'Notes'])

        # Write data
        for mapping in mappings:
            notes = ' | '.join(mapping['best_match']['reasoning'])
            writer.writerow([
                mapping['requirement_name'],
                mapping['best_match']['tag_name'],
                mapping['best_match']['details'].get('address', ''),
                mapping['best_match']['details'].get('data_type', ''),
                mapping['best_match']['details'].get('current_value', ''),
                f"{mapping['best_match']['confidence']}%",
                notes
            ])

        # Create response
        output.seek(0)
        return {
            'content': output.getvalue(),
            'filename': 'plc_mappings.csv'
        }

    except Exception as e:
        print(f"Error in export_csv: {str(e)}")
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@app.route('/export/yaml', methods=['POST'])
def export_yaml():
    """Export validated mappings as YAML"""
    try:
        data = request.json
        mappings = data.get('mappings', [])

        yaml_data = {'mappings': []}

        for mapping in mappings:
            # Extract unit from description if possible
            description = mapping['requirement_description'].lower()
            unit = 'unknown'
            if 'amp' in description:
                unit = 'Amperes'
            elif 'volt' in description:
                unit = 'Volts'
            elif 'celsius' in description or 'temperature' in description:
                unit = 'Celsius'
            elif 'kilowatt' in description or 'power' in description:
                unit = 'Kilowatts'

            yaml_data['mappings'].append({
                'business_name': mapping['requirement_name'],
                'plc_tag': mapping['best_match']['tag_name'],
                'address': mapping['best_match']['details'].get('address', ''),
                'data_type': mapping['best_match']['details'].get('data_type', '').lower(),
                'unit': unit,
                'confidence': mapping['best_match']['confidence']
            })

        yaml_output = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)

        return {
            'content': yaml_output,
            'filename': 'plc_mappings.yaml'
        }

    except Exception as e:
        print(f"Error in export_yaml: {str(e)}")
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("PLC Data Mapping Assistant - PROTOTYPE VERSION")
    print("=" * 60)
    print("\nThis is a DEMO with simulated AI matching.")
    print("No API keys or payment required!")
    print("\nStarting server...")
    print("Open http://localhost:5000 in your browser")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
