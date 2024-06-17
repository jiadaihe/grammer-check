import sqlite3
con = sqlite3.connect("take2ai.db")

cur = con.cursor()
cur.execute("""
    create table if not exists users(
        id integer primary key AUTOINCREMENT, 
        name text not null, 
        email text not null, 
        phone text
    )""")
con.commit()

cur.execute("""
    create table if not exists submissions(
        id integer primary key AUTOINCREMENT, 
        audio_url text not null,
        transcript text not null
    );""")
con.commit()

cur.execute("""
    create table if not exists feedbacks(
        id integer primary key AUTOINCREMENT,
        submission_id integer, 
        score int,
        feedback text,
        model text not null,
        foreign key (submission_id) references submissions(id)
    );""")
con.commit()

def create_submission(audio_url: str, transcript: str) -> int:
    cur.execute("INSERT INTO submissions (audio_url, transcript) VALUES (?, ?) RETURNING id", (audio_url, transcript))
    row = cur.fetchone()
    (id, ) = row if row else None
    con.commit()
    return id

def get_submission_transcript(id: int) -> str:
    res = cur.execute(f"SELECT transcript FROM submissions WHERE id={id}")
    return res.fetchone()

def create_feedback(submission_id: int, score: int, feedback: str, model: str="gpt-3.5-turbo") -> int:
    cur.execute(f"INSERT INTO feedbacks (submission_id, score, feedback, model) VALUES (?, ?, ?, ?) RETURNING id", (submission_id, score, feedback, model))
    row = cur.fetchone()
    (id, ) = row if row else None
    con.commit()
    return id

def create_user(name: str, email: str, phone: str) -> int:
    cur.execute(f"INSERT INTO users (name, email, phone) VALUES (?, ?, ?) RETURNING id", (name, email, phone))
    row = cur.fetchone()
    (id, ) = row if row else None
    con.commit()
    return id
    