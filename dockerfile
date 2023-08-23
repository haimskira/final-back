# Base image
FROM python:3.9

# Set up the working directory and copy the Django project files
WORKDIR /backend
COPY ./epsealon /backend

# Install dependencies using pip
RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose the necessary port
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
