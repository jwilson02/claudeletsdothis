// Path of Exile Build Guide - Main JavaScript

// State management
let currentBuild = null;
let currentProgress = null;

// API base URL
const API_BASE = '/api';

// Game data cache
let questsCache = {};
let labsData = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadBuilds();
    loadLabsData();
    initPixelArtGenerator();
});

// Event Listeners
function initializeEventListeners() {
    // Import button
    document.getElementById('import-btn').addEventListener('click', importBuild);

    // Demo button
    document.getElementById('demo-btn').addEventListener('click', loadDemoBuild);

    // Back button
    document.getElementById('back-btn').addEventListener('click', showBuildsList);

    // Delete button
    document.getElementById('delete-btn').addEventListener('click', deleteBuild);

    // Save progress button
    document.getElementById('save-progress-btn').addEventListener('click', saveProgress);

    // Tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            switchTab(e.target.dataset.tab);
        });
    });

    // Progress inputs
    document.getElementById('current-level').addEventListener('change', autoSaveProgress);
    document.getElementById('current-act').addEventListener('change', autoSaveProgress);

    // Quest act selector
    document.getElementById('quest-act-select').addEventListener('change', (e) => {
        loadQuestsForAct(parseInt(e.target.value));
    });
}

// API Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'API request failed');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Build Management
async function loadBuilds() {
    try {
        const data = await apiCall('/builds');
        renderBuildsList(data.builds);
    } catch (error) {
        showStatus('error', 'Failed to load builds: ' + error.message);
    }
}

async function importBuild() {
    const pobCode = document.getElementById('pob-input').value.trim();
    const importBtn = document.getElementById('import-btn');

    if (!pobCode) {
        showStatus('error', 'Please paste a Path of Building code');
        return;
    }

    importBtn.disabled = true;
    importBtn.textContent = 'Importing...';

    try {
        const data = await apiCall('/builds', 'POST', { pob_code: pobCode });
        showStatus('success', 'Build imported successfully!');
        document.getElementById('pob-input').value = '';

        // Reload builds and show the new build
        await loadBuilds();
        setTimeout(() => {
            loadBuildDetails(data.build_id);
        }, 500);
    } catch (error) {
        showStatus('error', 'Import failed: ' + error.message);
    } finally {
        importBtn.disabled = false;
        importBtn.textContent = 'Import Build';
    }
}

async function loadDemoBuild() {
    const demoBtn = document.getElementById('demo-btn');

    demoBtn.disabled = true;
    demoBtn.textContent = 'Loading...';

    try {
        const data = await apiCall('/builds/demo', 'POST');
        showStatus('success', 'Demo build loaded! Click on it below to explore features.');

        // Reload builds and show the demo build
        await loadBuilds();
        setTimeout(() => {
            loadBuildDetails(data.build_id);
        }, 500);
    } catch (error) {
        showStatus('error', 'Failed to load demo build: ' + error.message);
    } finally {
        demoBtn.disabled = false;
        demoBtn.textContent = 'Load Demo Build';
    }
}

async function deleteBuild() {
    if (!currentBuild) return;

    if (!confirm(`Are you sure you want to delete "${currentBuild.name}"?`)) {
        return;
    }

    try {
        await apiCall(`/builds/${currentBuild.id}`, 'DELETE');
        showBuildsList();
        await loadBuilds();
    } catch (error) {
        showStatus('error', 'Failed to delete build: ' + error.message);
    }
}

async function loadBuildDetails(buildId) {
    try {
        const data = await apiCall(`/builds/${buildId}`);
        currentBuild = data.build;
        currentProgress = data.progress || {
            current_level: 1,
            current_act: 1,
            completed_milestones: [],
            completed_gems: [],
            equipped_items: []
        };

        renderBuildDetails();
    } catch (error) {
        showStatus('error', 'Failed to load build: ' + error.message);
    }
}

// Progress Management
async function saveProgress() {
    if (!currentBuild) return;

    const level = parseInt(document.getElementById('current-level').value);
    const act = parseInt(document.getElementById('current-act').value);

    try {
        await apiCall(`/progress/${currentBuild.id}`, 'POST', {
            current_level: level,
            current_act: act,
            completed_milestones: currentProgress.completed_milestones
        });

        currentProgress.current_level = level;
        currentProgress.current_act = act;

        showStatus('success', 'Progress saved!');
    } catch (error) {
        showStatus('error', 'Failed to save progress: ' + error.message);
    }
}

