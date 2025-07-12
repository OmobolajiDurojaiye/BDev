from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date as dt_date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import JSON, Text

db = SQLAlchemy()


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=dt_date.today)
    description = db.Column(db.Text, nullable=False)
    
    video_filename = db.Column(db.String(255), nullable=True)
    poster_filename = db.Column(db.String(255), nullable=True)
    
    project_type = db.Column(db.String(50), nullable=False)
    tech_tags = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(100), nullable=False)
    client_name = db.Column(db.String(100), nullable=True)
    
    ai_used = db.Column(db.Boolean, default=False, nullable=False)
    ai_desc = db.Column(db.String(255), nullable=True)
    
    project_value = db.Column(db.String(100), nullable=True)
    live_site_url = db.Column(db.String(255), nullable=True)
    github_url = db.Column(db.String(255), nullable=True)
    case_study_url = db.Column(db.String(255), nullable=True)
    
    # REMOVED: Relationship to Collaborator model.
    
    @property
    def video_url(self):
        if self.video_filename:
            return url_for('static', filename=f'uploads/video/{self.video_filename}', _external=True)
        return None

    @property
    def poster_url(self):
        if self.poster_filename:
            return url_for('static', filename=f'uploads/image/{self.poster_filename}', _external=True)
        return url_for('static', filename='images/default_poster.jpg', _external=True)

    def __repr__(self):
        return f'<Project {self.title}>'

class ContactSubmission(db.Model):
    __tablename__ = 'contact_submissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<ContactSubmission from {self.name}>'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class ResumeProfile(db.Model):
    __tablename__ = 'resume_profile'
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(Text, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(100), nullable=False)

class Experience(db.Model):
    __tablename__ = 'experience'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    date_range = db.Column(db.String(100), nullable=False)
    description = db.Column(Text, nullable=False)
    tech_tags = db.Column(db.String(255), nullable=True)
    display_order = db.Column(db.Integer, default=0)

class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    date_range = db.Column(db.String(100), nullable=False)
    display_order = db.Column(db.Integer, default=0)

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    display_order = db.Column(db.Integer, default=0)
