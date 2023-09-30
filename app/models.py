from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    hero_power = db.relationship('HeroPower', backref='hero')


class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    hero_power = db.relationship('HeroPower', backref ='power')

    @validates('description')
    def validate_description(self, key, descriptions):
        if not descriptions or len(descriptions) < 20:
            raise ValueError("description must be present and at least 20 characters long")
        return descriptions


class HeroPower(db.Model):
    __tablename__ = 'heropowers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    herro_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @validates('strength')
    def validate_strength(self, key, strengths):
        if strengths not in [ 'Strong', 'Weak', 'Average']:
            raise ValueError("strength must be one of the following values: 'Strong', 'Weak', 'Average'")
        return strengths



# add any models you may need. 