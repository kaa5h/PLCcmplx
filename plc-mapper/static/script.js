// Global variable to store results
let analysisResults = [];
let acceptedMappings = new Set();

// Sample Data Examples
const EXAMPLES = {
    example1: {
        requirements: `Phase1_Current | Electrical current in Amps for phase 1
Phase2_Current | Electrical current in Amps for phase 2
Phase3_Current | Electrical current in Amps for phase 3
Total_Power | Total power consumption in Kilowatts`,
        plcTags: `CP_Ph1_I, DB45.DBD10, Float, 23.4
CP_Ph2_I, DB45.DBD14, Float, 24.1
CP_Ph3_I, DB45.DBD18, Float, 23.8
P_tot, DB45.DBD20, Float, 5.2
Motor_Status, DB100.DBX0, Boolean, True
Temp_Sensor_1, DB50.DBD0, Float, 45.2`,
        documentation: `Circuit Breaker Panel Documentation:
CP prefix indicates Circuit Panel
Ph1, Ph2, Ph3 represent three-phase power
I suffix represents current measurement
P_tot is total power consumption`
    },
    example2: {
        requirements: `Ambient_Temperature | Room temperature in Celsius
Motor_Temperature | Motor case temperature in Celsius
Oil_Temperature | Hydraulic oil temperature in Celsius`,
        plcTags: `T_Amb, MW100, Real, 22.5
T_Motor, MW104, Real, 67.3
T_Oil, MW108, Real, 55.8
Temp1, MW200, Real, 22.5
THM_02, MW204, Real, 67.3`,
        documentation: `Temperature Monitoring System:
T_ prefix indicates temperature sensor
Amb = Ambient
THM = Thermal sensor
All temperature values in Celsius`
    }
};

// Load Example Data
function loadExample1() {
    document.getElementById('requirementsInput').value = EXAMPLES.example1.requirements;
    document.getElementById('plcTagsInput').value = EXAMPLES.example1.plcTags;
    document.getElementById('documentationInput').value = EXAMPLES.example1.documentation;
}

function loadExample2() {
    document.getElementById('requirementsInput').value = EXAMPLES.example2.requirements;
    document.getElementById('plcTagsInput').value = EXAMPLES.example2.plcTags;
    document.getElementById('documentationInput').value = EXAMPLES.example2.documentation;
}

function clearAll() {
    document.getElementById('requirementsInput').value = '';
    document.getElementById('plcTagsInput').value = '';
    document.getElementById('documentationInput').value = '';
    document.getElementById('resultsSection').classList.add('d-none');
    document.getElementById('errorAlert').classList.add('d-none');
    analysisResults = [];
    acceptedMappings.clear();
}

// Analyze Mappings
async function analyzeMappings() {
    const requirementsInput = document.getElementById('requirementsInput').value.trim();
    const plcTagsInput = document.getElementById('plcTagsInput').value.trim();
    const documentationInput = document.getElementById('documentationInput').value.trim();

    // Validation
    if (!requirementsInput) {
        showError('Please enter business requirements');
        return;
    }

    if (!plcTagsInput) {
        showError('Please enter PLC tags');
        return;
    }

    // Hide error and results
    document.getElementById('errorAlert').classList.add('d-none');
    document.getElementById('resultsSection').classList.add('d-none');

    // Show loading state
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analyzeText = document.getElementById('analyzeText');
    const analyzeSpinner = document.getElementById('analyzeSpinner');

    analyzeBtn.disabled = true;
    analyzeText.textContent = 'Analyzing...';
    analyzeSpinner.classList.remove('d-none');

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                requirements: requirementsInput,
                plc_tags: plcTagsInput,
                documentation: documentationInput
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Analysis failed');
        }

        const results = await response.json();
        analysisResults = results;
        acceptedMappings.clear();
        displayResults(results);

    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        analyzeText.textContent = 'Analyze Mappings';
        analyzeSpinner.classList.add('d-none');
    }
}

// Display Results
function displayResults(results) {
    const resultsBody = document.getElementById('resultsBody');
    resultsBody.innerHTML = '';

    results.forEach((result, index) => {
        const row = createResultRow(result, index);
        resultsBody.appendChild(row);
    });

    document.getElementById('resultsSection').classList.remove('d-none');
}

