# TODO What kind of python I want to use
FROM python:3-alpine3.15

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install -r requirements.txt

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Which port to expose: Flask likes to use 5000, defined in app.py
EXPOSE 5000

# Run the command to start the Flask application
CMD ["python", "app.py"]
