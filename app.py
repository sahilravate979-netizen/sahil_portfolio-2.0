
from pathlib import Path
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash

# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "portfolio.db"

app = Flask(__name__)
app.secret_key = "sahil_portfolio_secret_key_2026"


# --------------------------------------------------
# DEFAULT PORTFOLIO DATA
# --------------------------------------------------

DEFAULT_PROJECTS = [
    (
        "College Event Resource Allocation",
        "A web application to manage college events, resources, and task allocation.",
        "Python, Flask, SQLite, HTML, CSS, JavaScript",
        "https://github.com/sahilravate979-netizen/college-event-resource-allocation"
    ),
    (
        "Task Management Application",
        "A task management platform with user authentication, task tracking, and admin features.",
        "Python, Flask, SQLite, HTML, CSS, JavaScript",
        "https://github.com/sahilravate979-netizen/task-management-application"
    ),
    (
        "E-Commerce Web Application",
        "An online shopping platform with product management, cart, checkout, and admin dashboard.",
        "PHP, MySQL, HTML, CSS, JavaScript",
        "https://github.com/sahilravate979-netizen/ecommerce-web-application"
    ),
    (
        "Blog Platform with Comments",
        "A blogging platform where users can publish posts and interact through comments.",
        "Python, Flask, SQLite, HTML, CSS, JavaScript",
        "https://github.com/sahilravate979-netizen/blog-platform-with-comments"
    ),
    (
        "EV Incentive Vehicle",
        "A web application for exploring electric vehicle incentives and related information.",
        "Python, Flask, SQLite, HTML, CSS, JavaScript",
        "https://github.com/sahilravate979-netizen/ev-incentive-vehicle"
    ),
    (
        "Desktop Expenses Tracker",
        "A desktop application to record expenses and visualize spending through charts.",
        "Python, Tkinter, SQLite, Matplotlib",
        "https://github.com/sahilravate979-netizen"
    )
]

DEFAULT_SKILLS = [
    ("Python", "Programming"),
    ("Java", "Programming"),
    ("PHP", "Programming"),
    ("HTML", "Web Development"),
    ("CSS", "Web Development"),
    ("JavaScript", "Web Development"),
    ("Flask", "Frameworks"),
    ("MySQL", "Database"),
    ("SQLite", "Database"),
    ("Git & GitHub", "Tools"),
    ("Machine Learning", "AI & ML"),
    ("Tkinter", "Frameworks")
]


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

def init_db():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                technologies TEXT,
                github TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Remove duplicate projects with the same title.
        # Keeps the project with the lowest ID.
        cursor.execute("""
            DELETE FROM projects
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM projects
                GROUP BY LOWER(TRIM(title))
            )
        """)

        # Add default projects only if the projects table is empty.
        cursor.execute("SELECT COUNT(*) FROM projects")
        project_count = cursor.fetchone()[0]

        if project_count == 0:
            cursor.executemany("""
                INSERT INTO projects
                (title, description, technologies, github)
                VALUES (?, ?, ?, ?)
            """, DEFAULT_PROJECTS)

        # Add default skills only if the skills table is empty.
        cursor.execute("SELECT COUNT(*) FROM skills")
        skill_count = cursor.fetchone()[0]

        if skill_count == 0:
            cursor.executemany("""
                INSERT INTO skills (name, category)
                VALUES (?, ?)
            """, DEFAULT_SKILLS)

        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def index():
    connection = get_db_connection()

    try:
        projects = connection.execute("""
            SELECT * FROM projects ORDER BY id ASC
        """).fetchall()

        skills = connection.execute("""
            SELECT * FROM skills ORDER BY category, name
        """).fetchall()

    finally:
        connection.close()

    return render_template(
        "index.html",
        projects=projects,
        skills=skills
    )


# --------------------------------------------------
# CONTACT FORM
# --------------------------------------------------

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill in all the contact form fields.", "error")
        return redirect(url_for("index") + "#contact")

    if "@" not in email or "." not in email:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("index") + "#contact")

    connection = get_db_connection()

    try:
        connection.execute("""
            INSERT INTO messages (name, email, message)
            VALUES (?, ?, ?)
        """, (name, email, message))

        connection.commit()
        flash("Thank you! Your message has been submitted successfully.", "success")

    except sqlite3.Error:
        connection.rollback()
        flash("Sorry, something went wrong. Please try again.", "error")

    finally:
        connection.close()

    return redirect(url_for("index") + "#contact")


# --------------------------------------------------
# CUSTOM 404 PAGE
# --------------------------------------------------

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("index"))


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    init_db()

    print("Portfolio application is starting...")
    print("Open http://127.0.0.1:5000 in your browser.")

    app.run(debug=True)
