# Use the official Python image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Django runs on
EXPOSE 8000

# Run migrations and start the Django server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecommercePrj.wsgi:application"]
