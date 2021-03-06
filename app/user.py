# This module contains all the database queries, except for those in forms.py 
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson.objectid import ObjectId 
from app.db import get_db

class User( ):
    def is_authenticated(self):
        return self.authenticated 

    def is_active(self):
        return self.active 

    def is_anonymous(self):
        return self.anonymous  

    def is_admin(self):
        if self.role == 'admin':
            return True    
        else: 
            return False 

    def get_id(self):
        return self.id      

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password) 
        
    # def __init__(self):
    #     self.clear_user()
    
    def __init__(self,user_id):
        if user_id is None:
            self.clear_user()
        else:    
            self.get_user_id(user_id)
 
    def add_user(self,username, password, role, email):
        hp = generate_password_hash(password)
        user_dict = {"name":username,"password":hp,"role":role,"email":email}
        user = get_db()["users"]
        
        # check if the username exists 
        cursor = user.find({"name":username})
        if cursor.count() > 0:
            message = f"User {username} is already registered." 
        else: 
            user_id = user.insert_one(user_dict).inserted_id
            message = f"User {username} registered."
        return message 

    def get_user(self, username, password): 
        self.clear_user()
        user = get_db()["users"]
        myuser = user.find_one({"name":username})
        if myuser is None: 
            return f"User {username} not found."

        if not check_password_hash(myuser['password'], password):
            return "Incorrect password"
        else: 
            self.id = str(myuser['_id'])
            self.name = myuser['name'] 
            self.role = myuser['role'] 
            self.email = myuser['email']    
            self.password = myuser['password']      
            self.active = True      
            self.anonymous = False 
            self.authenticated = True    
            self.administrator = self.is_admin()
            self.timestamp = datetime.now()      
            return None         

    def get_user_id(self, user_id): 
        self.clear_user()
        if user_id is None: 
            return
        myuser = get_db()['users'].find_one({ "_id":ObjectId(user_id)} )
        if myuser is not None:
            self.id = str(myuser['_id'])
            self.name = myuser['name'] 
            self.role = myuser['role'] 
            self.email = myuser['email']    
            self.password = myuser['password']      
            self.active = True      
            self.anonymous = False
            self.authenticated = True    
            self.administrator = self.is_admin()
            self.timestamp = datetime.now()      

    def clear_user(self):
        self.id = None 
        self.name = None 
        self.role = None 
        self.email = None    
        self.password = None      
        self.active = False       
        self.anonymous = True
        self.authenticated = False   
        self.administrator = False 
        self.timestamp = None      
