# Comments Project

This is a Django-based project that implements a simple comment system with API endpoints. The project includes functionalities such as posting comments, replying to comments, and performing CRUD operations on the comments via a RESTful API.

## Features

- **Comment Posting**: Users can post comments and reply to existing comments.
- **Comment Display**: Comments are displayed in a paginated list, with sorting options available.
- **CRUD Operations**: Create, Read, Update, and Delete operations can be performed on comments via the API.
- **Validation and Security**: Comments are sanitized to remove unwanted HTML tags and attributes.
- **API Documentation**: The project uses Swagger and Redoc to provide detailed API documentation.

## Technologies Used

- **Django**: Web framework used for building the application.
- **Django REST Framework (DRF)**: Used for creating RESTful API endpoints.
- **drf-yasg**: Automatically generates Swagger and ReDoc API documentation.
- **Bleach**: Used to sanitize and clean the content of the comments.
- **Faker**: Used to generate fake data for testing purposes.
- **Freezegun**: Used to mock the current time in tests.
- **Docker**: Containerization of the application.
- **Poetry**: Dependency management and packaging tool.

## Installation

### Prerequisites

- Python 3.10+
- Docker
- Poetry

### Steps

1. **Clone the repository**:

    ```bash
    git clone https://github.com/ALFANE/dZENcode_test_task.git
    cd comments
    ```

2. **Install dependencies with Poetry**:

    ```bash
    poetry install
    ```

3. **Activate the virtual environment**:

    ```bash
    poetry shell
    ```

4. **Run migrations**:

    ```bash
    python manage.py migrate
    ```

5. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

6. **Access the application**:

    Open your browser and go to `http://127.0.0.1:8000/comments/` to view the comment system.

### Docker

To run the application using Docker:

1. **Build the Docker image**:

    ```bash
    docker build -t comments_app .
    ```

2. **Run the Docker container**:

    ```bash
    docker run -p 8000:8000 comments_app
    ```

3. **Access the application**:

    Open your browser and go to `http://127.0.0.1:8000/comments/`.

## API Documentation

The project includes auto-generated API documentation using Swagger and ReDoc. You can access the documentation by visiting:

- **Swagger**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`

## Running Tests

Tests are written using Django's `APITestCase` and can be run using `pytest` or the Django test runner.

To run tests with Poetry:

```bash
poetry run pytest
```

## On sending emails

In the views.py file, there is a commented-out line related to sending emails:

```
# comment_form.cleaned_data["email"],
```
To enable email sending:

Uncomment the line above in the views.py file where email sending is implemented.
Create a .env file based on the provided .env.dist file. This file should include your email configuration settings.