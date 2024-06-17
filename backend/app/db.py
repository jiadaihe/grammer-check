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
        foreign key (submissionid) references submissions(id),
        unique (submissionid, model)
    );""")
con.commit()

def create_submission(userid: int, audio_url: str, transcript: str) -> int:
    cur.execute("INSERT INTO submissions (userid, audio_url, transcript) VALUES (?, ?, ?) RETURNING id", (userid, audio_url, transcript))
    row = cur.fetchone()
    if row is None:
        raise ValueError("Cannot insert into submissions table.")
    id = row[0]
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
    if row is None:
        raise ValueError("Cannot insert into feedbacks table.")
    id = row[0]
    return id

def get_feedback(submission_id: int, model: str) -> tuple[int, str] | None:
    """ If user not found, return None """
    logger.info(f"Getting feedback for submission {submission_id} and model {model}")
    row = cur.execute(f"SELECT score, feedback FROM feedbacks WHERE submissionid='{submission_id}' and model='{model}'").fetchone()
    return row

def delete_feedback(submission_id: int, model: str="gpt-3.5-turbo") -> int | None:
    """ If user not found, return None """
    logger.info(f"Deleting feedback with submissionid={submission_id} and model={model}")
    cur.execute(f"DELETE FROM feedbacks WHERE submissionid={submission_id} and model='{model}'")
    con.commit()

def get_user(email: str) -> int | None:
    """ If user not found, return None """
    logger.info(f"Getting user {email}")
    row = cur.execute(f"SELECT id FROM users WHERE email='{email}'").fetchone()
    if row is None:
        return None
    return row[0]

def delete_user(email: str) -> int | None:
    """ If user not found, return None """
    logger.info(f"Deleting user {email}")
    cur.execute(f"DELETE FROM users WHERE email='{email}'")
    con.commit()

def create_user(name: str, email: str, phone: str) -> int:
    logger.info(f"Creating user {name}")
    cur.execute(f"INSERT INTO users (name, email, phone) VALUES (?, ?, ?) RETURNING id", (name, email, phone))
    row = cur.fetchone()
    if row is None:
        raise ValueError("Cannot insert into users table.")
    id = row[0]
    return id
    