async function autoSaveProgress() {
    // Auto-save after a short delay
    clearTimeout(window.autoSaveTimer);
    window.autoSaveTimer = setTimeout(saveProgress, 1000);
}

async function toggleMilestone(index) {
    if (!currentBuild) return;

    try {
        const data = await apiCall(`/progress/${currentBuild.id}/milestone/${index}`, 'POST');
        currentProgress.completed_milestones = data.completed_milestones;
        renderMilestones();
    } catch (error) {
        showStatus('error', 'Failed to update milestone: ' + error.message);
    }
}

// Rendering Functions
function renderBuildsList(builds) {
    const buildsGrid = document.getElementById('builds-list');

    if (!builds || builds.length === 0) {
        buildsGrid.innerHTML = '<p class="empty-state">No builds imported yet. Import your first build above!</p>';
        return;
    }

    buildsGrid.innerHTML = builds.map(build => `
        <div class="build-card" onclick="loadBuildDetails('${build.id}')">
            <h3>${escapeHtml(build.name)}</h3>
            <div class="build-meta">
                <span class="badge">${escapeHtml(build.class)}</span>
                <span class="badge">${escapeHtml(build.ascendancy)}</span>
                <span class="badge">Level ${build.level}</span>
            </div>
        </div>
    `).join('');
}

function renderBuildDetails() {
    // Show build details section
    document.getElementById('import-section').style.display = 'none';
    document.getElementById('builds-section').style.display = 'none';
    document.getElementById('build-details').style.display = 'block';

    // Render build info
    document.getElementById('build-name').textContent = currentBuild.name;
    document.getElementById('build-class').textContent = currentBuild.class;
    document.getElementById('build-ascendancy').textContent = currentBuild.ascendancy;
    document.getElementById('build-level').textContent = `Level ${currentBuild.level}`;

    // Set progress values
    document.getElementById('current-level').value = currentProgress.current_level;
    document.getElementById('current-act').value = currentProgress.current_act;

    // Render all tabs
    renderMilestones();
    renderSkills();
    renderItems();
    renderTree();
    renderNotes();
    renderLabs();

    // Load quests for current act
    const currentAct = currentProgress.current_act || 1;
    document.getElementById('quest-act-select').value = currentAct;
    loadQuestsForAct(currentAct);

    // Switch to first tab
    switchTab('milestones');
}

function renderMilestones() {
    const milestonesList = document.getElementById('milestones-list');

    if (!currentBuild.milestones || currentBuild.milestones.length === 0) {
        milestonesList.innerHTML = '<p class="empty-state">No milestones available</p>';
        return;
    }

    milestonesList.innerHTML = currentBuild.milestones.map((milestone, index) => {
        const isCompleted = currentProgress.completed_milestones.includes(index);

        return `
            <div class="milestone ${isCompleted ? 'completed' : ''}">
                <input
                    type="checkbox"
                    class="milestone-checkbox"
                    ${isCompleted ? 'checked' : ''}
                    onchange="toggleMilestone(${index})">
                <div class="milestone-content">
                    <div class="milestone-header">
                        <span class="milestone-title">${escapeHtml(milestone.title)}</span>
                        <span class="milestone-level">Level ${milestone.level}</span>
                    </div>
                    <div class="milestone-description">${escapeHtml(milestone.description)}</div>
                </div>
            </div>
        `;
    }).join('');
}

