# Use the official Python base image with version 3.10
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire current directory into the container
COPY . .

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Set the entrypoint command to run the Streamlit application
ENTRYPOINT ["streamlit", "run"]

# Specify the default command to execute when the container starts
CMD ["app.py"]