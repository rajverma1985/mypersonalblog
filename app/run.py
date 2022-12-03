from app import app

if __name__ == "__main__":
    from app.main import main
    app.run(debug=True, port='5000')
