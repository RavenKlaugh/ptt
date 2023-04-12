# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
RUN apt-get -y update
RUN apt-get install -y curl unzip git

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

RUN apt-get install -y ffmpeg

RUN pip install git+https://github.com/openai/whisper.git 

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=ptt3.py

# Run your_script_name.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