function renderSkills() {
    const skillsList = document.getElementById('skills-list');

    if (!currentBuild.skills || currentBuild.skills.length === 0) {
        skillsList.innerHTML = '<p class="empty-state">No skills found in build</p>';
        return;
    }

    skillsList.innerHTML = currentBuild.skills.map(skill => `
        <div class="skill-group">
            <div class="skill-label">${escapeHtml(skill.label || 'Unnamed Skill')}</div>
            <div class="gems-list">
                ${skill.gems.map(gem => `
                    <div class="gem-item">
                        <span class="gem-name">${escapeHtml(gem.name)}</span>
                        <span class="gem-stats">Level ${gem.level} | Quality ${gem.quality}%</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
}

function renderItems() {
    const itemsList = document.getElementById('items-list');

    if (!currentBuild.items || currentBuild.items.length === 0) {
        itemsList.innerHTML = '<p class="empty-state">No items found in build</p>';
        return;
    }

    itemsList.innerHTML = currentBuild.items.map(item => `
        <div class="item-card">
            <div class="item-slot">${escapeHtml(item.slot)}</div>
            <div class="item-name">${escapeHtml(item.name)}</div>
        </div>
    `).join('');
}

function renderTree() {
    const treeInfo = document.getElementById('tree-info');

    if (!currentBuild.tree || !currentBuild.tree.nodes) {
        treeInfo.innerHTML = '<p class="empty-state">No passive tree data available</p>';
        return;
    }

    const nodeCount = currentBuild.tree.nodes.split(',').filter(n => n).length;

    treeInfo.innerHTML = `
        <p>This build uses <strong>${nodeCount}</strong> passive skill points.</p>
        <p>Open this build in Path of Building to view the full passive tree and progression.</p>
        <div class="tree-url">
            <p style="color: var(--text-primary); margin-top: 20px;">
                <strong>Tip:</strong> Import your PoB code in Path of Building to see detailed passive tree progression.
            </p>
        </div>
    `;
}

function renderNotes() {
    const notesContent = document.getElementById('build-notes');

    if (!currentBuild.notes || currentBuild.notes.trim() === '') {
        notesContent.innerHTML = '<p class="empty-state">No notes available for this build</p>';
        return;
    }

    notesContent.textContent = currentBuild.notes;
}

function showBuildsList() {
    document.getElementById('build-details').style.display = 'none';
    document.getElementById('import-section').style.display = 'block';
    document.getElementById('builds-section').style.display = 'block';
    currentBuild = null;
    currentProgress = null;
}

// UI Helper Functions
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Update tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        if (pane.id === `${tabName}-tab`) {
            pane.classList.add('active');
        } else {
            pane.classList.remove('active');
        }
    });
}

function showStatus(type, message) {
    const statusDiv = document.getElementById('import-status');
    statusDiv.className = `status-message ${type}`;
    statusDiv.textContent = message;
    statusDiv.style.display = 'block';

    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 5000);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

// Quest and Lab functions
async function loadLabsData() {
    try {
        const data = await apiCall('/game-data/labs');
        labsData = data.labs;
    } catch (error) {
        console.error('Failed to load labs data:', error);
    }
}

async function loadQuestsForAct(act) {
    if (!currentBuild) return;

    try {
        // Load quests
        const questData = await apiCall(`/game-data/quests/${act}`);
        const tipsData = await apiCall(`/game-data/tips/${act}`);

        // Cache the data
        questsCache[act] = {
            quests: questData.quests,
            tips: tipsData.tips
        };

        renderQuests(act);
    } catch (error) {
        console.error('Failed to load quest data:', error);
    }
}

function renderQuests(act) {
    const cached = questsCache[act];
    if (!cached) return;

    // Render tips
    const tipsDiv = document.getElementById('act-tips');
    if (cached.tips && cached.tips.title) {
        const tipsList = cached.tips.tips || [];
        tipsDiv.innerHTML = `
            <h4>${escapeHtml(cached.tips.title)}</h4>
            <ul>
                ${tipsList.map(tip => `<li>${escapeHtml(tip)}</li>`).join('')}
            </ul>
        `;
    } else {
        tipsDiv.innerHTML = '';
    }

    // Render quests
    const questsList = document.getElementById('quests-list');
    const quests = cached.quests || [];

    if (quests.length === 0) {
        questsList.innerHTML = '<p class="empty-state">No quest data available for this act</p>';
        return;
    }

    questsList.innerHTML = quests.map((quest, index) => {
        const questId = `act${act}_${index}`;
        const isCompleted = currentProgress.completed_quests?.includes(questId) || false;
        const importantClass = quest.important ? 'important' : '';

        // Format rewards
        let rewardText = '';
        if (Array.isArray(quest.rewards)) {
            rewardText = quest.rewards.join(', ');
        } else {
            rewardText = quest.rewards;
        }

        return `
            <div class="quest-item ${isCompleted ? 'completed' : ''} ${importantClass}">
                <input
                    type="checkbox"
                    class="quest-checkbox"
                    ${isCompleted ? 'checked' : ''}
                    onchange="toggleQuest('act${act}', ${index})">
                <div class="quest-content">
                    <div class="quest-name">
                        ${escapeHtml(quest.quest)}
                        ${quest.important ? '<span class="quest-important-badge">Important!</span>' : ''}
                    </div>
                    <div class="quest-rewards">Rewards: ${escapeHtml(rewardText)}</div>
                    <div class="quest-location">Location: ${escapeHtml(quest.location)}</div>
                    ${quest.notes ? `<div class="quest-notes">${escapeHtml(quest.notes)}</div>` : ''}
                </div>
            </div>
        `;
    }).join('');
}

