# from flask import current_app, url_for
# from flask_mail import Message
# from app import mail
# import jwt
# from datetime import datetime, timedelta

# def generate_reset_token(user_id):
#     """Generate a JWT token for password reset."""
#     token = jwt.encode(
#         {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(hours=1)},
#         current_app.config['JWT_SECRET_KEY'],
#         algorithm='HS256'
#     )
#     return token

# def verify_reset_token(token):
#     """Verify the JWT token for password reset."""
#     try:
#         decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
#         return decoded_token['user_id']
#     except jwt.ExpiredSignatureError:
#         return None
#     except jwt.InvalidTokenError:
#         return None

# def send_reset_email(user, token):
#     """Send a password reset email to the user."""
#     reset_url = url_for('user_endpoint.reset_password', token=token, _external=True)
#     msg = Message('Password Reset Request',
#                   sender='noreply@demo.com',
#                   recipients=[user.email])
#     msg.body = f'''To reset your password, visit the following link:
# {reset_url}

# If you did not make this request then simply ignore this email and no changes will be made.
# '''
#     mail.send(msg)
