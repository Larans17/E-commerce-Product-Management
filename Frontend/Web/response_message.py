
ERROR_WHILE_SAVE_RECORD = 'Oops! Something went wrong. Please check your input'
LOGIN_VALIDATION = 'Login username and password is incorrect..!'
LOGIN_FAILED = 'Failed to login'
LOGOUT = 'Logged out successfully'
SIGNUP_VALIDATION = 'Password and confirm password must be same'
OTP_VERIFIED = 'Otp is verified successfully'
ERROR_MSG = 'Something went wrong'


class EventMessages:

    @staticmethod

    def create (msg):
        message = f"{msg} created successfully"
        return message
    
    def failed(msg):
        message = f"failed to {msg}"
        return message
    
    def update (msg):
        message = f"{msg} updated successfully"
        return message
    
    def delete (msg):
        message = f"{msg} deleted successfully"
        return message
    
    def login():
        message = "Logged in successfully"
        return message
    
    def logout():
        message = "Logout successfully"
        return message