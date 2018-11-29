from flask import Blueprint, jsonify
from app.models import User

test = Blueprint('test', __name__)


@test.route('/')
def index():
    users = User.query.all()
    return str(users)

