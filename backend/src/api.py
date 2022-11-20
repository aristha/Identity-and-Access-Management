# import os
from flask import Flask, request, jsonify, abort
# from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
import sys
app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
with app.app_context():
    db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
# Get All drinks
@app.route("/drinks", methods=["GET"])
def get_drinks():

    drinks = Drink.query.all()
    formatted_categories = [drink.short() for drink in drinks]
    return jsonify(
        {
            "success": True,
            "drinks": formatted_categories
        }
    )

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
# Get All drinks
@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_drinks_detail(payload):

    drinks = Drink.query.all()
    try:
        formatted_drinks = [drink.long() for drink in drinks]
        return jsonify(
            {
                "success": True,
                "drinks": formatted_drinks
            }
        )
    except:
        print(sys.exc_info())

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
   # Create new question or Search question
@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drink(payload):
    
    body = request.get_json()
    try:
        title = body.get("title", None)
        recipe = body.get("recipe", None)
        searchTerm = body.get("searchTerm", None)
        if searchTerm: 
            selection = Drink.query.order_by(Drink.id).filter(
                Drink.question.ilike("%{}%".format(searchTerm))
            )
            current_questions = selection
            if len(current_questions) == 0:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(Drink.query.all()),
                    "current_category":None
                }
            )
        else:
            drink_new = Drink(title=title,recipe=json.dumps(recipe))
            drink_new.insert()
           
            drinks = Drink.query.all()
            formatted_drinks = [drink.long() for drink in drinks]
            return jsonify(
                {
                    "success": True,
                    "drinks": formatted_drinks
                }
            )
        
    except:
        print(sys.exc_info())
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
# Get questions based on category
@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@requires_auth("patch:drinks")
# @cross_origin
def update_drinks(payload, drink_id):
    try:
        drink = Drink.query.get(drink_id)
        if drink is None:
            abort(404)
        
        body = request.get_json()
        title = body.get("title", None)
        recipe = body.get("recipe", None)
        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
        drinks = Drink.query.all()
        formatted_drinks = [drink.long() for drink in drinks]
        return jsonify(
            {
                "success": True,
                "drinks": formatted_drinks
            }
        )
    except:
        print(sys.exc_info())
        abort(422)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
# Delete drinks
@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth("delete:drinks")
# @cross_origin
def delete_drinks(payload,drink_id):
    try:
        drink = Drink.query.get(drink_id)
        if drink is None:
            print("ok")
            abort(404)
        print("ok2")
        drink.delete()
        print("ok3")
        return jsonify(
            {
                "success": True,
                "drink":drink_id
            }
        )
    except:
        
        print(sys.exc_info())
        abort(422)

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404
'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def invalid_claims(ex):
    return jsonify({
                    "success": False,
                    "error": ex.status_code,
                    "message": ex.error
                    })
if __name__ == "__main__":
    app.run(ssl_context='adhoc')