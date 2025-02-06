from flaskapp import app 

# Dockerize and run app
if __name__ == "__main__":
    # Run app on port 5000 outside of the container
    app.run(host='0.0.0.0', port=5000, debug=True)