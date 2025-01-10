from flask import Flask, render_template

app = Flask(__name__)

# Homepage route
@app.route("/")
def index():
    return render_template("index.html")

# Dockerize app
if __name__ == "__main__":
    # Make sure the app is running on port 5000 outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)