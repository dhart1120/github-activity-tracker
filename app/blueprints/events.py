from datetime import datetime
from flask import Blueprint, jsonify, request, make_response

from app.services import github_service as github

events_blueprint = Blueprint('v1/repos', __name__, url_prefix='/api/v1/repos')

@events_blueprint.route('<string:repo_owner>/<string:repo_name>/events', methods=['GET'])
def get_repo_events(repo_owner, repo_name):
    def buildFilter():
        # Parse string dates to datetime objects
        start_date_str = request.args.get('start_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
        
        end_date_str = request.args.get('end_date')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
        
        return {
            "event_type": request.args.get('event_type', None),
            "start_date": start_date,
            "end_date": end_date    
        }
    events = github.list_repo_events(f"{repo_owner}/{repo_name}", buildFilter())

    format = request.args.get('format', "json")
    return jsonify({'events': format_many(format, events)})

@events_blueprint.route('<string:repo_owner>/<string:repo_name>/events/<int:event_id>', methods=['GET'])
def get_event(repo_owner, repo_name, event_id):
    format = request.args.get('format', "json")
    event = github.get_event(f"{repo_owner}/{repo_name}", event_id)
    if not event:
         return make_response(jsonify({"error": "Event not found"}), 404)

    return jsonify(format_one(format, event))    

def format_one(format, event):
    match format:
        case "raw":
            return event.to_raw()
        case "summary":
            return event.summary()
        case _:
            return event.to_json()
        
def format_many(format, events):
    return list(map(lambda evt: format_one(format, evt), events))