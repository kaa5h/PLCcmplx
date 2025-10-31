from flask import Flask, render_template, request, jsonify, send_file
import anthropic
import json
import os
import csv
import yaml
from io import StringIO, BytesIO

app = Flask(__name__)

# Initialize Anthropic client
def get_anthropic_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    return anthropic.Anthropic(api_key=api_key)

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

def format_tags_for_prompt(plc_tags):
    """Format PLC tags for the Claude prompt"""
    formatted = []
    for tag in plc_tags:
        formatted.append(
            f"- Tag: {tag['tag_name']}, Address: {tag['address']}, "
            f"Type: {tag['data_type']}, Value: {tag['current_value']}"
        )
    return '\n'.join(formatted)

def find_best_match(requirement, plc_tags, documentation, client):
    """Use Claude API to find the best matching PLC tag for a requirement"""

    formatted_tags = format_tags_for_prompt(plc_tags)

    prompt = f"""You are an industrial automation expert. Analyze PLC tags to find the best match for a business requirement.

REQUIREMENT:
Name: {requirement['name']}
Description: {requirement['description']}

AVAILABLE PLC TAGS:
{formatted_tags}

DOCUMENTATION CONTEXT (if provided):
{documentation if documentation else 'No additional documentation provided'}

TASK:
Find the best matching PLC tag for this requirement.

Consider:
1. Keyword matches - exact and common abbreviations (I=Current, V=Voltage, T=Temp, P=Power, Ph=Phase)
2. Industrial naming patterns (underscores, camel case, prefixes)
3. Data type suitability
4. Value range reasonableness
5. Tag grouping patterns (similar prefixes)

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "best_match": {{
    "tag_name": "CP_Ph1_I",
    "confidence": 95,
    "reasoning": [
      "Ph1 strongly indicates Phase 1",
      "I is standard electrical notation for current",
      "Float data type appropriate for current measurement",
      "Value 23.4A is reasonable for circuit current"
    ]
  }},
  "alternatives": [
    {{
      "tag_name": "example_tag",
      "confidence": 70,
      "reasoning": ["Reason for lower confidence match"]
    }}
  ]
}}"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            response_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else response_text

        response_data = json.loads(response_text)

        # Get tag details for best match
        best_match_tag = next(
            (tag for tag in plc_tags if tag['tag_name'] == response_data['best_match']['tag_name']),
            None
        )

        return {
            'requirement_name': requirement['name'],
            'requirement_description': requirement['description'],
            'best_match': {
                'tag_name': response_data['best_match']['tag_name'],
                'confidence': response_data['best_match']['confidence'],
                'reasoning': response_data['best_match']['reasoning'],
                'details': best_match_tag if best_match_tag else {}
            },
            'alternatives': response_data.get('alternatives', [])
        }

    except Exception as e:
        print(f"Error in find_best_match: {str(e)}")
        return {
            'requirement_name': requirement['name'],
            'requirement_description': requirement['description'],
            'best_match': {
                'tag_name': 'Error',
                'confidence': 0,
                'reasoning': [f'Error processing: {str(e)}'],
                'details': {}
            },
            'alternatives': []
        }

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze requirements and find matching PLC tags"""
    try:
        data = request.json
        requirements = parse_requirements(data['requirements'])
        plc_tags = parse_plc_tags(data['plc_tags'])
        documentation = data.get('documentation', '')

        if not requirements:
            return jsonify({'error': 'No valid requirements found'}), 400

        if not plc_tags:
            return jsonify({'error': 'No valid PLC tags found'}), 400

        client = get_anthropic_client()

        results = []
        for req in requirements:
            match = find_best_match(req, plc_tags, documentation, client)
            results.append(match)

        return jsonify(results)

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
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
    app.run(debug=True, host='0.0.0.0', port=5000)
