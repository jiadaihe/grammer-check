import logging
import sqlite3

con = sqlite3.connect("take2ai.db")
logger = logging.getLogger(__name__)

cur = con.cursor()
cur.execute("""
    create table if not exists users(
        id integer primary key AUTOINCREMENT, 
        name text not null,
        email text not null unique, 
        phone text
    )""")
con.commit()

cur.execute("""
    create table if not exists submissions(
        id integer primary key AUTOINCREMENT,
        userid integer,
        audio_url text not null,
        transcript text not null,
        foreign key (userid) references users(id)
    );""")
con.commit()

cur.execute("""
    create table if not exists feedbacks(
        id integer primary key AUTOINCREMENT,
        submissionid integer, 
        score int,
        feedback text,
        model text not null,
        foreign key (submissionid) references submissions(id)
    );""")
con.commit()

def create_submission(userid: int, audio_url: str, transcript: str) -> int:
    cur.execute("INSERT INTO submissions (userid, audio_url, transcript) VALUES (?, ?) RETURNING id", (userid, audio_url, transcript))
    row = cur.fetchone()
    (id, ) = row if row else None
    con.commit()
    return id

def get_submission_transcript(id: int) -> str:
    res = cur.execute(f"SELECT transcript FROM submissions WHERE id={id}").fetchone()
    if not res:
        raise ValueError(f"The submission {id} is not found.")
    return res

def create_feedback(submission_id: int, score: int, feedback: str, model: str="gpt-3.5-turbo") -> int:
    cur.execute(f"INSERT INTO feedbacks (submissionid, score, feedback, model) VALUES (?, ?, ?, ?) RETURNING id", (submission_id, score, feedback, model))
    row = cur.fetchone()
    (id, ) = row if row else None
    con.commit()
    return id

def get_user(email: str) -> int | None:
    """ If user not found, return None """
    logger.info(f"Getting user {email}")
    row = cur.execute(f"SELECT id FROM users WHERE email='{email}'").fetchone()
    (id, ) = row if row else None
    return id

def create_user(name: str, email: str, phone: str) -> int:
    logger.info(f"Creating user {name}")
    cur.execute(f"INSERT INTO users (name, email, phone) VALUES (?, ?, ?) RETURNING id", (name, email, phone))
    row = cur.fetchone()
    (id, ) = row if row else None
    con.commit()
    return id
    