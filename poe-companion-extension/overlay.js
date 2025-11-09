const { ipcRenderer } = require('electron');

// API Configuration
const API_BASE = 'http://localhost:5000/api';

// State
let currentBuild = null;
let currentProgress = null;
let questsCache = {};
let labsData = null;
let isCompactMode = false;

// DOM Elements
const importSection = document.getElementById('importSection');
const buildSection = document.getElementById('buildSection');
const pobInput = document.getElementById('pobInput');
const importBtn = document.getElementById('importBtn');
const loadDemoBtn = document.getElementById('loadDemoBtn');
const importStatus = document.getElementById('importStatus');
const contentArea = document.getElementById('contentArea');
const compactView = document.getElementById('compactView');

// Build info elements
const buildName = document.getElementById('buildName');
const buildClass = document.getElementById('buildClass');
const buildLevel = document.getElementById('buildLevel');
const levelInput = document.getElementById('levelInput');
const actSelect = document.getElementById('actSelect');

// Content sections
const questList = document.getElementById('questList');
const actTips = document.getElementById('actTips');
const skillsList = document.getElementById('skillsList');
const gearList = document.getElementById('gearList');
const labList = document.getElementById('labList');
const treeInfo = document.getElementById('treeInfo');
const milestoneList = document.getElementById('milestoneList');

// Compact mode elements
const compactBuildName = document.getElementById('compactBuildName');
const compactLevel = document.getElementById('compactLevel');
const compactAct = document.getElementById('compactAct');
const compactQuests = document.getElementById('compactQuests');

// Header controls
document.getElementById('minimizeBtn').addEventListener('click', () => {
  ipcRenderer.send('minimize-window');
});

document.getElementById('closeBtn').addEventListener('click', () => {
  ipcRenderer.send('close-window');
});

document.getElementById('compactBtn').addEventListener('click', () => {
  toggleCompactMode();
});

document.getElementById('expandBtn').addEventListener('click', () => {
  toggleCompactMode();
});

// Import handlers
importBtn.addEventListener('click', importBuild);
loadDemoBtn.addEventListener('click', loadDemoBuild);
pobInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    importBuild();
  }
});

// Progress handlers
levelInput.addEventListener('change', updateProgress);
actSelect.addEventListener('change', onActChange);

// Accordion functionality
document.querySelectorAll('.accordion-header').forEach(header => {
  header.addEventListener('click', () => {
    const target = header.getAttribute('data-target');
    const content = document.getElementById(target);

    // Toggle active class
    if (content.classList.contains('active')) {
      content.classList.remove('active');
    } else {
      // Close other accordions (optional)
      // document.querySelectorAll('.accordion-content').forEach(c => c.classList.remove('active'));
      content.classList.add('active');
    }
  });
});

