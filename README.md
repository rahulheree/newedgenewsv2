Real-Time News & Commenting Platform
This project is a modern, high-performance news portal built with FastAPI and PostgreSQL. It features a complete content management system for administrators and a public-facing interface for users. The standout feature is a real-time commenting system powered by WebSockets, allowing for instant user interaction on news articles.

Key Features
Admin Content Management: Secure, token-based authentication for administrators to perform full CRUD (Create, Read, Update, Delete) operations on news articles.

Dynamic News Feed: Publicly accessible news feed, with articles sorted chronologically and the ability to filter by category.

Real-Time Commenting: Utilizes WebSockets to broadcast new comments instantly to all users viewing an article, without requiring a page refresh.

User Interaction: Features include article view counters and social sharing options.

Asynchronous API: Built on an ASGI framework (FastAPI) for high performance and scalability, capable of handling many concurrent connections.

Robust Database: Uses PostgreSQL with SQLModel for clear, Python-based data modeling and validation.

Technology Stack
Backend: Python 3.9+

API Framework: FastAPI

Database: PostgreSQL

ORM / Data Validation: SQLModel (combines Pydantic and SQLAlchemy)

Real-time Communication: WebSockets

ASGI Server: Uvicorn

Dependencies:

fastapi

uvicorn[standard]

sqlmodel

psycopg2-binary

python-jose[cryptography] (for JWT)

passlib[bcrypt] (for password hashing)

Setup and Installation
Follow these steps to get the project up and running on your local machine.

1. Prerequisites
Python 3.9 or newer.

PostgreSQL installed and running.

A code editor like VS Code.

2. Clone the Repository
git clone <your-repository-url>
cd <repository-name>

3. Set Up a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

On macOS / Linux:

python3 -m venv venv
source venv/bin/activate

On Windows:

python -m venv venv
.\venv\Scripts\activate

4. Install Dependencies
Install all the required packages from the requirements.txt file.

pip install -r requirements.txt

5. Configure the Database
Create a new database in PostgreSQL for this project.

CREATE DATABASE news_portal;

Create a .env file in the root directory of the project. This file will store your database connection string and other secret keys.

Add your database URL to the .env file.

DATABASE_URL="postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost/news_portal"
SECRET_KEY="your-super-secret-key-for-jwt"
ALGORITHM="HS256"

6. Run the Application
Once the setup is complete, you can start the development server using Uvicorn.

uvicorn main:app --reload

main:app: Refers to the app instance in the main.py file.

--reload: Automatically restarts the server whenever you make changes to the code.

The application will be running at http://127.0.0.1:8000.

API Documentation
FastAPI automatically generates interactive API documentation. Once the server is running, you can access it at:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

These interfaces allow you to explore and test all the API endpoints directly from your browser.
