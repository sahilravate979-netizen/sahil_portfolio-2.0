from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "portfolio_secret_key"

DATABASE = "portfolio.db"


# -----------------------------
# Database Connection
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Initialize Database
# -----------------------------
def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            technologies TEXT NOT NULL,
            github TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add sample projects only if table is empty
    project_count = conn.execute(
        "SELECT COUNT(*) FROM projects"
    ).fetchone()[0]

    if project_count == 0:
        projects = [
            (
                "Personal Portfolio Website",
                "A full-stack personal portfolio website to showcase projects and skills.",
                "HTML, CSS, JavaScript, Flask, SQLite",
                "https://github.com/"
            ),
            (
                "EV Incentive Vehicle Website",
                "A website that educates users about government incentives and rebates for electric vehicle purchases.",
                "HTML, CSS, JavaScript, Flask, SQLite",
                "https://github.com/"
            ),
            (
                "Expense Tracker",
                "Desktop application for managing and analyzing personal expenses.",
                "Python, Tkinter, SQLite, Matplotlib",
                "https://github.com/"
            )
        ]

        conn.executemany("""
            INSERT INTO projects
            (title, description, technologies, github)
            VALUES (?, ?, ?, ?)
        """, projects)

    # Add sample skills
    skill_count = conn.execute(
        "SELECT COUNT(*) FROM skills"
    ).fetchone()[0]

    if skill_count == 0:
        skills = [
            ("HTML", "Frontend"),
            ("CSS", "Frontend"),
            ("JavaScript", "Frontend"),
            ("Python", "Backend"),
            ("Flask", "Backend"),
            ("SQLite", "Database"),
            ("Git & GitHub", "Tools")
        ]

        conn.executemany("""
            INSERT INTO skills (name, category)
            VALUES (?, ?)
        """, skills)

    conn.commit()
    conn.close()


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def index():
    conn = get_db_connection()

    projects = conn.execute("""
        SELECT * FROM projects
        ORDER BY id DESC
    """).fetchall()

    skills = conn.execute("""
        SELECT * FROM skills
        ORDER BY category, name
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        projects=projects,
        skills=skills
    )


# -----------------------------
# Projects Page
# -----------------------------
@app.route("/projects")
def projects():
    conn = get_db_connection()

    projects = conn.execute("""
        SELECT * FROM projects
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "projects.html",
        projects=projects
    )


# -----------------------------
# Contact Page
# -----------------------------
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip()
        message = request.form["message"].strip()

        if not name or not email or not message:
            flash("Please fill all fields.")
            return redirect(url_for("contact"))

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO messages
            (name, email, message)
            VALUES (?, ?, ?)
        """, (name, email, message))

        conn.commit()
        conn.close()

        flash("Your message has been sent successfully!")

        return redirect(url_for("contact"))

    return render_template("contact.html")


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    init_db()

    print("Database initialized successfully.")
    print("Starting Personal Portfolio Website...")

    app.run(debug=True)