// API Functions
async function apiCall(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

// Import build from PoB code
async function importBuild() {
  const pobCode = pobInput.value.trim();

  if (!pobCode) {
    showStatus('Please enter a PoB code or URL', 'error');
    return;
  }

  try {
    showStatus('Importing build...', 'info');

    const result = await apiCall('/builds', {
      method: 'POST',
      body: JSON.stringify({ pob_code: pobCode })
    });

    if (result.success) {
      showStatus('Build imported successfully!', 'success');
      pobInput.value = '';
      await loadBuild(result.build_id);
    } else {
      showStatus(result.message || 'Failed to import build', 'error');
    }
  } catch (error) {
    showStatus(`Error: ${error.message}`, 'error');
  }
}

// Load demo build
async function loadDemoBuild() {
  try {
    showStatus('Loading demo build...', 'info');

    const result = await apiCall('/builds/demo', {
      method: 'POST'
    });

    if (result.success) {
      showStatus('Demo build loaded!', 'success');
      await loadBuild(result.build_id);
    } else {
      showStatus('Failed to load demo build', 'error');
    }
  } catch (error) {
    showStatus(`Error: ${error.message}`, 'error');
  }
}

// Load build by ID
async function loadBuild(buildId) {
  try {
    const build = await apiCall(`/builds/${buildId}`);
    currentBuild = build;

    // Try to load progress
    try {
      currentProgress = await apiCall(`/progress/${buildId}`);
    } catch (e) {
      // Create initial progress
      currentProgress = {
        build_id: buildId,
        level: 1,
        act: 1,
        completed_milestones: [],
        completed_quests: {},
        completed_trials: {},
        completed_labs: []
      };
    }

    displayBuild();
    saveState();
  } catch (error) {
    showStatus(`Failed to load build: ${error.message}`, 'error');
  }
}

// Display build information
function displayBuild() {
  if (!currentBuild) return;

  // Show build section, hide import
  importSection.classList.add('hidden');
  buildSection.classList.remove('hidden');

  // Update build info
  buildName.textContent = currentBuild.name || 'Unnamed Build';
  buildClass.textContent = `${currentBuild.class}${currentBuild.ascendancy ? ' - ' + currentBuild.ascendancy : ''}`;
  buildLevel.textContent = `Level ${currentBuild.level || 100}`;

  // Update progress controls
  levelInput.value = currentProgress.level || 1;
  actSelect.value = currentProgress.act || 1;

  // Load and display sections
  displaySkills();
  displayGear();
  displayTree();
  displayMilestones();
  loadQuestsForAct(currentProgress.act || 1);
  loadActTips(currentProgress.act || 1);
  loadLabs();

  // Update compact view
  updateCompactView();
}

// Display skills
function displaySkills() {
  if (!currentBuild.skills || currentBuild.skills.length === 0) {
    skillsList.innerHTML = '<p class="loading">No skill information available</p>';
    return;
  }

  let html = '';
  currentBuild.skills.forEach(skillGroup => {
    html += `
      <div class="skill-group">
        <div class="skill-group-name">${skillGroup.slot || 'Skill Setup'}</div>
        <div class="gem-list">
          ${skillGroup.gems.map(gem => `
            <span class="gem">${gem.name}${gem.level ? ' L' + gem.level : ''}</span>
          `).join('')}
        </div>
      </div>
    `;
  });

  skillsList.innerHTML = html;
}

// Display gear
function displayGear() {
  if (!currentBuild.items || currentBuild.items.length === 0) {
    gearList.innerHTML = '<p class="loading">No gear information available</p>';
    return;
  }

  let html = '';
  currentBuild.items.forEach(item => {
    html += `
      <div class="gear-item">
        <div class="gear-slot">${item.slot}</div>
        <div class="gear-name">${item.name}</div>
      </div>
    `;
  });

  gearList.innerHTML = html;
}

// Display passive tree info
function displayTree() {
  if (!currentBuild.tree) {
    treeInfo.innerHTML = '<p class="loading">No passive tree information available</p>';
    return;
  }

  const nodeCount = currentBuild.tree.nodes ? currentBuild.tree.nodes.length : 0;
  treeInfo.innerHTML = `
    <p>Tree Version: ${currentBuild.tree.version || 'Unknown'}</p>
    <p>Allocated Nodes: ${nodeCount}</p>
    <p style="margin-top: 8px; color: #888; font-size: 11px;">
      View full tree in Path of Building for detailed node information.
    </p>
  `;
}

// Display milestones
function displayMilestones() {
  if (!currentBuild.milestones || currentBuild.milestones.length === 0) {
    milestoneList.innerHTML = '<p class="loading">No milestones available</p>';
    return;
  }

  let html = '';
  currentBuild.milestones.forEach((milestone, index) => {
    const isCompleted = currentProgress.completed_milestones?.includes(index) || false;
    html += `
      <div class="milestone-item ${isCompleted ? 'completed' : ''}">
        <input type="checkbox"
               class="milestone-checkbox"
               data-index="${index}"
               ${isCompleted ? 'checked' : ''}
               onchange="toggleMilestone(${index})">
        <span class="milestone-text">${milestone}</span>
      </div>
    `;
  });

  milestoneList.innerHTML = html;
}

// Load quests for act
async function loadQuestsForAct(act) {
  try {
    if (!questsCache[act]) {
      questsCache[act] = await apiCall(`/game-data/quests/${act}`);
    }

    displayQuests(act);
  } catch (error) {
    questList.innerHTML = `<p class="loading">Failed to load quests: ${error.message}</p>`;
  }
}

// Display quests
function displayQuests(act) {
  const quests = questsCache[act];
  if (!quests || quests.length === 0) {
    questList.innerHTML = '<p class="loading">No quests for this act</p>';
    return;
  }

  const completedQuests = currentProgress.completed_quests?.[act] || [];

  let html = '';
  quests.forEach((quest, index) => {
    const isCompleted = completedQuests.includes(index);
    html += `
      <div class="quest-item ${isCompleted ? 'completed' : ''}">
        <div class="quest-header">
          <span class="quest-name">${quest.name}</span>
          <input type="checkbox"
                 class="quest-checkbox"
                 data-act="${act}"
                 data-index="${index}"
                 ${isCompleted ? 'checked' : ''}
                 onchange="toggleQuest(${act}, ${index})">
        </div>
        <div class="quest-reward">${quest.reward}</div>
        ${quest.important ? `<div class="quest-important">⚠️ ${quest.important}</div>` : ''}
      </div>
    `;
  });

  questList.innerHTML = html;
  updateCompactView();
}

// Load act tips
async function loadActTips(act) {
  try {
    const tips = await apiCall(`/game-data/tips/${act}`);

    if (tips && tips.length > 0) {
      let html = '<ul style="margin-left: 20px; line-height: 1.6;">';
      tips.forEach(tip => {
        html += `<li style="margin-bottom: 6px; color: #e5e5e5;">${tip}</li>`;
      });
      html += '</ul>';
      actTips.innerHTML = html;
    } else {
      actTips.innerHTML = '<p class="loading">No tips available for this act</p>';
    }
  } catch (error) {
    actTips.innerHTML = `<p class="loading">Failed to load tips: ${error.message}</p>`;
  }
}

// Load labs
async function loadLabs() {
  try {
    if (!labsData) {
      labsData = await apiCall('/game-data/labs');
    }

    displayLabs();
  } catch (error) {
    labList.innerHTML = `<p class="loading">Failed to load lab data: ${error.message}</p>`;
  }
}

// Display labs
function displayLabs() {
  if (!labsData) return;

  const completedLabs = currentProgress.completed_labs || [];

  let html = '';
  Object.entries(labsData).forEach(([labName, labInfo]) => {
    const isCompleted = completedLabs.includes(labName);
    html += `
      <div class="lab-item">
        <div class="lab-name">
          <input type="checkbox"
                 style="margin-right: 8px;"
                 ${isCompleted ? 'checked' : ''}
                 onchange="toggleLab('${labName}')">
          ${labName} Lab (Level ${labInfo.level})
        </div>
        <div style="margin-top: 4px; color: #fbbf24; font-size: 12px;">
          Reward: ${labInfo.reward}
        </div>
        <div class="lab-trials">
          Trials: ${labInfo.trials.join(', ')}
        </div>
      </div>
    `;
  });

  labList.innerHTML = html;
}

// Toggle milestone
window.toggleMilestone = async function(index) {
  if (!currentProgress.completed_milestones) {
    currentProgress.completed_milestones = [];
  }

  const idx = currentProgress.completed_milestones.indexOf(index);
  if (idx > -1) {
    currentProgress.completed_milestones.splice(idx, 1);
  } else {
    currentProgress.completed_milestones.push(index);
  }

  await saveProgress();
  displayMilestones();
};

// Toggle quest
window.toggleQuest = async function(act, index) {
  if (!currentProgress.completed_quests) {
    currentProgress.completed_quests = {};
  }
  if (!currentProgress.completed_quests[act]) {
    currentProgress.completed_quests[act] = [];
  }

  const idx = currentProgress.completed_quests[act].indexOf(index);
  if (idx > -1) {
    currentProgress.completed_quests[act].splice(idx, 1);
  } else {
    currentProgress.completed_quests[act].push(index);
  }

  await saveProgress();
  displayQuests(act);
};

// Toggle lab
window.toggleLab = async function(labName) {
  if (!currentProgress.completed_labs) {
    currentProgress.completed_labs = [];
  }

  const idx = currentProgress.completed_labs.indexOf(labName);
  if (idx > -1) {
    currentProgress.completed_labs.splice(idx, 1);
  } else {
    currentProgress.completed_labs.push(labName);
  }

  await saveProgress();
  displayLabs();
};

// Update progress (level/act change)
async function updateProgress() {
  if (!currentProgress) return;

  currentProgress.level = parseInt(levelInput.value);
  currentProgress.act = parseInt(actSelect.value);

  await saveProgress();
  updateCompactView();
}

// Handle act change
function onActChange() {
  const newAct = parseInt(actSelect.value);
  currentProgress.act = newAct;

  loadQuestsForAct(newAct);
  loadActTips(newAct);
  updateProgress();
}

// Save progress to backend
async function saveProgress() {
  if (!currentBuild || !currentProgress) return;

  try {
    await apiCall(`/progress/${currentBuild.id}`, {
      method: 'POST',
      body: JSON.stringify(currentProgress)
    });
    saveState();
  } catch (error) {
    console.error('Failed to save progress:', error);
  }
}

// Toggle compact mode
function toggleCompactMode() {
  isCompactMode = !isCompactMode;

  if (isCompactMode) {
    contentArea.classList.add('hidden');
    compactView.classList.remove('hidden');
    updateCompactView();
  } else {
    contentArea.classList.remove('hidden');
    compactView.classList.add('hidden');
  }

  saveState();
}

// Update compact view
function updateCompactView() {
  if (!currentBuild || !currentProgress) {
    compactBuildName.textContent = 'No Build Loaded';
    compactLevel.textContent = 'Lv1';
    compactAct.textContent = 'Act 1';
    compactQuests.innerHTML = '<p>Import a build to get started</p>';
    return;
  }

  compactBuildName.textContent = currentBuild.name || 'Build';
  compactLevel.textContent = `Lv${currentProgress.level}`;
  compactAct.textContent = `Act ${currentProgress.act}`;

  // Show incomplete quests for current act
  const act = currentProgress.act;
  const quests = questsCache[act] || [];
  const completedQuests = currentProgress.completed_quests?.[act] || [];

  let html = '';
  quests.forEach((quest, index) => {
    const isCompleted = completedQuests.includes(index);
    html += `
      <div class="compact-quest ${isCompleted ? 'completed' : ''}">
        ${isCompleted ? '✓' : '○'} ${quest.name}
      </div>
    `;
  });

  if (html === '') {
    html = '<p>No quests for this act</p>';
  }

  compactQuests.innerHTML = html;
}

// Show status message
function showStatus(message, type = 'info') {
  importStatus.textContent = message;
  importStatus.className = `status-message ${type}`;

  if (type === 'success') {
    setTimeout(() => {
      importStatus.textContent = '';
      importStatus.className = 'status-message';
    }, 3000);
  }
}

// Save state to electron-store
function saveState() {
  const state = {
    currentBuildId: currentBuild?.id,
    isCompactMode: isCompactMode
  };
  ipcRenderer.send('save-state', state);
}

// Load state from electron-store
async function loadState() {
  const state = await ipcRenderer.invoke('load-state');
  if (state) {
    isCompactMode = state.isCompactMode || false;

    if (state.currentBuildId) {
      await loadBuild(state.currentBuildId);
    }

    if (isCompactMode) {
      toggleCompactMode();
    }
  }
}

// Listen for compact mode toggle from main process
ipcRenderer.on('toggle-compact-mode', (event, compact) => {
  if (compact !== isCompactMode) {
    toggleCompactMode();
  }
});

// Check backend connection on startup
async function checkBackendConnection() {
  try {
    await fetch(`${API_BASE}/builds`);
    console.log('Backend connection successful');
    return true;
  } catch (error) {
    showStatus('⚠️ Backend not running! Start the Flask server (port 5000)', 'error');
    return false;
  }
}

// Initialize
window.addEventListener('DOMContentLoaded', async () => {
  await checkBackendConnection();
  await loadState();
});
