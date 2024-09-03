from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from celery import Celery
from integrated_network_tools import IntegratedNetworkTools
from target_acquisition_module import TargetAcquisition
import json
import os
from datetime import datetime
import ipaddress

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

integrated_tools = IntegratedNetworkTools()
target_acquisition = TargetAcquisition()

@celery.task(bind=True)
def run_scan(self, targets, options):
    try:
        results = {}
        total_targets = len(targets)
        for i, target in enumerate(targets):
            target_results = integrated_tools.comprehensive_scan([target], options)
            results[target] = target_results
            self.update_state(state='PROGRESS',
                              meta={'current': i + 1, 'total': total_targets,
                                    'status': f'Scanning target {i + 1} of {total_targets}'})
            socketio.emit('scan_progress', {'current': i + 1, 'total': total_targets,
                                            'status': f'Scanning target {i + 1} of {total_targets}'})
        
        report_id = save_report(results)
        return {'status': 'Task completed!', 'report_id': report_id}
    except Exception as e:
        return {'status': 'Task failed!', 'error': str(e)}

@app.route('/api/integrated-scan', methods=['POST'])
def start_integrated_scan():
    try:
        data = request.json
        targets = data['targets']
        options = data.get('options', {})

        valid_targets = []
        for target in targets:
            try:
                if target.startswith('http'):
                    valid_targets.append(target)
                else:
                    ipaddress.ip_address(target)
                    valid_targets.append(target)
            except ValueError:
                pass

        if not valid_targets:
            return jsonify({"error": "No valid targets provided"}), 400

        task = run_scan.apply_async(args=[valid_targets, options])

        return jsonify({"message": "Scan started", "task_id": task.id}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scan-status/<task_id>')
def scan_status(task_id):
    task = run_scan.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Scan is pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'report_id' in task.info:
            response['report_id'] = task.info['report_id']
    else:
        response = {
            'state': task.state,
            'status': str(task.info),
        }
    return jsonify(response)

@app.route('/api/save-settings', methods=['POST'])
def save_settings():
    try:
        settings = request.json
        user_id = settings.get('user_id', 'default')
        filename = f"settings_{user_id}.json"
        
        with open(filename, 'w') as f:
            json.dump(settings, f)
        
        return jsonify({"message": "Settings saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/load-settings', methods=['GET'])
def load_settings():
    try:
        user_id = request.args.get('user_id', 'default')
        filename = f"settings_{user_id}.json"
        
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                settings = json.load(f)
            return jsonify(settings)
        else:
            return jsonify({"message": "No saved settings found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    try:
        filename = f"report_{report_id}.json"
        if os.path.exists(filename):
            return send_file(filename, as_attachment=True)
        else:
            return jsonify({"error": "Report not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    try:
        reports = []
        for filename in os.listdir():
            if filename.startswith("report_") and filename.endswith(".json"):
                with open(filename, 'r') as f:
                    report_data = json.load(f)
                    reports.append({
                        'id': filename[7:-5],  # Remove "report_" prefix and ".json" suffix
                        'name': report_data.get('name', 'Unnamed Report'),
                        'date': report_data.get('date', ''),
                        'targets': report_data.get('targets', [])
                    })
        return jsonify(reports)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def save_report(results):
    report_id = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"report_{report_id}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f)
    
    return report_id

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)