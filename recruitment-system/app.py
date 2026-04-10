from flask import Flask, render_template, request, redirect

import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def db():
    return sqlite3.connect("database.db")


@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ADMIN ----------------

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form["username"]=="admin" and request.form["password"]=="admin":
            return redirect("/admin_dashboard")
    return render_template("admin_login.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    conn = db()
    jobs = conn.execute("SELECT * FROM jobs").fetchall()
    return render_template("admin_dashboard.html",jobs=jobs)


@app.route("/add_job", methods=["POST"])
def add_job():
    title = request.form["title"]
    company = request.form["company"]
    desc = request.form["description"]

    conn=db()
    conn.execute("INSERT INTO jobs(title,company,description) VALUES(?,?,?)",
    (title,company,desc))
    conn.commit()

    return redirect("/admin_dashboard")


@app.route("/delete_job/<id>")
def delete_job(id):
    conn=db()
    conn.execute("DELETE FROM jobs WHERE id=?",(id,))
    conn.commit()
    return redirect("/admin_dashboard")


# ---------------- CANDIDATE ----------------

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method=="POST":

        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]

        resume=request.files["resume"]
        path=os.path.join(app.config["UPLOAD_FOLDER"],resume.filename)
        resume.save(path)

        conn=db()
        conn.execute("INSERT INTO candidates(name,email,password,resume) VALUES(?,?,?,?)",
        (name,email,password,resume.filename))
        conn.commit()

        return redirect("/login")

    return render_template("candidate_register.html")


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]

        conn=db()
        user=conn.execute("SELECT * FROM candidates WHERE email=? AND password=?",
        (email,password)).fetchone()

        if user:
            return redirect("/jobs")

    return render_template("candidate_login.html")


@app.route("/jobs")
def jobs():
    conn=db()
    jobs=conn.execute("SELECT * FROM jobs").fetchall()
    return render_template("jobs.html",jobs=jobs)

@app.route("/apply/<int:jobid>", methods=["GET", "POST"])
def apply(jobid):

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        candidate_id = 1   # later we can replace with session

        conn = db()
        conn.execute(
            "INSERT INTO applications(candidate_id, job_id, status) VALUES(?,?,?)",
            (candidate_id, jobid, "Applied")
        )
        conn.commit()

        return redirect("/jobs")
    

    return render_template("apply.html", jobid=jobid)

@app.route("/apply/<jobid>")
def apply_get(jobid):
    return render_template("apply.html",jobid=jobid)


# ---------------- RECRUITER ----------------

@app.route("/recruiter",methods=["GET","POST"])
def recruiter():

    if request.method=="POST":
        if request.form["username"]=="recruiter" and request.form["password"]=="123":
            return redirect("/recruiter_dashboard")

    return render_template("recruiter_login.html")


@app.route("/recruiter_dashboard")
def recruiter_dashboard():

    conn=db()
    apps=conn.execute("""
    SELECT applications.id,candidates.name,jobs.title,applications.status
    FROM applications
    JOIN candidates ON candidates.id=applications.candidate_id
    JOIN jobs ON jobs.id=applications.job_id
    """).fetchall()

    return render_template("applications.html",apps=apps)

@app.route("/shortlist/<int:id>")
def shortlist_candidate(id):
    conn = db()
    conn.execute("UPDATE applications SET status='Shortlisted' WHERE id=?", (id,))
    conn.commit()
    return redirect("/recruiter_dashboard")


#app.run(debug=True)
@app.route("/schedule/<int:id>")
def schedule(id):
     print("Schedule clicked:", id)
     conn = db()
     conn.execute( "UPDATE applications SET status='Interview Scheduled', interview_date='Tomorrow 10 AM' WHERE id=?", (id,) ) 
     conn.commit() 
     return redirect("/recruiter") 
if __name__ == '__main__': 
    app.run(debug=True)  
