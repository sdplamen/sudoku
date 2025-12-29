# Django Sudoku Solver & Game
- A full-stack Sudoku web application built with Django. Users can play puzzles from a database, enter their own custom grids, and use a built-in recursive backtracking solver to check their work or see the final solution.

## 🚀 Features
- Play by Difficulty: Select puzzles from the database categorized as Easy, Medium, or Hard.
- Custom Grid Entry: A dedicated interface to input your own puzzles with real-time validation to ensure they are solvable.
- Intelligent Solver: Uses a recursive backtracking algorithm to solve any valid Sudoku puzzle instantly.
- Live Timer: Track your solving speed with an integrated JavaScript timer.
- "Check My Work": Highlights incorrect entries in red without revealing the full solution.

Responsive Design: Styled with custom CSS to feature thick 3x3 grid boundaries for a classic Sudoku look and feel.

## 🛠️ Tech Stack
- Backend: Python 3.13, Django 5.2.7
- Frontend: HTML5, CSS3, JavaScript (Vanilla)
- Database: SQLite (default) / PostgreSQL compatible
- Logic: Custom Template Tags for complex dictionary lookups in Django templates.

## 📦 Installation
- Clone the repository:

### Bash
- git clone https://github.com/sdplamen/sudoku.git
- cd sudoku
- Set up a virtual environment:
- python -m venv venv
- On MAC: source venv/bin/activate  
- On Windows: venv\Scripts\activate
- Install dependencies:
- pip install -r requirements.txt
- Run Migrations:
- python manage.py migrate
- Start the server:
- python manage.py runserver

## 📂 Project Structure
- /game/views.py: Logic for puzzle selection, validation, and solving.
- /game/sudoku.py: The core mathematical solver algorithm.
- /game/templatetags/: Custom filters (get_item, get_field) for dynamic grid rendering.
- /templates/grid.html: A reusable component for rendering the Sudoku table.