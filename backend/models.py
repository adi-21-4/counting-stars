from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class AdminUser(db.Model):
    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="co_leader"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )


class RecruitmentApplication(db.Model):
    __tablename__ = "recruitment_applications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    player_name = db.Column(
        db.String(100),
        nullable=False
    )

    player_tag = db.Column(
        db.String(20),
        nullable=False
    )

    town_hall_level = db.Column(
        db.Integer,
        nullable=False
    )

    league = db.Column(
        db.String(50),
        nullable=True
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    discord = db.Column(
        db.String(100),
        nullable=True
    )

    reason = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    reviewed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    reviewed_by = db.Column(
        db.String(50),
        nullable=True
    )

class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(150),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(30),
        nullable=False,
        default="general"
    )

    is_published = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    created_by = db.Column(
        db.String(50),
        nullable=True
    )

class ClanSettings(db.Model):
    __tablename__ = "clan_settings"

    id = db.Column(db.Integer, primary_key=True)

    min_town_hall = db.Column(
        db.Integer,
        nullable=False,
        default=15
    )

    # Legacy field retained for compatibility with existing database data.
    min_trophies = db.Column(
        db.Integer,
        nullable=False,
        default=3000
    )

    # Current recruitment requirement.
    min_league = db.Column(
        db.String(50),
        nullable=True
    )

    war_participation_required = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    minimum_donations = db.Column(
        db.Integer,
        nullable=False,
        default=1000
    )

    recruitment_open = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    rules = db.Column(
        db.Text,
        nullable=False,
        default=""
    )

    recruitment_requirements = db.Column(
        db.Text,
        nullable=False,
        default=""
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    updated_by = db.Column(
        db.String(50),
        nullable=True
    )

class AdminRequest(db.Model):
    __tablename__ = "admin_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    requested_role = db.Column(
        db.String(20),
        nullable=False,
        default="co_leader"
    )

    reason = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    reviewed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    reviewed_by = db.Column(
        db.String(50),
        nullable=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)