function renderLabs() {
    const labsList = document.getElementById('labs-list');

    if (!labsData) {
        labsList.innerHTML = '<p class="empty-state">Loading lab data...</p>';
        return;
    }

    const labs = ['normal', 'cruel', 'merciless', 'eternal'];

    labsList.innerHTML = labs.map(labKey => {
        const lab = labsData[labKey];
        const isCompleted = currentProgress.completed_labs?.includes(labKey) || false;

        let trialsHtml = '';
        if (Array.isArray(lab.trials)) {
            trialsHtml = `
                <div class="lab-trials">
                    <h4>Required Trials (${lab.trials.length}):</h4>
                    ${lab.trials.map((trial, idx) => {
                        const trialId = `${labKey}_${idx}`;
                        const trialCompleted = currentProgress.completed_trials?.includes(trialId) || false;

                        return `
                            <div class="trial-item ${trialCompleted ? 'completed' : ''}">
                                <input
                                    type="checkbox"
                                    class="trial-checkbox"
                                    ${trialCompleted ? 'checked' : ''}
                                    onchange="toggleTrial('${labKey}', ${idx})">
                                <span class="trial-location">${escapeHtml(trial.location)}</span>
                                <span class="trial-act">Act ${trial.act}</span>
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
        } else if (typeof lab.trials === 'string') {
            trialsHtml = `
                <div class="lab-trials">
                    <h4>Trials:</h4>
                    <p style="color: var(--text-secondary); padding: 10px;">${escapeHtml(lab.trials)}</p>
                </div>
            `;
        }

        return `
            <div class="lab-section ${isCompleted ? 'completed' : ''}">
                <div class="lab-header">
                    <div>
                        <div class="lab-name">${escapeHtml(lab.name)}</div>
                        <div class="lab-level">Recommended Level: ${lab.level}</div>
                    </div>
                    <div class="lab-completion">
                        <label>Completed:</label>
                        <input
                            type="checkbox"
                            ${isCompleted ? 'checked' : ''}
                            onchange="toggleLab('${labKey}')">
                    </div>
                </div>
                <div class="lab-reward">
                    <div class="lab-reward-title">Reward:</div>
                    <div>${escapeHtml(lab.reward)}</div>
                </div>
                ${lab.notes ? `<p style="color: var(--text-secondary); margin-bottom: 15px;">${escapeHtml(lab.notes)}</p>` : ''}
                ${trialsHtml}
            </div>
        `;
    }).join('');
}

async function toggleQuest(act, questIndex) {
    if (!currentBuild) return;

    try {
        const data = await apiCall(`/progress/${currentBuild.id}/quest/${act}/${questIndex}`, 'POST');
        currentProgress.completed_quests = data.completed_quests;

        // Re-render quests for current act
        const currentAct = parseInt(document.getElementById('quest-act-select').value);
        renderQuests(currentAct);
    } catch (error) {
        console.error('Failed to toggle quest:', error);
    }
}

async function toggleTrial(lab, trialIndex) {
    if (!currentBuild) return;

    try {
        const data = await apiCall(`/progress/${currentBuild.id}/trial/${lab}/${trialIndex}`, 'POST');
        currentProgress.completed_trials = data.completed_trials;
        renderLabs();
    } catch (error) {
        console.error('Failed to toggle trial:', error);
    }
}

async function toggleLab(lab) {
    if (!currentBuild) return;

    try {
        const data = await apiCall(`/progress/${currentBuild.id}/lab/${lab}`, 'POST');
        currentProgress.completed_labs = data.completed_labs;
        renderLabs();
    } catch (error) {
        console.error('Failed to toggle lab:', error);
    }
}

// ========================================
// SCUMM-Style Pixel Art Generator
// ========================================

let pixelArtPresets = [];
let pixelArtPalettes = [];
let currentPixelArt = null;

