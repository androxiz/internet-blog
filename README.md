# Django Blog Project

This is a simple blog platform built with Django. Users can register, log in, create articles (with AI-generated content), upload photos, and manage their posts.

## Features

- User registration and authentication
- Create, update, and delete articles
- Upload multiple photos per article
- AI-powered article content generation (OpenAI API)
- Responsive Bootstrap-based UI

## Requirements

- Python 3.10+
- Django 5.x
- SQLite (default)
- OpenAI API key

## Getting Started

1. **Clone the repository**

   ```sh
   git clone https://github.com/androxiz/internet-blog
   cd internet-blog
   ```

2. **Create and activate a virtual environment**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   - Copy `.env-example` to `.env` and fill in your `OPENAI_API_KEY` and `SECRET_KEY`.

5. **Apply migrations**

   ```sh
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access)**

   ```sh
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```sh
   python manage.py runserver
   ```

8. **Open your browser**

   - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Docker (optional)

You can also run the project using Docker:

```sh
docker-compose up --build
```


---

**Note:** To use AI-powered content generation, you must provide a valid OpenAI API key in your `.env`
