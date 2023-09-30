from faker import Faker
import random
from app import app

from models import db, Hero, Power, HeroPower

with app.app_context():

    fake = Faker()

    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()
    db.session.commit()
    
    print("🦸‍♀️ Seeding powers...")
    
    powers_data = [
      { "name": "super strength", "description": "gives the wielder super-human strengths" },
      { "name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed" },
      { "name": "super human senses", "description": "allows the wielder to use her senses at a super-human level" },
      { "name": "elasticity", "description": "can stretch the human body to extreme lengths" }
    ]
    
    for power in powers_data:
      data = Power(**power)
      db.session.add(data)
    db.session.commit()
    
    
    print("🦸‍♀️ Seeding heroes...")
    
    heroes_data = [
      { "name": "Kamala Khan", "super_name": "Ms. Marvel" },
      { "name": "Doreen Green", "super_name": "Squirrel Girl" },
      { "name": "Gwen Stacy", "super_name": "Spider-Gwen" },
      { "name": "Janet Van Dyne", "super_name": "The Wasp" },
      { "name": "Wanda Maximoff", "super_name": "Scarlet Witch" },
      { "name": "Carol Danvers", "super_name": "Captain Marvel" },
      { "name": "Jean Grey", "super_name": "Dark Phoenix" },
      { "name": "Ororo Munroe", "super_name": "Storm" },
      { "name": "Kitty Pryde", "super_name": "Shadowcat" },
      { "name": "Elektra Natchios", "super_name": "Elektra" }
    ]
    
    for hero in heroes_data:
      data = Hero(**hero)
      db.session.add(data)
      
    db.session.commit()
    
    print("🦸‍♀️ Adding powers to heroes...")
    
    strengths = ["Strong", "Weak", "Average"]
    
    powers = Power.query.all()
    heroes = Hero.query.all()
    
    for hero in heroes:
      for i in range(random.randint(1, 7)):
        power = random.choice(powers)
        strength = random.choice(strengths)
        
        hero_power = HeroPower(herro_id=hero.id, power_id=power.id, strength= strength)
        db.session.add(hero_power)
        
    db.session.commit()
    
    print("🦸‍♀️ Done seeding!")
    