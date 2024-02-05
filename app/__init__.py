from flask import Flask
from app.blueprints.events import events_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(events_blueprint)
    
    @app.route('/', methods=['GET'])
    def get_home():
        return """
    You probably want <a href="http://127.0.0.1:5000/api/v1/repos/{repo_name}/events">/api/v1/repos/{repo_name}/events</a>
    """
    
    with app.app_context():
        print("Registered URLs:")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule}")

    return app