// Create Result Row
function createResultRow(result, index) {
    const tr = document.createElement('tr');
    tr.id = `result-row-${index}`;

    // Confidence class
    const confidence = result.best_match.confidence;
    let confidenceClass = 'confidence-low';
    if (confidence >= 80) confidenceClass = 'confidence-high';
    else if (confidence >= 60) confidenceClass = 'confidence-medium';

    // Requirement column
    const requirementTd = document.createElement('td');
    requirementTd.innerHTML = `
        <div class="requirement-name">${escapeHtml(result.requirement_name)}</div>
        <div class="requirement-description">${escapeHtml(result.requirement_description)}</div>
    `;

    // Best Match column
    const bestMatchTd = document.createElement('td');
    bestMatchTd.innerHTML = `<strong>${escapeHtml(result.best_match.tag_name)}</strong>`;

    // Confidence column
    const confidenceTd = document.createElement('td');
    confidenceTd.innerHTML = `<span class="confidence-badge ${confidenceClass}">${confidence}%</span>`;

    // Tag Details column
    const detailsTd = document.createElement('td');
    const details = result.best_match.details;
    detailsTd.innerHTML = `
        <div class="tag-details">
            <strong>Address:</strong> ${escapeHtml(details.address || 'N/A')}<br>
            <strong>Type:</strong> ${escapeHtml(details.data_type || 'N/A')}<br>
            <strong>Value:</strong> ${escapeHtml(details.current_value || 'N/A')}
        </div>
    `;

    // Evidence column
    const evidenceTd = document.createElement('td');
    const evidenceList = result.best_match.reasoning
        .map(r => `<li>${escapeHtml(r)}</li>`)
        .join('');
    evidenceTd.innerHTML = `<ul class="evidence-list">${evidenceList}</ul>`;

    // Actions column
    const actionsTd = document.createElement('td');
    actionsTd.innerHTML = `
        <div class="action-buttons">
            <button class="btn btn-sm btn-success" onclick="acceptMapping(${index})">✓ Accept</button>
            ${result.alternatives && result.alternatives.length > 0 ?
                `<button class="btn btn-sm btn-info" onclick="viewAlternatives(${index})">View Alternatives</button>` :
                ''}
        </div>
    `;

    tr.appendChild(requirementTd);
    tr.appendChild(bestMatchTd);
    tr.appendChild(confidenceTd);
    tr.appendChild(detailsTd);
    tr.appendChild(evidenceTd);
    tr.appendChild(actionsTd);

    return tr;
}

// Accept Mapping
function acceptMapping(index) {
    acceptedMappings.add(index);
    const row = document.getElementById(`result-row-${index}`);
    row.classList.add('row-accepted');

    // Update button to show accepted state
    const actionsTd = row.querySelector('.action-buttons');
    actionsTd.innerHTML = `
        <button class="btn btn-sm btn-secondary" disabled>✓ Accepted</button>
    `;
}

// View Alternatives
function viewAlternatives(index) {
    const result = analysisResults[index];
    const alternatives = result.alternatives || [];

    if (alternatives.length === 0) {
        alert('No alternatives available');
        return;
    }

    let alternativesHtml = '<div class="modal fade" id="alternativesModal" tabindex="-1">';
    alternativesHtml += '<div class="modal-dialog modal-lg">';
    alternativesHtml += '<div class="modal-content">';
    alternativesHtml += '<div class="modal-header">';
    alternativesHtml += `<h5 class="modal-title">Alternative Matches for ${escapeHtml(result.requirement_name)}</h5>`;
    alternativesHtml += '<button type="button" class="btn-close" data-bs-dismiss="modal"></button>';
    alternativesHtml += '</div>';
    alternativesHtml += '<div class="modal-body">';

    alternatives.forEach((alt, i) => {
        const confidenceClass = alt.confidence >= 60 ? 'confidence-medium' : 'confidence-low';
        alternativesHtml += `
            <div class="alternative-item">
                <h6>
                    ${escapeHtml(alt.tag_name)}
                    <span class="confidence-badge ${confidenceClass}">${alt.confidence}%</span>
                </h6>
                <ul class="evidence-list">
                    ${alt.reasoning.map(r => `<li>${escapeHtml(r)}</li>`).join('')}
                </ul>
                <button class="btn btn-sm btn-primary" onclick="selectAlternative(${index}, ${i})">
                    Select This Match
                </button>
            </div>
        `;
    });

    alternativesHtml += '</div></div></div></div>';

    // Remove existing modal if any
    const existingModal = document.getElementById('alternativesModal');
    if (existingModal) {
        existingModal.remove();
    }

    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', alternativesHtml);

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('alternativesModal'));
    modal.show();
}

// Select Alternative
function selectAlternative(resultIndex, alternativeIndex) {
    const result = analysisResults[resultIndex];
    const alternative = result.alternatives[alternativeIndex];

    // Swap alternative with best match
    const oldBestMatch = result.best_match;
    result.best_match = {
        tag_name: alternative.tag_name,
        confidence: alternative.confidence,
        reasoning: alternative.reasoning,
        details: {} // Alternative doesn't have full details, could be enhanced
    };

    // Add old best match to alternatives
    result.alternatives[alternativeIndex] = {
        tag_name: oldBestMatch.tag_name,
        confidence: oldBestMatch.confidence,
        reasoning: oldBestMatch.reasoning
    };

    // Redisplay results
    displayResults(analysisResults);

    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('alternativesModal'));
    modal.hide();
}

// Export Mappings
async function exportMappings(format) {
    // Get accepted mappings or all if none accepted
    let mappingsToExport = [];

    if (acceptedMappings.size > 0) {
        acceptedMappings.forEach(index => {
            mappingsToExport.push(analysisResults[index]);
        });
    } else {
        // Export all if none explicitly accepted
        if (confirm('No mappings have been accepted. Export all results?')) {
            mappingsToExport = analysisResults;
        } else {
            return;
        }
    }

    if (mappingsToExport.length === 0) {
        alert('No mappings to export');
        return;
    }

    try {
        const endpoint = format === 'csv' ? '/export/csv' : '/export/yaml';

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mappings: mappingsToExport
            })
        });

        if (!response.ok) {
            throw new Error('Export failed');
        }

        const data = await response.json();

        // Download file
        downloadFile(data.content, data.filename);

    } catch (error) {
        showError(`Export error: ${error.message}`);
    }
}

// Download File
function downloadFile(content, filename) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Show Error
function showError(message) {
    const errorAlert = document.getElementById('errorAlert');
    errorAlert.textContent = message;
    errorAlert.classList.remove('d-none');

    // Scroll to error
    errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Utility: Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
