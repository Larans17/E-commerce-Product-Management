# API RESPONSE MESSAGES
CODE = 'authorization'
VALIDATION_MSG = 'Must include "username" and "password"'
INVALID_ACCOUNT = "This account is invalid."
LOGIN_VERIFIED = "Logged-in successfully"
INVALID_EMAIL = "Username is incorrect..!"
USERNAME = "Please provide either username..!"
INVALID_USERNAME = "Invalid username..!"
INVALID_PASSWORD = "Password is incorrect..!"
PARAMS_MISSING = "Parameter is missed..!"



class CommonApiMessages:

    @staticmethod

    def create(msg):
        message = f"{msg} created successfully"
        return message
    
    def delete (msg):
        message = {'message':f"{msg} deleted successfully"}
        return message
    
    def restrict_delete (msg):
        message = {'message':f"{msg} is being referenced with another instance"}
        return message
    
    def does_not_exists(msg):
        message = f'{msg} ID does not exists.'
        return message
    
    def update(msg):
        message = f"{msg} updated successfully"
        return message
    
    

    
    
