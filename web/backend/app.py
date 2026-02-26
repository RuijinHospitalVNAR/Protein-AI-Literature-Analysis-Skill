from flask import Flask, jsonify, request, send_from_directory
import json
import os
import datetime

app = Flask(__name__, static_folder='../', static_url_path='')

# Data directories
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
PAPERS_FILE = os.path.join(DATA_DIR, 'improved_papers.json')
ANALYZED_FILE = os.path.join(DATA_DIR, 'improved_analyzed_papers.json')

# Helper function to load data
def load_json_file(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

# Helper function to save data
def save_json_file(file_path, data):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

# API endpoints

@app.route('/api/papers', methods=['GET'])
def get_papers():
    """Get all papers"""
    papers = load_json_file(PAPERS_FILE)
    return jsonify(papers)

@app.route('/api/analyzed', methods=['GET'])
def get_analyzed_data():
    """Get analyzed data"""
    analyzed_data = load_json_file(ANALYZED_FILE)
    return jsonify(analyzed_data)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    papers = load_json_file(PAPERS_FILE)
    analyzed_data = load_json_file(ANALYZED_FILE)
    
    stats = {
        'total_papers': len(papers),
        'average_score': analyzed_data.get('average_importance_score', 0),
        'category_counts': analyzed_data.get('category_counts', {}),
        'last_updated': datetime.datetime.now().isoformat()
    }
    
    return jsonify(stats)

@app.route('/api/search', methods=['GET'])
def search_papers():
    """Search papers"""
    query = request.args.get('q', '').lower()
    papers = load_json_file(PAPERS_FILE)
    
    results = []
    for paper in papers:
        if (
            query in paper.get('title', '').lower() or
            (paper.get('abstract') and query in paper.get('abstract').lower()) or
            (paper.get('authors') and any(query in author.lower() for author in paper.get('authors')))
        ):
            results.append(paper)
    
    return jsonify(results)

@app.route('/api/filter', methods=['GET'])
def filter_papers():
    """Filter papers by category, time, and source"""
    category = request.args.get('category', 'all')
    time_range = request.args.get('time', 'all')
    source = request.args.get('source', 'all')
    
    papers = load_json_file(PAPERS_FILE)
    analyzed_data = load_json_file(ANALYZED_FILE)
    
    # Create paper lookup by title
    paper_lookup = {paper['title']: paper for paper in papers}
    
    # Apply filters
    filtered_papers = []
    for paper in papers:
        # Apply source filter
        if source != 'all' and paper.get('source') != source:
            continue
        
        # Apply time filter
        if time_range != 'all':
            pub_date = paper.get('publication_date')
            if not pub_date:
                continue
            
            # Parse publication date
            try:
                pub_date_obj = datetime.datetime.strptime(pub_date, '%Y-%m-%d')
            except:
                try:
                    pub_date_obj = datetime.datetime.strptime(pub_date, '%Y-%b')
                except:
                    try:
                        pub_date_obj = datetime.datetime.strptime(pub_date, '%Y')
                    except:
                        continue
            
            # Calculate time cutoff
            now = datetime.datetime.now()
            if time_range == 'last-month':
                cutoff = now - datetime.timedelta(days=30)
            elif time_range == 'last-3months':
                cutoff = now - datetime.timedelta(days=90)
            elif time_range == 'last-6months':
                cutoff = now - datetime.timedelta(days=180)
            elif time_range == 'last-year':
                cutoff = now - datetime.timedelta(days=365)
            else:
                cutoff = datetime.datetime.min
            
            if pub_date_obj < cutoff:
                continue
        
        # Apply category filter
        if category != 'all':
            # Find paper in analyzed data
            analyzed_paper = None
            for p in analyzed_data.get('papers', []):
                if p['title'] == paper['title']:
                    analyzed_paper = p
                    break
            
            if not analyzed_paper or category not in analyzed_paper.get('classifications', []):
                continue
        
        filtered_papers.append(paper)
    
    return jsonify(filtered_papers)

# Static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    if path == '':
        return send_from_directory(app.static_folder, 'index.html')
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
