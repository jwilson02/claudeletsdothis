// Path of Exile Build Guide - Main JavaScript

// State management
let currentBuild = null;
let currentProgress = null;

// API base URL
const API_BASE = '/api';

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadBuilds();
});

// Event Listeners
function initializeEventListeners() {
    // Import button
    document.getElementById('import-btn').addEventListener('click', importBuild);

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

// Make functions globally accessible
window.loadBuildDetails = loadBuildDetails;
window.toggleMilestone = toggleMilestone;
