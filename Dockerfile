FROM python:3

ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /django

# Copy the requirements file to the container
COPY requirements.txt requirements.txt

# Install project dependencies
RUN pip3 install -r requirements.txt

# Copy the Django project files to the container
COPY . .

CMD python manage.py runserver 0.0.0.0:8000
