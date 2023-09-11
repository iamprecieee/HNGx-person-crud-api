from flask import abort
from flask_smorest import Blueprint
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from resources.db import db
from models import PersonModel
from schema import PersonSchema, PersonUpdateSchema


blp = Blueprint("Persons", "persons", description="Operations on persons.")

@blp.route("/api")
class PersonDetails(MethodView):
    @blp.response(200, PersonSchema(many=True))
    def get(self):
        """
        Retrieves a list of Persons
        """
        return PersonModel.query.all()
    
    @blp.arguments(PersonSchema)
    @blp.response(200)
    def post(self, person_data):
        """
        Creates a new Person instance
        """
        name = person_data.get("name", "").strip()
        if not name:
            abort(422, description="Name must be a valid string!")
        for key, value in person_data.items():
            if isinstance(value, str):
                person_data[key] = value.title().strip()
        person = PersonModel(**person_data)
        try:
            db.session.add(person)
            db.session.commit()
        except IntegrityError:
            abort(400, description="A person with that name already exists!")
        return "Person created successfully."
    
    
@blp.route("/api/<user_id>")
class Person(MethodView):
    @blp.response(200, PersonSchema)
    def get(self, user_id):
        """
        Returns a specific Person instance by id
        """
        person = PersonModel.query.get(user_id)
        if not user_id.isdigit():
            user_id = user_id.title()
            person =PersonModel.query.filter_by(name=user_id).first()
        if not person:
            abort(404, description="Person with this id could not be located.")
        return person
    
    @blp.arguments(PersonUpdateSchema)
    @blp.response(200, PersonSchema)
    def put(self, person_data, user_id):
        """
        Updates record of a Person instance by id
        """
        person = PersonModel.query.get(user_id)
        if not user_id.isdigit():
            user_id = user_id.title()
            person =PersonModel.query.filter_by(name=user_id).first()
        if not person:
            abort(404, description="Person with this id could not be located.")
        person.name = person_data["name"]
        try:
            db.session.add(person)
            db.session.commit()
        except IntegrityError:
            abort(400, description="A person with that name already exists!")
        return person
    
    @blp.response(200)
    def delete(self, user_id):
        """
        Deletes record of a Person instance by id
        """
        person = PersonModel.query.get(user_id)
        if not user_id.isdigit():
            user_id = user_id.title()
            person =PersonModel.query.filter_by(name=user_id).first()
        if not person:
            abort(404, description="Person with this id could not be located.")
        try:
            db.session.delete(person)
            db.session.commit()
        except IntegrityError:
            abort(400, description="A person with that name already exists!")
        return "Person deleted successfully."