import hashlib
from fastapi import HTTPException
from user_database import USER_DATABASE as db
from utils import users_util

def create_user(user_id, username, email, password):
    if users_util.uid_exists(user_id):
        return users_util.http_exception_message(status_code=500, message='Internal server error (uid already exists)')
    if users_util.username_exists(username):
        return users_util.http_exception_message(status_code=409, message='Username already exists')
    if users_util.email_exists(email):
        return users_util.http_exception_message(status_code=409, message='Email already exists')

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    db.execute_sql_write("INSERT INTO users (user_id, username, email, password) VALUES (%s, %s, %s, %s)",
                         params=(user_id, username, email, hashed_password))
    return {'message': f'User({user_id}) successfully created'}

def get_all_users():
    FIELD_NAMES = ['user_id', 'username', 'email', 'password', 'role']
    rows = db.execute_sql_read_fetchall(f"SELECT {', '.join(FIELD_NAMES)} FROM users")
    users = [dict(zip(FIELD_NAMES, row)) for row in rows]
    return users

def get_user(user_id):
    FIELD_NAMES = ['user_id', 'username', 'email', 'password', 'role']
    row = db.execute_sql_read_fetchone(f"SELECT {', '.join(FIELD_NAMES)} FROM users WHERE user_id = %s",
                                        params=(user_id,))
    user = dict(zip(FIELD_NAMES, row))
    return user

def update_user_info(user_id, username, password, email):
    if not users_util.uid_exists(user_id):
        raise HTTPException(status_code=404, detail="User does not exist")
    if users_util.check_duplicate_username(user_id, username):
            raise HTTPException(status_code=409, detail='Username already exists')
    if users_util.check_duplicate_email(user_id, email):
            raise HTTPException(status_code=409, detail='Email already exists')

    new_password = hashlib.md5(password.encode()).hexdigest()

    db.execute_sql_write("""UPDATE users
                        SET username = %s, password = %s, email = %s
                        WHERE user_id = %s""",
                        params=(username, new_password, email, user_id))
    return {'message': 'Successfully updated'}


def delete_all_users():
    db.execute_sql_write("DELETE FROM users")
    return {'message': 'All users deleted'}

def delete_user(user_id):
    if not users_util.uid_exists(user_id):
        raise HTTPException(status_code=404, detail="User does not exist")

    db.execute_sql_write("DELETE FROM users WHERE user_id = %s", params=(user_id,))
    return {'message': f'User id {user_id} deleted'}

def update_user_role(user_id, role):
    if role == "normal":
        if db.execute_sql_read_fetchone("SELECT COUNT(*) FROM users WHERE role = 'maintainer'")[0] <= 1:
            raise HTTPException(status_code=409, detail='Only one maintainer left')

    db.execute_sql_write("UPDATE users SET role = %s WHERE user_id = %s", params=(role, user_id))

    return {'message': 'Successfully updated'}
