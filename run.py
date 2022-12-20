from app import create_app, db
from flask_migrate import Migrate

app = create_app()
Migrate(app, db, render_as_batch=True)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
