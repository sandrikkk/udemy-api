FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of your application code
COPY . /app

# Make the entrypoint script executable
COPY scripts/docker-entrypoint.sh /app/scripts/docker-entrypoint.sh
COPY scripts/check_service.py /app/scripts/check_service.py
RUN chmod +x /app/scripts/docker-entrypoint.sh


# Set the entrypoint for the container
ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]
EXPOSE 8000
