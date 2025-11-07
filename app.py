"""
Path of Exile Build Guide Tool
Main Flask application
"""
import json
import os
import threading
import time
import webbrowser
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pob_parser import PoBParser

app = Flask(__name__)
CORS(app)

# Data storage
DATA_DIR = 'data'
BUILDS_FILE = os.path.join(DATA_DIR, 'builds.json')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def load_json_file(filepath, default=None):
    """Load JSON file or return default"""
    if default is None:
        default = {}
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
    return default


def save_json_file(filepath, data):
    """Save data to JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/builds', methods=['GET'])
def get_builds():
    """Get all saved builds"""
    builds = load_json_file(BUILDS_FILE, default=[])
    return jsonify({'builds': builds})


@app.route('/api/builds/<build_id>', methods=['GET'])
def get_build(build_id):
    """Get a specific build"""
    builds = load_json_file(BUILDS_FILE, default=[])
    build = next((b for b in builds if b.get('id') == build_id), None)

    if not build:
        return jsonify({'error': 'Build not found'}), 404

    # Get progress for this build
    progress = load_json_file(PROGRESS_FILE, default={})
    build_progress = progress.get(build_id, {})

    return jsonify({
        'build': build,
        'progress': build_progress
    })


@app.route('/api/builds', methods=['POST'])
def import_build():
    """Import a new build from PoB code"""
    data = request.get_json()
    pob_code = data.get('pob_code', '').strip()

    if not pob_code:
        return jsonify({'error': 'No PoB code provided'}), 400

    try:
        parser = PoBParser()
        build_data = parser.parse_pob_code(pob_code)

        # Add metadata
        build_id = datetime.now().strftime('%Y%m%d%H%M%S')
        build_data['id'] = build_id
        build_data['created_at'] = datetime.now().isoformat()
        build_data['pob_code'] = pob_code
        build_data['milestones'] = parser.get_leveling_milestones()

        # Save to builds
        builds = load_json_file(BUILDS_FILE, default=[])
        builds.append(build_data)
        save_json_file(BUILDS_FILE, builds)

        # Initialize progress
        progress = load_json_file(PROGRESS_FILE, default={})
        progress[build_id] = {
            'current_level': 1,
            'current_act': 1,
            'completed_milestones': [],
            'completed_gems': [],
            'equipped_items': []
        }
        save_json_file(PROGRESS_FILE, progress)

        return jsonify({
            'success': True,
            'build_id': build_id,
            'build': build_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/builds/<build_id>', methods=['DELETE'])
def delete_build(build_id):
    """Delete a build"""
    builds = load_json_file(BUILDS_FILE, default=[])
    builds = [b for b in builds if b.get('id') != build_id]
    save_json_file(BUILDS_FILE, builds)

    # Delete progress
    progress = load_json_file(PROGRESS_FILE, default={})
    if build_id in progress:
        del progress[build_id]
        save_json_file(PROGRESS_FILE, progress)

    return jsonify({'success': True})


@app.route('/api/progress/<build_id>', methods=['POST'])
def update_progress(build_id):
    """Update build progress"""
    data = request.get_json()

    progress = load_json_file(PROGRESS_FILE, default={})

    if build_id not in progress:
        progress[build_id] = {
            'current_level': 1,
            'current_act': 1,
            'completed_milestones': [],
            'completed_gems': [],
            'equipped_items': []
        }

    # Update progress
    if 'current_level' in data:
        progress[build_id]['current_level'] = data['current_level']
    if 'current_act' in data:
        progress[build_id]['current_act'] = data['current_act']
    if 'completed_milestones' in data:
        progress[build_id]['completed_milestones'] = data['completed_milestones']
    if 'completed_gems' in data:
        progress[build_id]['completed_gems'] = data['completed_gems']
    if 'equipped_items' in data:
        progress[build_id]['equipped_items'] = data['equipped_items']

    save_json_file(PROGRESS_FILE, progress)

    return jsonify({'success': True, 'progress': progress[build_id]})


@app.route('/api/progress/<build_id>/milestone/<int:milestone_index>', methods=['POST'])
def toggle_milestone(build_id, milestone_index):
    """Toggle a milestone completion"""
    progress = load_json_file(PROGRESS_FILE, default={})

    if build_id not in progress:
        return jsonify({'error': 'Build not found'}), 404

    completed = progress[build_id].get('completed_milestones', [])

    if milestone_index in completed:
        completed.remove(milestone_index)
    else:
        completed.append(milestone_index)

    progress[build_id]['completed_milestones'] = completed
    save_json_file(PROGRESS_FILE, progress)

    return jsonify({'success': True, 'completed_milestones': completed})


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')


if __name__ == '__main__':
    print("=" * 60)
    print("Path of Exile Build Guide Tool")
    print("=" * 60)
    print("\nServer starting on http://localhost:5000")
    print("Opening browser automatically...")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)

    # Open browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