async function initPixelArtGenerator() {
    try {
        // Load available presets and palettes
        const data = await apiCall('/pixel-art/presets');
        pixelArtPresets = data.presets;
        pixelArtPalettes = data.palettes;

        // Populate preset dropdown
        const presetSelect = document.getElementById('preset-select');
        presetSelect.innerHTML = '<option value="">-- Select a Preset Scene --</option>';

        pixelArtPresets.forEach(preset => {
            const option = document.createElement('option');
            option.value = preset.id;
            option.textContent = preset.name;
            presetSelect.appendChild(option);
        });

        // Populate palette dropdown
        const paletteSelect = document.getElementById('palette-select');
        paletteSelect.innerHTML = '';
        pixelArtPalettes.forEach(palette => {
            const option = document.createElement('option');
            option.value = palette;
            option.textContent = formatPaletteName(palette);
            paletteSelect.appendChild(option);
        });

        // Populate presets info list
        const presetsInfo = document.getElementById('presets-info');
        presetsInfo.innerHTML = '';
        pixelArtPresets.forEach(preset => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${preset.name}:</strong> ${preset.description}`;
            presetsInfo.appendChild(li);
        });

        // Add event listeners
        document.getElementById('generate-btn').addEventListener('click', generatePixelArt);
        document.getElementById('download-art-btn').addEventListener('click', downloadPixelArt);

    } catch (error) {
        console.error('Failed to initialize pixel art generator:', error);
    }
}

function formatPaletteName(palette) {
    // Convert snake_case to Title Case
    return palette
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

async function generatePixelArt() {
    const presetSelect = document.getElementById('preset-select');
    const paletteSelect = document.getElementById('palette-select');
    const generateBtn = document.getElementById('generate-btn');
    const previewDiv = document.getElementById('pixel-art-preview');

    const scene = presetSelect.value;
    const palette = paletteSelect.value;

    if (!scene) {
        previewDiv.innerHTML = '<p class="empty-state" style="color: #dc2626;">Please select a preset scene first!</p>';
        return;
    }

    // Show loading state
    generateBtn.disabled = true;
    generateBtn.textContent = 'Generating...';
    previewDiv.innerHTML = '<div class="loading"></div>';

    try {
        const data = await apiCall('/pixel-art/generate/preset', 'POST', {
            scene: scene,
            palette: palette
        });

        if (data.success) {
            currentPixelArt = data.image;

            // Display the generated image
            previewDiv.innerHTML = `
                <img src="${data.image}" alt="${scene}" class="animate">
            `;

            // Show download button
            document.getElementById('download-art-btn').style.display = 'inline-block';

            // Show success message
            const sceneName = pixelArtPresets.find(p => p.id === scene)?.name || scene;
            const paletteName = formatPaletteName(palette);

            // Add a success indicator
            previewDiv.insertAdjacentHTML('beforeend', `
                <div style="position: absolute; top: 10px; right: 10px; background: rgba(22, 163, 74, 0.9); color: white; padding: 8px 16px; border-radius: 6px; font-weight: 500;">
                    ✓ Generated!
                </div>
            `);

            setTimeout(() => {
                const indicator = previewDiv.querySelector('div[style*="position: absolute"]');
                if (indicator) indicator.remove();
            }, 3000);

        } else {
            throw new Error('Generation failed');
        }

    } catch (error) {
        console.error('Failed to generate pixel art:', error);
        previewDiv.innerHTML = `
            <p class="empty-state" style="color: #dc2626;">
                Failed to generate pixel art. Please try again.
            </p>
        `;
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate Pixel Art';
    }
}

function downloadPixelArt() {
    if (!currentPixelArt) return;

    const presetSelect = document.getElementById('preset-select');
    const paletteSelect = document.getElementById('palette-select');
    const scene = presetSelect.value;
    const palette = paletteSelect.value;

    // Create a temporary link element
    const link = document.createElement('a');
    link.href = currentPixelArt;
    link.download = `scumm_${scene}_${palette}.png`;

    // Trigger download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Show feedback
    const downloadBtn = document.getElementById('download-art-btn');
    const originalText = downloadBtn.textContent;
    downloadBtn.textContent = '✓ Downloaded!';
    downloadBtn.style.background = '#15803d';

    setTimeout(() => {
        downloadBtn.textContent = originalText;
        downloadBtn.style.background = '';
    }, 2000);
}

// Make functions globally accessible
window.loadBuildDetails = loadBuildDetails;
window.toggleMilestone = toggleMilestone;
window.toggleQuest = toggleQuest;
window.toggleTrial = toggleTrial;
window.toggleLab = toggleLab;
